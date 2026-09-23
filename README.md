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

- `main` is protected: changes land through PRs, the `check` workflow must pass, and code-owner
  review applies. Admins can bypass.
- `dev` accepts direct pushes but can't be deleted or force-pushed. The repo allows merge commits
  only, so `dev` and `main` don't drift apart after a `dev` → `main` merge.
- `.github/CODEOWNERS` gives Tom everything **except** `site/`, which has no owner. So Kennen can
  merge site-only PRs himself, and anything else needs Tom's review.
- The `check` workflow (`.github/workflows/check.yml`) fails any PR by someone other than
  `tomvonheill` that touches files outside `site/`, validates HTML with `html-validate`, and checks
  internal links with `.github/scripts/check_links.py`.
