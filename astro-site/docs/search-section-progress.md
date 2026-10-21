# Section search implementation

User request: jump from search results to the matching explanation, with small scope and resumable work.

Status: implementation and local validation complete. Production deployment status must be checked in hosting GitHub Actions rather than inferred from this document.

Implemented:
- Build-time section extraction using the existing Markdown processor and actual Astro heading IDs.
- Existing exact title/body/code matching, with section titles and snippets preserving code case.
- Direct section links, best-match article-title links, and expandable additional matches.
- Search destinations reveal matching collapsed details, scroll to the section and focus its heading.
- Ordinary TOC links remain unchanged. No new package, runtime server or search service.

Validation:
- npm run check: 0 errors, warnings or hints.
- npm test: 11 tests passed, including legacy indexes, Unicode/code punctuation, headings and extraction.
- npm run build: passed.
- Browser: all 321 indexed anchors in 6 articles exist; clicking search hits, folded answers, regular links, more results, mobile and empty results passed.

Release/recovery:
1. Inspect git status and preserve unrelated user edits.
2. Commit the implementation and tests.
3. Publish through the connected GitHub API with an expected-head lease (CLI authentication may be unavailable).
4. In alex-roh/alex-roh.github.io, run deploy-astro.yml using the published alex-roh-blog source commit SHA.
5. Re-run the saved browser validation against the live origin and record its result.

Deferred: modal/shortcut search, fuzzy matching, Colab and comments. These are not required for this change.
