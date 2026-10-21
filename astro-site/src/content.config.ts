import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { normalizeTimestampInput } from './lib/publication.mjs';

const posts = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './contents/posts',
    generateId: ({ entry }) => entry.split('/').at(-2)! }),
  schema: z.object({
    title: z.string(),
    description: z.string().nullish(),
    date: z.coerce.date().optional(),
    update: z.coerce.date().optional(),
    publishedAt: z.preprocess(normalizeTimestampInput, z.iso.datetime({ offset: true })).optional(),
    updatedAt: z.preprocess(normalizeTimestampInput, z.iso.datetime({ offset: true })).optional(),
    tags: z.array(z.string()).default([]),
    series: z.string().nullish(),
    seriesOrder: z.number().optional(),
  }),
});
export const collections = { posts };
