# Mission Vision Strategy website

The website for **Mission Vision Strategy** (www.missionvisionstrategy.com), Kennen Hutchison's
Chicago-based organizational strategy practice. Built with [Astro](https://astro.build): pages
are `.astro` files, and Cloudflare Pages builds and publishes the site.

## How we work

1. **Recommended flow: work on the `dev` branch**, preview it on
   https://dev.missionvisionstrategy.com, then publish.
2. **Publishing = merging the "Publish to the live site" pull request** (`dev` → `main`). It is
   opened automatically after every push to `dev`. Wait for **check** to be green, then merge
   with "Create a merge commit" (not squash, not rebase).
3. **Small urgent fix?** You can commit straight to `main`; it goes live in about a minute with
   no preview. Afterwards merge `main` into `dev` (PR `main` → `dev`) so `dev` doesn't fall behind.

Everything in this repo is Kennen's to change: pages, styles, dependencies, and
workflows. A failed Cloudflare build leaves the previous live
version up, so a broken change doesn't take the site down. Check the dev site and the **check**
run on GitHub to catch problems. Only force-push and deleting `main` or `dev` are blocked, to
protect history.

Tom manages the hosting outside the repo: the two Cloudflare Pages projects (build settings)
and DNS. Ask him if one of those needs to change.

| Branch | Site | Who sees it |
|---|---|---|
| `dev` | https://dev.missionvisionstrategy.com | Preview, hidden from search engines |
| `main` | https://www.missionvisionstrategy.com | The real site |

## What's where

```
src/
  pages/            index.astro (home), services.astro, approach.astro, 404.astro
  layouts/          Base.astro (every page: head, header, contact band, footer)
  components/       Header.astro (nav), Footer.astro, ContactBand.astro
  lib/              nav.ts (which nav link is "current")
  styles/           global.css (all site styling)
public/images/      star.svg, skyline.svg, other site images
```

- Header, footer and contact band exist **once** (in `components/`). Each page passes its own
  contact heading/text to `<Base>`.
- New nav link: edit `src/components/Header.astro`. If it is a new page, also add its name to
  the `Current` type in `src/lib/nav.ts` and pass `current="<name>"` to `<Base>` on that page.
- New page: copy `src/pages/approach.astro` to `src/pages/<name>.astro` (URL becomes `/<name>/`),
  then add it to the nav in `Header.astro` as above.
- Links are absolute with a trailing slash: `/services/#planning`, `/approach/`, `/#contact`.

## House style

- **Chicago flag palette**, defined as variables at the top of `src/styles/global.css`: navy `--navy`,
  light blue `--flag-blue`, star red `--star-red`. Use the variables rather than new colors.
- The red six-pointed star (`/images/star.svg`) is the brand mark. Use it as the small marker in
  eyebrow labels and lists, as the existing pages do.
- Headings use Barlow Condensed and body text uses Inter (loaded in `Base.astro`).
- Copy is plain and direct: short sentences, no jargon.
- Reuse the existing building blocks before inventing new ones: `.section`, `.section-warm`,
  `.section-head`, `.eyebrow`, `.cards`/`.card`, `.stats`, `.split`, `.work-list`, `.quote`,
  `.service`, `.steps`, `.contact`, `.button`, `.button-ghost`.

## Checking your work locally (optional)

Needs Node 22.23.4 or newer (see `.nvmrc`).

```bash
npm install
npm run dev          # http://localhost:4321
npm run build
```
