#!/usr/bin/env python3
"""THE WHOLE DAY DAILY — NI23 G4 compose (akun3, @cicihandayani).

1024x1024 newspaper front page, Monday 23 November 2026.
Variants A / B for the in-session duel; winner -> entry.png (quantized).
Local-only (PIL ok here, never in main.py). Palette: white paper,
dark-brown ink, gold accent. Fonts: PlayfairDisplay-Black masthead.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = 1024
PAPER = (255, 255, 255)
INK = (46, 27, 14)
INK2 = (84, 56, 32)
GOLD = (176, 132, 26)
GOLD_D = (146, 106, 16)
FAINT = (243, 236, 222)
LINE = (198, 178, 148)
RED = (168, 32, 24)
REG_COL = {"EUROPE": (146, 106, 16), "MIDDLE EAST": (168, 84, 24),
           "NORTH AMERICA": (84, 56, 32), "SOUTH ASIA": (120, 84, 140),
           "SOUTHEAST ASIA": (36, 110, 96), "AFRICA": (168, 32, 24),
           "GLOBAL": (70, 90, 140)}


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def pf(s):
    return F("PlayfairDisplay-Black.ttf", s)


def pfb(s):
    return F("PlayfairDisplay-Bold.ttf", s)


def ar(s):
    return F("Archivo.ttf", s)


def arb(s):
    return F("Archivo-Bold.ttf", s)


fb = pfb   # headline font factory (fleet naming)
fr = ar    # deck font factory
fsr = ar   # brief font factory


def tw(d, s, fnt):
    return d.textlength(s, font=fnt)


def wrap(d, s, fnt, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def trunc(d, s, fnt, maxw):
    if tw(d, s, fnt) <= maxw:
        return s
    while s and tw(d, s + "...", fnt) > maxw:
        s = s[:-1]
    return s.rstrip() + "..."


def icon(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    cx, cy = x + w // 2, y + h // 2
    if kind == "rubble":
        d.polygon([(x + 8, y + h - 3), (x + 30, y + 5), (x + 52, y + h - 3)], fill=INK2)
        d.polygon([(x + 40, y + h - 3), (x + 62, y + 10), (x + 84, y + h - 3)], fill=GOLD_D)
        d.line([x + 68, y + 3, x + 68, y + 13], fill=RED, width=3)
        d.line([x + 63, y + 8, x + 73, y + 8], fill=RED, width=3)
    elif kind == "radar":
        d.arc([x + 14, y + 1, x + 58, y + 30], 200, 340, fill=INK, width=3)
        d.line([x + 36, y + 15, x + 36, y + h - 2], fill=INK, width=3)
        d.arc([x + 46, y + 2, x + 70, y + 20], 200, 330, fill=GOLD_D, width=2)
    elif kind == "globe":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=INK, width=3)
        d.line([cx - 13, cy, cx + 13, cy], fill=GOLD_D, width=2)
        d.line([cx, cy - 13, cx, cy + 13], fill=GOLD_D, width=2)
        d.polygon([(cx + 10, cy - 17), (cx + 21, cy - 6), (cx + 8, cy - 4)], fill=(36, 110, 96))
    elif kind == "ship":
        d.polygon([(x + 10, cy + 5), (x + w - 10, cy + 5), (x + w - 22, cy + 14), (x + 22, cy + 14)], fill=INK)
        d.rectangle([cx - 16, cy - 7, cx + 10, cy + 5], fill=INK2)
        d.polygon([(cx + 2, cy - 19), (cx + 9, cy - 7), (cx - 4, cy - 7)], fill=(216, 110, 30))
        d.polygon([(cx - 2, cy - 14), (cx + 4, cy - 7), (cx - 7, cy - 7)], fill=GOLD)
    elif kind == "scales":
        d.line([cx, y + 3, cx, y + h - 5], fill=INK, width=3)
        d.line([cx - 18, y + 6, cx + 18, y + 6], fill=INK, width=3)
        d.polygon([(cx - 18, y + 6), (cx - 25, y + 17), (cx - 11, y + 17)], outline=GOLD_D, width=2)
        d.polygon([(cx + 18, y + 6), (cx + 11, y + 17), (cx + 25, y + 17)], outline=GOLD_D, width=2)
    elif kind == "bat":
        d.rectangle([x + 12, y + h - 7, x + w - 12, y + h - 3], fill=(36, 110, 96))
        d.polygon([(cx - 4, y + 3), (cx + 3, y + 3), (cx + 10, y + h - 8), (cx + 2, y + h - 8)], fill=INK2)
        d.ellipse([cx + 12, y + 5, cx + 22, y + 15], fill=(216, 60, 40))
    elif kind == "gold":
        d.polygon([(x + 16, y + h - 7), (x + 40, y + h - 7), (x + 34, y + h - 16), (x + 22, y + h - 16)], fill=GOLD)
        d.polygon([(x + 44, y + h - 7), (x + 68, y + h - 7), (x + 62, y + h - 16), (x + 50, y + h - 16)], fill=GOLD_D)
        d.line([x + 14, y + 8, x + 44, y + 17, x + 74, y + 5], fill=RED, width=3)
    elif kind == "burst":
        for ang in range(0, 360, 45):
            x1 = cx + 5 * math.cos(math.radians(ang)); y1 = cy + 5 * math.sin(math.radians(ang))
            x2 = cx + 15 * math.cos(math.radians(ang)); y2 = cy + 15 * math.sin(math.radians(ang))
            d.line([x1, y1, x2, y2], fill=(216, 110, 30), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    elif kind == "capitol":
        d.polygon([(cx - 24, y + 8), (cx, y + 1), (cx + 24, y + 8)], fill=INK)
        for i in range(5):
            xx = cx - 20 + i * 10
            d.rectangle([xx, y + 9, xx + 4, y + h - 5], fill=INK2)
        d.rectangle([cx - 26, y + h - 5, cx + 26, y + h - 2], fill=GOLD_D)
    elif kind == "drone":
        d.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=INK)
        for dx, dy in ((-14, -7), (14, -7), (-14, 7), (14, 7)):
            d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=2)
            d.ellipse([cx + dx - 4, cy + dy - 2, cx + dx + 4, cy + dy + 2], outline=GOLD_D, width=2)
    elif kind == "building":
        d.rectangle([x + 18, y + 2, x + 42, y + h - 2], fill=INK2)
        d.rectangle([x + 48, y + max(3, h - 8), x + 70, y + h - 2], fill=INK)
        for r in range(2):
            for c in range(2):
                d.rectangle([x + 23 + c * 9, y + 4 + r * 5, x + 27 + c * 9, y + 6 + r * 5], fill=GOLD)
    else:
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=INK, width=3)


# ------------------------------------------------------------ card data
# lead card (no. 1) and mini lead cards (nos. 2-3) are drawn via lead()/mini()
# calls in the variant functions; grid cards use this fleet-style table:
# (num, region, topic, src, head, deck, kind)
grid = [
    (4, "MIDDLE EAST", "MIDDLE EAST · WAR", "AP live, 23 Nov", "Tankers Set Ablaze",
     "Tankers were set ablaze in the Strait of Hormuz as the Iran-US war widened across the Gulf; the IRGC warned of unrest.", "ship"),
    (5, "EUROPE", "EUROPE · WAR", "JagranJosh, 23 Nov", "14 Missing in Kyiv",
     "14 people are missing after Russian drones hit a residential building in the Kyiv region, President Zelenskiy said.", "building"),
    (6, "NORTH AMERICA", "NORTH AMERICA · POLITICS", "BBC, 23 Nov", "Democrats' House: 258-173",
     "The majority was confirmed at 258 seats to 173 after Democrats won a North Carolina seat; the largest House majority since 1992.", "capitol"),
    (7, "EUROPE", "EUROPE · SEA", "BBC, 23 Nov", "Russian Ship Still Burns",
     "The Russian cargo vessel was still burning off Finland after an attack in the Gulf of Finland; it was towed, not sunk.", "ship"),
    (8, "SOUTHEAST ASIA", "WORLD COURT · MYANMAR", "Guardian / NYT, 23 Nov", "ICJ: Myanmar Guilty",
     "The International Court of Justice found Myanmar guilty of genocide over the 2017 Rohingya campaign, which drove out 700,000 people.", "scales"),
    (9, "SOUTH ASIA", "SOUTH ASIA · CRICKET", "ObserverVoice, 23 Nov", "India Declare on 720/9",
     "India declared at 720 for 9 at Wellington, the highest Test total ever made in New Zealand, passing the old mark.", "bat"),
    (10, "GLOBAL", "GLOBAL · MARKETS", "ObserverVoice, 23 Nov", "Gold Slides to $3,538",
     "Gold fell to $3,538 an ounce, down more than $2,000 from its 2026 record of $5,595 after a 2.41% slide on Friday.", "gold"),
    (11, "AFRICA", "AFRICA · SEA", "BBC, 23 Nov", "Benghazi Blast Probed",
     "An explosion hit a Russian ship in Benghazi port, Libya; a drone strike is suspected but has not been confirmed.", "drone"),
    (12, "NORTH AMERICA", "NORTH AMERICA · SAFETY", "BBC, 23 Nov", "Iowa Blast Planned",
     "The US Army will detonate tonnes of unstable explosives stored in Iowa, pressing ahead despite a court order against it.", "burst"),
]
GRID_META = {  # num -> (location, certainty chip)
    4: ("STRAIT OF HORMUZ", "ONGOING"), 5: ("KYIV REGION", "ON RECORD"),
    6: ("WASHINGTON, US", "OFFICIAL"), 7: ("GULF OF FINLAND", "ONGOING"),
    8: ("THE HAGUE", "OFFICIAL"), 9: ("WELLINGTON, NZ", "REPORTED"),
    10: ("WORLD MARKETS", "REPORTED"), 11: ("BENGHAZI, LIBYA", "CLAIM"),
    12: ("IOWA, US", "OFFICIAL"),
}

BRIEFS = [
    "Houthi missile at Saudi Arabia intercepted",
    "Swimmer crosses Hormuz for Iran's wildlife",
    "UN to keep talks on lethal AI weapons",
    "US declassifies more UFO footage",
    "Russia-bound ship towed after attack",
    "UK-EU reset deal: Burnham hails 'landmark'",
    "Thousands march in Lisbon over living costs",
    "Myanmar junta calls ASEAN ruling 'unfair'",
    "Cameroon ex-rebels trapped, promises broken",
    "Escaped lion spreads fear in Turkiye",
    "Nepal PM Shah holds talks with Modi in Delhi",
    "Guru Nanak Jayanti: 'Sewa, Simran aur Sangat'",
    "UP air-raid and blackout drills, 75 districts",
    "Indonesia fire, 23 Nov: 7 found, 50 lost",
    "Wellington day 5: India chase win, NZ 119/2",
    "India win ODI series in NZ 3-2; Phillips stars",
    "Anupama keeps world snooker title",
    "Rajya Sabha MP Wadkute dies in Delhi",
    "Kota pilgrim bus tragedy: 9 killed",
    "Tata Steel pipe sale: Rs 28,000 crore",
    "SpiceJet audit call; IndiGo at 65.9% share",
    "Modi opens AI Centre at IIT Patna",
    "JEE Main 2027 registration closes today",
    "Trump attacks Schumer over leadership",
    "FBI probes hack of its Justice Department database",
    "Miley Cyrus marries Maxx Morando",
    "Alcaraz beats Zverev, first ATP Finals title",
    "Mets sign A.J. Ewing: $95m over 8 years",
]

NUMS = [
    ("258-173", "Democrats' House majority, confirmed (card 6)"),
    ("720/9d", "India's record Test total, Wellington (card 9)"),
    ("$3,538", "gold per ounce after the slide (card 10)"),
    ("6", "killed in the Kyiv strike (card 1)"),
    ("14", "missing in Kyiv region, Zelenskiy says (card 5)"),
    ("Rs 28,000 cr", "Tata Steel pipe sale to APL Apollo (no. 32)"),
]

dc = ("Xi-Trump-Putin trilateral summit - 19 Nov 2026 · "
      "Russian missiles fell in Poland - 20 Nov 2026 · "
      "Paolo Bulgari death reported - 22 Nov 2026 · "
      "24 civilians killed in South Sudan - 22 Nov 2026 · "
      "Bolsonaro 'stable' in ICU, Brasilia - 22 Nov 2026 · "
      "S. Korea education minister quit - 22 Nov 2026 · "
      "Indonesia candy-factory fire ITSELF - 22 Nov 2026 (only its 23 Nov update is news)")
DATECHECK = dc.split(" · ")

REGIONS = [("EUROPE", 9), ("MIDDLE EAST", 4), ("N. AMERICA", 7), ("SOUTH ASIA", 13),
           ("S.E. ASIA", 3), ("AFRICA", 2), ("GLOBAL", 2)]
TL = [("00:02 UTC", "UN AI talks go on"), ("MORNING", "COP31 closes, no deal"),
      ("MIDDAY", "Kyiv boy alive"), ("AFTERNOON", "ICJ on Myanmar"),
      ("EVENING", "House 258-173 set")]

MAPGRID = [
    "                                                                ",
    "        oooo        oooooooooo ooo  oooooooooooooooooooo        ",
    "      ooooooooo    ooooooooooooooooooooooooooooooooooooooo      ",
    "       ooooooo      oooooo  ooooooooooooooooooooooooooooo       ",
    "        ooooo        oooo    ooooo oooooooooooooooooooo         ",
    "         ooo          oo      ooo   ooooooooooooooooo           ",
    "          o            o       oo     ooooooooooooo             ",
    "          oo                       oooo ooooooooo               ",
    "           ooo                    ooooooo  ooooo                  ",
    "            oooo                 ooooooooo  ooo                   ",
    "             ooooo              ooooooooo                         ",
    "              oooooo             ooooooo          oo              ",
    "               ooooo              ooooo          oooo             ",
    "                ooo                ooo          oooooo            ",
    "                oo                                  oo            ",
    "                                                                ",
]
PINS = {1: (30, 2), 2: (34, 5), 3: (31, 4), 4: (35, 5), 5: (32, 1), 6: (9, 3),
        7: (29, 1), 8: (44, 7), 9: (58, 13), 10: (46, 4), 11: (30, 6), 12: (8, 4)}
MAP_CAPTION = "Dotted map: numbered marks = card locations; dots are land."


# ------------------------------------------------------------ drawing
def header(d):
    d.rectangle([0, 0, W, 24], fill=INK)
    d.text((14, 5), "THE WHOLE DAY DAILY", font=arb(14), fill=(255, 244, 214))
    k = "40 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    d.text((W - 14 - tw(d, k, arb(13)), 5), k, font=arb(13), fill=(255, 244, 214))
    s = "Monday 23 November 2026"
    fd = pf(72)
    while tw(d, s, fd) > W - 40:
        fd = pf(fd.size - 2)
    d.text(((W - tw(d, s, fd)) / 2, 24), s, font=fd, fill=INK)
    nm = "THE WHOLE DAY DAILY"
    fnm = pfb(30)
    d.text(((W - tw(d, nm, fnm)) / 2, 102), nm, font=fnm, fill=GOLD_D)
    sub = "Boy, 7, pulled alive from Kyiv rubble, six killed  ·  IRGC claims Patriot radars hit in Bahrain  ·  COP31 ends without a deal"
    fs = arb(14)
    while tw(d, sub, fs) > W - 28:
        fs = arb(fs.size - 1)
    d.text(((W - tw(d, sub, fs)) / 2, 136), sub, font=fs, fill=INK2)
    d.line([14, 156, W - 14, 156], fill=GOLD, width=3)
    x, y = 14, 160
    d.text((x, y + 2), "REGIONS:", font=arb(13), fill=INK)
    x += tw(d, "REGIONS:", arb(13)) + 10
    for name, n in REGIONS:
        key = {"N. AMERICA": "NORTH AMERICA", "S.E. ASIA": "SOUTHEAST ASIA"}.get(name, name)
        label = "%s %d" % (name, n)
        wch = tw(d, label, arb(12)) + 14
        d.rectangle([x, y, x + wch, y + 18], fill=REG_COL[key])
        d.text((x + 7, y + 3), label, font=arb(12), fill=(255, 255, 255))
        x += wch + 6
    y = 182
    d.rectangle([14, y, W - 14, y + 19], fill=FAINT)
    x = 20
    d.text((x, y + 3), "THE DAY (UTC):", font=arb(12), fill=INK)
    x += tw(d, "THE DAY (UTC):", arb(12)) + 8
    for t, ev in TL:
        ss = "%s %s" % (t, ev)
        d.text((x, y + 3), ss, font=ar(12), fill=INK2)
        x += tw(d, ss, ar(12)) + 13
    return 206


def _card(img, d, x, y, w, h, num, loc, region, chip, cat, head, deck, src,
          kind, tf, ff, ih, leading, maxlines):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    d.rectangle([x, y, x + 28, y + 19], fill=INK)
    ns = str(num)
    d.text((x + (28 - tw(d, ns, arb(13))) / 2, y + 3), ns, font=arb(13), fill=(255, 244, 214))
    d.text((x + 33, y + 4), loc, font=arb(12), fill=INK)
    chw = tw(d, chip, arb(11)) + 12
    d.rectangle([x + w - chw - 3, y + 2, x + w - 3, y + 17], fill=GOLD)
    d.text((x + w - chw + 3, y + 4), chip, font=arb(11), fill=(255, 255, 255))
    tile = Image.new("RGB", (w - 8, 30), (255, 255, 255))
    icon(ImageDraw.Draw(tile), kind, 0, 0, w - 8, 30)
    img.paste(tile.resize((w - 8, ih)), (x + 4, y + 21))
    yy = y + 23 + ih
    d.text((x + 5, yy), cat, font=arb(10), fill=REG_COL[region])
    srct = "Source: " + src
    d.text((x + w - 5 - tw(d, srct, ar(10)), yy + 1), srct, font=ar(10), fill=GOLD_D)
    yy += 13
    for ln in wrap(d, head, tf, w - 10)[:maxlines]:
        d.text((x + 5, yy), ln, font=tf, fill=INK)
        yy += leading
    for ln in wrap(d, deck, ff, w - 10)[:1]:
        d.text((x + 5, yy), ln, font=ff, fill=INK2)
        yy += 19


def lead(img, d, x, y, w, h, num, src, head, deck, kind, loc, region, chip, cat):
    tf = fb(32)
    ff = fr(15)
    _card(img, d, x, y, w, h, num, loc, region, chip, cat, head, deck, src,
          kind, tf, ff, 26, 36, 2)


def mini(img, d, x, y, w, h, num, src, head, deck, kind, loc, region, chip, cat):
    tf = fb(28)
    ff = fr(15)
    _card(img, d, x, y, w, h, num, loc, region, chip, cat, head, deck, src,
          kind, tf, ff, 22, 30, 2)


def grid_card(img, d, x, y, w, h, t):
    num, region, topic, src, head, deck, kind = t
    loc, chip = GRID_META[num]
    _card(img, d, x, y, w, h, num, loc, region, chip, topic, head, deck, src,
          kind, fb(28), fr(15), 12, 30, 1)


def numbers_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=GOLD_D, width=2)
    d.rectangle([x, y, x + w, y + 20], fill=GOLD_D)
    d.text((x + 8, y + 4), "THE DAY IN NUMBERS", font=arb(12), fill=(255, 255, 255))
    cw = (w - 16) / 3
    rh = (h - 24) / 2
    for i, (val, lab) in enumerate(NUMS):
        cx = x + 8 + (i % 3) * cw
        cy = y + 23 + (i // 3) * rh
        d.text((cx, cy), val, font=pfb(26), fill=INK)
        d.text((cx, cy + 29), trunc(d, lab, ar(10), cw - 6), font=ar(10), fill=INK2)


def dotted_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    d.text((x + 8, y + 3), "WHERE IT HAPPENED - pins = card numbers", font=arb(11), fill=INK)
    d.text((x + 8, y + 16), MAP_CAPTION, font=ar(8), fill=INK2)
    rows, cols = len(MAPGRID), max(len(r) for r in MAPGRID)
    gx, gy = x + 8, y + 28
    gw, gh = w - 16, h - 46
    sx, sy = gw / cols, gh / rows
    for r, row in enumerate(MAPGRID):
        for ci, ch in enumerate(row):
            if ch == "o":
                px, py = gx + ci * sx, gy + r * sy
                d.ellipse([px, py, px + 2.2, py + 2.2], fill=(198, 178, 148))
    for num, (ci, r) in PINS.items():
        px, py = gx + ci * sx, gy + r * sy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED)
        ns = str(num)
        d.text((px - tw(d, ns, arb(8)) / 2, py - 4), ns, font=arb(8), fill=(255, 255, 255))
    ly = y + h - 16
    lx = x + 8
    for name, _n in REGIONS:
        key = {"N. AMERICA": "NORTH AMERICA", "S.E. ASIA": "SOUTHEAST ASIA"}.get(name, name)
        d.rectangle([lx, ly + 2, lx + 7, ly + 9], fill=REG_COL[key])
        d.text((lx + 10, ly), name, font=ar(8), fill=INK2)
        lx += 10 + tw(d, name, ar(8)) + 7


def also_on(d, x, y, w, cols=4):
    d.text((x, y), "ALSO ON MONDAY - THE REST OF THE DAY, NUMBERED", font=arb(13), fill=INK)
    cw = w / cols
    per = (len(BRIEFS) + cols - 1) // cols
    for ci in range(cols):
        cy = y + 17
        for j, txt in enumerate(BRIEFS[ci * per:(ci + 1) * per]):
            s = "%d. %s" % (13 + ci * per + j, txt)
            d.text((x + ci * cw, cy), trunc(d, s, fsr(11), cw - 8), font=fsr(11), fill=INK2)
            cy += 12


def datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.rectangle([x, y, x + w, y + 19], fill=RED)
    d.text((x + 8, y + 4), "DATE CHECK - NOT 23 NOVEMBER, SO NOT NEWS HERE", font=arb(11), fill=(255, 255, 255))
    cw = w / 2
    per = (len(DATECHECK) + 1) // 2
    for ci in range(2):
        cy = y + 24
        for s in DATECHECK[ci * per:(ci + 1) * per]:
            for ln in wrap(d, "x " + s, ar(10), cw - 14)[:2]:
                d.text((x + 6 + ci * cw, cy), ln, font=ar(10), fill=INK)
                cy += 11
            cy += 3


def footer(d):
    y = 978
    d.line([14, y, W - 14, y], fill=GOLD, width=2)
    s1 = "HOW SURE: REPORTED = reported by the cited source · CLAIM = one side's account, labelled as such · ONGOING = still developing · OFFICIAL / ON RECORD = stated by officials or named leaders."
    for i, ln in enumerate(wrap(d, s1, ar(11), W - 28)[:2]):
        d.text((14, y + 5 + i * 13), ln, font=ar(11), fill=INK2)
    s2 = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed.  ·  Original drawings."
    d.text((14, y + 32), s2, font=arb(11), fill=INK)


LEAD_ARGS = ("BBC, 23 Nov", "Boy, 7, Pulled Alive From Kyiv Rubble",
             "Rescuers freed the boy, 7, after hours under a collapsed block in Kyiv; 6 people were killed by the Russian strike.",
             "rubble", "KYIV, UKRAINE", "EUROPE", "REPORTED", "EUROPE · WAR")
MINI2_ARGS = ("AP / AFP wire, 23 Nov", "IRGC Claims Two Patriot Radars Hit",
              "Iran's Revolutionary Guards say they destroyed 2 Patriot radars at a US base in Bahrain; Washington has not confirmed the claim.",
              "radar", "BAHRAIN", "MIDDLE EAST", "CLAIM", "MIDDLE EAST · WAR")
MINI3_ARGS = ("BBC / AP, 23 Nov", "COP31 Ends Without a Deal",
              "The Antalya summit closed without agreement; Turkiye's final draft never mentions fossil fuels, and delegates left COP31 deadlocked.",
              "globe", "ANTALYA, TURKIYE", "EUROPE", "OFFICIAL", "EUROPE · CLIMATE")


def variant_a():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    top = header(d)  # 206
    # A: trio lead side by side, lead card widest
    lead(img, d, 14, top, 400, 156, "1", "BBC, 23 Nov", "Boy, 7, Pulled Alive From Kyiv Rubble", "Rescuers freed the boy, 7, after hours under a collapsed block in Kyiv; 6 people were killed by the Russian strike.", "rubble", "KYIV, UKRAINE", "EUROPE", "REPORTED", "EUROPE \u00b7 WAR")
    mini(img, d, 420, top, 298, 156, "2", "AP / AFP wire, 23 Nov", "IRGC Claims Two Patriot Radars Hit", "Iran's Revolutionary Guards say they destroyed 2 Patriot radars at a US base in Bahrain; Washington has not confirmed the claim.", "radar", "BAHRAIN", "MIDDLE EAST", "CLAIM", "MIDDLE EAST \u00b7 WAR")
    mini(img, d, 724, top, 286, 156, "3", "BBC / AP, 23 Nov", "COP31 Ends Without a Deal", "The Antalya summit closed without agreement; Turkiye's final draft never mentions fossil fuels, and delegates left COP31 deadlocked.", "globe", "ANTALYA, TURKIYE", "EUROPE", "OFFICIAL", "EUROPE \u00b7 CLIMATE")
    numbers_box(d, 14, top + 162, 996, 106)
    gy = top + 274
    cw, chh = 328, 90
    for i, t in enumerate(grid):
        grid_card(img, d, 14 + (i % 3) * (cw + 6), gy + (i // 3) * (chh + 10), cw, chh, t)
    by = gy + 3 * chh + 24
    dotted_map(d, 14, by, 400, 94)
    datecheck(d, 422, by, 588, 94)
    also_on(d, 14, by + 100, 996, cols=4)
    footer(d)
    return img


if __name__ == "__main__":
    img = variant_a()
    img.save(sys.argv[2], optimize=True)
    print(sys.argv[2], img.size)
