# missionvisionstrategy.com

Astro site for [Mission Vision Strategy](https://www.missionvisionstrategy.com), published by
Cloudflare Pages. Detailed editing guide (also read by Claude): [CLAUDE.md](CLAUDE.md).

## Making edits

The recommended flow: changes go to the **dev** site first, then you publish them. Everything in
this repo is yours to change: pages, styles, dependencies, and workflows.

### One-time setup for Claude
In Claude, connect GitHub and give it access to `tomvonheill/missionvisionstrategy.com`. Claude
reads [CLAUDE.md](CLAUDE.md) for the house style and how this repo works.

### Change a page, the layout, or the design (with Claude)
1. In Claude (with the GitHub connector on this repository), describe the change, e.g.
   "On the Services page, add a fifth service called …". Say **"work on the dev branch"**.
2. Claude commits to `dev`; about a minute later check https://dev.missionvisionstrategy.com.
3. Ask Claude for adjustments until it looks right.
4. Publish (below).

### Edit files yourself (optional)
1. `git checkout dev && git pull`, edit, then `npm install && npm run dev` to preview locally
   (Node 22.23.4 or newer, see `.nvmrc`).
2. `git commit` and `git push origin dev` → the dev site updates.
3. Publish (below).

### Publish to the live site
1. On GitHub, open **Pull requests → "Publish to the live site"** (it's created automatically
   whenever `dev` has something new).
2. Check the list of changes and wait for **check** to turn green. If it's red, open it to see
   why (or ask Claude to fix it on `dev`; the PR updates itself).
3. Click **Merge pull request** → **Create a merge commit** (not squash or rebase) → confirm.
   The live site updates in about a minute. Leave the `dev` branch in place.

### Small urgent fix
You can commit straight to `main`; it goes live in about a minute with no preview. Afterwards
merge `main` into `dev` (PR `main` → `dev`) so `dev` doesn't fall behind.

## How it's hosted

Tom manages the hosting outside the repo: the two Cloudflare Pages projects and their build
settings, and DNS.

| Pages project | Branch | Domain | Build |
|---|---|---|---|
| `missionvisionstrategy-com` | `main` | www.missionvisionstrategy.com | `npm run build` → `dist` |
| `missionvisionstrategy-dev` | `dev` | dev.missionvisionstrategy.com | `npm run build` → `dist` |

- Node version from `.nvmrc`. Build settings live in Cloudflare, not this repo.
- **Before bumping Node in `.nvmrc`,** make sure Cloudflare's build image knows that version: it
  lags new Node releases by days or weeks (22.23.5 failed with "definition not found", so we pin
  22.23.4). An unknown version fails the build and the site stays on its last good version.
- **DNS stays at GoDaddy** (Kennen's account): `www` → `missionvisionstrategy-com.pages.dev`,
  `dev` → `missionvisionstrategy-dev.pages.dev`, bare domain forwards (301) to www. Email records
  (Google Workspace MX, verification TXT, DMARC) are left alone.
- `public/_headers` sends `X-Robots-Tag: noindex` on the dev domain; `public/_redirects` maps
  the old `.html` URLs.
- The repo setting **Settings → Actions → General → "Allow GitHub Actions to create and approve
  pull requests"** must be on, or the Publish PR workflow can't open the pull request.

## Checks and safety net

- `check` (`.github/workflows/check.yml`) runs on PRs and pushes to `main`/`dev`: `astro check`,
  the build, HTML validation, and the internal link check. It is a helpful build check, not a gate.
- A failed Cloudflare build leaves the previous live version up, so a broken change doesn't take
  the site down. Check the dev site and the `check` run.
- `main` and `dev` can't be force-pushed or deleted (protects history). Direct pushes to `main`
  are allowed. Publish with merge commits.
- `publish-pr` (`.github/workflows/publish-pr.yml`) keeps the "Publish to the live site" PR open
  and its description current.
- The repo holds no secrets.
