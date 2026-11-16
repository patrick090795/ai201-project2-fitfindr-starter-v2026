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

  
**Moment 3 — Unit 4 Testing**

- *What I asked for:* I asked AI to help me review the results of my before-and-after evaluations and identify one improvement I could make without changing the original acceptance criteria.

- *What came back:* AI helped me identify that the fit-card prompt could be more specific, even though all five baseline trials met Criterion 4. It suggested clearer rules for including the item price, selling platform, sentence count, and outfit details.

- *What I changed:* I updated the prompt inside `tools.py::create_fit_card()` with seven specific instructions. I then ran `python run_eval.py --label after` with caching disabled and compared the new results with my baseline evaluation. The criteria still passed at 5/5, so I reported maintained performance rather than claiming an increase in the pass rate.


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before


| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Three-tool workflow | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item preserved | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit-card details | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Maximum price respected | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |


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

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Three-tool workflow | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item preserved | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit-card details | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Maximum price respected | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

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

I’m extending FitFindr, the outfit-shopping agent I built in Units 3 and 4.

**The Shape**

I chose Shape B to handle slow responses from the MCP listing search.
If the search exceeds its deadline, FitFindr will tell the user that
the search timed out, end the run before the outfit and fit-card steps,
and record the outcome using the existing structured logger.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
