"""
Fetches live GitHub contribution data and generates SVG cards for the profile README.
Produces:
  - assets/stats.svg          (Total Contributions · Current Streak · Longest Streak)
  - assets/graph.svg          (Last 30 days contribution bar chart)

Requires:
  env  GH_TOKEN       – a GitHub PAT with `read:user` scope
  env  GH_USERNAME    – GitHub username (default: gaaarrrgiiiiiiiiiii)
"""

import json, os, sys, math
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

# ── config ──────────────────────────────────────────────────────────────────
USERNAME = os.getenv("GH_USERNAME", "gaaarrrgiiiiiiiiiii")
TOKEN    = os.getenv("GH_TOKEN", "")
API      = "https://api.github.com/graphql"
ASSETS   = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

# ── colours (Tokyo Night palette) ───────────────────────────────────────────
BG       = "#0f1117"
CARD_BG  = "#161b22"
BORDER   = "#21262d"
TEXT     = "#c9d1d9"
DIM      = "#8b949e"
ACCENT   = "#58a6ff"
GREEN    = "#3fb950"
ORANGE   = "#d29922"
CYAN     = "#39d353"
BAR_COLORS = ["#0e4429", "#006d32", "#26a641", "#39d353"]


def gql(query: str, variables: dict | None = None) -> dict:
    """Execute a GitHub GraphQL query."""
    if not TOKEN:
        raise RuntimeError("GH_TOKEN required for GraphQL API")
    headers = {"Authorization": f"bearer {TOKEN}"}
    r = requests.post(API, json={"query": query, "variables": variables or {}}, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}", file=sys.stderr)
    return data.get("data", {})


def fetch_contributions_rest() -> dict | None:
    """Fallback: scrape contribution data from the public profile page."""
    import re
    try:
        # GitHub's public contribution calendar is available as HTML
        url = f"https://github.com/users/{USERNAME}/contributions"
        headers = {"Accept": "text/html"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        html = r.text

        # Parse contribution data from the HTML data attributes
        # Pattern: data-date="2024-01-01" data-level="1" data-count="3"
        # or newer: <td ... data-date="..." ...>N contribution...</td>
        pattern = r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?(?:data-count="(\d+)"|data-level="(\d+)")'
        matches = re.findall(pattern, html)

        if not matches:
            # Try alternate pattern for newer GitHub HTML
            pattern2 = r'data-date="(\d{4}-\d{2}-\d{2})"'
            dates_only = re.findall(pattern2, html)
            # Try to get counts from tool-tip or text nodes
            count_pattern = r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*>[^<]*?(\d+)\s+contribution'
            matches2 = re.findall(count_pattern, html)
            if matches2:
                days = [{"date": m[0], "contributionCount": int(m[1])} for m in matches2]
            elif dates_only:
                # If we only have dates, try level-based estimation
                level_pattern = r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"'
                level_matches = re.findall(level_pattern, html)
                if level_matches:
                    level_map = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}
                    days = [{"date": m[0], "contributionCount": level_map.get(int(m[1]), 1)} for m in level_matches]
                else:
                    return None
            else:
                return None
        else:
            days = []
            for m in matches:
                date = m[0]
                count = int(m[1]) if m[1] else (int(m[2]) if m[2] else 0)
                days.append({"date": date, "contributionCount": count})

        days.sort(key=lambda d: d["date"])
        total = sum(d["contributionCount"] for d in days)
        first_date = days[0]["date"] if days else datetime.now(timezone.utc).strftime("%Y-%m-%d")

        return {
            "user": {
                "contributionsCollection": {
                    "contributionCalendar": {
                        "totalContributions": total,
                        "weeks": [{"contributionDays": days}]  # flat list wrapped
                    }
                },
                "createdAt": first_date + "T00:00:00Z"
            }
        }
    except Exception as e:
        print(f"REST fallback failed: {e}", file=sys.stderr)
        return None


def fetch_contributions() -> dict:
    """Fetch the full contribution calendar for the current year and previous year."""
    now = datetime.now(timezone.utc)
    # We query two years to ensure we capture enough data for streaks
    from_date = (now - timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    to_date = now.strftime("%Y-%m-%dT23:59:59Z")

    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
        createdAt
      }
    }
    """
    return gql(query, {"username": USERNAME, "from": from_date, "to": to_date})


def compute_streaks(days: list[dict]) -> tuple[int, str, str, int, str, str, int]:
    """
    Given a sorted list of {date, contributionCount} dicts,
    compute:  total, current_streak, current_range, longest_streak, longest_range, first_date, last_count
    """
    total = sum(d["contributionCount"] for d in days)
    
    # Current streak (count backwards from today)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    current_streak = 0
    current_start = None
    current_end = None
    
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current_streak += 1
            current_start = d["date"]
            if current_end is None:
                current_end = d["date"]
        else:
            # Allow today to be zero (day not over yet)
            if d["date"] == today and current_streak == 0:
                continue
            break
    
    # Longest streak
    longest = 0
    longest_start = None
    longest_end = None
    run = 0
    run_start = None
    
    for d in days:
        if d["contributionCount"] > 0:
            run += 1
            if run_start is None:
                run_start = d["date"]
            if run > longest:
                longest = run
                longest_start = run_start
                longest_end = d["date"]
        else:
            run = 0
            run_start = None
    
    first_date = days[0]["date"] if days else today
    
    def fmt_range(start, end):
        if not start or not end:
            return ""
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        return f"{s.strftime('%b %d')} – {e.strftime('%b %d')}"
    
    return (
        total,
        current_streak,
        fmt_range(current_start, current_end) if current_start else "—",
        longest,
        fmt_range(longest_start, longest_end) if longest_start else "—",
        first_date,
        days[-1]["contributionCount"] if days else 0,
    )


def render_stats_svg(total, current, current_range, longest, longest_range, first_date):
    """Generate the contribution stats card SVG."""
    first_fmt = datetime.strptime(first_date, "%Y-%m-%d").strftime("%b %d, %Y")
    
    # Ring animation for current streak
    circumference = 2 * math.pi * 38
    progress = min(current / max(longest, 1), 1.0)
    dash = circumference * progress
    gap = circumference - dash

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="160" viewBox="0 0 800 160">
  <style>
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes countUp {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes ringDraw {{ from {{ stroke-dashoffset: {circumference}; }} to {{ stroke-dashoffset: {circumference - dash}; }} }}
    .card {{ animation: fadeIn 0.6s ease-out; }}
    .num {{ animation: countUp 0.8s ease-out 0.3s both; }}
    .ring {{ animation: ringDraw 1.2s ease-out 0.5s both; }}
  </style>
  
  <rect width="800" height="160" rx="10" fill="{BG}"/>
  
  <!-- Mac Window Dots -->
  <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="20" r="6" fill="#27c93f"/>

  <!-- Total Contributions -->
  <g class="card">
    <rect x="20" y="15" width="230" height="130" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="135" y="70" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="36" font-weight="700" fill="{ACCENT}" class="num">{total}</text>
    <text x="135" y="95" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="{TEXT}" font-weight="600">Total Contributions</text>
    <text x="135" y="115" text-anchor="middle" font-family="'Courier New', monospace" font-size="10" fill="{DIM}">{first_fmt} – Present</text>
  </g>
  
  <!-- Current Streak (center with ring) -->
  <g class="card" transform="translate(300, 15)">
    <rect width="200" height="130" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <!-- Ring background -->
    <circle cx="100" cy="55" r="38" fill="none" stroke="{BORDER}" stroke-width="4"/>
    <!-- Ring progress -->
    <circle cx="100" cy="55" r="38" fill="none" stroke="{GREEN}" stroke-width="4"
            stroke-dasharray="{dash} {gap}" stroke-linecap="round"
            transform="rotate(-90, 100, 55)" class="ring"/>
    <text x="100" y="62" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="28" font-weight="700" fill="{GREEN}" class="num">{current}</text>
    <text x="100" y="108" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="{TEXT}" font-weight="600">Current Streak</text>
    <text x="100" y="125" text-anchor="middle" font-family="'Courier New', monospace" font-size="10" fill="{DIM}">{current_range}</text>
  </g>
  
  <!-- Longest Streak -->
  <g class="card" transform="translate(550, 15)">
    <rect width="230" height="130" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
    <text x="115" y="70" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="36" font-weight="700" fill="{ORANGE}" class="num">{longest}</text>
    <text x="115" y="95" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="{TEXT}" font-weight="600">Longest Streak</text>
    <text x="115" y="115" text-anchor="middle" font-family="'Courier New', monospace" font-size="10" fill="{DIM}">{longest_range}</text>
  </g>
</svg>"""
    return svg


def render_graph_svg(days_30: list[dict]):
    """Generate the last-30-days contribution bar chart SVG."""
    max_count = max((d["contributionCount"] for d in days_30), default=1) or 1
    bar_w = 18
    gap = 5
    chart_w = len(days_30) * (bar_w + gap) - gap
    chart_h = 100
    left_pad = 40
    top_pad = 50
    svg_w = chart_w + left_pad + 40
    svg_h = chart_h + top_pad + 45

    bars = ""
    labels = ""
    for i, d in enumerate(days_30):
        x = left_pad + i * (bar_w + gap)
        h = max((d["contributionCount"] / max_count) * chart_h, 2)
        y = top_pad + chart_h - h
        
        # Color intensity based on count
        if d["contributionCount"] == 0:
            color = "#21262d"
        elif d["contributionCount"] <= max_count * 0.25:
            color = BAR_COLORS[0]
        elif d["contributionCount"] <= max_count * 0.5:
            color = BAR_COLORS[1]
        elif d["contributionCount"] <= max_count * 0.75:
            color = BAR_COLORS[2]
        else:
            color = BAR_COLORS[3]
        
        delay = 0.02 * i
        bars += f"""    <rect x="{x}" y="{y}" width="{bar_w}" height="{h}" rx="3" fill="{color}" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>
      <animate attributeName="y" from="{top_pad + chart_h}" to="{y}" begin="{delay}s" dur="0.4s" fill="freeze"/>
      <animate attributeName="height" from="0" to="{h}" begin="{delay}s" dur="0.4s" fill="freeze"/>
    </rect>
"""
        # Date label every 5 days
        if i % 5 == 0:
            dt = datetime.strptime(d["date"], "%Y-%m-%d")
            labels += f'    <text x="{x + bar_w/2}" y="{top_pad + chart_h + 18}" text-anchor="middle" font-family="\'Courier New\', monospace" font-size="9" fill="{DIM}">{dt.strftime("%b")}</text>\n'
            labels += f'    <text x="{x + bar_w/2}" y="{top_pad + chart_h + 30}" text-anchor="middle" font-family="\'Courier New\', monospace" font-size="9" fill="{DIM}">{dt.strftime("%d")}</text>\n'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
  <rect width="{svg_w}" height="{svg_h}" rx="10" fill="{BG}"/>
  <rect x="10" y="10" width="{svg_w - 20}" height="{svg_h - 20}" rx="8" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>
  
  <!-- Mac Window Dots -->
  <circle cx="30" cy="30" r="6" fill="#ff5f56"/>
  <circle cx="50" cy="30" r="6" fill="#ffbd2e"/>
  <circle cx="70" cy="30" r="6" fill="#27c93f"/>

  <!-- Title -->
  <text x="90" y="34" font-family="'Courier New', monospace" font-size="12" fill="{DIM}" letter-spacing="2">// CONTRIBUTION GRAPH — LAST 30 DAYS</text>
  
  <!-- Bars -->
{bars}
  <!-- Labels -->
{labels}
</svg>"""
    return svg


def main():
    print(f"Fetching contributions for {USERNAME}...")
    
    data = None
    
    # Try GraphQL first (requires GH_TOKEN)
    if TOKEN:
        try:
            data = fetch_contributions()
            print("  Using GraphQL API (authenticated)")
        except Exception as e:
            print(f"  GraphQL failed: {e}", file=sys.stderr)
    
    # Fallback to REST/scraping
    if not data or "user" not in data:
        print("  Trying REST fallback (public profile)...")
        data = fetch_contributions_rest()
    
    if not data or "user" not in data:
        print("ERROR: Could not fetch data. Set GH_TOKEN env var.", file=sys.stderr)
        print("  Generate a PAT at https://github.com/settings/tokens")
        print("  with 'read:user' scope, then:")
        print("  $env:GH_TOKEN='ghp_xxx'; python scripts/update_stats.py")
        sys.exit(1)
    
    calendar = data["user"]["contributionsCollection"]["contributionCalendar"]
    
    # Flatten all days
    all_days = []
    for week in calendar["weeks"]:
        all_days.extend(week["contributionDays"])
    all_days.sort(key=lambda d: d["date"])
    
    # Compute streaks
    total, current, current_range, longest, longest_range, first_date, _ = compute_streaks(all_days)
    
    print(f"  Total: {total} | Current Streak: {current} | Longest Streak: {longest}")
    
    # Last 30 days for bar chart
    days_30 = all_days[-30:]
    
    # Generate SVGs
    stats_svg = render_stats_svg(total, current, current_range, longest, longest_range, first_date)
    graph_svg = render_graph_svg(days_30)
    
    (ASSETS / "stats.svg").write_text(stats_svg, encoding="utf-8")
    (ASSETS / "graph.svg").write_text(graph_svg, encoding="utf-8")
    
    print(f"  Generated assets/stats.svg and assets/graph.svg")


if __name__ == "__main__":
    main()
