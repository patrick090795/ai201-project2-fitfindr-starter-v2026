# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---
## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because the search uses keyword matching, so some reasonable
phrasings may not match the listing text exactly. I still expect the normal
happy path to succeed most of the time.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because this branch is deterministic. When `search_listings`
returns an empty list, the loop should always stop and should never pass an
empty result into the next tool.

---

## 3. The selected item is preserved through session state

For a query that returns at least one result, the item stored in
`session["selected_item"]` is the same listing passed into `suggest_outfit`
— in 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because session state is controlled by the program and does not
depend on model variation. The selected listing should always move through the
session unchanged before it reaches `suggest_outfit`.

---

## 4. The fit card includes the important listing details

For a successful run, the fit card mentions the selected item's price and
platform, and stays between 2 and 4 sentences — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because `create_fit_card` uses a language model, so the wording
can vary between runs. Most cards should still include the required listing
details and stay short enough to read like a social-media caption.

---

## 5. Search results respect the maximum price

Given a query with a maximum price, every listing returned by
`search_listings` has a price less than or equal to that maximum — in 5 of 5
tries.

**Why this target:**
I chose 5 of 5 because the price filter is handled directly by the search tool,
not by the language model. A listing over the user's stated budget should never
be returned.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->



**Why this target:**



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->



**Why this target:**



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
