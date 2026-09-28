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

**Why this target:** My search is doing a keyword match, so some phrasings of the same thing will definitely miss (like asking for "vintage band tee" when I only look for exact words in the description). 4 of 5 feels realistic for that kind of matching.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** This one's deterministic — if the search returns an empty list, the branch just checks and stops. There's no randomness here, so it should work every time. The model isn't involved, just my branching logic.

---

## 3. Session state stays correct

When search_listings finds results, the selected_item in the session (the first result from the search) has the same title, price, and platform as the item that actually reaches suggest_outfit. Check this 5 of 5 tries.

**Why this target:** If I pass data through the session correctly, there's no randomness or matching involved — it's just moving the same dict from one place to another. As long as I'm reading and writing correctly, this should be 100% reliable.

---

## 4. Fit card varies but stays in bounds

For the same item and outfit suggestion, run create_fit_card three separate times and get three captions with different opening sentences. Also, all captions must be 2-4 sentences, mention the price exactly once, and mention the platform exactly once. Check this 5 of 5 tries.

**Why this target:** The model has temperature > 0, so it should always vary. But the structural stuff (sentence count, mentioning required fields) should be consistent — the prompt should be clear enough for that. That's 5 of 5.

---

## 5. Search respects the price ceiling

When given a max_price filter, search_listings returns zero results with a price above that ceiling. Test with different price ranges. Pass this 5 of 5 tries.

**Why this target:** Price filtering is just a number comparison, no AI involved. If I implement it, it should be bulletproof every time. This matters because someone actually trusts the budget they set.



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
