# Mission Vision Strategy website

The website for **Mission Vision Strategy** (www.missionvisionstrategy.com), Kennen Hutchison's
Chicago-based organizational strategy practice. Built with [Astro](https://astro.build): pages
are `.astro` files, posts are Markdown, and Cloudflare Pages builds and publishes the site.

## The rules

1. **Always work on the `dev` branch. Never commit to `main`** (it only accepts pull requests).
2. **Publishing = merging the "Publish to the live site" pull request** (`dev` → `main`). It is
   opened automatically after every push to `dev`. Wait for **check** to be green, then merge
   with "Create a merge commit" (not squash, not rebase).
3. **Don't change infrastructure:** `.github/`, `package.json`, `package-lock.json`,
   `astro.config.mjs`, `tsconfig.json`, `.nvmrc`, `public/admin/`, `scripts/`. The **check** fails if you do.
   Ask Tom instead.

| Branch | Site | Who sees it |
|---|---|---|
| `dev` | https://dev.missionvisionstrategy.com | Preview, hidden from search engines; shows drafts |
| `main` | https://www.missionvisionstrategy.com | The real site |

## What's where

```
src/
  pages/            index.astro (home), services.astro, approach.astro, 404.astro
  pages/insights/   Insights list + post pages (generated from the posts; don't edit per post)
  layouts/          Base.astro (every page: head, header, contact band, footer), Post.astro
  components/       Header.astro (nav), Footer.astro, ContactBand.astro
  lib/              nav.ts (which nav link is "current"), insights.ts (which posts are visible)
  content/insights/ one folder per post: <slug>/index.md, with its images beside it
  styles/           global.css (all site styling), prose.css (Insights)
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

## Insights posts

- The easiest way is the admin at https://www.missionvisionstrategy.com/admin/ (sign in with
  GitHub). It saves to `dev`. New posts start as a Draft.
- By hand / with Claude: create `src/content/insights/<slug>/index.md`, where `<slug>` is
  lowercase-with-dashes (plain ASCII) and becomes the URL `/insights/<slug>/`. Front matter:

```yaml
---
title: "Post title"
description: "One or two sentences for the list and search results."
pubDate: 2026-11-12
updatedDate: 2026-12-01      # optional
heroImage: ./hero.jpg        # optional, file sits next to index.md
heroAlt: "What the image shows"   # required when heroImage is set
draft: true                  # true = dev site only; set false to publish
---
```

- Styled in posts: `##`/`###` headings, paragraphs, bold/italic, links, bulleted and numbered
  lists, `>` blockquotes, images (`![description](./photo.jpg)`), tables, `---` divider.
  No HTML or components inside posts.
- Images: ≤ ~500 KB, `.jpg`/`.webp` for photos, always meaningful alt text. Astro resizes them.
  Images uploaded in the admin editor are saved in the post's own folder.
- The Insights nav link and pages appear automatically once at least one post has `draft: false`.
- `src/content/insights/sample-post/` is a draft showing every element; leave it or delete it.

## Checking your work locally (optional)

Needs Node 22.23.4 or newer (see `.nvmrc`).

```bash
npm install
npm run dev          # http://localhost:4321, shows drafts
npm test && npm run build
```
