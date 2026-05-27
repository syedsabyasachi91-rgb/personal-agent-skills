---
name: codebase-search-funnel
description: >
  Use when finding code elements in a codebase — functions, classes, imports,
  usages, patterns, configuration, error handling, or any code structure.
  Addresses ineffective search that misses results, returns too much noise,
  or lacks context for understanding.
---

# Codebase Search Funnel

## Overview

Searching is a multi-phase process, not a single grep command. The 5-phase funnel prevents common failure modes: missing results, too much noise, no context around matches, inconsistent output.

## When to Use

- Finding where a function/class/variable is defined
- Finding all usages or imports of something
- Searching for patterns (error handling, logging, validation)
- Tracing configuration loading and environment variables
- Finding files by name or path pattern
- Cross-referencing multiple related patterns

**When NOT to use:**
- Simple fact lookup in a single file — just read the file
- Checking a single known function — use grep directly
- Searching external web content — use research-funnel or web-fetching

## The 5-Phase Funnel

### Phase 0: Frame

Define what kind of search you're doing before touching any tool.

| Search Type | Question | Example |
|-------------|----------|---------|
| Definition | Where is X declared/defined? | `find class AuthService` |
| Usage/Reference | Where is X called or imported? | `find all imports of 'config'` |
| Pattern | Find instances of a semantic pattern | `find all error handling` |
| Config | Find configuration values/env vars | `find where DATABASE_URL is used` |
| File | Find files by name/pattern | `find all test files for auth` |
| Embedded | Find code inside a different host language | `find <button> in Python-generated HTML` |

**Exit:** Search type is identified. This determines tool, flags, and output format.

### Phase 1: Scope

Narrow the search space before executing. This prevents noise and speeds up results.

- **Which directories?** Target specific subdirectories (`src/auth/`, `packages/api/`)
- **Which file types?** Filter by extension (`*.ts`, `*.py`, `*.{ts,tsx}`)
- **Include or exclude tests?** Usually search test files separately from source
- **Respect boundaries** — ripgrep respects `.gitignore` by default; grep does not
- **Embedded detection:** If target code lives inside a different host language (JS in Python f-strings, HTML in Ruby heredocs), do NOT use language type flags — target the host file directly with plain text search
- **Template awareness:** Know the embedding mechanism (f-strings, heredocs, template literals, Jinja2, ERB) — it determines how much context you need and whether matches are in string literals or code

**Exit:** Clear search boundary. Known what dirs, file types, and exclusions apply.

### Phase 2: Execute

Choose the right tool and use correct flags.

| Search Type | Tool | Flags | Example |
|-------------|------|-------|---------|
| File by name | `glob` | pattern | `glob **/*auth*` |
| File by path pattern | `glob` | pattern | `glob **/*.test.ts` |
| Simple text pattern | `rg` or `grep` | `-rn` | `rg -rn "connect" src/` |
| Text + context | `rg` | `-rn -C 3` | `rg -rn -C 3 "class Auth"` |
| Pattern in file types | `rg` | `-t ts` | `rg -t ts -rn -C 3 "interface"` |
| Pattern in subdir only | `rg` | path arg | `rg -rn "error" src/auth/` |
| Embedded HTML/JS | `rg` | no type flag, target host file | `rg -rn -C 5 "<button" app.py` |
| Template patterns | `rg` | no type flag | `rg -rn -C 3 "{% .* %}\|{{ .* }}"` |
| Multi-file complex | `task` | explore agent | Dispatch with structured task |

**CRITICAL: Always use context flags when searching for definitions or usages.**
- `-C 3` (3 lines before and after) for function/class definitions
- `-C 5` for complex patterns where you need more surrounding logic
- `-C 0` only for simple existence checks

**EMBEDDED CONTENT: Never use `-t` type flags when searching embedded code.**
Type flags filter by the host language's syntax rules and will miss content inside string literals, template strings, and heredocs. Always search the host file as plain text.

**Tool decision:**
1. Finding a file? → `glob`
2. Simple text in known scope? → `rg` with `-C N`
3. Multi-pattern cross-reference? → Multiple `rg` calls + synthesis
4. Complex multi-file reasoning? → `task` subagent

**Large codebase rules:**
- Always prefer `rg` (ripgrep) over `grep` — respects `.gitignore`, faster
- Always include `-C N` context
- Search per-package in monorepos, not from root
- Use `--include` / `-g` patterns to narrow file types

### Phase 3: Synthesize

After getting raw results, process them before reporting.

- **For definitions:** Confirm primary definition vs overloads/re-exports
- **For usages:** Separate production code from test code
- **For patterns:** Group by category, identify themes
- **Prune false positives:** Dynamic references, string literals, comments, generated files

**Exit:** Matches are pruned, grouped by relevance, contextualized.

### Phase 4: Report

Use a structured output format. Every report must include file paths and line numbers.

**Definition search output:**
```
## Search: [query]

### Definition
- `path/to/file.ts:42` — `function connect(config: Config): Connection`

### Usages (N total)
- `path/to/file.ts:87` — `const db = connect(dbConfig)`

### Imports (N total)
- `path/to/other.ts:1` — `import { connect } from './db'`

### Test References (N total)
- `tests/db.test.ts:15` — `const mockConn = connect(mockConfig)`
```

**Pattern search output:**
```
## Search: [pattern description]

### Category 1: [category name]
- `path/to/file.ts:15-20` — [snippet with 3-line context]

### Category 2: [category name]
- ...
```

## Quick Reference

| What | Tool | Command |
|------|------|---------|
| Function/class def | `rg` | `rg -rn -C 3 "^function name"` / `"^class Name"` |
| Usage/calls | `rg` | `rg -rn -C 3 "name\("` |
| Imports | `rg` | `rg -rn "from ['\"]module['\"]"` |
| File by name | `glob` | `**/*name*` |
| Error handling | `rg` | `rg -rn -C 3 "catch|except|\.error|throw"` |
| Config loading | `rg` | `rg -rn -C 3 "load_config|config\(\)|getenv"` |
| Env vars | `rg` | `rg -rn "process\.env\.\|os\.getenv\|environ\.get"` |
| Pattern in file type | `rg` | `rg -t ts -rn -C 3 "pattern"` |
| Pattern in directory | `rg` | `rg -rn "pattern" src/subdir/` |
| Embedded HTML in Python | `rg` | `rg -rn -C 5 "HTML_tag\|class_name" host.py` |
| Embedded JS in strings | `rg` | `rg -rn -C 5 "function\|const\|let" host.py` |
| Template tags (Jinja2/Django/ERB) | `rg` | `rg -rn -C 3 "{%\|{{ \|{{-\|}}"` |

## Red Flags

STOP if you are:
- Using grep or rg without `-C` context flag
- Using `grep` instead of `rg` on 100K+ file repos
- Reading files one-by-one to find something
- Stopping at the first match without checking for more
- Not scoping the search to relevant directories
- Reporting raw grep output without grouping or context
- Confusing usages with definitions in your report
- Using `-t` type flag when content is embedded in a different host language

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Grep without context | Always use `-C 3` minimum |
| Searching entire repo | Scope to relevant subdirectory first |
| One pattern only for complex searches | Use multiple patterns and synthesize |
| Reading files to find things | Use grep/rg to locate, then read specific matches |
| No report structure | Use the structured report format |
| Forgetting test files | Check tests separately for complete picture |
| Not pruning false positives | Check for dynamic refs, strings, comments |
| Using `-t py` when searching HTML inside Python | Use plain text rg, no type flag |
| Searching by file extension only for embedded content | Target the host file by name, not its extension |
