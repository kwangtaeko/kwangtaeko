#!/usr/bin/env python3
"""README.md 를 .github/README.template.md 로 다시 쓴다.

하는 일
  1. assets/ 의 SVG 를 전부 다시 찍는다(assets.py).
  2. .github/repos.json 의 공개 저장소 스타 수를 조회해 카드와 히어로 알약에 넣는다.
     저장소가 아직 없으면(404) "coming soon" 으로 그린다 — 실패로 치지 않는다.
  3. GraphQL 로 기여 달력을 받아 통계 타일 · 31일 꺾은선 · 연속 기록 · 요일별 막대를
     직접 그린다. 달력은 GITHUB_TOKEN 으로 본다 — 프로필에 보이는 숫자와 같다.
     예전엔 꺾은선과 연속 기록을 외부 무료 서비스에서 받아 왔는데, 그쪽 한도에
     걸리면 README 에 깨진 그림만 남았다. 이제 남의 서버에 기대지 않는다.
  4. 카드도 SVG 로 그린다. GitHub 은 README 의 색·글꼴을 지워서 HTML 표로는
     카드 디자인을 맞출 수 없다.
  5. README_TOKEN(카드 저장소만 읽는 fine-grained 토큰)이 있으면 카드마다 마지막 push
     시각, 카드 저장소들의 언어 비율, 1년 커밋 · PR 수를 받아 그린다. 커밋 · PR 은
     GraphQL 기여 집계가 fine-grained 토큰으로는 비공개 몫을 세지 않아 저장소별로 직접 센다. 조회하는 저장소는 repos.json 의
     카드 저장소뿐이고, 로그에는 숫자만 남긴다 — Actions 로그는 누구나 볼 수 있다.
  6. 자산 주소에 내용 해시를 붙여(?v=) GitHub 이미지 캐시가 옛 그림을 붙들고 있지 않게 한다.

네트워크가 실패하면 이전에 그려 둔 히어로 · 공개 카드 · 통계 그림을 그대로 둔다 —
6시간마다 도는 작업이 한 번 실패했다고 README 숫자가 '—' 로 돌아가면 안 된다.

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
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_stats(owner: str, token: str | None) -> dict | None:
    """{'tiles': {...}, 'days': [(date, count), ...]} — 실패하면 None."""
    if not token:
        return None
    status, data = _request("https://api.github.com/graphql", token, {"query": STATS_QUERY, "variables": {"login": owner}})
    try:
        user = data["data"]["user"]  # type: ignore[index]
    except (TypeError, KeyError):
        return None
    if status != 200 or not user:
        return None
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    days = [d for d in days if d[0] <= today]
    return {
        "tiles": {
            "contrib": compact(cal["totalContributions"]),
            "best": compact(max((c for _, c in days), default=0)),
            "last30": compact(sum(c for _, c in days[-30:])),
        },
        "days": days,
    }


def fetch_pushed(owner: str, cards: list[dict], token: str | None) -> tuple[dict[str, dt.datetime], int]:
    """카드마다 묶인 저장소들 중 가장 최근 push 시각. (결과, 읽은 저장소 수)"""
    out: dict[str, dt.datetime] = {}
    ok = 0
    if not token:
        return out, ok
    for card in cards:
        for repo in card.get("repos", []):
            status, data = _request(f"https://api.github.com/repos/{owner}/{repo}", token)
            if status != 200 or not data or not data.get("pushed_at"):
                continue
            ok += 1
            when = dt.datetime.fromisoformat(data["pushed_at"].replace("Z", "+00:00"))
            if card["title"] not in out or when > out[card["title"]]:
                out[card["title"]] = when
    return out, ok


def fetch_work(owner: str, cards: list[dict], token: str | None) -> dict[str, int]:
    """카드 저장소의 최근 1년 내 커밋(기본 브랜치, 내가 author) · 내가 연 PR 수.
    한 저장소도 못 읽은 항목은 결과에 넣지 않는다 — 0 과 '모름' 을 구분하려고."""
    out: dict[str, int] = {}
    if not token:
        return out
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)
    since_s = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    commits = prs = 0
    commits_ok = prs_ok = False
    for repo in dict.fromkeys(r for c in cards for r in c.get("repos", [])):
        base = f"https://api.github.com/repos/{owner}/{repo}"
        for page in range(1, 31):
            status, data = _request(f"{base}/commits?author={owner}&since={since_s}&per_page=100&page={page}", token)
            if status == 409:  # 빈 저장소
                commits_ok = True
                break
            if status != 200 or not isinstance(data, list):
                break
            commits_ok = True
            commits += len(data)
            if len(data) < 100:
                break
        for page in range(1, 31):
            status, data = _request(f"{base}/pulls?state=all&sort=created&direction=desc&per_page=100&page={page}", token)
            if status != 200 or not isinstance(data, list):
                break
            prs_ok = True
            recent = [pr for pr in data if pr.get("created_at", "") >= since_s]
            prs += sum(1 for pr in recent if (pr.get("user") or {}).get("login", "").lower() == owner.lower())
            if len(data) < 100 or len(recent) < len(data):
                break
    if commits_ok:
        out["commits"] = commits
    if prs_ok:
        out["prs"] = prs
    return out


def fetch_languages(owner: str, cards: list[dict], token: str | None) -> dict[str, int]:
    """카드 저장소 전체의 언어별 바이트 합."""
    total: dict[str, int] = {}
    if not token:
        return total
    for repo in dict.fromkeys(r for c in cards for r in c.get("repos", [])):
        status, data = _request(f"https://api.github.com/repos/{owner}/{repo}/languages", token)
        if status != 200 or not isinstance(data, dict):
            continue
        for lang, n in data.items():
            total[lang] = total.get(lang, 0) + int(n)
    return total


# ── 그리기 ────────────────────────────────────────────────────────
def compact(n: int) -> str:
    if n >= 1000:
        s = f"{n / 1000:.1f}".rstrip("0").rstrip(".")
        return f"{s}k"
    return str(n)


def ver(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:8]


def public_block(it: dict, r: dict, url: str) -> str:
    """공개 카드는 그림 한 장. 저장소가 살아 있으면 그 그림을 저장소 링크로 감싼다."""
    img = f'<img width="100%" src="{url}" alt="{it["title"]} — {assets.desc_text(it)}" />'
    if r["state"] == "live":
        img = f'<a href="{r["url"]}">{img}</a>'
    return f'<p align="center">\n  {img}\n</p>'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="네트워크 없이 자리표시 값으로")
    ap.add_argument("--local", action="store_true", help="자산을 상대 경로로(로컬 미리보기)")
    args = ap.parse_args()

    cfg = json.loads(REPOS.read_text(encoding="utf-8"))
    owner = cfg["owner"]
    token = None if args.offline else (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    pat = None if args.offline else (os.environ.get("README_TOKEN") or None)
    ASSETS.mkdir(exist_ok=True)

    # 공개 저장소
    results: dict[str, dict] = {}
    for it in cfg["public"]:
        results[it["repo"]] = (
            {"state": "missing", "stars": 0, "url": ""} if args.offline else fetch_repo(owner, it["repo"], token)
        )

    # 자산 — 정적인 것은 매번 다시, 동적인 것은 값이 있을 때만
    files: dict[str, str] = dict(assets.static_assets())

    plugin = results.get(cfg["public"][0]["repo"], {"state": "missing"})
    if plugin["state"] == "live":
        chip = f"★ {compact(plugin['stars'])}"
    elif plugin["state"] == "missing":
        chip = "coming soon"
    else:
        chip = None  # 모름 — 이전 그림 유지
    hero_label = chip

    def keep_or(name: str, make, ready: bool) -> None:
        """값이 있으면 새로 그리고, 없으면 이전 그림을 둔다. 처음이면 자리표시로 그린다."""
        if ready or not (ASSETS / name).exists():
            files[name] = make()
        else:
            print(f"warn: {name} 은 이전 것을 유지", file=sys.stderr)

    keep_or("hero.svg", lambda: assets.hero(hero_label or "coming soon"), chip is not None)
    pub = cfg["public"][0]
    stars = plugin["stars"] if plugin["state"] == "live" else None
    keep_or(
        "card-public.svg",
        lambda: assets.card_public(pub, chip or "coming soon", stars, pub.get("star_goal")),
        chip is not None,
    )

    # 비공개 카드 — 토큰이 없으면 칩만 '● private'. 토큰이 있는데 하나도 못 읽었으면 이전 그림 유지.
    pushed, pushed_ok = fetch_pushed(owner, cfg["private"], pat)
    keep_or("cards-private.svg", lambda: assets.cards_private(cfg["private"], pushed), not pat or bool(pushed))
    langs = fetch_languages(owner, cfg["private"], pat)
    keep_or("languages.svg", lambda: assets.languages(langs), bool(langs))

    # 기여 통계 — 달력은 GITHUB_TOKEN 으로(프로필과 같은 숫자), 커밋 · PR 은 카드 저장소에서 직접
    stats = None if args.offline else fetch_stats(owner, token)
    work = fetch_work(owner, cfg["private"], pat)
    if stats:
        stats["tiles"].update({k: compact(v) for k, v in work.items()})
    days = stats["days"] if stats else []
    keep_or("stat-tiles.svg", lambda: assets.stat_tiles(stats["tiles"] if stats else {}), bool(stats))
    keep_or("activity.svg", lambda: assets.activity(days), bool(stats))
    keep_or("streak.svg", lambda: assets.streak(days), bool(stats))
    keep_or("weekday.svg", lambda: assets.weekday(days), bool(stats))

    for name, svg in files.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")

    # README
    tpl = TEMPLATE.read_text(encoding="utf-8")
    tpl = re.sub(r"\A<!--.*?-->\s*", "", tpl, flags=re.S)

    def asset_url_for(name: str) -> str:
        if args.local:
            return f"assets/{name}"
        content = (ASSETS / name).read_text(encoding="utf-8")
        return RAW.format(owner=owner, name=name, ver=ver(content))

    out = re.sub(r"\{\{asset:([\w.-]+)\}\}", lambda m: asset_url_for(m.group(1)), tpl)
    pub = cfg["public"][0]
    out = out.replace("{{PUBLIC}}", public_block(pub, results[pub["repo"]], asset_url_for("card-public.svg")))
    out = out.replace("{{MORE}}", str(cfg.get("more_private", 0)))
    header = "<!-- 이 파일은 자동 생성된다. 고칠 곳은 .github/README.template.md 와 .github/repos.json -->\n\n"
    README.write_text(header + out, encoding="utf-8")

    left = re.findall(r"\{\{[^}]+\}\}", out)
    if left:
        print(f"error: 채우지 못한 자리표시 {left}", file=sys.stderr)
        return 1
    states = ", ".join(f"{k}={v['state']}" for k, v in results.items())
    n_repos = sum(len(c.get("repos", [])) for c in cfg["private"])
    tiles = " ".join(f"{k}={v}" for k, v in stats["tiles"].items()) if stats else "kept"
    print(
        f"README 갱신 · {states} · token={'ok' if pat else 'none'} · pushed={pushed_ok}/{n_repos} "
        f"· langs={len(langs)} · stats: {tiles}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
