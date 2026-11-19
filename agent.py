"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import config
import trace
import re

from tools import suggest_outfit, create_fit_card
from generate import ModelUnavailable
from mcp_client import SearchTimeout, call_tool


RUN_LOG = Path(__file__).resolve().parent / "logs" / "runs.jsonl"


def _log_run(session: dict, started_at: float, search_started_at: float | None) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": session["query"],
        "response": session["error"] or session["fit_card"],
        "elapsed_ms": round((perf_counter() - started_at) * 1000, 3),
        "status": "error" if session["error"] else "success",
    }
    if search_started_at is not None:
        record["status"] = "timeout"
        record["search_timeout_ms"] = round(
            (perf_counter() - search_started_at) * 1000, 3
        )
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8") as log:
        log.write(json.dumps(record) + "\n")


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    started_at = perf_counter()
    search_started_at = None
    session = new_session(query, wardrobe)

    trace.start_trace()

    step = "parse"
    iterations = 0
    
    while step != "done":
        iterations += 1
        trace.check_iterations(iterations)
    
        if step == "parse":
            # Extract maximum price, e.g. "under $30"
            price_match = re.search(
                r"\b(?:under|below|max(?:imum)?)\s*\$?(\d+(?:\.\d+)?)",
                session["query"],
                re.IGNORECASE,
            )
    
            max_price = (
                float(price_match.group(1))
                if price_match
                else None
            )
    
            # Extract size, e.g. "size M" or "size 8"
            size_match = re.search(
                r"\bsize\s+([A-Za-z0-9/]+)",
                session["query"],
                re.IGNORECASE,
            )
    
            size = (
                size_match.group(1)
                if size_match
                else None
            )
    
            # Remove price and size phrases to leave the item description.
            description = session["query"]
    
            description = re.sub(
                r"\b(?:under|below|max(?:imum)?)\s*\$?\d+(?:\.\d+)?",
                "",
                description,
                flags=re.IGNORECASE,
            )
    
            description = re.sub(
                r"\b(?:in\s+)?size\s+[A-Za-z0-9/]+",
                "",
                description,
                flags=re.IGNORECASE,
            )
    
            description = " ".join(description.split()).strip()
    
            session["parsed"] = {
                "description": description,
                "size": size,
                "max_price": max_price,
            }
    
            step = "search"
    
       
        elif step == "search":
            parsed = session["parsed"]

            try:
                session["search_results"] = call_tool(
                    "search_listings",
                    {
                        "description": parsed["description"],
                        "size": parsed["size"],
                        "max_price": parsed["max_price"],
                    },
                )
            except SearchTimeout as exc:
                search_started_at = exc.started_at
                session["error"] = str(exc)
                trace.step(
                    "search_listings (via MCP)",
                    inputs=parsed,
                    note=session["error"],
                )
                break

            trace.step(
                "search_listings (via MCP)",
                inputs=parsed,
                returned=session["search_results"],
            )

            # Required branch: stop if no listings match
            if not session["search_results"]:
                session["error"] = (
                    "I couldn't find a matching listing. Try changing the "
                    "description, size, or maximum price."
                )

                trace.step(
                    "empty_search_branch",
                    note="No matching listings. Stopping the agent.",
                )

                step = "done"
                continue

            session["selected_item"] = session["search_results"][0]
            step = "outfit"

    
            # Required branch
            if not session["search_results"]:
                session["error"] = (
                    "I couldn't find a matching listing. Try changing the "
                    "description, size, or maximum price."
                )
                step = "done"
                continue
            
            session["selected_item"] = session["search_results"][0]
            step = "outfit"
    
        
        elif step == "outfit":
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"],
                session["wardrobe"],
            )

            trace.step(
                "suggest_outfit",
                inputs={
                    "selected_item": session["selected_item"],
                    "wardrobe": session["wardrobe"],
                },
                returned=session["outfit_suggestion"],
            )

            step = "fit_card"

    
        
        elif step == "fit_card":
            session["fit_card"] = create_fit_card(
                session["outfit_suggestion"],
                session["selected_item"],
            )

            trace.step(
                "create_fit_card",
                inputs={
                    "outfit": session["outfit_suggestion"],
                    "new_item": session["selected_item"],
                },
                returned=session["fit_card"],
            )

            step = "done"

    
    _log_run(session, started_at, search_started_at)
    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
