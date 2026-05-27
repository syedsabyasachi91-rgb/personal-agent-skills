---
name: finding-dead-code
description: Use when asked to find dead, unused, or unreachable code in a codebase for Python, JavaScript, or HTML files (including embedded code in single files)
---

# Finding Dead Code

## Overview

Dead code is code that is defined but never used, imported but never called, or written but never executed. It accumulates over time as features change, creating technical debt and confusion. Removing dead code improves maintainability, reduces bundle size, and can reveal bugs.

**Always use automated tools first** - manual code reading misses cases and is slow.

## Workflow

```
Detect → Analyze → Filter → Score → Report → Remove → Verify
```

Follow these phases in order. Each phase builds on the previous.

### Phase 1 — Detect

Run automated tools to find potential dead code.

| Language | Command |
|----------|---------|
| JS/TS | `npx eslint --quiet` |
| Python | `python -m pyflakes . && vulture .` |
| HTML | `npx eslint --ext .html --plugin html` |

**Output:** Raw list of potential dead code items.

### Phase 2 — Analyze

Cross-reference findings to verify actual unused status.

- Check cross-file imports
- Search test files for references
- Identify dynamic calls (`obj['fn']()`, `eval()`, event handlers)

### Phase 3 — Filter

Remove false positives using framework and pattern rules.

- Apply framework SKIPs (React, Django, Express)
- Exclude generated code
- Skip dynamic call files

### Phase 4 — Score

Apply confidence levels to prioritize removal.

- **High**: Private + multiple tools + no test refs
- **Medium**: Exported but multiple tools agree
- **Low**: Single tool or framework pattern

### Phase 5 — Report

Generate structured output with priorities.

- Group by priority (P1/P2/P3)
- Include confidence level per item
- Show LOC estimate

### Phase 6 — Remove

Execute safe removal with backup and dry-run.

1. Backup: `git stash push -m "pre-dead-code-cleanup"`
2. Dry-run: `autoflake --check-diff -r .` or `npx knip --dry-run`
3. Execute removal by priority (P1 first)

### Phase 7 — Verify

Run tests and build to confirm no breakage.

```bash
npm test && npm run build  # or pytest, go test, cargo test
```

If issues: `git stash pop` to rollback.

## Quick Scan

Run these commands first for fast detection:

| Language | Command |
|---------|---------|
| JavaScript/TypeScript | `npx eslint . --ext .js,.ts --no-eslintrc --rule '{"no-unused-vars":"warn","no-unused-expressions":"warn"}'` |
| Python | `python -m pylint --disable=all --enable=unused-import,unused-variable,unused-argument <file>.py` |
| HTML (with inline JS) | `npx eslint . --ext .html --rule '{"no-unused-private-class-members":"warn","no-unused-vars":"warn"}'` |

## Detection Levels

### Level 1 — Quick Scan (30 seconds)
Fast one-liners for immediate detection:
- JS: `npx eslint --quiet`
- Python: `python -m pyflakes .`
- HTML: `npx eslint --ext .html`

### Level 2 — Deep Analysis (2-5 minutes)
Comprehensive tools for thorough detection:
- JS: `npx knip`
- Python: `vulture + pylint`
- All: Cross-reference analysis

### Level 3 — Full Audit (10+ minutes)
Manual verification + edge case handling:
- Dynamic call detection
- Framework pattern awareness
- Export analysis

## JavaScript/TypeScript

### ESLint Rules

Add to `.eslintrc.json`:

```json
{
  "rules": {
    "no-unused-vars": "error",
    "no-unused-expressions": "error",
    "no-unused-imports": "error"
  }
}
```

### Common Unused Types

| Type | Detection |
|------|-----------|
| Unused function | `no-unused-vars` |
| Unused variable | `no-unused-vars` |
| Unused import | Track imports vs usage |
| Unused class method | `no-unused-vars` with `argsIgnorePattern: "^_"` |
| Unused export | Check if exported item is imported elsewhere |

### False Positives

Some patterns appear unused but aren't:
- Functions only called dynamically (e.g., `window['fn']()`)
- Functions used in callbacks or event handlers
- Exported utilities used in other files (check imports)

Run `eslint --quiet` to see only errors, not warnings.

## Python

### Pylint

```bash
python -m pylint --disable=all --enable=unused-import,unused-variable,unused-wildcard-import,unused-argument <file>.py
```

Key message codes:
- `W0611`: Unused import
- `W0612`: Unused variable
- `W0613`: Unused argument
- `W0614`: Unused wildcard import

### Flake8

```bash
flake8 --select=F401,F841 <file>.py
```

- `F401`: Module imported but unused
- `F841`: Local variable is assigned but never used

### Vulture (recommended for functions/classes)

```bash
pip install vulture
vulture <file>.py
```

Vulture catches unused functions, classes, and variables that Pylint misses. Use both: Pylint for imports/variables, Vulture for functions/classes.

### Coverage.py

For runtime-unused detection (code executed but results not used):

```bash
pip install coverage
coverage run test_runner.py
coverage report --show-missing
```

### False Positives

- Functions called via `getattr()` or `dispatch`
- Methods in base classes used by subclasses
- Variables assigned but used elsewhere in same scope

## HTML with Embedded Code

### Inline Scripts

ESLint with `eslint-plugin-html`:

```bash
npm install --save-dev eslint eslint-plugin-html
npx eslint . --ext .html --plugin html
```

**False positives:** ESLint may flag functions used in inline HTML event handlers (`onclick="fn()"`) as unused. Verify manually before deleting.

### Inline Styles

Manually verify CSS classes used in HTML:
```bash
# Extract defined classes
grep -oP '\.(?:[a-zA-Z_][\w-]*)\s*\{' file.html

# Extract used classes
grep -oP 'class="[^"]*"' file.html | grep -oE '[a-zA-Z_][\w-]*'
```

Compare the two lists to find unused classes.

### Embedded Frameworks

For PyScript, Brython, or similar:
- Check for `<py-script>` or `<script type="text/python">` elements
- Verify referenced Python functions are actually called
- Look for orphaned framework-specific attributes

## Manual Patterns

When tools aren't available, use these grep patterns:

### Commented-out code

```bash
# JavaScript
grep -rn "// const\|// let\|// var\|// function\|// class" --include="*.js" .

# Python
grep -rn "# def\|# class\|# import" --include="*.py" .
```

### Dead branches

```bash
# JavaScript
grep -rn "if (false)\|if (true) and not" --include="*.js" .

# Python
grep -rn "if False:\|if True:" --include="*.py" .
```

### TODO cleanup

```bash
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.js" --include="*.py" --include="*.ts" .
```

## Prioritization

Confidence levels for removal decisions:

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 High | Exported by 1 tool, private symbol, no test refs | Safe to remove |
| 🟡 Medium | Multiple tools agree, but exported or in tests | Review before remove |
| 🟢 Low | Single tool report, framework pattern match | Manual inspection |

**Signs of safe removal:**
- Private (not exported)
- No test file references
- Multiple tools report same issue
- Old (not touched recently)

**Signs to review before removal:**
- Exported or in public API
- Referenced in tests
- Single-tool report only
- Framework hook pattern

## Safety Checklist

Before removing any dead code:

1. **Backup first**
   ```bash
   git stash push -m "pre-dead-code-cleanup"
   # or: cp -r project project-backup
   ```

2. **Dry run**
   ```bash
   # Python
   autoflake --check-diff -r .
   
   # JavaScript
   npx knip --dry-run
   ```

3. **Run tests**
   ```bash
   npm test  # or pytest, go test, cargo test
   ```

4. **Verify build**
   ```bash
   npm run build  # or python -m compile, go build
   ```

5. **Rollback if needed**
   ```bash
   git stash pop
   ```

## Verification

Before deleting any dead code:

1. **Run tests** - Ensure removal doesn't break functionality
2. **Check cross-file references** - Some "unused" code may be called from other files
3. **Search for dynamic calls** - `obj['fn']()`, `eval()`, event handlers
4. **Verify exports** - Exported functions used in other packages

## Edge Cases

### Monorepo
Run tools per-package, not at root:
```bash
cd packages/app && npx eslint .
cd packages/lib && python -m pylint .
```

### Dynamic Calls
Code called via `obj['fn']()` or `eval()`:
- Flag file as "requires manual review"
- Don't auto-remove anything in that file

### Generated Code
Exclude from analysis:
- `*.generated.*`, `*_pb2.py`, `*.pb.go`
- `schema.graphql.ts`, `*.d.ts`

### Framework Hooks
Don't flag as unused:
- React/Next.js: `getStaticProps`, `getServerSideProps`, `getStaticPaths`, `_app`, `_document`, `middleware`
- Django: `urlpatterns`, `admin.*`
- Express/Fastify: `router.*`, `app.use`

### Tests
Check if "unused" code has test references:
```bash
grep -r "functionName" --include="*test*" .
```

### Framework-Specific False Positives

| Framework | Skip these patterns |
|-----------|---------------------|
| React/Next.js | `getServerSideProps`, `getStaticProps`, `getStaticPaths`, `_app`, `_document`, `middleware` |
| Django | `urlpatterns`, `INSTALLED_APPS`, `MIDDLEWARE`, `admin.*`, management commands |
| Express/Fastify | `router.get/post`, `app.use`, `@Controller`, `@Module` |
| Go | `init()`, `TestXxx()`, exported funcs in non-main packages |
| Rust | `pub fn` in lib crates, `#[test]`, `impl Display` |

## When NOT to Use

- Single-file scripts (< 500 LOC)
- Throwaway/prototype code
- Already-optimized production code
- Code with heavy dynamic patterns (eval, reflection)

## Common Mistakes

- **Manual reading only** - Misses cross-file imports, dynamic calls
- **Ignoring false positives** - Some "unused" code has legitimate uses
- **Not checking tests** - Test files may call the code
- **Deleting framework code** - Some frameworks add code at runtime

## Red Flags

STOP if you are:
- Manually reading through code line-by-line to find unused items
- Not using ESLint/Pylint as the primary detection method
- Assuming a function is unused without checking all import sites
- Deleting code without running tests first

**Always use automated tools first, then verify manually.**