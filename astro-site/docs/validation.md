# Migration validation

Validated on 2026-10-20 with Node 24.19.0 and Astro 7.4.1.

- `npm run check`: zero errors, warnings, and hints.
- `npm test`: four search tests passed, including Korean normalization and code punctuation.
- Root and `/alex-roh-blog/` builds succeeded.
- Browser: 11 posts; newest lecture first; six series; tags and legacy tag query links.
- Browser: both lecture series links; 69 / 63 code and output blocks preserved.
- Browser: desktop sticky table of contents and active section, mobile expandable table of contents.
- Browser: title/body search for Korean, English, and `fields[1:]`; empty result handling.
- Browser: post images, math rendering, downloadable attachment; no client errors or failed requests.
- Mobile viewport 390 x 844: no page overflow.
- Original content: all 19 files copied byte for byte (11 Markdown, 6 images, 2 Python attachments).
- Original Gatsby working tree clean and unchanged.

The public remote repository was created separately. No production switchover has been performed.

## Archive change (2026-10-20)

- Nine older posts moved to archive/posts with their six images and two Python attachments.
- All 17 archived files matched the original SHA-256 manifest.
- Build succeeded with two published ENAI607 posts.
- Search index contains only the two ENAI607 posts; archived routes, media, RSS and sitemap entries are absent.
- Existing production site still serves Gatsby 2.32.13; no production deployment was changed.
