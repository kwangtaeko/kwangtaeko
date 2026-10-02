"""TGX 프로필 README 의 SVG 자산을 만든다.

손으로 그린 SVG 파일을 따로 두지 않고 여기서 전부 찍어 낸다. 히어로의
플러그인 상태와 통계 타일은 Actions 가 6시간마다 다시 쓰는데, 정적인 것까지
같은 곳에서 나와야 색이 한 군데에서만 바뀐다.

팔레트는 tonygwangsk.dev 의 다크 토큰과 같다. GitHub 남색(#0D1117) 위에
따뜻한 검정(#100E0D) 판을 올리는 것이 의도 — 사이트와 README 가 한 브랜드로
읽힌다.

GitHub 은 README 의 SVG 를 <img> 로 그리므로 외부 폰트·스크립트는 쓸 수 없다.
글꼴은 시스템 모노/산세리프, 움직임은 SVG 안의 SMIL 만 쓴다.
"""

from __future__ import annotations

from html import escape

BG = "#100e0d"
CARD = "#1a1715"
LINE = "#332b26"
DOT = "#2a2420"
ORANGE = "#fb923c"
DEEP = "#bf4008"
VIOLET = "#7c4dd6"
LILAC = "#b79cf0"
INK = "#f2e9e3"
MUTE = "#a99a90"
FAINT = "#6f625a"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def _wrap(w: int, h: int, label: str, body: str, *, plate: bool = True) -> str:
    """viewBox 와 판(바탕·점무늬·테두리)을 씌운다."""
    pid = "d" + str(w) + str(h)
    plate_svg = (
        f'<defs><pattern id="{pid}" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="{DOT}"/></pattern></defs>'
        f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#{pid})"/>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13.5" fill="none" stroke="{LINE}"/>'
        if plate
        else ""
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>{plate_svg}{body}</svg>\n"
    )


# ── 히어로 ─────────────────────────────────────────────────────────
def hero(plugin_label: str) -> str:
    """TGX 마크 · 한 줄 소개 · 에이전트 메시.

    plugin_label 은 알약 안의 상태 문구다. 저장소가 없으면 "coming soon",
    공개되면 스타 수가 들어간다(update_readme.py 가 정한다).
    """
    b = []
    a = b.append
    a(
        f'<defs><radialGradient id="hglow"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="hbar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{ORANGE}"/>'
        f'<stop offset="1" stop-color="{DEEP}"/></linearGradient>'
        '<path id="he1" d="M640 160 L515 95"/><path id="he3" d="M640 160 L775 205"/>'
        '<path id="he5" d="M640 160 L560 270"/></defs>'
    )
    # 왼쪽 — 브랜드 마크와 한 줄
    a(
        f'<text x="34" y="128" font-family="{MONO}" font-size="64" font-weight="800" '
        f'fill="{INK}" letter-spacing="-2">TGX<tspan fill="{ORANGE}">.</tspan></text>'
    )
    a('<rect x="36" y="160" width="3" height="34" rx="1.5" fill="url(#hbar)"/>')
    a(
        f'<text x="50" y="184" font-family="{SANS}" font-size="19" font-weight="650" '
        f'fill="{ORANGE}">Agents, leading what&#8217;s next.</text>'
    )
    pill_w = 28 + int(7.3 * (len("tgx-agent-mash · ") + len(plugin_label))) + 16
    a(
        f'<g transform="translate(36 236)"><rect width="{pill_w}" height="30" rx="15" fill="{ORANGE}" '
        f'fill-opacity=".09" stroke="{ORANGE}" stroke-opacity=".55"/>'
        f'<circle cx="16" cy="15" r="4" fill="{ORANGE}"><animate attributeName="opacity" '
        f'values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="28" y="19.5" font-family="{MONO}" font-size="12" fill="{INK}">tgx-agent-mash '
        f'<tspan fill="{MUTE}">· {escape(plugin_label)}</tspan></text></g>'
    )
    # 오른쪽 — 가운데 TGX 로 모이는 에이전트들
    a(f'<g stroke="{LINE}" stroke-width="1" fill="none">')
    for d in ["M515 95 L740 72", "M740 72 L775 205", "M775 205 L690 275", "M690 275 L560 270", "M560 270 L500 205", "M500 205 L515 95"]:
        a(f'<path d="{d}"/>')
    a("</g>")
    a(f'<g stroke="{DEEP}" stroke-width="1.4" stroke-dasharray="4 5" fill="none" opacity=".85">')
    for x, y in [(515, 95), (740, 72), (775, 205), (690, 275), (560, 270), (500, 205)]:
        a(f'<path d="M640 160 L{x} {y}"/>')
    a('<animate attributeName="stroke-dashoffset" from="0" to="-18" dur="1.4s" repeatCount="indefinite"/></g>')
    for pid, beg, col, rev in [("he1", "0s", ORANGE, False), ("he3", "-0.8s", ORANGE, True), ("he5", "-1.6s", LILAC, False)]:
        kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ""
        a(
            f'<circle r="3" fill="{col}"><animateMotion dur="2.4s" begin="{beg}" repeatCount="indefinite"{kp}>'
            f'<mpath xlink:href="#{pid}" href="#{pid}"/></animateMotion></circle>'
        )
    a('<circle cx="640" cy="160" r="46" fill="url(#hglow)"/>')
    for x, y, name, col, tx, ty, anchor in [
        (515, 95, "plan", ORANGE, 515, 80, "middle"),
        (740, 72, "research", ORANGE, 740, 57, "middle"),
        (775, 205, "review", VIOLET, 775, 228, "middle"),
        (690, 275, "test", ORANGE, 690, 298, "middle"),
        (560, 270, "verify", VIOLET, 560, 293, "middle"),
        (500, 205, "code", ORANGE, 482, 209, "end"),
    ]:
        a(f'<circle cx="{x}" cy="{y}" r="6" fill="{CARD}" stroke="{col}" stroke-width="1.5"/>')
        a(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-family="{MONO}" font-size="11" fill="{MUTE}">{name}</text>')
    a(f'<circle cx="640" cy="160" r="12" fill="{ORANGE}"/>')
    a(
        f'<circle cx="640" cy="160" r="12" fill="none" stroke="{ORANGE}" stroke-opacity=".5">'
        '<animate attributeName="r" values="12;24" dur="2.2s" repeatCount="indefinite"/>'
        '<animate attributeName="stroke-opacity" values=".55;0" dur="2.2s" repeatCount="indefinite"/></circle>'
    )
    a(
        f'<text x="640" y="191" text-anchor="middle" font-family="{MONO}" font-size="12" '
        f'font-weight="800" fill="{INK}" letter-spacing=".5">TGX</text>'
    )
    return _wrap(830, 320, "TGX — Agents, leading what's next.", "".join(b))


# ── 섹션 머리 ──────────────────────────────────────────────────────
def section(key: str, rest: str, color: str = ORANGE) -> str:
    """선 위의 노드 두 개 + 라벨. 판 없이 GitHub 바탕 위에 바로 놓인다."""
    text_col = LILAC if color == VIOLET else ORANGE
    width = 24 + int(8.6 * (len(key) + 3 + len(rest)))
    body = (
        f'<line x1="10" y1="23" x2="820" y2="23" stroke="{LINE}"/>'
        f'<line x1="10" y1="23" x2="170" y2="23" stroke="{color}" stroke-dasharray="4 5"/>'
        f'<circle cx="10" cy="23" r="5" fill="{color}"/>'
        f'<circle cx="170" cy="23" r="4" fill="{BG}" stroke="{color}" stroke-width="1.5"/>'
        f'<rect x="186" y="10" width="{width}" height="26" rx="4" fill="{BG}" stroke="{LINE}"/>'
        f'<text x="198" y="27.5" font-family="{MONO}" font-size="12" font-weight="700" fill="{text_col}" '
        f'letter-spacing="1.4">{escape(key)} <tspan fill="{MUTE}" font-weight="500">· {escape(rest)}</tspan></text>'
        f'<circle cx="820" cy="23" r="3" fill="{LINE}"/>'
    )
    return _wrap(830, 46, f"{key} — {rest}", body, plate=False)


# ── 일하는 방식 ────────────────────────────────────────────────────
def workflow() -> str:
    """tonygwangsk.dev/projects 의 Orchestra 를 한 장으로 줄인 것.

    메인 모델(Claude Code / Codex)은 그때그때 바뀌고 교차검증은 항상 반대
    모델이 맡는다. 그래서 MAIN 라벨과 CROSS-CHECK 노드 이름이 같은 박자로
    함께 뒤바뀐다. 정지 화면에서도 읽히도록 "always the other" 를 적어 둔다.
    """
    H, DY = 398, 22
    A_ = '<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.44;.5;.94;1" dur="9s" repeatCount="indefinite"/>'
    B_ = '<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.44;.5;.94;1" dur="9s" repeatCount="indefinite"/>'
    b = []
    a = b.append
    a(
        "<defs>"
        '<path id="wfp1" d="M125 170 L160 170"/>'
        '<path id="wfp2" d="M300 170 C 332 170, 332 125, 364 125"/>'
        '<path id="wfp3" d="M476 215 L512 215 L512 147.5 L550 147.5"/>'
        '<path id="wfp4" d="M650 192.5 C 676 192.5, 676 170, 700 170"/>'
        '<path id="wfp5" d="M760 202 L760 300 Q760 312 748 312 L82 312 Q70 312 70 300 L70 194"/>'
        "</defs>"
    )
    for x, t in [(70, "DECIDE"), (230, "ORCHESTRATE"), (420, "EXECUTE"), (600, "VERIFY"), (760, "CROSS-CHECK")]:
        a(f'<text x="{x}" y="34" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{FAINT}">{t}</text>')
    a(f'<g transform="translate(0 {DY})">')
    a(f'<rect x="148" y="30" width="516" height="258" rx="14" fill="{ORANGE}" fill-opacity=".03" stroke="{ORANGE}" stroke-opacity=".45" stroke-dasharray="6 5"/>')
    a(f'<rect x="330" y="20" width="152" height="20" rx="10" fill="{BG}" stroke="{ORANGE}" stroke-opacity=".6"/>')
    a(f'<text x="406" y="34" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{ORANGE}">MAIN · Claude Code{A_}</text>')
    a(f'<text x="406" y="34" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{ORANGE}" opacity="0">MAIN · Codex{B_}</text>')
    ex = [80, 125, 170, 215, 260]
    gt = [102.5, 147.5, 192.5, 237.5]
    a('<g fill="none">')
    a(f'<line x1="125" y1="170" x2="160" y2="170" stroke="{ORANGE}" stroke-width="1.5"/>')
    for cy in ex:
        a(f'<path d="M300 170 C 332 170, 332 {cy}, 364 {cy}" stroke="{DEEP}" stroke-width="1.3" stroke-dasharray="3 4"/>')
        a(f'<line x1="476" y1="{cy}" x2="512" y2="{cy}" stroke="{VIOLET}" stroke-opacity=".55" stroke-width="1.2"/>')
    a(f'<line x1="512" y1="80" x2="512" y2="260" stroke="{VIOLET}" stroke-opacity=".55" stroke-width="1.2"/>')
    for gy in gt:
        a(f'<line x1="512" y1="{gy}" x2="550" y2="{gy}" stroke="{VIOLET}" stroke-opacity=".55" stroke-width="1.2"/>')
        a(f'<path d="M650 {gy} C 676 {gy}, 676 170, 700 170" stroke="{VIOLET}" stroke-width="1.2"/>')
    a(f'<path d="M760 202 L760 300 Q760 312 748 312 L82 312 Q70 312 70 300 L70 194" stroke="{LILAC}" stroke-width="1.3" stroke-dasharray="5 5" opacity=".8"/>')
    a("</g>")
    a(f'<path d="M64 202 L70 194 L76 202" fill="none" stroke="{LILAC}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<text x="415" y="306" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTE}" stroke="{BG}" stroke-width="5" paint-order="stroke">report back · critical / warning / suggestion</text>')
    # 사람 · 팀리더
    a(f'<rect x="15" y="147" width="110" height="46" rx="23" fill="{ORANGE}"/>')
    a(f'<text x="70" y="167" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="800" fill="{BG}">ME · human</text>')
    a(f'<text x="70" y="182" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#3b2416">go / no-go</text>')
    a(f'<rect x="160" y="147" width="140" height="46" rx="10" fill="{CARD}" stroke="{ORANGE}" stroke-width="1.5"/>')
    a(f'<text x="230" y="167" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">team-leader</text>')
    a(f'<text x="230" y="182" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTE}">plan · split · merge</text>')
    for cy, n in zip(ex, ["frontend", "backend", "database", "security", "design"]):
        a(f'<rect x="364" y="{cy - 15}" width="112" height="30" rx="8" fill="{CARD}" stroke="{DEEP}" stroke-width="1.3"/>')
        a(f'<text x="420" y="{cy + 4}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{INK}">{n}</text>')
    for gy, n in zip(gt, ["test", "review", "workflow", "mockup"]):
        a(f'<rect x="550" y="{gy - 15}" width="100" height="30" rx="8" fill="{CARD}" stroke="{VIOLET}" stroke-width="1.3"/>')
        a(f'<text x="600" y="{gy + 4}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#e7dcfb">{n}</text>')
    # 교차검증 — 항상 반대 모델
    a(f'<rect x="700" y="138" width="120" height="64" rx="10" fill="{CARD}" stroke="{LILAC}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    a(f'<text x="760" y="161" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">codex{A_}</text>')
    a(f'<text x="760" y="161" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}" opacity="0">claude code{B_}</text>')
    a(f'<text x="760" y="177" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{LILAC}">always the other</text>')
    for x, c in [(744, "#ef6b5b"), (760, ORANGE), (776, LILAC)]:
        a(f'<circle cx="{x}" cy="190" r="3.5" fill="{c}"/>')
    a(f'<path d="M482 30 C 640 30, 760 60, 760 132" fill="none" stroke="{LILAC}" stroke-opacity=".45" stroke-width="1" stroke-dasharray="2 4"/>')
    a(f'<text x="676" y="54" font-family="{MONO}" font-size="13" fill="{LILAC}">&#8644;</text>')
    for pid, dur, beg, col in [("wfp1", "1.2s", "0s", ORANGE), ("wfp2", "1.6s", "-0.4s", ORANGE), ("wfp3", "1.8s", "-0.9s", LILAC), ("wfp4", "1.4s", "-0.2s", LILAC), ("wfp5", "4.2s", "-1.5s", LILAC)]:
        a(f'<circle r="3" fill="{col}"><animateMotion dur="{dur}" begin="{beg}" repeatCount="indefinite"><mpath xlink:href="#{pid}" href="#{pid}"/></animateMotion></circle>')
    a("</g>")
    y0 = 330 + DY
    a(f'<line x1="24" y1="{y0}" x2="806" y2="{y0}" stroke="{DOT}"/>')
    for x, c, t in [(24, ORANGE, "Human decides — agents propose"), (262, DEEP, "Agents verify agents"), (420, VIOLET, "Automate the repeatable"), (588, LILAC, "Cross-check with the other model")]:
        a(f'<circle cx="{x + 4}" cy="{y0 + 22}" r="4" fill="{c}"/>')
        a(f'<text x="{x + 16}" y="{y0 + 26}" font-family="{SANS}" font-size="11.5" fill="{INK}">{t}</text>')
    label = (
        "TGX workflow — a human decides; the main model, Claude Code or Codex, runs a team-leader, "
        "five execution agents and four verification agents; the other model cross-checks; findings report back"
    )
    return _wrap(830, H, label, "".join(b))


# ── 포트폴리오 버튼 ────────────────────────────────────────────────
def portfolio_button() -> str:
    """shields.io 는 라벨 글자색을 못 바꿔서 직접 그린다."""
    body = (
        f'<rect width="240" height="34" rx="5" fill="{BG}"/>'
        f'<rect x="96" width="144" height="34" rx="5" fill="{DEEP}"/><rect x="96" width="10" height="34" fill="{DEEP}"/>'
        f'<text x="48" y="22" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" '
        f'letter-spacing="1.4" fill="{ORANGE}">PORTFOLIO</text>'
        f'<text x="168" y="22" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" '
        f'letter-spacing="1" fill="#fff7f0">TONYGWANGSK.DEV</text>'
    )
    return _wrap(240, 34, "portfolio — tonygwangsk.dev", body, plate=False)


# ── 통계 타일 ──────────────────────────────────────────────────────
def stat_tiles(stats: dict[str, str]) -> str:
    """네 칸. 값이 없으면 '—' 를 그린다(API 실패 시에도 깨지지 않게)."""
    tiles = [
        ("PUBLIC ★", stats.get("stars", "—"), ORANGE),
        ("PUBLIC REPOS", stats.get("repos", "—"), INK),
        ("CONTRIBUTIONS · 1Y", stats.get("contrib", "—"), INK),
        ("ACTIVE DAYS · 1Y", stats.get("active", "—"), LILAC),
    ]
    b = []
    for i, (label, value, col) in enumerate(tiles):
        x = 14 + (i % 2) * 192
        y = 14 + (i // 2) * 78
        b.append(
            f'<g transform="translate({x} {y})"><rect width="180" height="64" rx="7" fill="{CARD}"/>'
            f'<text x="12" y="22" font-family="{MONO}" font-size="10" fill="{MUTE}" letter-spacing="1">{escape(label)}</text>'
            f'<text x="12" y="50" font-family="{MONO}" font-size="24" font-weight="800" fill="{col}">{escape(value)}</text></g>'
        )
    return _wrap(400, 170, "TGX stats", "".join(b))


# ── 꼬리 ──────────────────────────────────────────────────────────
def footer() -> str:
    d = "M0 40 C 120 40, 160 22, 260 22 S 420 44, 560 34 S 700 22, 760 30"
    body = (
        f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
        f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="3 7" opacity=".7"/>'
        f'<circle cx="260" cy="22" r="3.5" fill="{ORANGE}"/><circle cx="560" cy="34" r="3.5" fill="{VIOLET}"/>'
        f'<circle cx="420" cy="36" r="2.5" fill="{MUTE}"/>'
        f'<text x="766" y="36" font-family="{MONO}" font-size="16" font-weight="800" fill="{MUTE}">TGX<tspan fill="{ORANGE}">.</tspan></text>'
    )
    return _wrap(830, 64, "TGX", body, plate=False)


def star() -> str:
    body = (
        f'<path fill="{ORANGE}" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279'
        "l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194"
        'L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/>'
    )
    return _wrap(16, 16, "star", body, plate=False)


def static_assets() -> dict[str, str]:
    """매번 같은 결과가 나오는 자산."""
    return {
        "star.svg": star(),
        "section-public.svg": section("PUBLIC", "the one to star"),
        "section-workflow.svg": section("HOW TGX WORKS", "human decides, agents verify"),
        "section-private.svg": section("BUILT IN PRIVATE", "code stays home", VIOLET),
        "section-graph.svg": section("COMMITS", "private ones included"),
        "workflow.svg": workflow(),
        "portfolio.svg": portfolio_button(),
        "footer.svg": footer(),
    }
