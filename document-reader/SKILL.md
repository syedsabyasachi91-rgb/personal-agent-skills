---
name: document-reader
description: Use when reading document files to extract API endpoints, schemas, backend logic, or production code patterns for integration and implementation tasks
---

# Document Reader

## Overview
When reading documentation to build an integration, a partial read causes integration bugs: missed auth schemes, missing error codes, hallucinated schemas. Read completely, extract systematically, report gaps.

## When to Use
- Extracting endpoints, request/response formats from API docs
- Pulling schemas, interfaces, or database definitions from markdown docs
- Finding backend logic patterns for integration work

When NOT to use: quick lookups (Grep directly), small config files, binary formats.

## Coverage Workflow
1. Read the file. If output is truncated, continue reading with offset until EOF — a truncation notice means "not done."
2. For very large files (>2000 lines), Grep section headers first (`^#{1,3} `), then read each section's range.
3. Never summarize from the first chunk alone.

## Extraction Checklist
For integration work, extract ALL of:
- Endpoints: method + path + description
- Request/response shapes: fields, types, required/optional
- Auth scheme (Bearer / API key / OAuth / basic) and where credentials go
- Error codes and meanings
- Rate limits, pagination, versioning constraints

## Report Gaps Explicitly
If docs omit something the integration needs (response schema, error format), state it as an assumption or gap — never silently guess. Separate what was documented from what was assumed.

## Common Mistakes
- Reading only the first chunk of a large doc and proceeding
- Extracting endpoints but skipping auth and error handling
- Guessing undocumented fields instead of flagging them
