---
name: web-fetching
description: >
  Use when you need to retrieve content from the web — fetching specific URLs,
  searching for information, retrieving API documentation, finding code examples,
  or getting error message solutions. Covers both webfetch and websearch tools.
  Trigger for any request involving URLs, web content, online documentation, or
  web searches. Do NOT use for local files — use txt-reader for those.
---

# Web Fetching Skill

Retrieve web content completely and correctly for coding tasks — no guessing,
no sampling, use the right tool for the right job.

---

## Overview

This skill covers two tools:
- **webfetch**: Fetch specific URLs (documentation, APIs, code files)
- **websearch**: Search the web for information (solutions, examples, best practices)

Key principle: Choose the right tool based on whether you know the exact resource.

---

## PHASE 1 — Choose the Right Tool

| Signal | Tool |
|---|---|
| "fetch this URL", "get content from [url]" | **webfetch** |
| "look up", "search for", "find how to" | **websearch** |
| Specific documentation page, API endpoint, file | **webfetch** |
| Error message, "how do I", "what's the best way" | **websearch** |
| Know the exact URL | **webfetch** |
| Don't know the URL, need to find it | **websearch** |

When ambiguous, ask: *"Do you have a specific URL, or should I search for it?"*

---

## PHASE 2 — Using webfetch

### 2.1 Validate the URL

Before fetching, verify:
- URL is well-formed (https://, proper path)
- URL points to the exact resource needed
- URL is accessible (not behind authentication without credentials)

### 2.2 Fetch with Format Options

```python
webfetch(url="https://example.com/docs/api", format="markdown")
```

| Format | Best For |
|---|---|
| `markdown` | Documentation, articles, README files (default) |
| `text` | Raw text, code snippets, log content |
| `html` | HTML pages, web apps, interactive content |

Use `format="text"` for code files, raw data, or when markdown parsing fails.

### 2.3 Handle Large Responses

If response exceeds ~50KB:
- Use offset/limit parameters if available
- Fetch specific sections separately
- Prioritize the information needed

### 2.4 Content Type Detection

| Content Type | Expected Format |
|---|---|
| API docs / README | `markdown` |
| Source code files | `text` |
| Stack Overflow | `markdown` |
| GitHub issues/PRs | `markdown` |
| Blog posts | `markdown` |
| Raw config/data files | `text` |

### 2.5 Error Handling

**Retry Strategy:**
1. First failure: Retry once (network issues are often transient)
2. Second failure: Try alternative format
3. Third failure: Report error to user with specific URL and issue

**Common Errors:**
- `404 Not Found`: URL is wrong or resource moved — verify URL or search for updated location
- `403 Forbidden`: Access denied — check if authentication needed or if bot is blocked
- `Connection timeout`: Server is slow or unreachable — retry with longer timeout
- `Invalid URL`: URL is malformed — validate and correct

---

## PHASE 3 — Using websearch

### 3.1 When to Use websearch

Use websearch when:
- **Error resolution**: Getting error messages, debugging issues
- **How-to questions**: "How do I implement X", "What's the best way to do Y"
- **Best practices**: Finding recommended approaches
- **Library research**: Comparing packages, finding alternatives
- **Version info**: Checking latest versions, compatibility

### 3.2 websearch Parameters

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Search query (required) |
| `numResults` | number | Number of results (default: 8) |
| `livecrawl` | string | `"fallback"` (default) or `"preferred"` |
| `type` | string | `"auto"`, `"fast"`, or `"deep"` |

**Live Crawl Modes:**
- `fallback`: Use cached if available, crawl live if not (default)
- `preferred`: Always crawl live content

**Search Types:**
- `auto`: Balanced results (default)
- `fast`: Quick results for simple queries
- `deep`: Comprehensive search for complex topics

### 3.3 Craft Effective Queries

**Good Patterns:**
- Include technology/libraries: "react hooks custom state management"
- Include context: "python async vs sync performance"
- Include version when relevant: "nodejs 20 new features"
- Be specific: "create-react-app vs vite SSR"

**Avoid:**
- Too broad: "help with coding"
- Too vague: "how to fix error"
- Overly long queries (keep under 50 words)

### 3.4 Process Search Results

1. Review titles and snippets
2. Prioritize official documentation, trusted sources
3. Fetch the most relevant result first
4. If first result doesn't answer the question, fetch the next most relevant

### 3.5 Handle Multiple Results

- Start with most authoritative source (official docs, established blogs)
- If results are from forums (Stack Overflow, Reddit), verify with official docs
- For multiple valid approaches, present options with trade-offs

---

## PHASE 4 — Coding-Specific Patterns

### 4.1 API Documentation

**Steps:**
1. Identify the library/package
2. Find official docs URL (usually `https://[package].js.org` or `https://docs.[package].com`)
3. Use webfetch to get relevant sections
4. If docs are unclear, use websearch for examples

**Examples:**
- Fetch: `webfetch(url="https://docs.example.com/api/client", format="markdown")`
- Search: `websearch(query="example api client authentication oauth")`

### 4.2 Error Resolution

**When encountering an error:**
1. Copy exact error message
2. Search with key terms: `[error-message] [language/framework]`
3. Prioritize Stack Overflow, GitHub issues, official docs
4. Verify solution works with your specific version

**Example workflow:**
```
Error: "Cannot read property 'map' of undefined"
1. websearch(query="Cannot read property 'map' of undefined react")
2. Fetch most relevant result
3. Apply fix and verify
```

### 4.3 Library/Dependency Research

**Before adding a dependency:**
1. Search for alternatives: `[use-case] npm package alternative`
2. Check popularity: stars, downloads, maintenance status
3. Look for examples: `[package] example usage`
4. Check compatibility: `[package] node version support`

### 4.4 Code Examples

**Finding working examples:**
1. Search: `[feature] example code [language]`
2. Prioritize official examples, then reputable tutorials
3. Verify code is current (not deprecated)
4. Check for TypeScript/ES6+ syntax if relevant

### 4.5 Version/Compatibility Research

**When version matters:**
1. Search: `[package] version 3 vs 2 migration guide`
2. Check changelog for breaking changes
3. Verify with official docs before upgrading
4. Look for compatibility notes with your stack

### 4.6 Architecture/Design Patterns

**For best practices:**
1. Search: `[pattern] best practices [language/framework]`
2. Check official style guides
3. Look at popular open-source projects for reference
4. Verify pattern is not outdated

---

## PHASE 5 — Error Handling & Edge Cases

### 5.1 Common Errors and Solutions

| Error | Cause | Solution |
|---|---|---|
| 404 Not Found | URL changed, page removed | Search for updated URL |
| 403 Forbidden | Bot blocked, auth required | Check headers, try websearch instead |
| Connection Timeout | Server slow/unreachable | Retry, try alternative source |
| Content Truncated | Response too large | Fetch in sections or use specific URLs |
| Invalid Format | Wrong format for content | Try different format option |

### 5.2 Edge Cases

**Redirects:**
- Follow redirects automatically (default behavior)
- If too many redirects, verify URL manually

**Large Pages:**
- Fetch specific sections rather than entire page
- Use anchor links to target content

**Mixed Content:**
- Some pages block fetch due to CORS
- Try websearch for cached/similar content

**Rate Limiting:**
- If getting 429 errors, wait and retry
- Use websearch as alternative

**Authentication Required:**
- Cannot fetch protected content
- Use websearch to find public alternatives

---

## Quick Reference Decision Tree

```
START: User needs web content
│
├─ Do you know the exact URL?
│   ├─ YES → Use webfetch
│   │   │
│   │   └─ What format?
│   │       ├─ Docs/Articles → markdown
│   │       ├─ Code/Raw → text
│   │       └─ HTML pages → html
│   │
│   └─ NO → Use websearch
│       │
│       └─ Craft query:
│           • Include technology
│           • Be specific
│           • Under 50 words
│
└─ Processing results:
    • Prioritize official docs
    • Start with most relevant
    • Verify with multiple sources if needed
```

---

## Summary

1. **Know the URL?** → webfetch | **Don't know?** → websearch
2. **webfetch**: Use correct format (markdown/text/html), handle large content, retry on failure
3. **websearch**: Craft good queries, process results strategically, verify with authoritative sources
4. **Coding tasks**: Focus on API docs, error resolution, library research, code examples
5. **Handle errors**: Retry, try alternatives, report clearly when stuck