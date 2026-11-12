import { type CollectionEntry, getCollection } from 'astro:content'
import { isVisible, newestFirst } from './posts.ts'

// Drafts show under `astro dev` and on the dev site (Pages project sets PUBLIC_SITE_ENV=dev).
export const includeDrafts: boolean = import.meta.env.DEV || import.meta.env.PUBLIC_SITE_ENV === 'dev'

export async function getVisiblePosts(): Promise<CollectionEntry<'insights'>[]> {
  return newestFirst(await getCollection('insights', ({ data }) => isVisible(data, includeDrafts)))
}

export async function hasVisiblePosts(): Promise<boolean> {
  return (await getVisiblePosts()).length > 0
}
