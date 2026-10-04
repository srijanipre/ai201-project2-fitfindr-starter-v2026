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

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card varies but stays in bounds | 5 of 5 | FAIL | FAIL | FAIL | FAIL | PASS | MISSED (1/5) |
| 5. Search respects the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (4/5) |

**Real output from criterion 4, try 1** (from `results/run_2026-10-04_1700_before.md`):

```
Fit card:

The 90s indie sleaze dress of your dreams just dropped. 🥀 Midi length muted floral silk with adjustable straps—throw it on with combat boots and an oversized sweatshirt or a denim jacket and chunky sneakers. One tiny snag on the side seam that completely disappears when it's on, yours for $30. ✨ DM to claim!
```

**Real output from criterion 4, try 5**:

```
Fit card:

the 90s model-off-duty slip dress of your dreams 🕊️ throw an oversized crewneck over it to turn it into a midi skirt, or layer a vintage leather jacket and combat boots on top. minor snag on the side seam that completely disappears when it's on, yours for $30 ✨ #9ugs #depop #slipdress #90sgrunge
```

**Real output from criterion 2, try 1**:

```
stopped early: yes — Couldn't find anything matching that. Try a different search or higher budget.
```

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Full three-tool run returns a fit card | 4 of 5 | MET | All 5 tries completed all three tools and returned a fit card. |
| 2 | Empty search stops before tool 2 | 5 of 5 | MET | All 5 tries on the impossible query returned "stopped early: yes" with the error message before calling suggest_outfit. |
| 3 | Item in session matches item passed on | 5 of 5 | MET | All 5 tries on the matching query returned the same selected_item that was the first result from search_listings. |
| 4 | Fit card varies but stays in bounds | 5 of 5 | MISSED | Only 1 of 5 fit cards mentions the platform (depop). Tries 1-4 don't include the platform in the caption, violating the "mention the platform exactly once" requirement. |
| 5 | Search respects the price ceiling | 5 of 5 | MET | All 5 tries returned only items under $25 when given max_price=$25. All selected items were $18.0. |

**Diagnoses**

**Criterion 4 miss:** The create_fit_card tool's prompt mentions that the caption should "mention the item and its price and platform once each," but only 1 of 5 tries actually included the platform in the caption. The other 4 tries included the price but omitted the platform entirely. This is a model output issue — the prompt isn't constraining the model strongly enough to guarantee platform inclusion.



---

## Loop Trace

**Happy path** (vintage graphic tee under $30):

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +7 more
[3] select_item
      in:  10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +7 more
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: new_item, wardrobe_size
      out: Here are two outfit combinations using the new Y2K baby tee and pieces from your existing wardrobe: …
[5] create_fit_card
      in:  dict with keys: outfit_length, item
      out: The Y2K butterfly baby tee of your dreams just dropped 🦋✨ Super fitted crop length that looks so good with bag…
```

**Empty search** (designer ballgown size XXS under $5):

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch
      →    search returned empty, stopping
```

**On the MCP move:** Changed run_agent() in agent.py to call `call_tool("search_listings", {...})` instead of the direct function call. The MCP call succeeds — search_listings still returns the same list of dicts it did before. The trace.step() call for search_listings now shows "(via MCP)" to make the protocol change visible in the trace.



---

## The Improvement

**What I changed:** Modified the create_fit_card() prompt to explicitly require the platform in the caption. Changed from a soft suggestion ("mention the price and platform") to explicit instructions: "Your caption must mention the price exactly once and the platform ({platform_name}) exactly once. Include price and platform in the caption."

**Which failure it was meant to fix:** Criterion 4 — fit card variance. The model was not consistently including the platform (depop) in 4 of 5 tries. By making the prompt constraint more explicit, the model should reliably include both price and platform.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card varies but stays in bounds | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search respects the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (4/5) |

**Sample fit card from after run, try 1:**

```
Obsessed with this 90s floral midi slip dress, but I have way too many dresses right now. Throwing a black hoodie and combat boots over it is my absolute favorite way to style it. Grab it on my depop for just $30 before I change my mind!
```

**Did it help, and how do I know:** Yes. Criterion 4 went from 1/5 to 5/5. All five after-test captions now mention the platform (depop) explicitly and meet all the constraints: different opening sentences, 2-4 sentences, price mentioned once, platform mentioned once. The tightened prompt fixed the reliability issue.



---

## What's Still Broken

All five criteria now pass in the after run. The one miss in criterion 4 was fixed by tightening the create_fit_card prompt. No further work needed for this submission.



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
