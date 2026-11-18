Talk to the user in Korean (reports, questions, cards). The session-start hook injects the common rules as `[공통 규칙]`. If missing from context or `못 받음`, say so first in the first reply. If `agent-kit/RULES.md` exists in the folder holding the repos, read and follow it. Below is this repo's guidance.

# Blog agent entry guide

This repo deploys public content. Never put private content, credentials or personal information into content or build output. Also follow the content rules in the `AGENTS.md` under a post folder.

Deploy is an exception to the common rule `ship.md` (push main). GitHub Pages deploys only through Actions: pushing a commit that changes `astro-site/` to main makes `deploy-astro.yml` deploy. If Actions is off, nothing deploys, so after pushing check that Pages updated.
