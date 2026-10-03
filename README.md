# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is an AI-powered agent that helps a user search for thrifted clothing
items based on a description, size, and maximum price. It searches the available
listings, selects a matching item, and suggests outfits using pieces from the
user's existing wardrobe. It then creates a short social-media-style fit card
for the selected item and outfit. If no listing matches the request, the agent
stops early and tells the user what they can change in their search.

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the available clothing listings using the user's description, and optionally filters by size and maximum price.
- **Inputs:** `description` (str), `size` (str | None), `max_price` (float | None)
- **Returns:** A list of matching listing dictionaries, ordered with the best match first, up to `config.SEARCH_RESULT_LIMIT`. Each dictionary includes `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]` when no listings match the request.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits that combine the selected listing with items from the user's wardrobe.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing outfit suggestions based on the selected item and the user's wardrobe.
- **When it has nothing:** If the wardrobe has no items, it returns general styling advice for the selected item instead of failing or returning an empty string.

### `create_fit_card`

- **What it does:** Creates a short social-media-style caption about the selected item and suggested outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A two-to-four sentence caption that mentions the item, its price, its platform, and the overall vibe.
- **When it has nothing:** If `outfit` is empty or contains only whitespace, it returns a descriptive message instead of raising an error.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, store a helpful message in the session explaining what the user could change and stop the agent. Otherwise, select the first matching listing, store it in the session, continue to `suggest_outfit`, and then continue to `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** The query is parsed with simple string matching and regular expressions in `agent.py::run_agent` to extract the description, size, and maximum price.

**What moves through the session:** The original query is stored in `session["query"]`. The parsed `description`, `size`, and `max_price` go into `session["parsed"]`. Search results go into `session["search_results"]`, the first selected result goes into `session["selected_item"]`, the outfit suggestion goes into `session["outfit_suggestion"]`, and the final caption goes into `session["fit_card"]`. If the run stops early, the message goes into `session["error"]`.

---

## Sample Run

**One full query**
```text

python app.py ask 'vintage graphic tee under $30'

Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit:
Outfit 1: Y2K Streetwear
New Item: Y2K Baby Tee
Wardrobe Pieces: Baggy straight-leg jeans, Chunky white sneakers, Black crossbody bag
Why it works: The fitted, graphic nature of the baby tee contrasts with the relaxed,
baggy silhouette of the dark wash jeans for an authentic Y2K streetwear look.

Outfit 2: Casual Vintage Edge
New Item: Y2K Baby Tee
Wardrobe Pieces: Wide-leg khaki trousers, Vintage black denim jacket,
Black combat boots, Brown leather belt
Why it works: The pink and purple butterfly print adds a soft pop of color that
balances the earthy khaki trousers and the grunge-inspired black combat boots
and denim jacket.

Fit card:
Channeling major 2000s pop star energy with this Y2K baby tee, and it can be
yours for just $18.0! I love styling it with baggy denim and chunky sneakers
for the ultimate off-duty streetwear vibe, or dressing it down with khaki
trousers and combat boots for a bit of grunge edge. Grab this cute butterfly
print over on my depop before it's gone!

2 model calls this session, 586 prompt + 254 output tokens
```
**The three tools, tested one at a time**

```text
python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```text
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit ideas using the new Vintage Levi's 501 Jeans and your existing wardrobe:

**Outfit 1: Casual Streetwear**
*   **New Item:** Vintage Levi's 501 Jeans
*   **Wardrobe Pieces:** White ribbed tank top, oversized grey crewneck sweatshirt (layered over or worn on its own), chunky white sneakers, and black crossbody bag.
*   *Vibe:* Effortless, classic off-duty casual with a great contrast between the medium wash denim and the bright white top and sneakers.

**Outfit 2: Vintage Grunge**
*   **New Item:** Vintage Levi's 501 Jeans
*   **Wardrobe Pieces:** Black cropped zip hoodie, vintage black denim jacket, black combat boots, and brown leather belt.
*   *Vibe:* Edgy and textured, playing with double-denim (medium wash paired with black denim) and anchored by heavy combat boots.
```

```text
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi's 501 jeans for just $38.0 on depop, and they fit like an absolute dream. I love styling them with crisp white sneakers for that effortlessly cool, off-duty weekend aesthetic. Grab them before I change my mind and keep them forever!
```
---
## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to help me review my `search_listings`
  implementation and spot errors in the code.
- *What came back:* The AI pointed out that my `sort()` and `return` statements
  were indented inside the `for` loop, which caused the function to return
  after checking only the first listing.
- *What I changed:* I moved the sorting and final return outside the loop so
  every listing is checked before the results are ranked and returned.

**Moment 2**

- *What I asked for:* I asked AI to help me design and connect the planning
  loop in `agent.py`.
- *What came back:* The AI suggested storing each tool result in the session
  dictionary and branching immediately when `search_listings` returned an
  empty list.
- *What I changed:* I implemented the loop so search results, the selected item,
  the outfit suggestion, and the fit card all move through session state. I also
  added an early-stop message that tells the user to change the description,
  size, or maximum price when no listing matches.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
