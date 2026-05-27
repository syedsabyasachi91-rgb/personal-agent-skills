---
name: reviewing-implementation
description: >
  Use when verifying that a completed code change correctly implements its plan
  document or specification — checking that tasks and acceptance criteria from
  the plan are addressed in the diff. Triggered by "check against the plan",
  "verify acceptance criteria", "validate against requirements", "did I miss
  anything from the plan", or "plan compliance". Do NOT trigger for general
  code review, bug finding, security audit, performance review, or style —
  those use the code-review skill.
---

# Reviewing Implementation

Verify a code change (identified by a git diff) correctly implements all tasks and acceptance criteria from a plan document. Uses a fresh subagent to avoid confirmation bias.

## When to Use

- After completing a task or feature from an implementation plan
- Before marking a task as done or moving to the next task
- When you need to verify scope compliance (no missing items, no over-scope)

**Do NOT use for:**
- General code quality review (use `code-review` skill instead)
- Reviewing feedback from others (use `receiving-code-review` instead)

## Process

### Step 1 — Gather inputs

1. **Plan document path** — the plan the implementation was based on (e.g., `docs/superpowers/plans/2026-05-25-feature.md`)
2. **BASE_SHA** — commit SHA before the implementation started (usually `HEAD~N` or `origin/main`)
3. **HEAD_SHA** — current tip commit (`git rev-parse HEAD`)

### Step 2 — Dispatch subagent

Use `Task` tool with `general-purpose` type, filling the template at `reviewer-prompt.md`.

**Placeholders:**
- `{PLAN_PATH}` — path to the plan document
- `{PLAN_CONTENT}` — the full text of the plan document
- `{BASE_SHA}` — starting commit
- `{HEAD_SHA}` — ending commit

### Step 3 — Act on findings

| Severity | Action |
|----------|--------|
| **Blocking** | Fix immediately — missing requirements, broken tests, build failures |
| **Important** | Fix before proceeding — partial implementation, quality gaps |
| **Minor** | Note for later — style, naming, non-functional improvements |

Push back if the reviewer is wrong, with technical reasoning. If the reviewer identifies a problem with the plan itself (not the implementation), flag it to your partner before changing anything.

## Red Flags

- Skipping review because "it was a simple change" or "I just built it"
- Accepting partial implementation as "good enough for now"
- Ignoring Blocking items
- Not actually re-reading the plan document during review — always read the plan file directly, never rely on the user's summary
- Marking a task complete without verification
- Accepting the user's claim that "tests pass" without running them yourself
- Checking that code *exists* without verifying the code *behaves correctly* per the acceptance criteria

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reviewing the diff without the plan | Always re-read the plan file directly — never rely on the user's summary |
| Accepting off-by-one-line implementations as "close enough" | Every plan task must be fully addressed |
| Confusing code quality review with plan compliance | This skill checks WHAT was built, not HOW well it was built |
| Not checking for scope creep | Flag any feature or file change not called for in the plan |
| Not verifying the build/tests actually pass | Run the test/lint/build commands yourself — don't take the user's word |
| Checking code exists without checking behavior | Verify acceptance criteria are met, not just that a file was created |
| Reading the plan summary from the user instead of the file | Read the actual plan document — user summaries miss details and acceptance criteria |

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task completion, before moving to next task

**Executing Plans:**
- Review at each natural checkpoint in the plan

**Ad-Hoc Development:**
- Review before merge or when marking a feature complete
