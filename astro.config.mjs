// missionvisionstrategy.com — static Astro site, published by Cloudflare Pages (dist/).
// Pages build to /<path>/index.html and are linked with a trailing slash.
import sitemap from '@astrojs/sitemap'
import { defineConfig } from 'astro/config'

export default defineConfig({
  site: 'https://www.missionvisionstrategy.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
})
