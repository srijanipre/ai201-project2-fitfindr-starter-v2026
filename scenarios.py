"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # Criterion 1: A query the data can match should complete all three tools
        # and return a fit card without stopping early.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # Criterion 2: A query that matches nothing should stop before calling
        # suggest_outfit, returning only an error message. Tests the branch logic.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3: The item selected from search results should be stored in
        # the session and passed to suggest_outfit unchanged. Verifies data flow.
        "name": "session state - search matches selected",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: Running the same query multiple times should produce
        # different fit cards with varying opening sentences, but all must be
        # 2-4 sentences and mention price and platform exactly once each.
        "name": "fit card variance - same item",
        "query": "silk slip dress under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: When search is given a max_price filter, all returned
        # items must be at or below that price. Tests the price ceiling logic.
        "name": "price ceiling filter",
        "query": "vintage under $25",
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
