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

import datetime as dt
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
    pill_w = 28 + int(7.3 * (len("tgx-agent-mesh · ") + len(plugin_label))) + 16
    a(
        f'<g transform="translate(36 236)"><rect width="{pill_w}" height="30" rx="15" fill="{ORANGE}" '
        f'fill-opacity=".09" stroke="{ORANGE}" stroke-opacity=".55"/>'
        f'<circle cx="16" cy="15" r="4" fill="{ORANGE}"><animate attributeName="opacity" '
        f'values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="28" y="19.5" font-family="{MONO}" font-size="12" fill="{INK}">tgx-agent-mesh '
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
        ("CONTRIBUTIONS · 1Y", stats.get("contrib", "—"), ORANGE),
        ("COMMITS · 1Y", stats.get("commits", "—"), INK),
        ("PULL REQUESTS · 1Y", stats.get("prs", "—"), INK),
        ("CODE REVIEWS · 1Y", stats.get("reviews", "—"), LILAC),
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


# ── 카드 ──────────────────────────────────────────────────────────
def _char_w(ch: str, size: float) -> float:
    """SVG 는 글자를 스스로 줄바꿈하지 못해 폭을 어림한다. 한글·CJK 는 1em,
    나머지는 대략 반 폭. 약간 넉넉하게 잡아 오른쪽 끝에 닿지 않게 한다."""
    o = ord(ch)
    if o >= 0x1100 and (0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFF60):
        return size * 1.0
    if ch == " ":
        return size * 0.3
    if ch in "·.,:;'\"()+×":
        return size * 0.38
    if ch.isupper() or ch.isdigit():
        return size * 0.64
    return size * 0.56


def text_w(s: str, size: float) -> float:
    return sum(_char_w(c, size) for c in s)


def wrap(text: str, width: float, size: float) -> list[str]:
    """공백에서 끊는다(한국어도 어절 단위 — keep-all). 한 어절이 너무 길면 그 안에서 끊는다."""
    lines: list[str] = []
    cur = ""
    for word in text.split(" "):
        cand = word if not cur else f"{cur} {word}"
        if text_w(cand, size) <= width:
            cur = cand
            continue
        if cur:
            lines.append(cur)
        cur = ""
        while text_w(word, size) > width:
            cut = len(word)
            while cut > 1 and text_w(word[:cut], size) > width:
                cut -= 1
            lines.append(word[:cut])
            word = word[cut:]
        cur = word
    if cur:
        lines.append(cur)
    return lines


CARD_PAD = 18
TITLE = 15
DESC = 12.5
DESC_LH = 19
CHIP = 10.5


def _card(x: float, y: float, w: float, h: float, it: dict, chip: str, chip_col: str, chip_bg: str, title_font: str) -> str:
    """카드 한 장. 칩은 제목과 같은 줄, 오른쪽 위에 붙는다."""
    p = []
    p.append(f'<g transform="translate({x} {y})">')
    p.append(f'<rect width="{w}" height="{h}" rx="10" fill="{CARD}" stroke="{LINE}"/>')
    cw = len(chip) * CHIP * 0.62 + 20  # 칩 글자는 고정폭(모노)이라 글자 수로 잰다
    p.append(f'<rect x="{w - CARD_PAD - cw:.1f}" y="18" width="{cw:.1f}" height="20" rx="10" fill="{chip_bg}"/>')
    p.append(
        f'<text x="{w - CARD_PAD - cw / 2:.1f}" y="31.5" text-anchor="middle" font-family="{MONO}" '
        f'font-size="{CHIP}" fill="{chip_col}">{escape(chip)}</text>'
    )
    p.append(
        f'<text x="{CARD_PAD}" y="34" font-family="{title_font}" font-size="{TITLE}" font-weight="700" '
        f'fill="{INK}">{escape(it["title"])}</text>'
    )
    lines = _desc_lines(it, w)
    for i, (ln, col) in enumerate(lines):
        p.append(
            f'<text x="{CARD_PAD}" y="{60 + i * DESC_LH}" font-family="{SANS}" font-size="{DESC}" '
            f'fill="{col}">{escape(ln)}</text>'
        )
    stack = it.get("stack") or []
    if stack:
        cy = 60 + (len(lines) - 1) * DESC_LH + 14
        cx = CARD_PAD
        for s in stack:
            sw = text_w(s, CHIP) + 16
            p.append(f'<rect x="{cx:.1f}" y="{cy}" width="{sw:.1f}" height="20" rx="4" fill="{BG}" stroke="{LINE}"/>')
            p.append(
                f'<text x="{cx + sw / 2:.1f}" y="{cy + 13.5}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="{CHIP}" fill="{INK}">{escape(s)}</text>'
            )
            cx += sw + 6
    p.append("</g>")
    return "".join(p)


def _desc_lines(it: dict, w: float) -> list[tuple[str, str]]:
    """설명 줄과 색. desc 가 배열이면 첫 줄(무엇)은 밝게, 나머지(핵심 기능)는 흐리게."""
    desc = it["desc"]
    if isinstance(desc, str):
        return [(ln, MUTE) for ln in wrap(desc, w - CARD_PAD * 2, DESC)]
    return [(ln, INK if k == 0 else MUTE) for k, part in enumerate(desc) for ln in wrap(part, w - CARD_PAD * 2, DESC)]


def desc_text(it: dict) -> str:
    """그림 설명(alt)용 — 줄을 한 문장으로 잇는다."""
    d = it["desc"]
    return d if isinstance(d, str) else " ".join(d)


def _card_h(it: dict, w: float) -> float:
    n = len(_desc_lines(it, w))
    last = 60 + (n - 1) * DESC_LH
    return last + (14 + 20 + 18 if it.get("stack") else 20)


def ago(when: dt.datetime, now: dt.datetime | None = None) -> str:
    """마지막 push 가 얼마나 지났는지 — today · 3d · 2w · 4mo."""
    days = ((now or dt.datetime.now(dt.timezone.utc)) - when).days
    if days < 1:
        return "today"
    if days < 14:
        return f"{days}d ago"
    if days < 60:
        return f"{days // 7}w ago"
    return f"{days // 30}mo ago"


def cards_private(items: list[dict], pushed: dict[str, dt.datetime] | None = None) -> str:
    """비공개 대표 카드 — 2열. 같은 행 두 장은 높이를 맞춘다.
    pushed 가 있으면 칩에 마지막 작업 시각을 붙인다(● private · 2d ago)."""
    pushed = pushed or {}
    W, GAP = 830, 14
    cw = (W - GAP) / 2
    parts = []
    y = 0.0
    for i in range(0, len(items), 2):
        row = items[i : i + 2]
        h = max(_card_h(it, cw) for it in row)
        for j, it in enumerate(row):
            when = pushed.get(it["title"])
            chip = f"● private · {ago(when)}" if when else "● private"
            parts.append(_card(j * (cw + GAP), y, cw, h, it, chip, MUTE, LINE, SANS))
        y += h + GAP
    H = int(y - GAP + 1)
    label = "built in private — " + ", ".join(it["title"] for it in items)
    return _wrap(W, H, label, "".join(parts), plate=False)


def card_public(it: dict, chip: str, stars: int | None = None, goal: int | None = None) -> str:
    """공개 플러그인 카드. 칩은 coming soon 또는 ★ 스타 수.
    저장소가 공개돼 스타 수를 알면 설명 아래에 목표까지의 막대를 그린다."""
    W = 830
    h = _card_h(it, W)
    bar = ""
    if stars is not None and goal:
        by = h - 6
        label = f"★ {stars} / {goal}"
        lw = text_w(label, CHIP) + 14
        bw = W - CARD_PAD * 2 - lw
        fill = max(6.0, bw * min(stars, goal) / goal)
        bar = (
            f'<defs><linearGradient id="goal" x1="0" x2="1"><stop offset="0" stop-color="{DEEP}"/>'
            f'<stop offset="1" stop-color="{ORANGE}"/></linearGradient></defs>'
            f'<rect x="{CARD_PAD}" y="{by}" width="{bw:.1f}" height="6" rx="3" fill="{LINE}"/>'
            f'<rect x="{CARD_PAD}" y="{by}" width="{fill:.1f}" height="6" rx="3" fill="url(#goal)"/>'
            f'<text x="{W - CARD_PAD}" y="{by + 6.5}" text-anchor="end" font-family="{MONO}" font-size="{CHIP}" '
            f'fill="{ORANGE}">{escape(label)}</text>'
        )
        h += 22
    body = _card(0, 0, W, h, it, chip, ORANGE, "#2a1a10", MONO) + bar
    return _wrap(W, int(h + 1), f'{it["title"]} — {desc_text(it)}', body, plate=False)


# ── 기여 그래프 · 연속 기록 ────────────────────────────────────────
def activity(days: list[tuple[str, int]]) -> str:
    """최근 31일 기여 꺾은선. days 는 (YYYY-MM-DD, count) 오래된 순."""
    W, H = 830, 190
    recent = days[-31:] if days else []
    x0, x1, y0, y1 = 44, 806, 40, 158
    top = max([c for _, c in recent] + [4])
    top = (top + 4) // 5 * 5
    b = [f'<defs><linearGradient id="actg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".35"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient></defs>']
    for g in range(5):
        gy = y0 + (y1 - y0) * g / 4
        b.append(f'<line x1="{x0}" x2="{x1}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="#211c19"/>')
    for v in (0, top // 2, top):
        b.append(f'<text x="{x0 - 10}" y="{y1 - (y1 - y0) * v / top + 4:.1f}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{FAINT}">{v}</text>')
    total = sum(c for _, c in recent)
    b.append(f'<text x="{x0}" y="26" font-family="{MONO}" font-size="11" fill="{MUTE}" letter-spacing="1">CONTRIBUTIONS · LAST 31 DAYS · {total}</text>')
    if len(recent) >= 2:
        n = len(recent)
        pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * c / top) for i, (_, c) in enumerate(recent)]
        line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        b.append(f'<path d="{line} L{x1} {y1} L{x0} {y1} Z" fill="url(#actg)"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-linejoin="round"/>')
        for x, y in pts:
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{INK}"/>')
        for idx in (0, n // 2, n - 1):
            d = recent[idx][0][5:].replace("-", ".")
            anchor = "start" if idx == 0 else "end" if idx == n - 1 else "middle"
            b.append(f'<text x="{pts[idx][0]:.1f}" y="{y1 + 18}" text-anchor="{anchor}" font-family="{MONO}" font-size="10" fill="{FAINT}">{d}</text>')
    return _wrap(W, H, f"contributions in the last 31 days: {total}", "".join(b))


def streak(days: list[tuple[str, int]]) -> str:
    """현재 연속 · 최장 연속 · 1년 활동 일수. 오늘 아직 기여가 없으면 어제부터 센다."""
    counts = [c for _, c in days]
    cur = 0
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    active = sum(1 for c in counts if c > 0)
    show = (lambda v: str(v)) if days else (lambda v: "—")
    b = [
        f'<circle cx="104" cy="80" r="40" fill="none" stroke="{LINE}" stroke-width="6"/>',
        f'<circle cx="104" cy="80" r="40" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" '
        f'stroke-dasharray="{min(cur, 30) / 30 * 251.3:.1f} 251.3" transform="rotate(-90 104 80)"/>',
        f'<text x="104" y="90" text-anchor="middle" font-family="{MONO}" font-size="28" font-weight="800" fill="{INK}">{show(cur)}</text>',
        f'<text x="104" y="146" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{ORANGE}" letter-spacing="1">CURRENT STREAK</text>',
        f'<line x1="208" y1="30" x2="208" y2="140" stroke="{LINE}"/>',
    ]
    for k, (lab, v, col) in enumerate([("LONGEST STREAK", show(longest), LILAC), ("ACTIVE DAYS · 1Y", show(active), INK)]):
        yy = 52 + k * 62
        b.append(f'<text x="232" y="{yy}" font-family="{MONO}" font-size="10" fill="{MUTE}" letter-spacing="1">{lab}</text>')
        b.append(f'<text x="232" y="{yy + 30}" font-family="{MONO}" font-size="24" font-weight="800" fill="{col}">{v}</text>')
    return _wrap(400, 170, f"current streak {cur}, longest {longest}, active days {active}", "".join(b))


LANG_COLORS = [ORANGE, DEEP, VIOLET, LILAC, MUTE, FAINT]


def languages(langs: dict[str, int]) -> str:
    """카드 저장소들의 언어 비율 — 띠 하나와 범례. 상위 5개 + Other."""
    W, H = 830, 120
    x0, x1 = 44, 806
    total = sum(langs.values())
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("Other", rest))
    b = [
        f'<text x="{x0}" y="30" font-family="{MONO}" font-size="11" fill="{MUTE}" letter-spacing="1">LANGUAGES · ACROSS THE CARDS ABOVE</text>',
        f'<clipPath id="lbar"><rect x="{x0}" y="44" width="{x1 - x0}" height="12" rx="6"/></clipPath>',
        f'<rect x="{x0}" y="44" width="{x1 - x0}" height="12" rx="6" fill="{LINE}"/>',
    ]
    if total:
        b.append('<g clip-path="url(#lbar)">')
        x = float(x0)
        for k, (_, v) in enumerate(top):
            w = (x1 - x0) * v / total
            b.append(f'<rect x="{x:.1f}" y="44" width="{max(w - 2, 0.5):.1f}" height="12" fill="{LANG_COLORS[k]}"/>')
            x += w
        b.append("</g>")
        lx = float(x0)
        for k, (name, v) in enumerate(top):
            pct = f"{v / total * 100:.1f}%"
            b.append(f'<circle cx="{lx + 4:.1f}" cy="84" r="4" fill="{LANG_COLORS[k]}"/>')
            b.append(
                f'<text x="{lx + 14:.1f}" y="88" font-family="{MONO}" font-size="11.5" fill="{INK}">{escape(name)}'
                f'<tspan fill="{FAINT}"> {pct}</tspan></text>'
            )
            lx += 14 + text_w(f"{name} {pct}", 11.5) + 22
    label = "languages — " + ", ".join(f"{n} {v / total * 100:.0f}%" for n, v in top) if total else "languages"
    return _wrap(W, H, label, "".join(b))


def weekday(days: list[tuple[str, int]]) -> str:
    """1년 기여를 요일별로 — 월~일 막대 일곱 개. 제일 많은 요일만 주황."""
    W, H = 830, 170
    sums = [0] * 7
    for d, c in days:
        sums[dt.date.fromisoformat(d).weekday()] += c
    top = max(sums) or 1
    names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    x0, x1, base, tall = 44, 806, 140, 92
    slot = (x1 - x0) / 7
    bw = 46
    b = [f'<text x="{x0}" y="26" font-family="{MONO}" font-size="11" fill="{MUTE}" letter-spacing="1">CONTRIBUTIONS BY WEEKDAY · 1Y</text>']
    for k, v in enumerate(sums):
        cx = x0 + slot * k + slot / 2
        hgt = max(3.0, tall * v / top)
        col = ORANGE if v == top and v > 0 else DEEP
        op = "1" if col == ORANGE else ".55"
        b.append(f'<rect x="{cx - bw / 2:.1f}" y="{base - hgt:.1f}" width="{bw}" height="{hgt:.1f}" rx="4" fill="{col}" fill-opacity="{op}"/>')
        b.append(f'<text x="{cx:.1f}" y="{base - hgt - 7:.1f}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{INK if col == ORANGE else MUTE}">{v}</text>')
        b.append(f'<text x="{cx:.1f}" y="{base + 18}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{FAINT}" letter-spacing="1">{names[k]}</text>')
    label = "contributions by weekday — " + ", ".join(f"{n} {v}" for n, v in zip(names, sums))
    return _wrap(W, H, label, "".join(b))


def static_assets() -> dict[str, str]:
    """매번 같은 결과가 나오는 자산."""
    return {
        "section-public.svg": section("PUBLIC", "the one to star"),
        "section-workflow.svg": section("HOW TGX WORKS", "human decides, agents verify"),
        "section-private.svg": section("BUILT IN PRIVATE", "code stays home", VIOLET),
        "section-graph.svg": section("COMMITS", "private ones included"),
        "workflow.svg": workflow(),
        "portfolio.svg": portfolio_button(),
        "footer.svg": footer(),
    }
