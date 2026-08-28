---
name: web-fetching
description: >
  Use when you need to retrieve content from the web — fetching specific URLs,
  searching for information, retrieving API documentation, finding code examples,
  or getting error message solutions.
  Trigger for any request involving URLs, web content, online documentation, or
  web searches.
  Do NOT use for local files.
  Only webfetch is available — websearch is NOT available.
---

# Web Fetching Skill

Retrieve web content for coding tasks — use the right format, handle errors,
and perform searches via webfetch with search engine URLs.

---

## Overview

The only web tool available is **webfetch**. There is no separate websearch tool.
To perform web searches, use webfetch with a search engine URL.

```python
webfetch(url="https://example.com/docs/api", format="markdown")
```

| Parameter | Type | Description |
|---|---|---|
| `url` | string | Target URL (required) |
| `format` | string | `"markdown"` (default), `"text"`, or `"html"` |
| `timeout` | number | Optional timeout in seconds |

---

## PHASE 1 — Fetching Content

### 1.1 Validate the URL

- URL is well-formed (https://, proper path)
- URL points to the exact resource needed
- URL is accessible (not behind authentication without credentials)

### 1.2 Choose Format

| Format | Best For |
|---|---|
| `markdown` | Documentation, articles, README files (default) |
| `text` | Code files, raw data, config, logs |
| `html` | HTML pages, web apps, interactive content |

Use `format="text"` for raw file URLs (GitHub raw content, pastebin, etc.).

### 1.3 Content Type Reference

| Content Type | Expected Format |
|---|---|
| API docs / README | `markdown` |
| Source code files | `text` |
| Stack Overflow | `markdown` |
| GitHub issues/PRs | `markdown` |
| Blog posts | `markdown` |
| Raw config/data files | `text` |

---

## PHASE 2 — Web Search via webfetch

**websearch is NOT available.** To search the web, use webfetch with a search engine URL.

### Search Engine URLs

| Engine | URL Pattern | Format |
|---|---|---|
| Google (Basic HTML) | `https://www.google.com/search?q=QUERY&gbv=1` | `html` or `text` |

URL-encode the query. Use Google's basic HTML view (`gbv=1`) — it avoids JS-heavy rendering and is less likely to trigger CAPTCHA than the standard endpoint. Use `format="html"` or `format="text"` (avoid `markdown` for search results pages).

**Example — searching for a topic:**

```
User: "Search for python async best practices"
You: webfetch(url="https://www.google.com/search?q=python+async+best+practices&gbv=1", format="html")
```

**Example — searching for error resolution:**

```
User: "How do I fix 'Connection refused' in Node.js?"
You: webfetch(url="https://www.google.com/search?q=nodejs+connection+refused+fix&gbv=1", format="html")
```

### Search Results Processing

1. Fetch search results with webfetch
2. Review results for relevant links
3. Fetch the most relevant result with webfetch to get full content
4. Synthesize findings for the user

---

## PHASE 3 — Coding Patterns

### 3.1 API Documentation

1. Identify the library/package
2. Find official docs URL (e.g., `https://docs.example.com`)
3. Use webfetch to get relevant sections
4. If docs are unclear, search via search engine URL to find examples

### 3.2 Error Resolution

1. Copy exact error message
2. Fetch with search engine URL: `[error-message] [language/framework]`
3. Fetch the most relevant result
4. Verify solution works with your specific version

### 3.3 Code Examples

1. Search: `[feature] example code [language]`
2. Prioritize official examples, then reputable tutorials
3. Verify code is current (not deprecated)

### 3.4 Version/Compatibility Research

1. Search: `[package] version 3 vs 2 migration guide`
2. Fetch changelog or migration guide
3. Look for compatibility notes with your stack

---

## PHASE 4 — Error Handling

### 4.1 Retry Strategy

1. **First failure:** Retry once (network issues are often transient)
2. **Second failure:** Try alternative format (e.g., `html` instead of `markdown`)
3. **Third failure:** Report error to user with specific URL and issue

### 4.2 Common Errors

| Error | Likely Cause | Action |
|---|---|---|
| 404 Not Found | URL wrong or moved | Verify URL or search for updated location |
| 403 Forbidden | Access denied | Check if authentication needed |
| Connection timeout | Server slow/unreachable | Retry with longer timeout |
| Invalid URL | Malformed URL | Validate and correct |
| CAPTCHA / consent page | Google bot detection | Refine query with `site:` filter or more specific terms; retry; or fall back to a known URL |

### 4.3 Edge Cases

**Redirects:** Followed automatically. If too many redirects, verify URL manually.

**Large pages:** Fetch specific sections rather than entire page. Use anchor links.

**Rate limiting:** If getting 429 errors, wait and retry with delay.

**Authentication required:** Cannot fetch protected content. Inform the user.

---

## Quick Reference

```
Fetch URL → webfetch(url, format)
Search web → webfetch(https://www.google.com/search?q=QUERY&gbv=1, format)
  Format: html or text (avoid markdown for search results)
```

**Format defaults:** docs → markdown, code → text, HTML → html

**On error:** retry → try different format → report to user

**No websearch tool exists.** Always use webfetch with search engine URLs.
