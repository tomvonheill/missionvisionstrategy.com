# missionvisionstrategy.com

Astro site for [Mission Vision Strategy](https://www.missionvisionstrategy.com), published by
Cloudflare Pages. Detailed editing guide (also read by Claude): [CLAUDE.md](CLAUDE.md).

## Making edits

Every change goes to the **dev** site first, then you publish it.

### Write or edit an Insights post (no code)
1. Go to https://www.missionvisionstrategy.com/admin/ and **Sign in with GitHub**.
2. **Insights → New Post.** Fill in title, summary, date, body (and a hero image + description
   if you like). New posts start with **Draft** on; leave it on for now.
3. **Save.** About a minute later it appears on https://dev.missionvisionstrategy.com/insights/
   marked "Draft".
4. When you're happy, open the post again, turn **Draft** off, and **Save**.
5. Publish (below).

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

## How it's hosted

| Pages project | Branch | Domain | Build | Env |
|---|---|---|---|---|
| `missionvisionstrategy-com` | `main` | www.missionvisionstrategy.com | `npm run build` → `dist` | — |
| `missionvisionstrategy-dev` | `dev` | dev.missionvisionstrategy.com | `npm run build` → `dist` | `PUBLIC_SITE_ENV=dev` (shows drafts) |

- Node version from `.nvmrc`. Build settings live in Cloudflare, not this repo.
- **DNS stays at GoDaddy** (Kennen's account): `www` → `missionvisionstrategy-com.pages.dev`,
  `dev` → `missionvisionstrategy-dev.pages.dev`, bare domain forwards (301) to www. Email records
  (Google Workspace MX, verification TXT, DMARC) are left alone.
- `public/_headers` sends `X-Robots-Tag: noindex` on the dev domain; `public/_redirects` maps
  the old `.html` URLs.
- The repo setting **Settings → Actions → General → "Allow GitHub Actions to create and approve
  pull requests"** must be on, or the Publish PR workflow can't open the pull request.
- **/admin sign-in:** Cloudflare Worker `mvs-cms-auth` (https://mvs-cms-auth.tvh92.workers.dev,
  Tom's Cloudflare account; source: sveltia/sveltia-cms-auth) + GitHub OAuth App
  "Mission Vision Strategy CMS" (Tom's GitHub). Worker secrets: `GITHUB_CLIENT_ID`,
  `GITHUB_CLIENT_SECRET`; `ALLOWED_DOMAINS=www.missionvisionstrategy.com, dev.missionvisionstrategy.com`.
  Only GitHub users with write access to this repo can save.

## Guardrails

- `main` accepts pull requests only (ruleset; Tom can bypass); `check` must pass. No force-push
  or delete on `main` or `dev`. Publish with merge commits only.
- `check` (`.github/workflows/check.yml`) runs on PRs and pushes to `main`/`dev`: an
  infrastructure-path guard, `astro check`, unit tests, dev and live builds, HTML validation,
  internal link check, and an Insights presence/absence check. The guard judges each commit by
  its author: commits by Tom (his GitHub noreply identity) may change infrastructure paths;
  anyone else's commits (including edits made inside merge commits) that touch them fail `check`.
- `publish-pr` (`.github/workflows/publish-pr.yml`) keeps the "Publish to the live site" PR open
  and its description current.
- `.github/CODEOWNERS` gives Tom the infrastructure paths. The repo holds no secrets.
