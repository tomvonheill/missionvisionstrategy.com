# missionvisionstrategy.com

Static site for [Mission Vision Strategy](https://www.missionvisionstrategy.com). Plain HTML/CSS
in `site/`, published by Cloudflare Pages. Content editing guide: [CLAUDE.md](CLAUDE.md).

## How it's hosted

- **Cloudflare Pages** project `missionvisionstrategy`, connected to this repo. Production branch
  `main`, no build command, output directory `site`. Every PR gets a preview deployment. Build
  settings live in the Cloudflare dashboard, not in this repo.
- **DNS stays at GoDaddy** (Kennen's account). `www` is a CNAME to
  `missionvisionstrategy.pages.dev`; the bare domain uses GoDaddy domain forwarding (301) to
  `https://www.missionvisionstrategy.com`. The email records (Google Workspace MX,
  site-verification TXT, DMARC) are GoDaddy's and are deliberately left alone.

## Guardrails

- `main` is protected: changes land through PRs, the `check` workflow must pass, and code-owner
  review applies. Admins can bypass.
- `.github/CODEOWNERS` gives Tom everything **except** `site/`, which has no owner. So Kennen can
  merge site-only PRs himself, and anything else needs Tom's review.
- The `check` workflow (`.github/workflows/check.yml`) fails any PR by someone other than
  `tomvonheill` that touches files outside `site/`, validates HTML with `html-validate`, and checks
  internal links with `.github/scripts/check_links.py`.
