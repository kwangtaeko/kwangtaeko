<!--
  이 파일이 README 의 원본이다. README.md 는 .github/scripts/update_readme.py 가
  6시간마다 이 파일로 다시 쓰므로 README.md 를 직접 고치면 덮어써진다.

  자리표시:
    {{asset:파일명}}  assets/ 의 파일을 내용 해시가 붙은 raw 주소로 (캐시 무력화)
    {{PUBLIC}}        .github/repos.json 의 public — 스타 수를 조회해 카드로
    {{PRIVATE}}       .github/repos.json 의 private — 2열 카드
    {{MORE}}          비공개 저장소 나머지 개수
    {{SYNC}}          마지막 갱신 날짜
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

{{PRIVATE}}

<p align="center"><sub>+{{MORE}} more in private · 아키텍처와 설계 결정은 <a href="https://tonygwangsk.dev">tonygwangsk.dev</a> 에</sub></p>

<p align="center">
  <a href="https://tonygwangsk.dev"><img height="34" src="{{asset:portfolio.svg}}" alt="portfolio — tonygwangsk.dev" /></a>
</p>

<br/>

<img width="100%" src="{{asset:section-graph.svg}}" alt="commits — private ones included" />

<p align="center">
  <img height="170" src="{{asset:stat-tiles.svg}}" alt="TGX stats" />
  <img height="170" src="https://streak-stats.demolab.com?user=kwangtaeko&hide_border=true&background=100E0D&ring=FB923C&fire=FB923C&currStreakLabel=FB923C&currStreakNum=F2E9E3&sideNums=F2E9E3&sideLabels=A99A90&dates=6F625A&stroke=332B26" alt="streak" />
</p>

<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=kwangtaeko&bg_color=100E0D&color=A99A90&title_color=A99A90&line=FB923C&point=F2E9E3&area=true&area_color=FB923C&hide_border=true&radius=10" alt="contribution graph" />

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-light.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/kwangtaeko/kwangtaeko/output/snake-dark.svg" width="100%" />
</picture>

<p align="center"><sub><img src="{{asset:star.svg}}" height="11" alt="star" /> 카드 · 스타 수 · 히어로는 GitHub Actions 가 6시간마다 다시 그립니다 · last sync: <code>{{SYNC}}</code></sub></p>

<img width="100%" src="{{asset:footer.svg}}" alt="TGX" />
