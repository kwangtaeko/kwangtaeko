#!/usr/bin/env python3
"""README.md 를 .github/README.template.md 로 다시 쓴다.

하는 일
  1. assets/ 의 SVG 를 전부 다시 찍는다(assets.py).
  2. .github/repos.json 의 공개 저장소 스타 수를 조회해 카드와 히어로 알약에 넣는다.
     저장소가 아직 없으면(404) "coming soon" 으로 그린다 — 실패로 치지 않는다.
  3. GraphQL 로 공개 스타 합 · 공개 저장소 수 · 1년 기여 · 활동 일수를 받아 통계 타일을 그린다.
  4. 자산 주소에 내용 해시를 붙여(?v=) GitHub 이미지 캐시가 옛 그림을 붙들고 있지 않게 한다.

네트워크가 실패하면 이전에 그려 둔 히어로와 통계 타일을 그대로 둔다 — 6시간마다
도는 작업이 한 번 실패했다고 README 숫자가 '—' 로 돌아가면 안 된다.

외부 패키지 없이 표준 라이브러리만 쓴다(러너에 아무것도 설치하지 않으려고).

  python3 .github/scripts/update_readme.py            # Actions 와 같은 동작
  python3 .github/scripts/update_readme.py --offline  # 네트워크 없이, 자리표시 값으로
  python3 .github/scripts/update_readme.py --local    # 자산을 상대 경로로(로컬 미리보기용)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import assets  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
TEMPLATE = ROOT / ".github" / "README.template.md"
REPOS = ROOT / ".github" / "repos.json"
README = ROOT / "README.md"

RAW = "https://raw.githubusercontent.com/{owner}/{owner}/main/assets/{name}?v={ver}"
SHIELD = "https://img.shields.io/badge/{label}-{msg}-{color}?style=flat&labelColor=100E0D"
STAR = "%E2%98%85"  # ★
DOT = "%E2%97%8F"  # ●


# ── GitHub API ────────────────────────────────────────────────────
def _request(url: str, token: str | None, body: dict | None = None) -> tuple[int, dict | None]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "tgx-readme"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if body else "GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return 0, None


def fetch_repo(owner: str, repo: str, token: str | None) -> dict:
    """{'state': 'live'|'missing'|'unknown', 'stars': int, 'url': str}"""
    status, data = _request(f"https://api.github.com/repos/{owner}/{repo}", token)
    if status == 200 and data and not data.get("private"):
        return {"state": "live", "stars": int(data.get("stargazers_count", 0)), "url": data["html_url"]}
    if status == 404:
        return {"state": "missing", "stars": 0, "url": ""}
    return {"state": "unknown", "stars": 0, "url": ""}


STATS_QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}
"""


def fetch_stats(owner: str, token: str | None) -> dict[str, str] | None:
    if not token:
        return None
    status, data = _request("https://api.github.com/graphql", token, {"query": STATS_QUERY, "variables": {"login": owner}})
    try:
        user = data["data"]["user"]  # type: ignore[index]
    except (TypeError, KeyError):
        return None
    if status != 200 or not user:
        return None
    repos = user["repositories"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]
    return {
        "stars": compact(sum(n["stargazerCount"] for n in repos["nodes"])),
        "repos": str(repos["totalCount"]),
        "contrib": compact(cal["totalContributions"]),
        "active": str(sum(1 for c in days if c > 0)),
    }


# ── 그리기 ────────────────────────────────────────────────────────
def compact(n: int) -> str:
    if n >= 1000:
        s = f"{n / 1000:.1f}".rstrip("0").rstrip(".")
        return f"{s}k"
    return str(n)


def ver(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:8]


def render_public(items: list[dict], owner: str, results: dict[str, dict]) -> str:
    cells = []
    for it in items:
        r = results[it["repo"]]
        if r["state"] == "live":
            title = f'<a href="{r["url"]}"><b><code>{it["title"]}</code></b></a>'
            badge_url = SHIELD.format(label=STAR, msg=compact(r["stars"]), color="FB923C")
            badge = f'<a href="{r["url"]}/stargazers"><img src="{badge_url}" alt="stars" /></a>'
        else:
            title = f'<b><code>{it["title"]}</code></b>'
            badge = f'<img src="{SHIELD.format(label=STAR, msg="soon", color="332B26")}" alt="coming soon" />'
        cells.append(f'{title}&nbsp;{badge}<br/>\n      <sub>{it["desc"]}</sub>')
    return _table(cells, cols=min(2, len(cells)))


def render_private(items: list[dict]) -> str:
    badge = f'<img src="{SHIELD.format(label=DOT, msg="private", color="332B26")}" alt="private" />'
    cells = []
    for it in items:
        stack = " ".join(f"<code>{s}</code>" for s in it["stack"])
        cells.append(
            f'<b>{it["title"]}</b>&nbsp;{badge}<br/>\n'
            f'      <sub>{it["desc"]}</sub><br/>\n'
            f"      <sub>{stack}</sub>"
        )
    return _table(cells, cols=2)


def _table(cells: list[str], cols: int) -> str:
    width = f"{100 // cols}%"
    rows = []
    for i in range(0, len(cells), cols):
        tds = "".join(f'\n    <td width="{width}" valign="top">\n      {c}\n    </td>' for c in cells[i : i + cols])
        rows.append(f"  <tr>{tds}\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="네트워크 없이 자리표시 값으로")
    ap.add_argument("--local", action="store_true", help="자산을 상대 경로로(로컬 미리보기)")
    args = ap.parse_args()

    cfg = json.loads(REPOS.read_text(encoding="utf-8"))
    owner = cfg["owner"]
    token = None if args.offline else (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    ASSETS.mkdir(exist_ok=True)

    # 공개 저장소
    results: dict[str, dict] = {}
    for it in cfg["public"]:
        results[it["repo"]] = (
            {"state": "missing", "stars": 0, "url": ""} if args.offline else fetch_repo(owner, it["repo"], token)
        )

    # 자산 — 정적인 것은 매번 다시, 동적인 것은 값이 있을 때만
    files: dict[str, str] = dict(assets.static_assets())

    plugin = results.get("tgx-agent-mash", {"state": "missing"})
    hero_path = ASSETS / "hero.svg"
    if plugin["state"] == "live":
        files["hero.svg"] = assets.hero(f"★ {compact(plugin['stars'])}")
    elif plugin["state"] == "missing" or not hero_path.exists():
        files["hero.svg"] = assets.hero("coming soon")
    else:
        print("warn: 플러그인 상태를 모름 — 히어로는 이전 것을 유지", file=sys.stderr)

    stats = None if args.offline else fetch_stats(owner, token)
    tiles_path = ASSETS / "stat-tiles.svg"
    if stats:
        files["stat-tiles.svg"] = assets.stat_tiles(stats)
    elif not tiles_path.exists():
        files["stat-tiles.svg"] = assets.stat_tiles({})
    else:
        print("warn: 통계를 못 받음 — 통계 타일은 이전 것을 유지", file=sys.stderr)

    for name, svg in files.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")

    # README
    tpl = TEMPLATE.read_text(encoding="utf-8")
    tpl = re.sub(r"\A<!--.*?-->\s*", "", tpl, flags=re.S)

    def asset_url(m: re.Match) -> str:
        name = m.group(1)
        if args.local:
            return f"assets/{name}"
        content = (ASSETS / name).read_text(encoding="utf-8")
        return RAW.format(owner=owner, name=name, ver=ver(content))

    out = re.sub(r"\{\{asset:([\w.-]+)\}\}", asset_url, tpl)
    out = out.replace("{{PUBLIC}}", render_public(cfg["public"], owner, results))
    out = out.replace("{{PRIVATE}}", render_private(cfg["private"]))
    out = out.replace("{{MORE}}", str(cfg.get("more_private", 0)))
    out = out.replace("{{SYNC}}", dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    header = "<!-- 이 파일은 자동 생성된다. 고칠 곳은 .github/README.template.md 와 .github/repos.json -->\n\n"
    README.write_text(header + out, encoding="utf-8")

    left = re.findall(r"\{\{[^}]+\}\}", out)
    if left:
        print(f"error: 채우지 못한 자리표시 {left}", file=sys.stderr)
        return 1
    states = ", ".join(f"{k}={v['state']}" for k, v in results.items())
    print(f"README 갱신 · {states} · stats={'ok' if stats else 'kept'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
