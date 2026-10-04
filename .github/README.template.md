<!--
  이 파일이 README 의 원본이다. README.md 는 .github/scripts/update_readme.py 가
  6시간마다 이 파일로 다시 쓰므로 README.md 를 직접 고치면 덮어써진다.

  자리표시:
    {{asset:파일명}}  assets/ 의 파일을 내용 해시가 붙은 raw 주소로 (캐시 무력화)
    {{PUBLIC}}        공개 플러그인 카드 그림(저장소가 공개되면 링크로 감싸짐)
    {{MORE}}          비공개 저장소 나머지 개수

  카드 · 꺾은선 · 연속 기록은 전부 assets/ 의 SVG 다. GitHub 은 README 의 색과
  글꼴을 지우므로 HTML 표로는 디자인을 맞출 수 없어 그림으로 그린다.
-->

<p align="center">
  <img width="100%" src="{{asset:hero.svg}}" alt="TGX — Agents, leading what's next." />
</p>

<img width="100%" src="{{asset:section-public.svg}}" alt="public — the one to star" />

{{PUBLIC}}

<br/>

<img width="100%" src="{{asset:section-workflow.svg}}" alt="how TGX works — human decides, agents verify" />

<p align="center">
  <img width="100%" src="{{asset:workflow.svg}}" alt="TGX workflow — a human decides; the main model (Claude Code or Codex) runs a team-leader, five execution agents and four verification agents; the other model cross-checks and reports back" />
</p>

<p align="center"><sub>에이전트 13개짜리 전체 구성도는 <a href="https://tonygwangsk.dev/projects">tonygwangsk.dev/projects</a> 의 Orchestra 에</sub></p>

<br/>

<img width="100%" src="{{asset:section-private.svg}}" alt="built in private — code stays home" />

<p align="center">
  <img width="100%" src="{{asset:cards-private.svg}}" alt="built in private — TG Platform, TGX Agent Chatbot, TG-Nova, 시장장터, 네오뮤직, TG Launcher" />
</p>

<p align="center"><sub>+{{MORE}} more in private · 아키텍처와 설계 결정은 <a href="https://tonygwangsk.dev">tonygwangsk.dev</a> 에</sub></p>

<p align="center">
  <a href="https://tonygwangsk.dev"><img height="34" src="{{asset:portfolio.svg}}" alt="portfolio — tonygwangsk.dev" /></a>
</p>

<br/>

<img width="100%" src="{{asset:section-graph.svg}}" alt="commits — private ones included" />

<p align="center">
  <img height="170" src="{{asset:stat-tiles.svg}}" alt="TGX stats" />
  <img height="170" src="{{asset:streak.svg}}" alt="streak" />
</p>

<img width="100%" src="{{asset:activity.svg}}" alt="contributions in the last 31 days" />

<img width="100%" src="{{asset:languages.svg}}" alt="languages across the private cards" />

<img width="100%" src="{{asset:weekday.svg}}" alt="contributions by weekday over the last year" />

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-light.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" width="100%" />
</picture>

<img width="100%" src="{{asset:footer.svg}}" alt="TGX" />
