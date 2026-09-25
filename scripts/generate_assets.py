#!/usr/bin/env python3
"""Generate every profile SVG in assets/ from one design system.

Static assets (banner, engineering map, icons) are pure layout. Data assets
(github-stats, contribution fleet maps) are built from the public GitHub
GraphQL API, so nothing on the profile is typed in by hand.

    GITHUB_TOKEN=... python scripts/generate_assets.py

A token is required for GraphQL (the Actions GITHUB_TOKEN is enough).
"""

from __future__ import annotations

import json
import math
import os
import random
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = "Pouya-Mansournia"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ICONS = ASSETS / "icons"

# ---------------------------------------------------------------- tokens --
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

DARK = {
    "bg": "#0d1117", "panel": "#161b22", "panel2": "#1c2230", "grid": "#21262d",
    "line": "#30363d", "text": "#e6edf3", "muted": "#8b949e", "faint": "#6e7681",
    "cyan": "#22d3ee", "blue": "#58a6ff", "green": "#3fb950", "orange": "#f0883e",
    "violet": "#a371f7",
    "cells": ["#161b22", "#0b3a4a", "#0e6177", "#1596b0", "#22d3ee"],
}
LIGHT = {
    "bg": "#ffffff", "panel": "#f6f8fa", "panel2": "#eef2f6", "grid": "#e5e9ef",
    "line": "#d0d7de", "text": "#1f2328", "muted": "#59636e", "faint": "#818b98",
    "cyan": "#0891b2", "blue": "#0969da", "green": "#1a7f37", "orange": "#bc4c00",
    "violet": "#8250df",
    "cells": ["#eef2f6", "#b6ecf5", "#67d3e8", "#1ba6c4", "#0e7490"],
}
DOMAIN = {"robotics": "cyan", "precision": "orange", "software": "violet", "product": "green"}


def write(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1024:.1f} KB)")


def grid_pattern(pid: str, color: str, size: int = 24, opacity: float = 1.0) -> str:
    return (
        f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
        f'<path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{color}" stroke-width="1" opacity="{opacity}"/>'
        f"</pattern>"
    )


# ---------------------------------------------------------------- header --
def header_banner() -> str:
    c = DARK
    # AMR route across a warehouse grid: waypoints -> smooth polyline
    route = "M 760 300 L 760 220 Q 760 196 784 196 L 900 196 Q 924 196 924 172 L 924 104 Q 924 80 948 80 L 1100 80"
    nodes = [(760, 300, "DOCK"), (924, 196, "NAV2"), (1100, 80, "GOAL")]
    shelves = "".join(
        f'<rect x="{x}" y="{y}" width="56" height="22" rx="3" fill="{c["panel2"]}" stroke="{c["line"]}"/>'
        for x, y in [(800, 236), (872, 236), (980, 236), (1052, 236), (980, 124), (1052, 124), (800, 124), (980, 164)]
    )
    lidar = "".join(
        f'<line x1="0" y1="0" x2="{70 * math.cos(a / 10)}" y2="{70 * math.sin(a / 10)}" '
        f'stroke="{c["cyan"]}" stroke-width="1" opacity="0.18"/>'
        for a in range(-31, 32, 4)
    )
    node_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="6" fill="{c["bg"]}" stroke="{c["cyan"]}" stroke-width="2"/>'
        f'<text x="{x + 12}" y="{y - 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{label}</text>'
        for x, y, label in nodes
    )
    tags = ["ROBOTICS", "AI", "EMBEDDED", "AUTOMATION", "PRODUCT"]
    tag_svg, x = "", 64
    for t in tags:
        w = 16 + len(t) * 8.4
        tag_svg += (
            f'<rect x="{x}" y="262" width="{w:.0f}" height="28" rx="14" fill="none" stroke="{c["line"]}"/>'
            f'<text x="{x + w / 2:.0f}" y="281" text-anchor="middle" font-family="{MONO}" font-size="12" '
            f'fill="{c["text"]}" letter-spacing="1">{t}</text>'
        )
        x += w + 10
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img"
     aria-label="Pouya Mansournia. Robotics Engineer, Technical Founder, Product Leader. Robotics, AI, Embedded Systems, Automation and Product Engineering. An autonomous mobile robot follows a navigation path across a warehouse grid.">
  <defs>
    {grid_pattern("g", c["grid"], 24, 0.7)}
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0.45" stop-color="{c['bg']}" stop-opacity="1"/><stop offset="0.62" stop-color="{c['bg']}" stop-opacity="0"/></linearGradient>
    <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{c['cyan']}"/><stop offset="1" stop-color="{c['blue']}"/></linearGradient>
  </defs>
  <rect width="1200" height="360" rx="14" fill="{c['bg']}"/>
  <rect width="1200" height="360" rx="14" fill="url(#g)"/>
  <rect width="1200" height="360" rx="14" fill="url(#fade)"/>
  <rect x="0.5" y="0.5" width="1199" height="359" rx="14" fill="none" stroke="{c['line']}"/>
  <rect x="64" y="0" width="120" height="3" fill="url(#bar)"/>

  <g font-family="{FONT}">
    <text x="64" y="74" font-family="{MONO}" font-size="13" fill="{c['cyan']}" letter-spacing="3">SYSTEM://PROFILE</text>
    <text x="62" y="146" font-size="60" font-weight="700" fill="{c['text']}" letter-spacing="-1">Pouya Mansournia</text>
    <text x="64" y="194" font-size="24" fill="{c['text']}" opacity="0.92">Robotics Engineer · Technical Founder · Product Leader</text>
    <text x="64" y="228" font-size="16" fill="{c['muted']}">From mechanism and firmware to fleet software and shipped product.</text>
  </g>
  {tag_svg}

  <g>
    {shelves}
    <path d="{route}" fill="none" stroke="{c['line']}" stroke-width="3" stroke-linecap="round"/>
    <path id="route" d="{route}" fill="none" stroke="{c['cyan']}" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round" opacity="0.9"/>
    {node_svg}
    <g>
      <animateMotion dur="9s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;0.85;1" calcMode="linear"><mpath href="#route"/></animateMotion>
      <g opacity="0.9">{lidar}</g>
      <rect x="-14" y="-10" width="28" height="20" rx="5" fill="{c['cyan']}"/>
      <rect x="4" y="-6" width="6" height="12" rx="2" fill="{c['bg']}"/>
    </g>
  </g>
  <text x="1136" y="330" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c['faint']}">amr_01 · /cmd_vel · nav2 · slam_toolbox</text>
</svg>"""


# ------------------------------------------------------- engineering map --
MAP = [
    ("robotics", "ROBOTICS & AUTONOMY", 40, 96, [
        ("Warehouse AMR ROS2", "Multi-robot fleet · SLAM · Nav2"),
        ("Delivery Robot ROS", "6-wheel robot · LiDAR · waypoints"),
        ("ROS 2: Zero to Robot", "Book · EN + FA editions"),
        ("RACA / Emergent Agents", "Multi-robot coordination research"),
    ], ["ROS 2", "SLAM", "Nav2", "Gazebo", "AMR", "Multi-robot"]),
    ("precision", "PRECISION & MECHATRONICS", 620, 96, [
        ("Piezo Controller", "Closed-loop piezo · strain gauge"),
        ("Stepper Controllers", "STM32 · DRV8825 / L297"),
        ("FSR Board", "Force sensing for manipulation"),
        ("Flexure mechanisms", "Precision motion design"),
    ], ["Piezo", "Flexures", "Motion control", "Mechanism design"]),
    ("software", "AI, EMBEDDED & SOFTWARE", 40, 372, [
        ("FoundryOS", "Agentic OS for AI teams"),
        ("ARCHON", "Architecture decision system"),
        ("Robot Vision → SLAM", "CV book · pixel to V-SLAM"),
        ("Multifunctional Probe", "ESP32 industrial I/O board"),
    ], ["Python", "C/C++", "ESP32", "STM32", "OpenCV", "AI agents"]),
    ("product", "PRODUCT & FOUNDER SYSTEMS", 620, 372, [
        ("X-ROBOTIICS", "Co-founder · CINO"),
        ("Acust.ai sensing", "IoT acoustic monitoring"),
        ("FlexSim Digital Twin", "Warehouse twin · fleet RMS"),
        ("Warehouse automation", "Sorters · conveyors · AMRs"),
    ], ["Product discovery", "IoT SaaS", "Systems eng.", "Leadership"]),
]


def engineering_network() -> str:
    c = DARK
    W, H = 1200, 700
    cx, cy = 600, 356
    parts = []
    for key, title, x, y, projects, concepts in MAP:
        col = c[DOMAIN[key]]
        w, h = 540, 232
        # bus line from core to panel
        px = x + (w if x < cx else 0)
        py = y + h / 2
        parts.append(
            f'<path d="M {cx} {cy} L {px + (30 if x < cx else -30)} {cy} L {px + (30 if x < cx else -30)} {py} L {px} {py}" '
            f'fill="none" stroke="{col}" stroke-width="1.5" opacity="0.55" stroke-dasharray="4 5"/>'
            f'<circle cx="{px}" cy="{py}" r="4" fill="{col}"/>'
        )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>'
            f'<rect x="{x}" y="{y + 18}" width="3" height="22" rx="1.5" fill="{col}"/>'
            f'<text x="{x + 20}" y="{y + 35}" font-family="{MONO}" font-size="13" font-weight="700" fill="{col}" letter-spacing="1.5">{escape(title)}</text>'
        )
        for i, (name, sub) in enumerate(projects):
            gx = x + 20 + (i % 2) * 258
            gy = y + 56 + (i // 2) * 66
            parts.append(
                f'<rect x="{gx}" y="{gy}" width="244" height="54" rx="8" fill="{c["panel2"]}" stroke="{c["line"]}"/>'
                f'<circle cx="{gx + 16}" cy="{gy + 20}" r="4" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<text x="{gx + 28}" y="{gy + 25}" font-family="{FONT}" font-size="15" font-weight="600" fill="{c["text"]}">{escape(name)}</text>'
                f'<text x="{gx + 28}" y="{gy + 44}" font-family="{FONT}" font-size="12" fill="{c["muted"]}">{escape(sub)}</text>'
            )
        tx = x + 20
        for concept in concepts:
            tw = 14 + len(concept) * 7
            parts.append(
                f'<rect x="{tx}" y="{y + 196}" width="{tw}" height="22" rx="11" fill="none" stroke="{col}" stroke-opacity="0.45"/>'
                f'<text x="{tx + tw / 2}" y="{y + 211}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{escape(concept)}</text>'
            )
            tx += tw + 8
    # value chain across the top
    chain = ["MECHANISM", "ELECTRONICS", "FIRMWARE", "SOFTWARE", "PRODUCT", "DEPLOYMENT"]
    chain_svg, x0, step = "", 128, 190
    for i, label in enumerate(chain):
        x = x0 + i * step
        chain_svg += (
            f'<text x="{x}" y="52" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["text"]}" letter-spacing="1.5">{label}</text>'
            + (f'<path d="M {x + 62} 48 L {x + step - 62} 48" stroke="{c["line"]}" stroke-width="1.5"/>'
               f'<path d="M {x + step - 68} 44 L {x + step - 62} 48 L {x + step - 68} 52" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>'
               if i < len(chain) - 1 else "")
        )
    core = (
        f'<circle cx="{cx}" cy="{cy}" r="46" fill="{c["bg"]}" stroke="{c["cyan"]}" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="{c["cyan"]}" stroke-opacity="0.25">'
        f'<animate attributeName="r" values="50;64;50" dur="4s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values="0.35;0;0.35" dur="4s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{c["text"]}" letter-spacing="2">POUYA</text>'
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{c["muted"]}">systems core</text>'
    )
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="Engineering system map. A value chain from mechanism to deployment sits above four domains connected to a central core: Robotics and Autonomy (Warehouse AMR ROS2, Delivery Robot ROS, ROS 2 Zero to Robot, RACA multi-robot research); Precision and Mechatronics (Piezo Controller, stepper controllers, FSR board, flexure mechanisms); AI, Embedded and Software (FoundryOS, ARCHON, Robot Vision to SLAM, Multifunctional Probe); Product and Founder Systems (X-ROBOTIICS, Acust.ai sensing, FlexSim digital twin, warehouse automation).">
  <defs>{grid_pattern("g", c["grid"], 20, 0.5)}</defs>
  <rect width="{W}" height="{H}" rx="14" fill="{c['bg']}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{c['line']}"/>
  {chain_svg}
  {''.join(parts)}
  {core}
</svg>"""


# ----------------------------------------------------------------- icons --
ICON_PATHS = {
    "robotics": '<rect x="5" y="8" width="14" height="10" rx="2"/><circle cx="9.5" cy="13" r="1.3"/><circle cx="14.5" cy="13" r="1.3"/><path d="M12 8V5M10 4h4"/>',
    "precision": '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.5"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',
    "embedded": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "ai": '<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4M18 8.2v7.6"/>',
    "product": '<path d="M4 18l5-5 4 3 7-8"/><path d="M15 8h5v5"/>',
    "book": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
    "fleet": '<rect x="3" y="4" width="7" height="5" rx="1"/><rect x="14" y="15" width="7" height="5" rx="1"/><path d="M6.5 9v5a3 3 0 0 0 3 3H14"/>',
    "twin": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>',
    "research": '<path d="M9 3v6l-5 9a2 2 0 0 0 1.7 3h12.6a2 2 0 0 0 1.7-3l-5-9V3M8 3h8"/>',
    "vision": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}


def icon(name: str, color: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{name} icon">'
        f"{ICON_PATHS[name]}</svg>"
    )


ICON_COLORS = {
    "robotics": DARK["cyan"], "precision": DARK["orange"], "embedded": DARK["violet"], "ai": DARK["violet"],
    "product": DARK["green"], "book": DARK["cyan"], "fleet": DARK["cyan"], "twin": DARK["green"],
    "research": DARK["blue"], "vision": DARK["blue"],
}


# ------------------------------------------------------------------ data --
def graphql(query: str, variables: dict) -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required for the GraphQL API.")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]


QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date weekday } }
      }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100, isFork: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name stargazerCount forkCount pushedAt
        languages(first: 6, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}
"""


def fetch() -> dict:
    user = graphql(QUERY, {"login": USERNAME})["user"]
    repos = user["repositories"]["nodes"]
    langs: Counter = Counter()
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
    cc = user["contributionsCollection"]
    return {
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "forks": sum(r["forkCount"] for r in repos),
        "followers": user["followers"]["totalCount"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "weeks": cc["contributionCalendar"]["weeks"],
        "langs": langs.most_common(6),
        "recent": [r["name"] for r in repos[:4]],
    }


# ----------------------------------------------------------------- stats --
def github_stats(d: dict) -> str:
    c = DARK
    W, H = 1200, 300
    metrics = [
        ("OWN PUBLIC REPOS", d["repos"], c["cyan"]),
        ("STARS", d["stars"], c["orange"]),
        ("COMMITS · 12 MO", d["commits"], c["green"]),
        ("CONTRIBUTIONS · 12 MO", d["contributions"], c["blue"]),
        ("FOLLOWERS", d["followers"], c["violet"]),
    ]
    tiles = ""
    for i, (label, value, col) in enumerate(metrics):
        x = 32 + (i % 3) * 190
        y = 64 + (i // 3) * 104
        tiles += (
            f'<rect x="{x}" y="{y}" width="176" height="90" rx="10" fill="{c["panel"]}" stroke="{c["line"]}"/>'
            f'<rect x="{x + 16}" y="{y + 18}" width="18" height="3" rx="1.5" fill="{col}"/>'
            f'<text x="{x + 16}" y="{y + 60}" font-family="{FONT}" font-size="32" font-weight="700" fill="{c["text"]}">{value:,}</text>'
            f'<text x="{x + 16}" y="{y + 78}" font-family="{MONO}" font-size="10" fill="{c["muted"]}" letter-spacing="1">{label}</text>'
        )
    total = sum(s for _, s in d["langs"]) or 1
    palette = [c["cyan"], c["blue"], c["violet"], c["orange"], c["green"], c["faint"]]
    bar, legend, bx = "", "", 640
    for i, (name, size) in enumerate(d["langs"]):
        w = 528 * size / total
        bar += f'<rect x="{bx:.1f}" y="92" width="{max(w - 2, 1):.1f}" height="12" fill="{palette[i]}"/>'
        bx += w
        lx, ly = 640 + (i % 2) * 264, 138 + (i // 2) * 30
        legend += (
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{palette[i]}"/>'
            f'<text x="{lx + 18}" y="{ly}" font-family="{FONT}" font-size="14" fill="{c["text"]}">{escape(name)}</text>'
            f'<text x="{lx + 244}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{c["muted"]}">{100 * size / total:.1f}%</text>'
        )
    recent = "  ·  ".join(d["recent"])
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="GitHub statistics: {d['repos']} public repositories, {d['stars']} stars, {d['commits']} commits and {d['contributions']} contributions in the last 12 months, {d['followers']} followers. Top languages by code size: {', '.join(n for n, _ in d['langs'])}.">
  <rect width="{W}" height="{H}" rx="14" fill="{c['bg']}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{c['line']}"/>
  <text x="32" y="42" font-family="{MONO}" font-size="13" font-weight="700" fill="{c['cyan']}" letter-spacing="2">TELEMETRY</text>
  <text x="{W - 32}" y="42" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c['faint']}">updated {date.today().isoformat()} · GitHub GraphQL API</text>
  {tiles}
  <rect x="624" y="64" width="560" height="194" rx="10" fill="{c['panel']}" stroke="{c['line']}"/>
  <text x="640" y="82" font-family="{MONO}" font-size="10" fill="{c['muted']}" letter-spacing="1">LANGUAGES · BY CODE SIZE, PUBLIC NON-FORK REPOS</text>
  <clipPath id="bar"><rect x="640" y="92" width="528" height="12" rx="6"/></clipPath>
  <g clip-path="url(#bar)">{bar}</g>
  {legend}
  <text x="32" y="{H - 18}" font-family="{MONO}" font-size="11" fill="{c['faint']}">recently pushed: {escape(recent)}</text>
</svg>"""


# ---------------------------------------------------------- contribution --
def contribution_fleet(d: dict, c: dict) -> str:
    """Contribution calendar drawn as a warehouse floor: each day is a storage
    cell whose fill is its activity level; AMRs patrol aisles between the
    busiest weeks."""
    weeks = d["weeks"][-53:]
    counts = [day["contributionCount"] for w in weeks for day in w["contributionDays"]]
    nonzero = sorted(x for x in counts if x)
    q = [nonzero[int(len(nonzero) * p)] if nonzero else 1 for p in (0.25, 0.5, 0.75)]

    def level(n: int) -> int:
        if n == 0:
            return 0
        return 1 + sum(n > t for t in q)

    cell, gap, ox, oy = 16, 4, 40, 70
    W = ox * 2 + len(weeks) * (cell + gap) - gap
    H = 300
    cells = ""
    week_activity = []
    for wi, w in enumerate(weeks):
        wx = ox + wi * (cell + gap)
        week_activity.append(sum(dd["contributionCount"] for dd in w["contributionDays"]))
        for dd in w["contributionDays"]:
            y = oy + dd["weekday"] * (cell + gap)
            lv = level(dd["contributionCount"])
            cells += (
                f'<rect x="{wx}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{c["cells"][lv]}"'
                f'{"" if lv else " stroke=" + chr(34) + c["line"] + chr(34) + " stroke-width=" + chr(34) + "0.6" + chr(34)}>'
                f'<title>{dd["date"]}: {dd["contributionCount"]} contributions</title></rect>'
            )
    # aisle under the grid; robots travel to the three busiest weeks
    aisle_y = oy + 7 * (cell + gap) + 14
    busiest = sorted(range(len(weeks)), key=lambda i: week_activity[i], reverse=True)[:3]
    rng = random.Random(7)
    robots = ""
    for n, wi in enumerate(sorted(busiest)):
        tx = ox + wi * (cell + gap) + cell / 2
        start = ox + rng.randint(0, len(weeks) - 1) * (cell + gap) + cell / 2
        dur = 7 + n * 2
        robots += (
            f'<g><rect x="-9" y="-6" width="18" height="12" rx="3" fill="{c["cyan"]}"/>'
            f'<rect x="3" y="-3" width="4" height="6" rx="1" fill="{c["bg"]}"/>'
            f'<animateTransform attributeName="transform" type="translate" dur="{dur}s" repeatCount="indefinite" '
            f'values="{start} {aisle_y}; {tx} {aisle_y}; {tx} {aisle_y}; {start} {aisle_y}" keyTimes="0;0.45;0.55;1"/></g>'
            f'<line x1="{tx}" y1="{oy + 7 * (cell + gap)}" x2="{tx}" y2="{aisle_y - 8}" stroke="{c["cyan"]}" stroke-width="1.5" stroke-dasharray="2 3" opacity="0.7"/>'
        )
    months, last = "", None
    for wi, w in enumerate(weeks):
        m = w["contributionDays"][0]["date"][5:7]
        if m != last and not (wi == 0 and weeks[min(2, len(weeks) - 1)]["contributionDays"][0]["date"][5:7] != m):
            label = date(2000, int(m), 1).strftime("%b").upper()
            months += f'<text x="{ox + wi * (cell + gap)}" y="{oy - 10}" font-family="{MONO}" font-size="10" fill="{c["muted"]}">{label}</text>'
            last = m
    legend = "".join(
        f'<rect x="{W - 40 - (5 - i) * 20}" y="{H - 34}" width="14" height="14" rx="3" fill="{c["cells"][i]}" stroke="{c["line"]}" stroke-width="0.6"/>'
        for i in range(5)
    )
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="Contribution activity for the last 12 months drawn as a warehouse floor: {d['contributions']} contributions. Each cell is one day, brighter cells mean more activity. Small autonomous robots drive along an aisle to the three busiest weeks.">
  <rect width="{W}" height="{H}" rx="14" fill="{c['bg']}"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{c['line']}"/>
  <text x="{ox}" y="36" font-family="{MONO}" font-size="13" font-weight="700" fill="{c['cyan']}" letter-spacing="2">FLEET FLOOR · CONTRIBUTIONS</text>
  <text x="{W - ox}" y="36" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c['muted']}">{d['contributions']:,} in the last 12 months</text>
  {months}
  {cells}
  <line x1="{ox}" y1="{aisle_y}" x2="{W - ox}" y2="{aisle_y}" stroke="{c['line']}" stroke-width="10" stroke-linecap="round" opacity="0.6"/>
  <line x1="{ox}" y1="{aisle_y}" x2="{W - ox}" y2="{aisle_y}" stroke="{c['faint']}" stroke-width="1" stroke-dasharray="8 8"/>
  {robots}
  <text x="{ox}" y="{H - 22}" font-family="{MONO}" font-size="10" fill="{c['faint']}">robots dock at the three most active weeks</text>
  <text x="{W - 148}" y="{H - 23}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{c['faint']}">less</text>
  {legend}
  <text x="{W - 36}" y="{H - 23}" font-family="{MONO}" font-size="10" fill="{c['faint']}">more</text>
</svg>"""


def main() -> None:
    write(ASSETS / "header-banner.svg", header_banner())
    write(ASSETS / "engineering-network.svg", engineering_network())
    for name, col in ICON_COLORS.items():
        write(ICONS / f"{name}.svg", icon(name, col))
    data = fetch()
    write(ASSETS / "github-stats.svg", github_stats(data))
    write(ASSETS / "contribution-system-dark.svg", contribution_fleet(data, DARK))
    write(ASSETS / "contribution-system-light.svg", contribution_fleet(data, LIGHT))


if __name__ == "__main__":
    main()
