<!-- 이 파일은 자동 생성된다. 고칠 곳은 .github/README.template.md 와 .github/repos.json -->

<p align="center">
  <img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/hero.svg?v=3897e5cb" alt="TGX — Agents, leading what's next." />
</p>

<img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/section-public.svg?v=67865fff" alt="public — the one to star" />

<table>
  <tr>
    <td width="100%" valign="top">
      <b><code>tgx-agent-mash</code></b>&nbsp;<img src="https://img.shields.io/badge/%E2%98%85-soon-332B26?style=flat&labelColor=100E0D" alt="coming soon" /><br/>
      <sub>특정 도구에 묶이지 않는 범용 에이전트 플러그인.</sub>
    </td>
  </tr>
</table>

<br/>

<img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/section-workflow.svg?v=f14a534b" alt="how TGX works — human decides, agents verify" />

<p align="center">
  <img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/workflow.svg?v=a2a6613d" alt="TGX workflow — a human decides; the main model (Claude Code or Codex) runs a team-leader, five execution agents and four verification agents; the other model cross-checks and reports back" />
</p>

<p align="center"><sub>에이전트 13개짜리 전체 구성도는 <a href="https://tonygwangsk.dev/projects">tonygwangsk.dev/projects</a> 의 Orchestra 에</sub></p>

<br/>

<img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/section-private.svg?v=583cd3e7" alt="built in private — code stays home" />

<table>
  <tr>
    <td width="50%" valign="top">
      <b>TG Platform</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>저장소 간 개발 표준의 정본. RFC 9457 오류 계약을 패키지로 배포하고, requestId · traceId · 구조화 로그를 기본으로 주는 Spring Boot Starter까지.</sub><br/>
      <sub><code>Spring Boot</code> <code>RFC 9457</code> <code>ADR ×5</code></sub>
    </td>
    <td width="50%" valign="top">
      <b>TGX Agent Chatbot</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>로컬 Ollama 위의 에이전트형 RAG 를 어느 사이트에나 위젯으로 붙이는 범용 챗봇으로 키웠다. 멀티 테넌트 · 가드레일 · BM25 + 벡터 하이브리드 · 런북 9종.</sub><br/>
      <sub><code>FastAPI</code> <code>LangGraph</code> <code>OpenTelemetry</code></sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>TG-Nova</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>송금 · 페이 · 투자가 한 원장을 공유하는 핀테크 백엔드. 잔액은 저장하지 않고 원장에서 도출한다.</sub><br/>
      <sub><code>Kotlin</code> <code>Spring Boot</code> <code>jOOQ</code></sub>
    </td>
    <td width="50%" valign="top">
      <b>시장장터</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>도매와 구매업주를 잇는 B2B 마켓. 브랜드 · 본사 · 매장 3층 멀티테넌시와 Outbox 비동기. 친구들과 함께, PM 은 내가.</sub><br/>
      <sub><code>Spring Boot</code> <code>Next.js</code> <code>Expo</code></sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>네오뮤직</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>실용음악 학원 예약 앱. 연습실 예약과 레슨 일정을 한곳에서 잡는다. 설치 없는 PWA 로, 엣지에서 돈다.</sub><br/>
      <sub><code>Next.js</code> <code>Cloudflare Workers</code> <code>Neon</code></sub>
    </td>
    <td width="50%" valign="top">
      <b>TG Launcher</b>&nbsp;<img src="https://img.shields.io/badge/%E2%97%8F-private-332B26?style=flat&labelColor=100E0D" alt="private" /><br/>
      <sub>배포한 TG 사이트들로 들어가는 단 하나의 문. 허용된 구글 계정 + TOTP 2단계 인증을 통과해야 열리고, 보호 사이트에는 서명 토큰으로 SSO. 누가 들어오면 폰으로 웹푸시.</sub><br/>
      <sub><code>Next.js 16</code> <code>Auth.js</code> <code>TOTP</code></sub>
    </td>
  </tr>
</table>

<p align="center"><sub>+12 more in private · 아키텍처와 설계 결정은 <a href="https://tonygwangsk.dev">tonygwangsk.dev</a> 에</sub></p>

<p align="center">
  <a href="https://tonygwangsk.dev"><img height="34" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/portfolio.svg?v=ac4634a8" alt="portfolio — tonygwangsk.dev" /></a>
</p>

<br/>

<img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/section-graph.svg?v=7e6b280d" alt="commits — private ones included" />

<p align="center">
  <img height="170" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/stat-tiles.svg?v=df4f39e9" alt="TGX stats" />
  <img height="170" src="https://streak-stats.demolab.com?user=kwangtaeko&hide_border=true&background=100E0D&ring=FB923C&fire=FB923C&currStreakLabel=FB923C&currStreakNum=F2E9E3&sideNums=F2E9E3&sideLabels=A99A90&dates=6F625A&stroke=332B26" alt="streak" />
</p>

<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=kwangtaeko&bg_color=100E0D&color=A99A90&title_color=A99A90&line=FB923C&point=F2E9E3&area=true&area_color=FB923C&hide_border=true&radius=10" alt="contribution graph" />

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-light.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" width="100%" />
</picture>

<p align="center"><sub><img src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/star.svg?v=f94ae67b" height="11" alt="star" /> 카드 · 스타 수 · 히어로는 GitHub Actions 가 6시간마다 다시 그립니다 · last sync: <code>2026-10-02</code></sub></p>

<img width="100%" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/main/assets/footer.svg?v=431ac485" alt="TGX" />
