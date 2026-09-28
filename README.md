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

<!-- Three or four sentences: what a user asks for, and what they get back. -->

User gives a search query (like "vintage graphic tee under $30"). The agent searches for matching listings, picks the best one, asks the model to suggest outfits using their wardrobe, then asks the model to write a social media caption for the item. Returns the caption or an error if nothing matched.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches through all the listings data to find items that match what the user is looking for, filtering by keywords, size, and price if needed.
- **Inputs:** `description` (string — what the user wants to find), `size` (string or None — clothing size to filter by), `max_price` (float or None — highest price the user will pay)
- **Returns:** A list of listing dicts, ordered best match first. Each dict has: id, title, description, category, style_tags, size, condition, price, colors, brand, and platform.
- **When it has nothing:** Returns an empty list (not None or an exception) when no listings match the search.

### `suggest_outfit`

- **What it does:** Takes a new item someone found and looks at their existing wardrobe, then asks the model to suggest one or two outfit combinations they could make.
- **Inputs:** `new_item` (a listing dict), `wardrobe` (a dict with an 'items' key that holds a list of wardrobe items — might be empty)
- **Returns:** A non-empty string with outfit suggestions and styling ideas.
- **When it has nothing:** If the wardrobe is empty, return general styling advice for that item instead of trying to pair it with stuff they don't have.

### `create_fit_card`

- **What it does:** Takes the outfit suggestion and the new item, then asks the model to write a short caption like someone would post on social media about finding the item.
- **Inputs:** `outfit` (a string — the outfit suggestion from suggest_outfit), `new_item` (a listing dict)
- **Returns:** A two-to-four sentence caption that sounds like a real post, mentions the item, price, and platform once each, and captures the vibe.
- **When it has nothing:** If the outfit string is empty or just whitespace, return a descriptive message instead of crashing.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put an error message in the session and stop. Otherwise, take the first result, pass it to suggest_outfit, then pass that outfit to create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** String splitting — looks for "under" or "$" to find max_price, "size" to find size, and treats the whole query as the search description.

**What moves through the session:** parsed query → search_results list → selected_item → outfit_suggestion → fit_card (error is set only if search is empty)

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; results = search_listings('graphic tee', max_price=30); print(f'Found {len(results)} results'); print(f'First: {results[0][\"title\"]} - \${results[0][\"price\"]}' if results else 'No results')"
Found 7 results
First: Y2K Baby Tee — Butterfly Print - $18.0
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; result = suggest_outfit(load_listings()[0], get_example_wardrobe()); print(result[:200])"
Here are two ways to style the Vintage Levi's 501 jeans using pieces from your existing wardrobe:

### Look 1: Casual & Effortless
* **Top:** White ribbed tank top
* **Outerwear:** Oversized grey crew
```

```
$ python -c "from tools import create_fit_card; outfit = 'white tank with vintage jeans'; from utils.data_loader import load_listings; item = load_listings()[0]; print(create_fit_card(outfit, item))"
Found the holy grail of denim today 😭 The wash on these vintage 501s is unreal, and that little bit of knee fading gives them so much character. Style them with a basic white tank and you're literally good to go. Grab them before I change my mind and keep them forever! 🤌✨
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Why is create_fit_card giving me the same exact words three times?
- *What came back:* Check if CACHE_ENABLED is on (it probably is), or if TEMPERATURE is 0.
- *What I changed:* Found CACHE_ENABLED was True. Added `cache=False` when calling generate in create_fit_card so it wouldn't reuse the same answer.

**Moment 2**

- *What I asked for:* Why does my agent stop when it shouldn't? Let me trace through it.
- *What came back:* The agent was working fine, but I realized I wasn't putting the selected item in the session first before passing it to suggest_outfit. Without that, I couldn't test if the right item made it through.
- *What I changed:* Now I put everything in session — selected_item, outfit_suggestion, fit_card so I can see what's moving through the loop.

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
