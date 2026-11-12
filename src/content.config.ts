import { defineCollection } from 'astro:content'
import { glob } from 'astro/loaders'
import { z } from 'astro/zod'

// One folder per post: src/content/insights/<slug>/index.md, images beside it.
// The CMS (public/admin/config.yml) writes exactly these fields — keep the two in sync.
const insights = defineCollection({
  loader: glob({
    pattern: '*/index.md',
    base: './src/content/insights',
    generateId: ({ entry }) => entry.split('/')[0] ?? entry,
  }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        description: z.string(),
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        heroImage: image().optional(),
        heroAlt: z.string().optional(),
        draft: z.boolean().default(false),
      })
      .refine((d) => !d.heroImage || (d.heroAlt ?? '').trim() !== '', {
        message: 'heroAlt is required when heroImage is set',
        path: ['heroAlt'],
      }),
})

export const collections = { insights }
