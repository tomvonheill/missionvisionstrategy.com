// Pure helpers for Insights posts. No astro:content imports, so `node --test` can load this file.
export type PostLike = { id: string; data: { pubDate: Date; draft: boolean } }

export function isVisible(data: { draft: boolean }, includeDrafts: boolean): boolean {
  return includeDrafts || !data.draft
}

export function newestFirst<T extends PostLike>(posts: readonly T[]): T[] {
  return [...posts].sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime() || a.id.localeCompare(b.id),
  )
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' })
}
