#!/usr/bin/env python3
"""Generate assets/github-stats.svg from the public GitHub API.

Run with GITHUB_TOKEN set (higher rate limit) or unauthenticated for
public data only. Intended to run on a schedule via GitHub Actions so
the profile README never depends on third-party stats services.
"""
import json
import os
import urllib.request
from collections import Counter

USERNAME = "Pouya-Mansournia"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def paginated(path):
    items, page = [], 1
    while True:
        chunk = api(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        if not chunk:
            break
        items.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return items


def main():
    user = api(f"/users/{USERNAME}")
    repos = paginated(f"/users/{USERNAME}/repos?type=owner")

    public_repos = user.get("public_repos", len(repos))
    followers = user.get("followers", 0)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)

    langs = Counter()
    for r in repos:
        lang = r.get("language")
        if lang:
            langs[lang] += 1
    top_langs = langs.most_common(5)
    top_total = sum(c for _, c in top_langs) or 1

    palette = ["#22d3ee", "#0ea5e9", "#818cf8", "#f59e0b", "#34d399"]

    lang_rows = ""
    y = 0
    for i, (lang, count) in enumerate(top_langs):
        pct = round(100 * count / top_total)
        color = palette[i % len(palette)]
        bar_w = max(4, round(2.4 * pct))
        lang_rows += f'''
    <text x="0" y="{y+14}" font-size="12" fill="#cbd5e1">{lang}</text>
    <rect x="120" y="{y+3}" width="240" height="10" rx="5" fill="#0f2036"/>
    <rect x="120" y="{y+3}" width="{bar_w}" height="10" rx="5" fill="{color}"/>
    <text x="368" y="{y+13}" font-size="11" fill="#64748b">{pct}%</text>'''
        y += 28

    svg = f'''<svg width="760" height="230" viewBox="0 0 760 230" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub statistics for {USERNAME}">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="760" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22d3ee"/>
      <stop offset="1" stop-color="#3b82f6"/>
    </linearGradient>
  </defs>
  <rect width="760" height="230" rx="10" fill="#0a0f1a" stroke="#1f2937"/>
  <rect x="0" y="0" width="760" height="3" fill="url(#accent)"/>
  <text x="24" y="34" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="14" font-weight="700" fill="#e2e8f0" letter-spacing="0.5">GITHUB STATISTICS</text>

  <g font-family="'Segoe UI', Helvetica, Arial, sans-serif" transform="translate(24,60)">
    <text font-size="26" font-weight="700" fill="#22d3ee">{public_repos}</text>
    <text y="20" font-size="11" fill="#64748b">Public Repos</text>
  </g>
  <g font-family="'Segoe UI', Helvetica, Arial, sans-serif" transform="translate(200,60)">
    <text font-size="26" font-weight="700" fill="#22d3ee">{total_stars}</text>
    <text y="20" font-size="11" fill="#64748b">Total Stars</text>
  </g>
  <g font-family="'Segoe UI', Helvetica, Arial, sans-serif" transform="translate(376,60)">
    <text font-size="26" font-weight="700" fill="#22d3ee">{total_forks}</text>
    <text y="20" font-size="11" fill="#64748b">Total Forks</text>
  </g>
  <g font-family="'Segoe UI', Helvetica, Arial, sans-serif" transform="translate(552,60)">
    <text font-size="26" font-weight="700" fill="#22d3ee">{followers}</text>
    <text y="20" font-size="11" fill="#64748b">Followers</text>
  </g>

  <line x1="24" y1="110" x2="736" y2="110" stroke="#1f2937"/>

  <text x="24" y="132" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="12" font-weight="700" fill="#e2e8f0" letter-spacing="0.5">TOP LANGUAGES BY REPO COUNT</text>
  <g font-family="'Segoe UI', Helvetica, Arial, sans-serif" transform="translate(24,150)">{lang_rows}
  </g>
</svg>
'''

    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "github-stats.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
