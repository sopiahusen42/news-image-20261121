#!/usr/bin/env python3
"""gen_entry.py — draws the front-page digest for SATURDAY, 21 NOVEMBER 2026.

Output: entry.png, 1024x1024, three colors (cream paper #f5efe3, ink #191919,
red accent #b3202c). Deterministic: no randomness, no timestamps, no network.
Re-running always writes byte-identical output.

Layout: MASTHEAD / HERO GRID (8 cards, 2x4) / WIRE COLUMNS (3) / FOOTER.
Every text block is measured and auto-shrunk so nothing overflows or clips.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 239, 227)  # #f5efe3
INK = (25, 25, 25)       # #191919
RED = (179, 32, 44)      # #b3202c

OUT = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1048576

# --------------------------------------------------------------------- fonts
_FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{_FDIR}/DejaVuSerif-Bold.ttf"
SERIF = f"{_FDIR}/DejaVuSerif.ttf"
SANS_B = f"{_FDIR}/DejaVuSans-Bold.ttf"
SANS = f"{_FDIR}/DejaVuSans.ttf"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def serif_bold(size):
    return _font(SERIF_B, size)


def serif(size):
    return _font(SERIF, size)


def sans_bold(size):
    return _font(SANS_B, size)


def sans(size):
    return _font(SANS, size)


# ------------------------------------------------------------------- helpers
def text_len(d, s, f, tracking=0.0):
    if tracking:
        return sum(d.textlength(c, font=f) for c in s) + tracking * (len(s) - 1)
    return d.textlength(s, font=f)


def draw_tracked(d, x, y, s, f, fill, tracking=0.0):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def draw_centered(d, y, s, f, fill, cx, tracking=0.0):
    w = text_len(d, s, f, tracking)
    draw_tracked(d, cx - w / 2, y, s, f, fill, tracking)


def wrap(d, s, f, max_w, tracking=0.0):
    """Greedy word wrap; every returned line is <= max_w wide."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if not cur or text_len(d, trial, f, tracking) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------- data
TITLE = "THE WORLD"
DATELINE = "SATURDAY, 21 NOVEMBER 2026"
DECK = "One-page digest of the day's world news - wire as of 02:00 UTC"

CARDS = [
    ("WORLD",
     "ICJ FINDS MYANMAR GUILTY OF GENOCIDE; WORLD REACTS",
     'Bangladesh demands compensation and safe, voluntary return of Rohingya; Myanmar rejects the 9-to-6 ruling as "unfair"; Rohingya in Australia mark the "historic judgment"'),
    ("CONFLICT",
     "RUSSIA'S MISSILE WAVE STRIKES UKRAINE; POLAND ON ALERT",
     'Overnight strikes kill 3 in Kyiv and cut power; Poland calls two objects over its border a "provocation" and NATO condemns the incursion'),
    ("MIDDLE EAST",
     "RIYADH UNDER MISSILE ALERT AS HOUTHI BARRAGE GROWS",
     'Coalition says it intercepted 3 ballistic missiles over the Saudi capital - second strike in days after the Jeddah tower was hit; airspace warned "unsafe"'),
    ("DIPLOMACY",
     'TRUMP HOME FROM SHENZHEN: "MOST SUCCESSFUL" ASIA TRIP',
     'APEC "peace declaration" with Xi and Putin; US-China deal to keep humans in military AI decisions; Ukraine talks "very good"; North Korea visit postponed'),
    ("MARKETS",
     "US STOCKS CONFIRM CORRECTION AFTER ANTHROPIC IPO WEEK",
     "S&P 500 and Dow now more than 10% below record highs as AI-trade worries spread; Anthropic's record debut raised $81.3bn"),
    ("SCIENCE",
     "RESEARCHER CLAIMS RIEMANN PROOF, MADE WITH CLAUDE",
     "Anthropic's Levent Alpoge publishes a four-page note claiming to prove the 160-year-old conjecture; independent verification awaited"),
    ("US POLITICS",
     "SENATE REJECTS IRAN WAR-POWERS RESOLUTION 51-48",
     'Trump says Iran "may be exploring bioweapons" and postpones a strike decision past 1 Jan; White House fires cybersecurity chief after outages'),
    ("SPORTS",
     "ALCARAZ SWEEPS ATP FINAL GROUP; F1 TO RETURN TO V8",
     "Alcaraz 3-0 (6-4 6-1 over Cobolli) and through to face Shelton; FIA green-lights V8 engines from 2030; India 159/1 vs New Zealand; Pochettino's first Man Utd session"),
]

WIRE = [
    ("EUROPE", [
        'Estonia to close border with Russia; Moscow decries "new Iron Curtain"',
        "UK and EU clinch food, emissions and youth deals; stuck on tuition fees",
        "PM Burnham in Brussels: all options on table, including EU return",
        "Young protesters hit the streets across Europe",
        "de Villepin launches French presidential bid, warns against Le Pen",
        "BBC faces deeper cuts; audit office flags risk in 500m savings plan",
        "Spain's 69-dead rail crash probe: EU rail agency to assist Madrid",
        "19 crew airlifted after cargo ship runs aground off SW France",
        "UK finds fix for fridge and freezer hack flaw",
    ]),
    ("AMERICAS", [
        "Ex-President Bolsonaro hospitalized with intestinal obstruction",
        "American woman freed after 10 years in Cuba",
        "Virginia records first measles-associated death of 2026",
        "Thousands protest tax plan across Colombia",
        "DOJ drops Alaska lawsuit",
        "Ford, Honda, Stellantis, VW sue New Jersey over vehicle repair law",
        "USDA breached by hackers this week, sources say",
        "Trump's $15bn suit against the New York Times allowed to proceed",
    ]),
    ("ASIA-PACIFIC", [
        "Rohingya in Australia react to ICJ genocide ruling",
        "Sydney man arrested over car-bomb research, IS links alleged",
        "Senate inquiry backs digital duty-of-care bill, with amendments",
        "Sandpapergate: government urges Cricket Australia forum transparency",
        "Turkey starts offshore hydrocarbon exploration in Pakistan waters",
        'BJP slams Rahul Gandhi over "Pak fan boy" remark',
        "US religious-freedom panel: India targeting Muslims in voter-roll revisions",
        "GTA 6 sales top $2.3bn, industry estimate",
        "Scientists study rare Ebola variant in Congo outbreak",
    ]),
]

FOOTER = [
    "Compiled Saturday 21 November 2026, 02:00 UTC - a digest of events reported on 21 November (any time zone) and late 20 November. Sources: AP, Reuters, AFP, Straits Times, SBS, NYT, Business Standard, Arab News, CNN, DW, Times of Israel, The Hill.",
    "Built by an AI agent for the make.fun bounty 'Sum up 21 November's world news in one image' - entry.png, 1024x1024, MIT licensed.",
]

# ----------------------------------------------------------------- geometry
M = 40                      # side margin
CW = W - 2 * M              # content width 944

HERO_Y0 = 180
CARD_H = 120
CARD_GAP = 8
CARD_W = (CW - 16) // 2     # 464
CARD_XS = [M, M + CARD_W + 16]
HERO_Y1 = HERO_Y0 + 4 * CARD_H + 3 * CARD_GAP   # 674

WIRE_Y0 = 696
WIRE_TITLE_Y = WIRE_Y0
WIRE_ITEMS_Y0 = 722
WIRE_Y1 = 946
WIRE_COLS = 3
WIRE_COL_W = (CW - 2 * 14) // 3   # 305
WIRE_GX = 14

FOOTER_RULE_Y = 958
FOOTER_TEXT_Y = 968


# ------------------------------------------------------------------- blocks
def masthead(d):
    cx = W / 2
    f_title = serif_bold(84)
    draw_centered(d, 14, TITLE, f_title, INK, cx, tracking=10)
    f_date = serif_bold(30)
    draw_centered(d, 103, DATELINE, f_date, INK, cx, tracking=2)
    d.line([M, 143, W - M, 143], fill=INK, width=3)
    d.line([M, 148, W - M, 148], fill=INK, width=1)
    f_deck = sans(14)
    draw_centered(d, 155, DECK, f_deck, INK, cx)


# Preference ladder: (headline size, subline size, max subline lines).
# Prefer the largest subline type that still fits; headline stays at 2 lines,
# subline may take a third line rather than shrinking two long subs to 10 px.
_CARD_FITS = (
    (22, 12, 2), (22, 11, 3), (20, 12, 2), (20, 11, 3),
    (18, 12, 3), (18, 11, 3), (16, 11, 3),
)


def draw_card(d, x, y, kicker, headline, sub, report):
    pad = 10
    inner = CARD_W - 2 * pad
    limit = CARD_H - 4  # bottom padding

    def block(h_size, s_size, h_lines, s_lines):
        h_lead = h_size * 1.12
        s_lead = s_size * 1.18
        s_top = 22 + len(h_lines) * h_lead + 5
        return s_top + len(s_lines) * s_lead

    chosen = None
    for h_size, s_size, max_s in _CARD_FITS:
        f_h, f_s = serif_bold(h_size), sans(s_size)
        h_lines = wrap(d, headline, f_h, inner)
        s_lines = wrap(d, sub, f_s, inner)
        if len(h_lines) > 2 or len(s_lines) > max_s:
            continue
        if block(h_size, s_size, h_lines, s_lines) <= limit:
            chosen = (h_size, s_size, h_lines, s_lines)
            break
    if chosen is None:
        raise RuntimeError(f"card {kicker!r} does not fit at minimum sizes")
    h_size, s_size, h_lines, s_lines = chosen

    # kicker
    f_k = sans_bold(10)
    draw_tracked(d, x + pad, y + 7, kicker, f_k, RED, tracking=1.5)

    # headline + subline
    h_lead = h_size * 1.12
    s_lead = s_size * 1.18
    s_top = y + 22 + len(h_lines) * h_lead + 5
    for i, ln in enumerate(h_lines):
        d.text((x + pad, y + 22 + i * h_lead), ln, font=serif_bold(h_size), fill=INK)
    for i, ln in enumerate(s_lines):
        d.text((x + pad, s_top + i * s_lead), ln, font=sans(s_size), fill=INK)

    if s_top + len(s_lines) * s_lead > y + limit:
        raise RuntimeError(f"card {kicker!r} overflows after layout")

    report.append((kicker, len(h_lines), h_size, len(s_lines), s_size))


def hero_grid(d, report):
    # frame rules
    d.line([M, HERO_Y0 - 6, W - M, HERO_Y0 - 6], fill=INK, width=1)
    d.line([M, HERO_Y1 + 6, W - M, HERO_Y1 + 6], fill=INK, width=1)
    # vertical hairline between columns
    midx = M + CARD_W + 8
    d.line([midx, HERO_Y0, midx, HERO_Y1], fill=INK, width=1)
    # horizontal hairlines between rows
    for i in range(1, 4):
        gy = HERO_Y0 + i * (CARD_H + CARD_GAP) - CARD_GAP // 2
        d.line([M, gy, W - M, gy], fill=INK, width=1)
    # cards (row-major: 1-2 top row, 3-4 next, ...)
    for idx, (kicker, headline, sub) in enumerate(CARDS):
        col, row = idx % 2, idx // 2
        x = CARD_XS[col]
        y = HERO_Y0 + row * (CARD_H + CARD_GAP)
        draw_card(d, x, y, kicker, headline, sub, report)


def draw_wire(d, report):
    for c in range(WIRE_COLS):
        title, items = WIRE[c]
        x0 = M + c * (WIRE_COL_W + WIRE_GX)
        x1 = x0 + WIRE_COL_W

        # column title + hairline running out to the column edge
        f_t = sans_bold(13)
        draw_tracked(d, x0, WIRE_TITLE_Y, title, f_t, INK, tracking=2)
        tw = text_len(d, title, f_t, tracking=2)
        d.line([x0 + tw + 10, WIRE_TITLE_Y + 9, x1, WIRE_TITLE_Y + 9], fill=INK, width=1)
        d.line([x0, WIRE_TITLE_Y + 14, x1, WIRE_TITLE_Y + 14], fill=RED, width=2)

        # adaptive fit: shrink font/leading/gap until the column fits
        budget = WIRE_Y1 - WIRE_ITEMS_Y0
        chosen = None
        for fsize, lead, gap in ((11, 15, 3), (10.5, 14, 3), (10, 13, 2),
                                 (10, 12, 2), (9.5, 12, 2)):
            f = sans(fsize)
            used, y = 0, WIRE_ITEMS_Y0
            wrapped = []
            for item in items:
                lines = wrap(d, item, f, WIRE_COL_W - 14)
                wrapped.append(lines)
                used += len(lines) * lead + gap
            if used <= budget:
                chosen = (fsize, lead, gap, wrapped)
                break
        if chosen is None:
            raise RuntimeError(f"wire column {title!r} cannot fit its budget")
        fsize, lead, gap, wrapped = chosen

        # justify item spacing so every column ends on the same baseline
        n_items = len(wrapped)
        used = sum(len(l) for l in wrapped) * lead + (n_items - 1) * gap
        extra = (budget - used) / (n_items - 1) if n_items > 1 else 0.0
        item_gap = gap + extra

        y = WIRE_ITEMS_Y0
        for item, lines in zip(items, wrapped):
            for i, ln in enumerate(lines):
                if i == 0:
                    d.ellipse([x0 + 1, y + 1, x0 + 6.5, y + 6.5], fill=RED)
                d.text((x0 + 14, y), ln, font=sans(fsize), fill=INK)
                y += lead
            y += item_gap
        report.append((title, len(items), sum(len(l) for l in wrapped),
                       fsize, y - item_gap))


def footer(d):
    d.line([M, FOOTER_RULE_Y, W - M, FOOTER_RULE_Y], fill=INK, width=1)
    f = sans(10)
    lead = 13
    y = FOOTER_TEXT_Y
    for para in FOOTER:
        for ln in wrap(d, para, f, CW - 40):
            draw_centered(d, y, ln, f, INK, W / 2)
            y += lead
        y += 3
    if y > H - 6:
        raise RuntimeError(f"footer overflows: bottom {y} > {H - 6}")
    return y


# --------------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    card_report = []
    wire_report = []

    masthead(d)
    hero_grid(d, card_report)
    draw_wire(d, wire_report)
    footer_end = footer(d)

    img.save(OUT, "PNG", optimize=True)
    n = OUT.stat().st_size

    print(f"masthead: title 84px, dateline 30px, deck 14px")
    for kicker, hlines, hsize, slines, ssize in card_report:
        print(f"card {kicker:<12} headline {hlines} line(s) @{hsize}px | "
              f"sub {slines} line(s) @{ssize}px")
    for title, nitems, nlines, fsize, end_y in wire_report:
        print(f"wire {title:<14} {nitems} items, {nlines} lines @{fsize}px, "
              f"ends y={end_y:.0f}")
    print(f"footer ends at y={footer_end:.0f}")
    print(f"wrote {OUT} ({n} bytes, {W}x{H})")
    assert n <= MAX_BYTES, f"entry.png too large: {n} bytes"
    print("self-check: OK (size <= 1 MiB, 1024x1024, no overflow)")


if __name__ == "__main__":
    main()
