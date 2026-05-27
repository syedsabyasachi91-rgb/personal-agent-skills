---
name: github-finder
description: >
  Use when searching for anything on GitHub — repositories, code,
  issues, PRs, users, topics, trending projects, or any GitHub-hosted
  content. Triggered by queries like "find a repo/library that...",
  "search GitHub for...", "what's the best/trending/most popular...",
  "look up [project] on GitHub", "find code/snippets that do X",
  "are there any alternatives to...", "how many stars does Y have",
  "who maintains Z", "find issues about...", or any request involving
  finding projects, code, issues, or resources hosted on GitHub.
  Covers all GitHub search dimensions (repos, code, issues, users,
  topics) with multiple connection methods. Addresses shallow single-
  tool searches that miss results due to not knowing available search
  qualifiers, APIs, or fallback strategies.
---

# GitHub Finder

## Overview

A tiered search router for GitHub. It detects what you're searching for (repo, code, issue, user, or topic) and tries connection methods in order: `gh` CLI → REST API → web search fallback. Each search mode has its own query construction patterns and structured output template.

## When to Use

- "Find a repo/library that does X"
- "Search GitHub for code examples of Y"
- "Look up issues/PRs for project Z"
- "Find a developer/user on GitHub"
- "What are the trending projects in language L?"
- "Are there any open-source alternatives to tool T?"

**When NOT to use:**
- Searching local codebase → use codebase-search-funnel
- General web research (outside GitHub) → use research-funnel or web-fetching
- Reading local files → use document-reader

## Phase 1: Detect Search Mode

Parse the user's natural language query to determine what's being searched.

| Signal keywords | Mode |
|----------------|------|
| "repo", "library", "framework", "project", "tool", "package", "alternative to" | **Repositories** |
| "code", "snippet", "implementation", "example", "how to", "function that", "pattern" | **Code** |
| "issue", "bug", "bug report", "pull request", "PR", "feature request", "ticket" | **Issues & PRs** |
| "user", "profile", "who is", "developer", "contributor" | **Users** |
| "topic", "trending", "popular", "best", "top" | **Topics** |

If no clear signal, default to **Repositories** (broadest search).

**Precedence:** If multiple modes match, prioritize in this order: Issues & PRs > Users > Code > Topics > Repositories. This prevents general phrases from overriding more specific intents.

## Phase 2: Detect Available Tools

Try in order. Use the first that succeeds.

```
1. gh CLI:  gh --version && gh auth status
2. REST API: curl -s "https://api.github.com" (check response)
3. Web:     Always available (websearch + webfetch)
```

### Error Recovery

If all 3 tiers fail:
1. **Report what failed** — was `gh` not found? API rate-limited? Web search offline?
2. **Check API rate limits** — unauthenticated: 60 req/hr. Run `curl -sI "https://api.github.com" | grep x-ratelimit-remaining` to check remaining quota. Retry after the reset time.
3. **Retry web search** — sometimes rephrasing the query or removing qualifiers resolves issues. Try `websearch` with a simpler query first.
4. **If webfetch returns 404** — the repo/user/issue may not exist or the URL is wrong. Verify the URL path.
5. **If webfetch times out** — GitHub may be rate-limiting HTML page fetches. Wait 60 seconds and retry, or use the API instead.

## Phase 3: Execute Search

### Mode: Repositories

| Method | Command |
|--------|---------|
| gh | `gh search repos "<query>" [--language=<lang>] [--stars ">N"] [--sort=stars] [--limit N]` |
| API | `curl -s "https://api.github.com/search/repositories?q=<query>&sort=stars&per_page=10"` |
| Web | `websearch("site:github.com <query> language:<lang> stars:>N")` |

**Qualifier reference:**
- `language:python` — filter by language
- `stars:>1000` — minimum stars
- `topic:machine-learning` — filter by topic
- `user:facebook` — from specific user/org
- `in:name,description,readme` — where to search

### Mode: Code

| Method | Command |
|--------|---------|
| gh | `gh search code "<query>" [--language=<lang>] [--owner=<org>]` |
| API | `curl -s "https://api.github.com/search/code?q=<query>+language:..."` (needs auth for private repos) |
| Web | `websearch("site:github.com <query> extension:<ext>")` |

**Qualifier reference:**
- `extension:<ext>` — file extension (`.py`, `.rs`, `.ts`, `.js`, `.go`)
- `filename:test` — file name
- `user:facebook repo:react` — scope to repo
- `language:python` — language filter

**Extension hint:** Use the detected language's file extension (`.py`, `.rs`, `.ts`, `.js`, `.go`). If unsure, omit `extension:` for broader results.

### Mode: Issues & PRs

| Method | Command |
|--------|---------|
| gh | `gh search issues "<query>" [--label=<label>] [--state=open] [--author=<user>]` |
| API | `curl -s "https://api.github.com/search/issues?q=<query>+is:issue+state:open"` |
| Web | `websearch("site:github.com/<org>/<repo>/issues <query>")` |

**Qualifier reference:**
- `is:issue` / `is:pr` — type filter
- `is:open` / `is:closed` — state filter
- `label:bug` — label filter
- `author:username` — author filter

### Mode: Users

| Method | Command |
|--------|---------|
| gh | `gh search users "<query>"` |
| API | `curl -s "https://api.github.com/search/users?q=<query>"` |
| Web | `websearch("site:github.com <username>")` |

### Mode: Topics

| Method | Command |
|--------|---------|
| gh | `gh search repos --topic=<topic>` |
| API | `curl -s "https://api.github.com/search/topics?q=<query>"` |
| Web | `websearch("github.com/topics/<topic>")` |

## Phase 4: Report

Use the structured template matching the search mode.

### Repository search output

```
## GitHub Search: [query]

### Repositories (N found)
| Name | Stars | Language | Description |
|------|-------|----------|-------------|
| [owner/repo](url) | ⭐ N | Lang | Description |

### Search Details
- **Mode:** repositories
- **Method:** [gh/API/web]
- **Qualifiers used:** [list]

### Next Steps
- [Suggestion for narrowing]
```

### Code search output

```
## GitHub Search: [query]

### Code Results (N found)
- **[owner/repo](url)** — `path/to/file:line`
  ```lang
  snippet with context
  ```

### Search Details
- **Mode:** code
- **Method:** [gh/API/web]
```

### Issues & PRs search output

```
## GitHub Search: [query]

### Issues & PRs (N found)
| # | Title | State | Labels | Repo |
|---|-------|-------|--------|------|
| #N | [title](url) | ✅ Open | bug | owner/repo |

### Search Details
- **Mode:** issues
- **Method:** [gh/API/web]
```

### Users search output

```
## GitHub Search: [query]

### Users (N found)
| Username | Name | Location | Repos | Followers |
|----------|------|----------|-------|-----------|
| [@user](url) | Name | Location | N | N |
```

### Topics search output

```
## GitHub Search: [query]

### Topics (N found)
| Topic | Description | Repos |
|-------|-------------|-------|
| [topic](url) | Description | N |

### Top Repos
- [owner/repo](url) ⭐ N stars — Description
```

## Connection Reference

### GitHub CLI
```bash
gh search repos "<query>" --limit 10 --sort stars
gh search code "<query>" --language py --limit 10
gh search issues "<query>" --state open --limit 10
gh search users "<query>" --limit 10
```

### REST API (unauthenticated: 60 req/hr, authenticated: 5000 req/hr)
```bash
# Repositories
curl -s "https://api.github.com/search/repositories?q=<query>&sort=stars&per_page=10&order=desc"

# Code
curl -s "https://api.github.com/search/code?q=<query>"

# Issues
curl -s "https://api.github.com/search/issues?q=<query>"

# Users
curl -s "https://api.github.com/search/users?q=<query>"

# Topics
curl -s "https://api.github.com/search/topics?q=<query>"
```

### Web Search (always available)
```bash
websearch("site:github.com <query>")
webfetch("https://github.com/<owner>/<repo>")
webfetch("https://github.com/<owner>/<repo>/issues")
webfetch("https://github.com/topics/<topic>")
```

**Failure handling:**
- **404 on webfetch:** The repo/user/issue/topic doesn't exist at that URL — double-check spelling and path
- **Timeout on webfetch:** GitHub rate-limits HTML page fetches — wait 60s and retry, or use the API instead
- **websearch returns no results:** Remove qualifiers and retry with a broader query

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping qualifiers, getting too many results | Use `language:`, `stars:>`, `topic:` to narrow |
| Using only one search method | Try all 3 tiers — websearch often finds things API misses |
| Forgetting rate limits | Unauthenticated API = 60 req/hr. Use web search for bulk. |
| Searching code without `site:` prefix | Always use `site:github.com` in web search for GitHub |
| Over-narrowing with too many qualifiers | Start broad, add qualifiers one at a time |
| Not checking if `gh` is available | Always check `gh --version` first before assuming |
