import rss from '@astrojs/rss'
import type { APIContext, GetStaticPaths } from 'astro'
import { getVisiblePosts } from '../../lib/insights'

// Emitted only when there is at least one visible post.
export const getStaticPaths = (async () =>
  (await getVisiblePosts()).length ? [{ params: { feed: 'rss.xml' } }] : []) satisfies GetStaticPaths

export async function GET(context: APIContext) {
  const posts = await getVisiblePosts()
  return rss({
    title: 'Mission Vision Strategy — Insights',
    description: 'Notes on strategy, planning, and operations for mission-driven organizations.',
    site: context.site ?? 'https://www.missionvisionstrategy.com',
    items: posts.map((p) => ({ title: p.data.title, description: p.data.description, pubDate: p.data.pubDate, link: `/insights/${p.id}/` })),
  })
}
