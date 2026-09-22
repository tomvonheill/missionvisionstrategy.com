# Mission Vision Strategy website

The website for **Mission Vision Strategy** (www.missionvisionstrategy.com), Kennen Hutchison's
Chicago-based organizational strategy practice. Plain HTML and CSS: no build step, no framework,
no JavaScript. What's in `site/` is exactly what gets published.

## The one rule

**Only edit files inside `site/`.** Everything else (`.github/`, this file, the README) is
infrastructure. A pull request that changes anything outside `site/` fails its checks and needs
Tom to review it.

## How changes go live

1. Make a branch, edit files in `site/`, and open a pull request.
2. Two things happen automatically on the PR:
   - The **`check`** job validates the HTML and makes sure every internal link and image
     exists. It must be green before you can merge.
   - **Cloudflare Pages** comments with a **preview link**. Open it to see your change as it
     will look live.
3. Merge the PR. The live site updates within about a minute.

## What's where

```
site/
  index.html      home page: hero, who we work with, services overview, numbers, about, contact
  services.html   the four services in detail (anchors: #assessment #planning #operations #research)
  approach.html   Mission / Vision / Strategy / Follow-through
  styles.css      all styling, one file
  images/         star.svg (the red Chicago star, also the favicon), skyline.svg
```

The header (`<header class="site-header">`), footer (`<footer class="site-footer">`), and
contact band (`<section class="contact">`) are copied on every page. **When you change one, change
it on all three pages.** In the nav, the current page's link carries `aria-current="page"`.

## House style

- **Chicago flag palette**, defined as variables at the top of `styles.css`: navy `--navy`,
  light blue `--flag-blue`, star red `--star-red`. Use the variables rather than new colors.
- The red six-pointed star (`images/star.svg`) is the brand mark. Use it as the small marker in
  eyebrow labels and lists, as the existing pages do.
- Headings use Barlow Condensed and body text uses Inter (loaded from Google Fonts in each page's
  `<head>`).
- Copy is plain and direct: short sentences, no jargon.
- Reuse the existing building blocks before inventing new ones: `.section`, `.section-warm`,
  `.section-head`, `.eyebrow`, `.cards`/`.card`, `.stats`, `.split`, `.work-list`, `.quote`,
  `.service`, `.steps`, `.contact`, `.button`, `.button-ghost`.

## Adding things

- **A new page:** copy an existing page such as `approach.html`, keep its `<head>`, header,
  contact band, and footer, then add a link to it in the nav on **every** page.
- **Images:** put them in `site/images/`, keep them reasonably small (under ~500 KB; export
  photos as `.jpg` or `.webp`), and always give `<img>` an `alt` description (`alt=""` only for
  purely decorative images).
- **Links between pages** are relative, like `services.html#planning`. The check fails if a link
  points at a file that doesn't exist.

## Checking your work locally (optional)

```bash
npx --yes html-validate@9 "site/**/*.html"
python3 .github/scripts/check_links.py site
python3 -m http.server -d site 8000   # then open http://localhost:8000
```
