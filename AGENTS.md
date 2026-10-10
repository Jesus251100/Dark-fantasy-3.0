# AGENTS.md

## What this is

Dark-fantasy-themed bingo game. Vue 3 + TypeScript + Vite 8 + Pinia 3 + Vue Router 5. Client-side only, no backend. All UI text is in **Spanish**.

## Commands

```sh
npm install          # deps
npm run dev          # vite dev server (port 5173)
npm run build        # type-check + production build (runs vue-tsc --build && vite build in parallel)
npm run type-check   # vue-tsc --build only
npm run lint         # runs oxlint --fix then eslint --fix sequentially (run-s)
npm run lint:oxlint  # oxlint alone
npm run lint:eslint  # eslint alone
npm run format       # prettier on src/
```

Lint order matters: `oxlint` runs first, then `eslint`. Both use `--fix`.

**Build verification order:** `npm run lint && npm run type-check` (no test suite exists).

## Key architecture

- `src/game/` — Pure game logic (bingo engine, AI bots, win patterns). **No Vue deps** — safe to modify independently.
- `src/composables/` — `useBingoGame.ts` (reactive game state machine) and `useBingoBots.ts` (AI opponents). These are the core runtime.
- `src/views/` — 24 page components. Each level view is a self-contained ~500-900 line SFC.
- `src/stores/` — Only a boilerplate counter store (`counter.ts`). **Not used.** All game state lives in composables.
- `src/router/index.ts` — 26 flat routes, no guards, no lazy loading, all eager imports.
- `src/components/` — `BossCard`, `VictoryChallengeOverlay`, `MethodPatternPreview`, `NextLevelButton`, `AppSidebar`.

## Level system

10 levels with increasing difficulty. Each level view configures `useBingoGame` + `useBingoBots` differently. **Level 10** is a 3-phase boss fight using `reconfigure()` to hot-swap card sizes and win modes mid-session.

Win patterns (`game/bingo.ts`): `row`, `column`, `diagonal`, `L`, `O`, `plus`, `T`, `arrow`, `H`, `zigzag`, `full` (blackout), `crown`.

## TypeScript config

Two tsconfigs via project references:
- `tsconfig.app.json` — app code (`src/`). Extends `@vue/tsconfig/tsconfig.dom.json`. `noUncheckedIndexedAccess: true`.
- `tsconfig.node.json` — tooling files (vite.config, eslint.config, etc.). Extends `@tsconfig/node24`.

Path alias: `@/` maps to `src/`.

## Linting & formatting

- **oxlint** (`.oxlintrc.json`): plugins `eslint`, `typescript`, `unicorn`, `oxc`, `vue`. Category `correctness` = error.
- **eslint** (`eslint.config.ts`): Vue essential + TypeScript recommended. Ignores `dist/`, `dist-ssr/`, `coverage/`.
- **prettier** (`.prettierrc.json`): no semicolons, single quotes, 100 char width.
- **editorconfig**: 2-space indent, LF line endings, `trim_trailing_whitespace`.

## Gotchas

- Auth is mocked via `sessionStorage` (keys `df_user_role`, `df_logged_in`). Mock verification code is `123456`.
- Shop/booster state stored in `sessionStorage` as JSON under `df_boosters`.
- Profile data (coins, diamonds, XP) is hardcoded in `LobbyView.vue`.
- No test suite. No CI workflows.
- Node engine: `^20.19.0 || >=22.12.0`.
- `scripts/` folder contains one-off Python/MJS patch scripts — not part of the build.
