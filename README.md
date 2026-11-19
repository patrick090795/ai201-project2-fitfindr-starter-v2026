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

- _What I asked for:_ I asked AI to help me review my `search_listings`
  implementation and spot errors in the code.
- _What came back:_ The AI pointed out that my `sort()` and `return` statements
  were indented inside the `for` loop, which caused the function to return
  after checking only the first listing.
- _What I changed:_ I moved the sorting and final return outside the loop so
  every listing is checked before the results are ranked and returned.

**Moment 2**

- _What I asked for:_ I asked AI to help me design and connect the planning
  loop in `agent.py`.
- _What came back:_ The AI suggested storing each tool result in the session
  dictionary and branching immediately when `search_listings` returned an
  empty list.
- _What I changed:_ I implemented the loop so search results, the selected item,
  the outfit suggestion, and the fit card all move through session state. I also
  added an early-stop message that tells the user to change the description,
  size, or maximum price when no listing matches.

**Moment 3 — Unit 4 Testing**

- _What I asked for:_ I asked AI to help me review the results of my before-and-after evaluations and identify one improvement I could make without changing the original acceptance criteria.

- _What came back:_ AI helped me identify that the fit-card prompt could be more specific, even though all five baseline trials met Criterion 4. It suggested clearer rules for including the item price, selling platform, sentence count, and outfit details.

- _What I changed:_ I updated the prompt inside `tools.py::create_fit_card()` with seven specific instructions. I then ran `python run_eval.py --label after` with caching disabled and compared the new results with my baseline evaluation. The criteria still passed at 5/5, so I reported maintained performance rather than claiming an increase in the pass rate.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

| Criterion                   | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict   |
| --------------------------- | ------ | ----- | ----- | ----- | ----- | ----- | --------- |
| 1. Three-tool workflow      | 4/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 2. Empty search stops early | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 3. Selected item preserved  | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 4. Fit-card details         | 4/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 5. Maximum price respected  | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |

### Evidence from the Baseline Evaluation

The following examples are actual outputs from the baseline evaluation,
produced by `run_eval.py::main` using `agent.py::run_agent`.

### Evidence — Criterion 1

**Source:** `results/run_2026-10-11_2216_before.md`  
**Produced by:** `run_eval.py::main`, using `agent.py::run_agent`

**Query:** `vintage graphic tee under $30`

**Try 1:**

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: **Outfit 1: Ultimate Y2K Streetwear** Pair the Y2K Butterfly Baby Tee with your **baggy straight-leg jeans (da…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channeling total early 2000s energy with this dreamy butterfly print baby tee, yours on depop for just $18.0! …
```

### Evidence — Criterion 2

**Source:** `results/run_2026-10-11_2216_before.md`  
**Produced by:** `run_eval.py::main`, using `agent.py::run_agent`

**Query:** `designer ballgown size XXS under $5`

**Try 1:**

```text
- stopped early: yes — I couldn't find a matching listing. Try changing the description, size, or maximum price.
- selected_item: (none)
- search_results: 0

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] empty_search_branch
      →    No matching listings. Stopping the agent.
```

### Evidence — Criterion 3

**Source:** `results/run_2026-10-11_2216_before.md`  
**Produced by:** `run_eval.py::main`, using `agent.py::run_agent`

**Query:** `vintage graphic tee under $30`

**Try 1:**

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: **Outfit 1: Y2K Streetwear** *   **New Item:** Y2K Baby Tee *   **Wardrobe Pieces:** Baggy straight-leg jeans …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Living out my early 2000s pop star dreams in this butterfly Y2K Baby Tee. Grabbed it for just $18.0 over on de…
```

**Verification:** In `agent.py::run_agent`, the agent assigns `session["search_results"][0]` to `session["selected_item"]` and passes `session["selected_item"]` directly to `suggest_outfit()`. The trace shows that the outfit was generated for the selected Y2K Baby Tee.

The trace does not independently compare the complete item dictionaries.

### Evidence — Criterion 4

**Source:** `results/run_2026-10-11_2216_before.md`  
**Produced by:** `run_eval.py::main`, using `agent.py::run_agent`

**Query:** `vintage graphic tee under $30`

**Selected item:** Y2K Baby Tee — Butterfly Print ($18.0, depop)

**Try 1 — Fit card:**

```text

Channeling peak early 2000s streetwear with this dreamy Y2K Baby Tee — Butterfly Print, paired with baggy denim and chunky white sneakers. It's the ultimate casual vintage mix for running errands or grabbing iced coffee. Grab this piece for just $18.0 before it's gone, exclusively on depop!

```

**Verification:** The fit card includes the selected item's price ($18) and platform (Depop) and contains between 2 and 4 sentences.

### Evidence — Criterion 5

**Source:** `results/run_2026-10-11_2216_before.md`  
**Produced by:** `run_eval.py::main`, using `agent.py::run_agent`

**Query:** `vintage graphic tee under $20`

**Try 1:**

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 8
```

**Verification:** The selected listing costs $18, which is within the $20 maximum price. The `search_listings()` function in `tools.py` checks each listing against `max_price` and excludes listings whose prices exceed the limit.

The baseline run log reports eight matching results but does not display all eight prices. Therefore, the code logic supports the criterion, while the saved trace alone does not independently prove that every result meets the price limit.

## Verdicts and Diagnoses

I tested my five acceptance criteria using five trials for each criterion, with caching disabled. All five criteria met their original targets.

**Criterion 1 — MET (5/5):** The agent completed the full three-tool workflow in all five trials. It searched for listings through MCP, generated outfit suggestions, and created a fit card.

**Criterion 2 — MET (5/5):** The agent correctly stopped when the search returned no matching listings. It displayed a message suggesting changes to the description, size, or maximum price without calling the remaining tools.

**Criterion 3 — MET (5/5):** The selected item remained consistent throughout the workflow. The agent stored the first search result in `session["selected_item"]` and passed that same item to `suggest_outfit()`.

**Criterion 4 — MET (5/5):** All five generated fit cards included the selected item's price and platform and stayed within the required 2–4 sentences. The wording varied, but the required information remained present.

**Criterion 5 — MET (5/5):** The search respected the maximum price. The filtering logic excluded listings priced above the user's budget before returning the results.

### Diagnosis

None of the five criteria missed its target in the baseline evaluation.

However, I noticed that my tests mainly used straightforward queries. For example, the matching-query tests repeatedly selected the same Y2K Baby Tee. This means the results do not fully demonstrate how the agent performs with more difficult descriptions or different listing types.

If I were to make one criterion stricter, I would improve Criterion 1 by testing five different matching queries instead of repeating the same query. This would help measure the agent's ability to handle different clothing descriptions.

---

## Loop Trace

I added tracing to `run_agent()` using `trace.start_trace()` and `trace.step()`. The trace records each tool call, its inputs, and its returned results. The `search_listings` tool now runs through MCP, while the other two tools remain direct Python function calls.

**Test command:**

`python app.py ask 'vintage graphic tee under $30' --trace`

**Actual trace output:**

```text
[1] search_listings (via MCP)
    in:  dict with keys: description, size, max_price
    out: 10 items: Y2K Baby Tee – Butterfly Print, Graphic Tee – 2003 Tour Bootleg Style, Vintage Band Tee – Faded Grey … +7 more

[2] suggest_outfit
    in:  dict with keys: selected_item, wardrobe
    out: **Outfit 1: Y2K Streetwear** **New Item:** Y2K Baby Tee ...

[3] create_fit_card
    in:  dict with keys: outfit, new_item
    out: Channeling major 2000s pop star energy with this Y2K baby tee, and it can be yours for just $18.0! ...
```

**Result:** The agent successfully completed all three tool calls in the correct order. The MCP search returned matching clothing listings, the outfit tool generated styling suggestions, and the fit-card tool created a final caption.

No errors occurred during this run.

### Additional Failure-Mode Tests

**Empty wardrobe**

I tested the agent with an empty wardrobe to check whether `suggest_outfit()` could handle missing wardrobe items. Instead of failing, the tool provided general styling advice for the selected listing. The additional diagnostic completed successfully in all five evaluation trials.

**Unavailable model / invalid API key**

I temporarily tested the application with an invalid Gemini API key to trigger a model failure. The application reported an error explaining that the model rejected the API key and directed me to check `GEMINI_API_KEY` in the `.env` file.

The error was:

```text id="91d2ym"
ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

I restored the valid configuration after the test. This verified that a model authentication failure produces a useful diagnostic message instead of silently returning a misleading result.

**Empty search**

Command:

`python app.py ask 'designer ballgown size XXS under $5' --trace`

Output from `results/run_2026-10-11_2216_before.md`, produced by `run_eval.py::main` using `agent.py::run_agent`:

```text
- stopped early: yes — I couldn't find a matching listing. Try changing the description, size, or maximum price.
- selected_item: (none)
- search_results: 0

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] empty_search_branch
      →    No matching listings. Stopping the agent.
```

The agent correctly stopped after the MCP search returned an empty list. It did not call `suggest_outfit` or `create_fit_card`.

**On the MCP move:**

I moved `search_listings` from a direct Python function call to an MCP tool.

I created `mcp_server.py` using `FastMCP` and registered `search_listings` as an MCP tool. I then updated `agent.py::run_agent` to call the search tool through `mcp_client.py`.

The other two tools, `suggest_outfit` and `create_fit_card`, remain direct Python function calls.

After the change, the agent successfully searched listings through MCP, selected a matching item, generated outfit suggestions, and created a fit card. The trace confirms that the MCP search runs before the other tools.

The MCP integration did not change the expected behavior of the agent. The empty-search branch also continued to work correctly.

---

## The Improvement

### What I changed

I improved the prompt inside `create_fit_card()` in `tools.py`.

Before the change, the prompt asked the model to create a natural social-media caption of 2–4 sentences and mention the item, price, and selling platform.

I replaced those general instructions with seven specific rules. The updated prompt asks the model to include the exact price, mention the selling platform, keep the caption between 2 and 4 sentences, describe at least one outfit detail, avoid repeating information, and return only the caption.

### Why I chose this improvement

During my baseline evaluation, all five criteria met their targets. However, because the fit card is generated by an AI model, I wanted to make its instructions clearer and reduce the chance of missing important listing details in future runs.

### Run Log — After

I ran the same six scenarios again using:

`python run_eval.py --label after`

Caching was disabled, and each scenario ran five times.

| Criterion                   | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict   |
| --------------------------- | ------ | ----- | ----- | ----- | ----- | ----- | --------- |
| 1. Three-tool workflow      | 4/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 2. Empty search stops early | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 3. Selected item preserved  | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 4. Fit-card details         | 4/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 5. Maximum price respected  | 5/5    | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |

Criteria 3 and 5 were evaluated using the deterministic session-state handoff and price-filtering logic. The run logs do not independently assert these conditions.

The additional empty-wardrobe diagnostic completed successfully in all five trials.

### Did the improvement help?

The results stayed at 5/5 for all five acceptance criteria.

The updated prompt continued to generate captions with the required price, platform, and sentence count. All five fit cards in the after-run met Criterion 4.

I cannot conclude that the improvement increased the pass rate because the baseline already achieved 5/5. However, the new prompt provides clearer instructions about the required caption format.

One remaining limitation is that some captions use similar opening phrases. In the future, I would test more clothing items and improve the variety of generated captions.

### Evidence — After Run, Criterion 4

**Source:** `results/run_2026-10-11_2252_after.md`  
**Produced by:** `run_eval.py::main`, `agent.py::run_agent`, and `tools.py::create_fit_card`

**Query:** `vintage graphic tee under $30`

**Try 1:**

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Channel your inner 2000s pop star with this adorable Y2K baby tee featuring a gorgeous butterfly print! It looks so good styled with baggy dark-wash jeans and a cropped zip hoodie for the ultimate streetwear vibe. Grab this rare little gem for just $18.0 over on Depop before it's gone!
```

**Verification:** The after-run fit card contains three sentences, includes the $18.0 price and Depop platform, and describes the outfit. It meets Criterion 4.

---

## What's Still Broken

All five acceptance criteria met their original targets in both the before and after evaluations. There are no known failures against these criteria.

However, I identified a few limitations that I would like to improve in future work.

First, my evaluation repeatedly selected the same Y2K Baby Tee, so it did not test many different clothing items. I would add more search queries covering different styles, sizes, and categories.

Second, some generated fit cards still use similar opening sentences. I would improve the prompt further to generate more varied captions while keeping the required price, platform, and outfit details.

Third, my evaluation logs do not independently verify that the complete selected-item dictionary stays unchanged or that every returned listing meets the maximum price. I would add automatic assertions to check these conditions.

I stopped after making one prompt improvement because I wanted to compare the before and after results without introducing several changes at once. The results showed that the agent maintained its original performance.

<!-- ===================================================================== -->
<!-- =====================================================================-->

## Capstone

**What This Extends**

I extended FitFindr, the outfit-shopping agent I built in Units 3 and 4. The capstone adds a two-second deadline to the MCP listing request and writes structured evidence for successful runs and timeouts.

**The Shape**

I chose Shape B, Harden against failure. If the listing search times out, FitFindr asks the user to try again and stops before generating an outfit or fit card. Automatic retries, fallback search providers, and changes to outfit generation were out of scope.

**Running It**

I chose Path B, local with logs. Follow [RUNNING.md](RUNNING.md) to set up the environment, then run the query below from the repository root in Git Bash. For live fit-card generation, set `GEMINI_API_KEY` in the checkout’s local `.env`.

```bash
python app.py ask 'vintage graphic tee under $30' --trace
```

I verified both paths in a separate local checkout at commit `d8ba7b8`. With `FITFINDR_TEST_SEARCH_DELAY=5`, the MCP timeout was recorded after 2,020.224 ms. With the API key configured, the normal run generated a fit card and logged `success` in 6,633.215 ms of agent runtime, using 581 prompt tokens and 170 output tokens across two live Gemini calls.

**Instrumentation**

FitFindr appends JSON records to `logs/runs.jsonl`. Each record below includes a UTC timestamp, query, response, agent duration in milliseconds, and status. Timeout records also include `search_timeout_ms`, measured from the start of the MCP tool request through cleanup and the timeout trace. Agent duration also includes MCP startup.

The excerpt contains the six scored after trials and four additional successful runs.

```jsonl
{"timestamp": "2026-11-19T00:56:20.144984+00:00", "query": "vintage graphic tee under $30", "response": "The listing search timed out. Please try again.", "elapsed_ms": 4279.787, "status": "timeout", "search_timeout_ms": 2015.848}
{"timestamp": "2026-11-19T00:56:25.165372+00:00", "query": "vintage graphic tee under $30", "response": "The listing search timed out. Please try again.", "elapsed_ms": 4362.671, "status": "timeout", "search_timeout_ms": 2010.926}
{"timestamp": "2026-11-19T00:56:30.301992+00:00", "query": "vintage graphic tee under $30", "response": "The listing search timed out. Please try again.", "elapsed_ms": 4419.346, "status": "timeout", "search_timeout_ms": 2012.162}
{"timestamp": "2026-11-19T00:56:33.296176+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2364.071, "status": "success"}
{"timestamp": "2026-11-19T00:56:36.289341+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2478.234, "status": "success"}
{"timestamp": "2026-11-19T00:56:39.261072+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2516.346, "status": "success"}
{"timestamp": "2026-11-19T01:00:03.225922+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2477.773, "status": "success"}
{"timestamp": "2026-11-19T01:00:06.535304+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2783.831, "status": "success"}
{"timestamp": "2026-11-19T01:00:09.784001+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2776.119, "status": "success"}
{"timestamp": "2026-11-19T01:00:12.914333+00:00", "query": "vintage graphic tee under $30", "response": "Channel your inner early 2000s icon with this adorable Y2K baby tee featuring a dreamy butterfly print! Style it with baggy dark-wash jeans and chunky white sneakers for the ultimate nostalgic streetwear fit. Grab this nostalgic gem right now on depop for just $18.0!", "elapsed_ms": 2645.402, "status": "success"}
```

Failure example from a separate run with a five-second server delay:

```jsonl
{"timestamp": "2026-11-19T01:06:12.628221+00:00", "query": "vintage graphic tee under $30", "response": "The listing search timed out. Please try again.", "elapsed_ms": 5004.415, "status": "timeout", "search_timeout_ms": 2067.542}
```

**What It Costs**

I measured elapsed agent time on ten local runs by averaging the `elapsed_ms` field in the excerpt above. The sample included seven successful searches with cached model responses and three timeouts. It averaged **3.11 seconds per run**. At the same mix of outcomes and cache behavior, 100 sequential runs per day would take about 3.11 × 100 = **311 seconds**, or **5 minutes and 11 seconds**. The separate live checkout run took 6.63 seconds and used 751 tokens.

**Run Log and Verdicts**

I used the same query in all trials. For criteria 1–4, the server delayed its search response by five seconds. For criterion 5, it used a 100 ms delay. The slow baseline runs took **8.043 s**, **8.010 s**, and **8.373 s** end to end. Those timings include process startup and downstream work.

| Criterion | Trial 1 | Trial 2 | Trial 3 | Evidence and diagnosis |
|---|---|---|---|---|
| 1. Enforce the MCP search deadline | MISSED | MISSED | MISSED | The client awaited the delayed MCP response without a request deadline. No trial reported a timeout. |
| 2. Show a clear timeout message | MISSED | MISSED | MISSED | The agent received a normal search result and had no timeout branch to display a retry message. |
| 3. Stop the outfit workflow after a timeout | MISSED | MISSED | MISSED | All three searches returned listings and the agent ran both downstream tools. |
| 4. Write a structured timeout record | MISSED | MISSED | MISSED | The terminal trace was the only run evidence. No `logs/runs.jsonl` file existed. |
| 5. Create a fit card when the search succeeds | MET | MET | MET | Each fast trial produced a card describing the matching butterfly-print Y2K baby tee at $18. |

**The Improvement**

I applied the deadline to the MCP listing request after server initialization. When the deadline expires, the client cancels the request and the agent ends the workflow before calling either downstream tool. I also added JSONL logging so the response and timing can be checked for each completed run covered by the tests. The server’s test delay lets me reproduce both the slow and fast cases.

| Criterion | Trial 1 | Trial 2 | Trial 3 | Evidence |
|---|---|---|---|---|
| 1. Enforce the MCP search deadline | MET | MET | MET | The MCP timeout was recorded at 2,015.848 ms, 2,010.926 ms, and 2,012.162 ms, all below the 3,000 ms target. |
| 2. Show a clear timeout message | MET | MET | MET | Every slow trial displayed “The listing search timed out. Please try again.” |
| 3. Stop the outfit workflow after a timeout | MET | MET | MET | The slow traces showed zero calls to `suggest_outfit` and `create_fit_card`. |
| 4. Write a structured timeout record | MET | MET | MET | The six scored runs produced six log records that minute. Each slow trial had its own UTC timestamp, query, message, positive duration, and `timeout` status. |
| 5. Create a fit card when the search succeeds | MET | MET | MET | All three fast trials produced a fit card describing the matching butterfly-print baby tee at $18. |

**What's Still Broken**

All five criteria were met after the change. I would tighten criterion 1 by lowering the reporting limit from 3,000 ms to 2,500 ms while keeping the two-second request deadline. The three measured timeout trials used only a small fraction of the original one-second allowance for cleanup and reporting.

During the clean-checkout test, Gemini authentication errors could exit before writing a run record. With another unit, I would first add an error record for that failure path. This would make a failed run visible in the log even when it stops before creating a fit card.

**How I Used AI**

1. I asked why the five-second test runs were finishing in under five seconds. AI suggested checking how the MCP subprocess received the test environment variable. I used Git output to inspect the startup code, added explicit forwarding, and reran the baseline with the delay in effect.
2. I asked for help verifying the clean checkout after Gemini rejected the API key. AI suggested checking the exact configuration path and whether the key loaded without printing it. I found that the checkout had no local `.env`, copied the working configuration locally, and reran the test to verify a live fit card and a new success record.
