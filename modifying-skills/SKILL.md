---
name: modifying-skills
description: Use when editing an existing skill's SKILL.md — adding sections, updating descriptions, restructuring, fixing gaps, or closing loopholes in testing
---

# Modifying Skills

## Overview

**Modifying a skill has different failure modes than creating one.** The risk is breaking tested behaviors during a seemingly safe edit.

**REQUIRED BACKGROUND:** You MUST understand superpowers:writing-skills (TDD foundation). This skill adds the modification-specific workflow.

## When to Modify vs Rewrite

| Condition | Action |
|-----------|--------|
| <50% changes | Modify in place |
| >50% changes | Rewrite with writing-skills |
| Fundamental contradiction with existing content | Rewrite from scratch |

## Workflow: READ → INVENTORY → CHANGE → REGRESS → VERIFY

**1. READ** — Read entire SKILL.md. Note frontmatter, structure, and existing test files.

**2. INVENTORY** — Find all test/pressure scenario files. Know what's tested before changing anything.

**3. CHANGE** — State "I am changing X because Y." Make only targeted edits.

**4. REGRESS** — Run ALL existing tests. **No exceptions:** not for descriptions, additive sections, or one-word fixes.

**5. VERIFY** — If adding behavior, write new tests. Pass old AND new.

## Red Flags — STOP

| Rationalization | Reality |
|----------------|---------|
| "Just a description update" | Descriptions are trigger conditions. Wrong description = wrong behavior. |
| "It's additive, can't break" | New sections can contradict existing workflow. |
| "One-word bug fix" | One word changes meaning. Regression test it. |
| "Testing was already done" | Edits introduce new failure modes. Old tests passing is the check. |
| "Only need to test my changes" | Unchanged sections interact with changed ones. |
| "User is waiting" | #1 rationalization for skipping tests. |
| "Tests test functionality, not docs" | Every edit affects agent interpretation. |

## Common Mistakes

1. **Over-editing** — Scope creep breaks tested content.
2. **Breaking frontmatter** — YAML is fragile. One wrong indent breaks loading.
3. **Deleting tested content** — Removing behaviors without checking scenarios.
4. **Description/metadata mismatch** — Changing description without updating how agents discover the skill.
5. **Assuming additive is safe** — New sections can contradict existing steps.
