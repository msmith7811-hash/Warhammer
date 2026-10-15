#!/usr/bin/env python3
"""
Generate a printable HTML character sheet for Warhammer Fantasy Roleplay 4th Edition.

Usage:
    python wfrp_character_sheet.py                      # builds the sample character
    python wfrp_character_sheet.py -i hero.json         # builds from your own JSON
    python wfrp_character_sheet.py -i hero.json -o hero.html
    python wfrp_character_sheet.py --dump-template > hero.json   # starter JSON to edit

Derived values calculated for you:
  * Characteristic = initial + advances; Bonus = tens digit (+ optional "bonus_mod",
    e.g. 1 for the Very Strong talent).
  * Skill total = linked characteristic + skill advances.
  * Max Wounds = SB + 2xTB + WPB (Halflings: 2xTB + WPB). Override with "wounds_max".
  * Corruption threshold = TB + WPB. Encumbrance limit = SB + TB.
  * Armour Points per hit location, summed from your armour items.
  * Melee weapon damage = SB + modifier when "adds_sb" is true.

Anything you set explicitly in the data overrides the calculation.
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path

# Characteristic key -> (abbreviation, full name)
CHARACTERISTICS = [
    ("WS", "Weapon Skill"),
    ("BS", "Ballistic Skill"),
    ("S", "Strength"),
    ("T", "Toughness"),
    ("I", "Initiative"),
    ("Ag", "Agility"),
    ("Dex", "Dexterity"),
    ("Int", "Intelligence"),
    ("WP", "Willpower"),
    ("Fel", "Fellowship"),
]
CHAR_KEYS = [k for k, _ in CHARACTERISTICS]

BASIC_SKILLS = {
    "Art": "Dex",
    "Athletics": "Ag",
    "Bribery": "Fel",
    "Charm": "Fel",
    "Charm Animal": "WP",
    "Climb": "S",
    "Cool": "WP",
    "Consume Alcohol": "T",
    "Dodge": "Ag",
    "Drive": "Ag",
    "Endurance": "T",
    "Entertain": "Fel",
    "Gamble": "Int",
    "Gossip": "Fel",
    "Haggle": "Fel",
    "Intimidate": "S",
    "Intuition": "I",
    "Leadership": "Fel",
    "Melee (Basic)": "WS",
    "Melee (Other)": "WS",
    "Navigation": "I",
    "Outdoor Survival": "Int",
    "Perception": "I",
    "Ride": "Ag",
    "Row": "S",
    "Stealth": "Ag",
}

# (label, d100 range, key used on armour items)
HIT_LOCATIONS = [
    ("Head", "01\u201309"),
    ("Left arm", "10\u201324"),
    ("Right arm", "25\u201344"),
    ("Body", "45\u201379"),
    ("Left leg", "80\u201389"),
    ("Right leg", "90\u201300"),
]
LOCATION_ALIASES = {
    "head": ["Head"],
    "body": ["Body"],
    "arms": ["Left arm", "Right arm"],
    "left arm": ["Left arm"],
    "right arm": ["Right arm"],
    "legs": ["Left leg", "Right leg"],
    "left leg": ["Left leg"],
    "right leg": ["Right leg"],
}

SAMPLE_CHARACTER = {
    "name": "Hilde Brandt",
    "species": "Human (Reiklander)",
    "career": "Soldier",
    "career_level": "Recruit",
    "career_class": "Warrior",
    "status": "Brass 3",
    "player": "Sam",
    "age": "27",
    "height": "5'7\"",
    "hair": "Dark brown, cropped",
    "eyes": "Grey",
    "distinguishing_marks": "Brand from a deserter's flogging; missing two fingertips on her left hand.",
    "characteristics": {
        "WS": {"initial": 38, "advances": 5},
        "BS": {"initial": 35, "advances": 0},
        "S": {"initial": 38, "advances": 5},
        "T": {"initial": 36, "advances": 5},
        "I": {"initial": 31, "advances": 0},
        "Ag": {"initial": 34, "advances": 0},
        "Dex": {"initial": 29, "advances": 0},
        "Int": {"initial": 30, "advances": 0},
        "WP": {"initial": 32, "advances": 0},
        "Fel": {"initial": 28, "advances": 0},
    },
    "movement": 4,
    "fate": 2,
    "fortune": 2,
    "resilience": 3,
    "resolve": 2,
    "motivation": "Duty. A debt is a debt, even to a regiment that no longer exists.",
    "wounds_current": 15,
    "experience": {"current": 20, "spent": 180, "total": 200},
    "corruption": {"current": 0},
    "basic_skill_advances": {
        "Athletics": 5,
        "Cool": 5,
        "Dodge": 5,
        "Endurance": 5,
        "Melee (Basic)": 10,
        "Perception": 3,
        "Gamble": 3,
        "Consume Alcohol": 3,
        "Intimidate": 3,
    },
    "advanced_skills": [
        {"name": "Language (Battle Tongue)", "characteristic": "Int", "advances": 3},
        {"name": "Ranged (Crossbow)", "characteristic": "BS", "advances": 5},
        {"name": "Melee (Polearm)", "characteristic": "WS", "advances": 3},
    ],
    "talents": [
        {"name": "Strike Mighty Blow", "ranks": 1, "text": "+1 Damage on all successful melee hits."},
        {"name": "Warrior Born", "ranks": 1, "text": "+5 Weapon Skill (included in the initial value above)."},
        {"name": "Stout-hearted", "ranks": 1, "text": "Re-roll failed Cool tests once per encounter when under pressure."},
    ],
    "bonus_mods": {},
    "weapons": [
        {"name": "Hand Weapon (sword)", "group": "Basic", "enc": 1, "reach_range": "Average",
         "adds_sb": True, "damage_mod": 4, "qualities": "\u2013"},
        {"name": "Spear", "group": "Polearm", "enc": 1, "reach_range": "Long",
         "adds_sb": True, "damage_mod": 4, "qualities": "Hack, Impale"},
        {"name": "Crossbow", "group": "Crossbow", "enc": 3, "reach_range": "60 yds",
         "adds_sb": False, "damage_mod": 9, "qualities": "Precise, Reload 1"},
    ],
    "armour": [
        {"name": "Leather Jack", "locations": ["Body", "Arms"], "ap": 1, "enc": 1, "qualities": "Flexible"},
        {"name": "Leather Skullcap", "locations": ["Head"], "ap": 1, "enc": 0, "qualities": "Partial"},
        {"name": "Leather Leggings", "locations": ["Legs"], "ap": 1, "enc": 1, "qualities": "Flexible"},
    ],
    "spells": [],
    "magic_lore": "",
    "trappings": [
        {"name": "Backpack", "enc": 0, "note": "Worn"},
        {"name": "Bedroll", "enc": 1, "note": ""},
        {"name": "Rations (1 day)", "enc": 0, "note": ""},
        {"name": "Tinderbox", "enc": 0, "note": ""},
        {"name": "Regimental badge (Reikland)", "enc": 0, "note": "Wears it face-down"},
    ],
    "money": {"gc": 0, "s": 14, "d": 23},
    "psychology": ["Animosity (Deserter-hunters)"],
    "mutations": [],
    "ambitions": {
        "short": "Find work with a caravan heading north, away from Altdorf.",
        "long": "Learn who sold out the Third Company at the Reikwald crossing.",
    },
    "party": {
        "name": "The Lantern Road",
        "short": "Reach Ubersreik before the thaw.",
        "long": "Establish a trading charter.",
        "members": "Otto (Rat Catcher), Marta (Initiate), Jaro (Boatman)",
    },
    "notes": "",
}


# --------------------------------------------------------------------------
# Rules helpers
# --------------------------------------------------------------------------

def esc(value) -> str:
    return escape(str(value if value is not None else ""))


def signed(n: int) -> str:
    return f"+{n}" if n >= 0 else f"\u2212{abs(n)}"


def expand_locations(locs) -> list[str]:
    out: list[str] = []
    for loc in locs:
        out.extend(LOCATION_ALIASES.get(str(loc).strip().lower(), []))
    return out


def compute(c: dict) -> dict:
    raw = c.get("characteristics", {})
    mods = c.get("bonus_mods", {})
    chars = {}
    for key in CHAR_KEYS:
        v = raw.get(key, 0)
        if isinstance(v, dict):
            initial, adv = int(v.get("initial", 0)), int(v.get("advances", 0))
            bonus_mod = int(v.get("bonus_mod", 0))
        else:
            initial, adv, bonus_mod = int(v), 0, 0
        bonus_mod += int(mods.get(key, 0))
        current = initial + adv
        chars[key] = {
            "initial": initial, "advances": adv, "current": current,
            "bonus": current // 10 + bonus_mod,
        }

    sb, tb, wpb = chars["S"]["bonus"], chars["T"]["bonus"], chars["WP"]["bonus"]
    species = str(c.get("species", "")).lower()
    if "halfling" in species:
        wounds = 2 * tb + wpb
    else:
        wounds = sb + 2 * tb + wpb
    wounds = int(c.get("wounds_max", wounds))

    # Skills
    basic = {}
    for name, ch in BASIC_SKILLS.items():
        adv = int(c.get("basic_skill_advances", {}).get(name, 0))
        basic[name] = {"char": ch, "adv": adv, "total": chars[ch]["current"] + adv}
    advanced = []
    for s in c.get("advanced_skills", []):
        ch = s.get("characteristic", "Int")
        adv = int(s.get("advances", 0))
        advanced.append({
            "name": s.get("name", ""), "char": ch, "adv": adv,
            "total": chars.get(ch, {"current": 0})["current"] + adv,
        })

    # Armour points by location
    ap = {label: 0 for label, _ in HIT_LOCATIONS}
    for item in c.get("armour", []):
        for loc in expand_locations(item.get("locations", [])):
            ap[loc] += int(item.get("ap", 0))

    # Encumbrance
    enc = sum(int(i.get("enc", 0)) for i in c.get("weapons", []))
    enc += sum(int(i.get("enc", 0)) for i in c.get("armour", []))
    enc += sum(int(i.get("enc", 0)) for i in c.get("trappings", []))
    enc_limit = int(c.get("encumbrance_limit", sb + tb))

    return {
        "chars": chars, "sb": sb, "tb": tb, "wpb": wpb, "wounds": wounds,
        "basic": basic, "advanced": advanced, "ap": ap,
        "enc": enc, "enc_limit": enc_limit,
        "corruption_max": int(c.get("corruption", {}).get("max", tb + wpb)),
    }


# --------------------------------------------------------------------------
# HTML rendering
# --------------------------------------------------------------------------

CSS = """
:root {
  --paper: #dedcd8;
  --sheet: #f6f5f2;
  --ink: #1e1b1b;
  --muted: #5e5a5a;
  --line: #b3aeaa;
  --accent: #6e1a26;
  --accent-soft: #ead8d9;
  --iron: #3f444c;
}
* { box-sizing: border-box; }
html { background: var(--paper); }
body {
  margin: 0; padding: 24px 16px 48px; color: var(--ink);
  font: 15px/1.5 "Source Serif 4", "Source Serif Pro", Georgia, serif;
}
h1, h2, h3, .display { font-family: "IM Fell English", "Palatino Linotype", Palatino, Georgia, serif; font-weight: 400; }
.sheet {
  max-width: 1120px; margin: 0 auto; background: var(--sheet);
  border: 2px solid var(--iron); outline: 1px solid var(--iron); outline-offset: 4px;
  padding: 28px;
}
header.top {
  display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end;
  padding-bottom: 16px; border-bottom: 2px solid var(--accent);
}
header.top h1 { margin: 0; font-size: 2.8rem; line-height: 1.05; }
header.top .subtitle { margin: 4px 0 0; font-size: 1.15rem; color: var(--accent); font-family: "IM Fell English", Georgia, serif; }
.meta { display: grid; grid-template-columns: repeat(2, auto); gap: 3px 18px; font-size: .88rem; margin: 0; }
.meta div { display: contents; }
.meta dt { color: var(--muted); }
.meta dd { margin: 0; font-weight: 600; }

h2 {
  margin: 0 0 8px; font-size: 1.25rem; color: var(--accent);
  border-bottom: 1px solid var(--line); padding-bottom: 2px;
}
.box { border: 1px solid var(--line); background: #fff; padding: 10px 12px; margin-bottom: 14px; }
.scroll { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .92rem; }
th { text-align: left; font-weight: 600; color: var(--muted); border-bottom: 1px solid var(--line); padding: 3px 8px 3px 0; white-space: nowrap; }
td { padding: 3px 8px 3px 0; border-bottom: 1px dotted var(--line); vertical-align: top; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
td.strong { font-weight: 700; }

/* characteristics */
.chars th, .chars td { text-align: center; padding: 4px 6px; }
.chars th.rowlabel, .chars td.rowlabel { text-align: left; color: var(--muted); font-weight: 600; white-space: nowrap; }
.chars .abbr { font-family: "IM Fell English", Georgia, serif; font-size: 1.15rem; color: var(--ink); }
.chars .full { display: block; font-size: .68rem; font-weight: 400; color: var(--muted); }
.chars tr.current td { font-size: 1.35rem; font-weight: 700; border-bottom: 2px solid var(--accent); }
.chars td.rowlabel { font-size: .9rem; font-weight: 600; }
.chars tr.bonus td { color: var(--accent); font-weight: 700; }

.layout {
  display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); gap: 20px; margin-top: 20px;
}
.vitals { display: grid; grid-template-columns: repeat(auto-fit, minmax(92px, 1fr)); gap: 8px; margin-bottom: 14px; }
.vital { text-align: center; border: 1px solid var(--line); background: #fff; padding: 8px 4px; }
.vital .n { display: block; font-family: "IM Fell English", Georgia, serif; font-size: 1.8rem; line-height: 1.1; }
.vital .l { font-size: .75rem; color: var(--muted); }
.vital.hl { border-color: var(--accent); }
.vital.hl .n { color: var(--accent); }

.cols2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.cols3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.coins { display: flex; gap: 10px; margin-bottom: 8px; }
.coins div { flex: 1; text-align: center; border: 1px solid var(--line); padding: 4px 0; }
.coins b { display: block; font-size: 1.1rem; }
.coins span { font-size: .72rem; color: var(--muted); }
ul.plain { margin: 0; padding-left: 18px; }
.small { font-size: .9rem; white-space: pre-wrap; margin: 0; }
.muted { color: var(--muted); }
.talent { margin-bottom: 7px; }
.talent b { font-family: "IM Fell English", Georgia, serif; font-size: 1.05rem; font-weight: 400; }
.talent p { margin: 0; font-size: .9rem; }
.full { grid-column: 1 / -1; }
.over { color: var(--accent); font-weight: 700; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .cols3 { grid-template-columns: 1fr; }
}
@media (max-width: 620px) {
  header.top { grid-template-columns: 1fr; }
  .cols2 { grid-template-columns: 1fr; }
  .sheet { padding: 16px; }
}
@media print {
  html, body { background: #fff; }
  body { padding: 0; font-size: 11.5px; }
  .sheet { border: none; outline: none; padding: 0; max-width: none; }
  .box, .talent { break-inside: avoid; }
  @page { margin: 10mm; }
}
"""


def render_header(c: dict) -> str:
    career = esc(c.get("career", ""))
    level = c.get("career_level")
    career_line = f"{career} ({esc(level)})" if level else career
    subtitle = f"{esc(c.get('species', ''))} {career_line}"
    meta_items = [
        ("Class", c.get("career_class")),
        ("Status", c.get("status")),
        ("Player", c.get("player")),
        ("Age", c.get("age")),
        ("Height", c.get("height")),
        ("Hair", c.get("hair")),
        ("Eyes", c.get("eyes")),
    ]
    meta = "".join(
        f"<div><dt>{label}</dt><dd>{esc(v)}</dd></div>" for label, v in meta_items if v
    )
    return f"""
<header class="top">
  <div>
    <h1>{esc(c.get('name', 'Unnamed character'))}</h1>
    <p class="subtitle">{subtitle}</p>
  </div>
  <dl class="meta">{meta}</dl>
</header>"""


def render_characteristics(d: dict) -> str:
    head = "".join(
        f'<th><span class="abbr">{k}</span><span class="full">{name}</span></th>'
        for k, name in CHARACTERISTICS
    )

    def row(label, field, cls=""):
        cells = "".join(f"<td>{d['chars'][k][field]}</td>" for k in CHAR_KEYS)
        return f'<tr class="{cls}"><td class="rowlabel">{label}</td>{cells}</tr>'

    return f"""
<div class="box scroll" style="margin-top:18px">
  <table class="chars">
    <thead><tr><th class="rowlabel"></th>{head}</tr></thead>
    <tbody>
      {row("Initial", "initial")}
      {row("Advances", "advances")}
      {row("Current", "current", "current")}
      {row("Bonus", "bonus", "bonus")}
    </tbody>
  </table>
</div>"""


def render_vitals(c: dict, d: dict) -> str:
    wounds_now = c.get("wounds_current", d["wounds"])
    corr_now = c.get("corruption", {}).get("current", 0)
    over = "over" if d["enc"] > d["enc_limit"] else ""
    return f"""
<div class="vitals">
  <div class="vital hl"><span class="n">{esc(wounds_now)} / {d['wounds']}</span><span class="l">Wounds</span></div>
  <div class="vital"><span class="n">{esc(c.get('movement', 4))}</span><span class="l">Movement</span></div>
  <div class="vital"><span class="n">{esc(c.get('fate', 0))} / {esc(c.get('fortune', 0))}</span><span class="l">Fate / Fortune</span></div>
  <div class="vital"><span class="n">{esc(c.get('resilience', 0))} / {esc(c.get('resolve', 0))}</span><span class="l">Resilience / Resolve</span></div>
  <div class="vital"><span class="n">{esc(corr_now)} / {d['corruption_max']}</span><span class="l">Corruption</span></div>
  <div class="vital"><span class="n {over}">{d['enc']} / {d['enc_limit']}</span><span class="l">Encumbrance</span></div>
</div>"""


def render_experience(c: dict) -> str:
    xp = c.get("experience", {})
    motivation = c.get("motivation")
    mot = f'<p class="small" style="margin-top:8px"><b>Motivation:</b> {esc(motivation)}</p>' if motivation else ""
    return f"""
<div class="box"><h2>Experience</h2>
  <div class="coins">
    <div><b>{esc(xp.get('current', 0))}</b><span>Current</span></div>
    <div><b>{esc(xp.get('spent', 0))}</b><span>Spent</span></div>
    <div><b>{esc(xp.get('total', 0))}</b><span>Total</span></div>
  </div>{mot}
</div>"""


def render_skills(d: dict) -> str:
    basic_rows = "".join(
        f"<tr><td>{esc(n)}</td><td>{s['char']}</td><td class='num'>{s['adv']}</td>"
        f"<td class='num strong'>{s['total']}</td></tr>"
        for n, s in d["basic"].items()
    )
    adv_rows = "".join(
        f"<tr><td>{esc(s['name'])}</td><td>{esc(s['char'])}</td><td class='num'>{s['adv']}</td>"
        f"<td class='num strong'>{s['total']}</td></tr>"
        for s in d["advanced"]
    ) or "<tr><td colspan='4' class='muted'>None</td></tr>"
    head = "<thead><tr><th>Skill</th><th>Char.</th><th class='num'>Adv.</th><th class='num'>Skill</th></tr></thead>"
    return f"""
<div class="box"><h2>Basic skills</h2>
  <table>{head}<tbody>{basic_rows}</tbody></table>
</div>
<div class="box"><h2>Advanced skills</h2>
  <table>{head}<tbody>{adv_rows}</tbody></table>
</div>"""


def render_talents(c: dict) -> str:
    talents = c.get("talents", [])
    if not talents:
        return ""
    body = "".join(
        f'<div class="talent"><b>{esc(t.get("name"))}</b>'
        f' <span class="muted">(rank {esc(t.get("ranks", 1))})</span>'
        f'<p>{esc(t.get("text", ""))}</p></div>'
        for t in talents
    )
    return f'<div class="box"><h2>Talents</h2>{body}</div>'


def render_weapons(c: dict, d: dict) -> str:
    weapons = c.get("weapons", [])
    if not weapons:
        return ""
    rows = []
    for w in weapons:
        if "damage" in w:
            dmg = esc(w["damage"])
        else:
            mod = int(w.get("damage_mod", 0))
            if w.get("adds_sb"):
                dmg = f"+{d['sb'] + mod} <span class='muted'>(SB+{mod})</span>"
            else:
                dmg = f"+{mod}"
        rows.append(
            f"<tr><td>{esc(w.get('name'))}</td><td>{esc(w.get('group'))}</td>"
            f"<td class='num'>{esc(w.get('enc', 0))}</td><td>{esc(w.get('reach_range'))}</td>"
            f"<td>{dmg}</td><td>{esc(w.get('qualities'))}</td></tr>"
        )
    return f"""
<div class="box scroll"><h2>Weapons</h2>
  <table><thead><tr><th>Weapon</th><th>Group</th><th class="num">Enc</th><th>Reach / range</th><th>Damage</th><th>Qualities</th></tr></thead>
  <tbody>{"".join(rows)}</tbody></table>
</div>"""


def render_armour(c: dict, d: dict) -> str:
    loc_rows = "".join(
        f"<tr><td>{label}</td><td class='muted'>{rng}</td><td class='num strong'>{d['ap'][label]}</td></tr>"
        for label, rng in HIT_LOCATIONS
    )
    items = c.get("armour", [])
    item_rows = "".join(
        f"<tr><td>{esc(a.get('name'))}</td><td>{esc(', '.join(a.get('locations', [])))}</td>"
        f"<td class='num'>{esc(a.get('ap', 0))}</td><td class='num'>{esc(a.get('enc', 0))}</td>"
        f"<td>{esc(a.get('qualities'))}</td></tr>"
        for a in items
    )
    item_table = (
        f"<div class='scroll' style='margin-top:10px'><table><thead><tr><th>Armour</th><th>Covers</th>"
        f"<th class='num'>AP</th><th class='num'>Enc</th><th>Qualities</th></tr></thead>"
        f"<tbody>{item_rows}</tbody></table></div>"
    ) if items else ""
    return f"""
<div class="box"><h2>Armour and hit locations</h2>
  <table><thead><tr><th>Location</th><th>d100</th><th class="num">AP</th></tr></thead>
  <tbody>{loc_rows}</tbody></table>
  <p class="small muted" style="margin-top:6px">Damage taken is reduced by AP, then by Toughness Bonus ({d['tb']}).</p>
  {item_table}
</div>"""


def render_spells(c: dict) -> str:
    spells = c.get("spells", [])
    if not spells:
        return ""
    lore = c.get("magic_lore")
    lore_html = f'<p class="small" style="margin-bottom:6px"><b>Lore:</b> {esc(lore)}</p>' if lore else ""
    rows = "".join(
        f"<tr><td>{esc(s.get('name'))}</td><td class='num'>{esc(s.get('cn'))}</td>"
        f"<td>{esc(s.get('range'))}</td><td>{esc(s.get('target'))}</td>"
        f"<td>{esc(s.get('duration'))}</td><td>{esc(s.get('effect'))}</td></tr>"
        for s in spells
    )
    return f"""
<div class="box scroll"><h2>Spells and prayers</h2>{lore_html}
  <table><thead><tr><th>Name</th><th class="num">CN</th><th>Range</th><th>Target</th><th>Duration</th><th>Effect</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>"""


def render_trappings(c: dict) -> str:
    m = c.get("money", {})
    coins = (
        f"<div class='coins'><div><b>{esc(m.get('gc', 0))}</b><span>Gold crowns</span></div>"
        f"<div><b>{esc(m.get('s', 0))}</b><span>Silver shillings</span></div>"
        f"<div><b>{esc(m.get('d', 0))}</b><span>Brass pennies</span></div></div>"
    )
    rows = "".join(
        f"<tr><td>{esc(t.get('name'))}</td><td class='num'>{esc(t.get('enc', 0))}</td>"
        f"<td class='muted'>{esc(t.get('note', ''))}</td></tr>"
        for t in c.get("trappings", [])
    )
    table = (
        f"<table><thead><tr><th>Item</th><th class='num'>Enc</th><th>Notes</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    ) if rows else ""
    return f'<div class="box"><h2>Money and trappings</h2>{coins}{table}</div>'


def render_condition_lists(c: dict) -> str:
    def block(title, items):
        if not items:
            return ""
        li = "".join(f"<li>{esc(i)}</li>" for i in items)
        return f'<div class="box"><h2>{title}</h2><ul class="plain">{li}</ul></div>'
    out = block("Psychology", c.get("psychology", [])) + block("Mutations", c.get("mutations", []))
    return f'<div class="cols2">{out}</div>' if out else ""


def render_ambitions(c: dict) -> str:
    a = c.get("ambitions", {})
    p = c.get("party", {})
    char_box = ""
    if a:
        char_box = (
            f'<div class="box"><h2>Ambitions</h2>'
            f'<p class="small"><b>Short-term:</b> {esc(a.get("short", ""))}</p>'
            f'<p class="small" style="margin-top:6px"><b>Long-term:</b> {esc(a.get("long", ""))}</p></div>'
        )
    party_box = ""
    if p:
        party_box = (
            f'<div class="box"><h2>Party: {esc(p.get("name", ""))}</h2>'
            f'<p class="small"><b>Short-term:</b> {esc(p.get("short", ""))}</p>'
            f'<p class="small" style="margin-top:6px"><b>Long-term:</b> {esc(p.get("long", ""))}</p>'
            f'<p class="small" style="margin-top:6px"><b>Members:</b> {esc(p.get("members", ""))}</p></div>'
        )
    return f'<div class="cols2">{char_box}{party_box}</div>' if (char_box or party_box) else ""


def render_notes(c: dict) -> str:
    parts = []
    if c.get("distinguishing_marks"):
        parts.append(f'<div class="box"><h2>Distinguishing marks</h2><p class="small">{esc(c["distinguishing_marks"])}</p></div>')
    if c.get("notes"):
        parts.append(f'<div class="box"><h2>Notes</h2><p class="small">{esc(c["notes"])}</p></div>')
    return f'<div class="cols2">{"".join(parts)}</div>' if parts else ""


def render_sheet(c: dict) -> str:
    d = compute(c)
    left = f"""
  <div>
    {render_vitals(c, d)}
    {render_experience(c)}
    {render_skills(d)}
  </div>"""
    right = f"""
  <div>
    {render_talents(c)}
    {render_weapons(c, d)}
    {render_armour(c, d)}
    {render_spells(c)}
    {render_trappings(c)}
  </div>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c.get('name', 'Character'))} \u2013 WFRP 4e character sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IM+Fell+English&family=Source+Serif+4:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<main class="sheet">
{render_header(c)}
{render_characteristics(d)}
<div class="layout">
  {left}
  {right}
  <div class="full">
    {render_condition_lists(c)}
    {render_ambitions(c)}
    {render_notes(c)}
  </div>
</div>
</main>
</body>
</html>
"""


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Generate a WFRP 4e HTML character sheet.")
    parser.add_argument("-i", "--input", help="JSON file describing the character (default: sample character)")
    parser.add_argument("-o", "--output", help="Output HTML path (default: <name>.html)")
    parser.add_argument("--dump-template", action="store_true",
                        help="Print the sample character as JSON and exit")
    args = parser.parse_args(argv)

    if args.dump_template:
        json.dump(SAMPLE_CHARACTER, sys.stdout, indent=2)
        print()
        return 0

    if args.input:
        try:
            character = json.loads(Path(args.input).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Could not read {args.input}: {exc}", file=sys.stderr)
            return 1
    else:
        character = SAMPLE_CHARACTER

    if args.output:
        out = Path(args.output)
    else:
        slug = "".join(ch if ch.isalnum() else "_" for ch in character.get("name", "character")).strip("_")
        out = Path(f"{slug or 'character'}.html")

    out.write_text(render_sheet(character), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())