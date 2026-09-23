# missionvisionstrategy.com

Static site for [Mission Vision Strategy](https://www.missionvisionstrategy.com). Plain HTML/CSS
in `site/`, published by Cloudflare Pages. Content editing guide: [CLAUDE.md](CLAUDE.md).

## How it's hosted

Two **Cloudflare Pages** projects build this same repo, both with no build command and output
directory `site`. Build settings live in the Cloudflare dashboard, not in this repo.

| Project | Production branch | Custom domain | Notes |
|---|---|---|---|
| `missionvisionstrategy-com` | `main` | www.missionvisionstrategy.com | Also builds a preview for every PR/branch and comments the link |
| `missionvisionstrategy-dev` | `dev` | dev.missionvisionstrategy.com | Previews and PR comments off; exists only to put `dev` on a custom domain |

Two projects because Pages attaches custom domains to a project's production branch; with DNS
outside Cloudflare, a branch can't get its own custom domain any other way.
`site/_headers` sends `X-Robots-Tag: noindex` on the dev domain.

**DNS stays at GoDaddy** (Kennen's account): `www` → `missionvisionstrategy-com.pages.dev`, `dev` →
`missionvisionstrategy-dev.pages.dev`, and the bare domain uses GoDaddy domain forwarding (301) to
`https://www.missionvisionstrategy.com`. The email records (Google Workspace MX,
site-verification TXT, DMARC) are deliberately left alone.

## Guardrails

- `main` and `dev` both accept direct pushes from collaborators, but neither can be force-pushed or
  deleted. The repo allows merge commits only, so `dev` and `main` don't drift apart.
- The `check` workflow (`.github/workflows/check.yml`) runs on every push to `main` and on every PR.
  On PRs it fails any change by someone other than `tomvonheill` that touches files outside
  `site/`. It validates HTML with `html-validate` and checks internal links with
  `.github/scripts/check_links.py`. On direct pushes it reports but can't block; a required check
  would block direct pushes entirely.
- `.github/CODEOWNERS` gives Tom everything except `site/`. It only takes effect on PRs, since direct
  pushes skip review.
- Cloudflare Pages only publishes `site/`, and the repo holds no secrets.
