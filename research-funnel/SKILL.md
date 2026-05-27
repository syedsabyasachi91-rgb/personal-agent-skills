---
name: research-funnel
description: >
  Use when conducting research on a topic, technology, or domain —
  gathering information from web searches, documentation, or academic
  sources. Triggered by questions about how something works, comparing
  approaches, investigating technologies, or understanding unfamiliar
  domains. Addresses shallow research that stops at the first result,
  poor source evaluation, lack of synthesis, and unstructured exploration.
---

# Research Funnel

## Overview

A 5-phase structured research methodology centered on **iterative deepening** — the principle that understanding comes from multiple rounds of: search, extract, cross-reference, verify, identify gaps, and repeat. Prevents stopping at the first result.

The single most common failure mode in AI research is **"I already know this"** — the agent skips searching, relies on memory, and delivers surface-level answers. This skill forces research before answers.

## When to Use

- Answering "how does X work?" or "what's the best approach for Y?"
- Comparing technologies, libraries, or frameworks
- Investigating unfamiliar domains or concepts
- Validating claims, evaluating source quality
- Making evidence-based technical decisions
- Academic or technical deep-dives

**When NOT to use:**
- Simple fact lookup — if the answer requires no synthesis across sources, just answer it
- Checking a single known API endpoint — use web-fetching skill
- Reading local files — use document-reader skill

## The Stop Rule

**You may stop researching only when BOTH conditions are met:**

1. **Answer condition:** You can answer the original question with evidence from 2+ independent authoritative sources
2. **Diminishing returns condition:** Your last 2 deepen iterations each found 0 new facts that materially change the answer or raise new unanswered questions

If condition 1 is not met, you must keep deepening.
If condition 1 is met but condition 2 is not, you must keep deepening.

**Violating this rule is violating the skill.** There is no "spirit of the rule" exception. There is no "close enough" exception. There is no "diminishing returns is good enough" exception.

### Red Flags — KEEP GOING when:

| Red flag | What to do |
|----------|-----------|
| "I already know this" | Verify your knowledge against a source anyway |
| "This one source is enough" | Find a second independent source |
| "I found the answer" | Check for contradictions, nuance, edge cases |
| "Let me summarize" | Not yet — deepen first |
| "This seems comprehensive" | Prove it — find a gap |
| "Search snippets tell me enough" | Fetch the full article and verify |

## The 5-Phase Research Funnel

### Phase 1: Frame

Define the research clearly before searching.

- State the research question in one sentence
- Define scope: what's in bounds, what's out
- Define output format: decision, explainer, comparison, detailed-report
- Define success criteria: "I'll stop when I can X"

**Exit:** Question is precisely defined. Scope and output format are clear.

### Phase 2: Explore

Cast a wide net. Do NOT go deep yet.

- Search from 3+ different angles/phrasings
- Scan results for breadth: what subtopics exist?
- Collect 5+ sources (even if some are tangentially relevant)
- Do not evaluate quality yet — just gather

**Quality gate:** Before exiting, rank each collected source by hierarchy tier. Drop sources below tier 4 if you already have 3+ from tiers 1-3. Note any vendor/source bias.

**Exit:** Landscape is mapped. Sources are ranked by quality. You know what subtopics exist.

### Phase 3: Deepen (Iterative Deepening Loop)

**This is the core of the skill.** Run the loop:

1. Pick one finding or open question
2. Search for related information using different keywords/angles
3. Cross-reference against existing findings — do they agree?
4. Verify source authority using the Source Hierarchy
5. Identify remaining gaps — what is still unknown?
6. If gaps remain AND not diminishing returns — repeat from step 1
7. If no gaps OR diminishing returns — exit to synthesis

**Each iteration must change at least one of:**
- **Keywords** — search using different terms
- **Angle** — approach from a different perspective (practical vs theoretical, beginner vs advanced)
- **Source type** — move up or down the hierarchy for balance

**Exit:** Original question is answerable AND last 2 iterations found 0 new relevant facts.

### Phase 4: Synthesize

Connect findings into a coherent understanding.

For each subtopic identified during research:
- **Summarize** — what does the evidence say about this subtopic?
- **Weigh evidence** — which sources support each position? What are their hierarchy ranks?
- **Assign per-subtopic confidence** — High/Medium/Low for this specific subtopic

Then across all subtopics:
- Identify **patterns** — what do most sources agree on?
- Identify **contradictions** — where do sources disagree and why?
- Identify **gaps** — what's still unknown or uncertain?
- Identify **implications** — what are the practical consequences of each finding?
- Draw **conclusions** — what's the answer to the original question?
- Assign **overall confidence** — how certain are you of the final conclusion?

**Exit:** Coherent understanding exists with known confidence levels.

### Phase 5: Report

Output findings in the target format determined in Phase 1.

**Report format variants — use the one matching your Phase 1 output decision:**

| Phase 1 Format | Report Variant |
|----------------|----------------|
| `decision` | **Variant A: Decision Report** — compare options, recommend |
| `explainer` | **Variant B: Explainer** — explain how something works |
| `comparison` | **Variant C: Comparison** — side-by-side comparison |
| `detailed-report` | **Variant D: Detailed Research Report** — comprehensive deep-dive |

**Variant A: Decision Report** (for "which to choose" questions)
```
## Research: [Topic]

**Question:** [Original question]
**Confidence:** [High/Medium/Low]

### Summary
[2-3 sentence answer with recommendation]

### Options Considered
- **[Option 1]** — Pros, cons, when to use. Sources: [A, B]. Confidence: High
- **[Option 2]** — Pros, cons, when to use. Sources: [C]. Confidence: Medium

### Key Trade-offs
- [Dimension 1]: Option 1 wins because...
- [Dimension 2]: Option 2 wins because...

### Recommendation
[Clear recommendation with rationale]

### Open Questions
- [What's still uncertain]

### Sources
1. [Source name] — [URL] — [Rank in hierarchy]
```

**Variant B: Explainer** (for "how does X work" questions)
```
## Research: How [Topic] Works

**Question:** [Original question]
**Confidence:** [High/Medium/Low]

### Core Concept
[1-2 sentence fundamental idea]

### How It Works (Step by Step)
1. [Step 1] — [Detail]. Source: [A]
2. [Step 2] — [Detail]. Source: [A], [B]
3. [Step 3] — [Detail]. Source: [C]

### Key Components
- **[Component 1]:** What it does. How it fits. Confidence: High
- **[Component 2]:** What it does. How it fits. Confidence: Medium

### Open Questions
- [What's still unknown or debated]

### Sources
1. [Source name] — [URL] — [Rank in hierarchy]
```

**Variant C: Comparison** (for "X vs Y" questions)
```
## Research: [A] vs [B]

**Question:** [Original question]
**Confidence:** [High/Medium/Low]

### Summary
[2-3 sentence conclusion]

### Comparison
| Dimension | [A] | [B] | Winner |
|-----------|-----|-----|--------|
| [Dim 1] | ... | ... | [A/B] |
| [Dim 2] | ... | ... | [A/B] |

### When to Choose Each
- **Choose [A] when:** [Conditions]. Sources: [A], [B]
- **Choose [B] when:** [Conditions]. Sources: [C], [D]

### Open Questions
- [What's still uncertain]

### Sources
1. [Source name] — [URL] — [Rank in hierarchy]
```

**Variant D: Detailed Research Report** (for comprehensive understanding, use when Phase 1 output format is `detailed-report`)
```
## Research: [Topic]

**Question:** [Original question]
**Overall Confidence:** [High/Medium/Low]

### Executive Summary
[2-3 paragraph condensed answer covering the main question, key findings, and bottom-line conclusions]

### Background & Context
- Why this question matters
- Scope of the research (what was investigated and what was excluded)
- Key subtopics explored

### Detailed Findings by Subtopic

For each subtopic investigated, repeat this block:

#### Subtopic: [Name]
- **Evidence:** [What the sources say]
- **Supporting Sources:** [Source A — Rank 1, Source B — Rank 3]
- **Contradicting Sources:** [Source C — Rank 4, if any]
- **Confidence:** High / Medium / Low
- **Remaining Uncertainty:** [What's still unclear]

### Analysis & Synthesis
- **Patterns:** [What most sources agree on]
- **Contradictions:** [Where sources disagree and why — note vendor bias if present]
- **Gaps:** [What's still unknown or insufficiently covered]

### Implications
- [Practical consequence 1]
- [Practical consequence 2]

### Recommendations
- [Actionable conclusion 1 based on evidence]
- [Actionable conclusion 2 based on evidence]

### Open Questions & Future Research
- [Question 1 — what would resolve remaining uncertainty]
- [Question 2 — adjacent topics worth exploring]

### Conclusion
[Final paragraph tying everything together]

### Sources
1. [Source name] — [URL] — [Rank in hierarchy]
2. [Source name] — [URL] — [Rank in hierarchy]
```

**Exit:** Deliverable matches the format defined in Phase 1.

## Source Hierarchy

| Rank | Source Type | Examples |
|------|-------------|---------|
| 1 | Official documentation | MDN, docs.python.org, RFCs |
| 1a | Peer-reviewed / academic | Papers, journals, IEEE (tier 1 for academic research topics; tier 2 for technical/software research) |
| 3 | Authoritative references | O'Reilly books, Wikipedia (starting point) |
| 4 | Well-maintained tutorials | DigitalOcean, AWS blogs, official examples |
| 5 | Community knowledge | Stack Overflow, GitHub discussions |
| 6 | Opinion / anecdotal | Blog posts, Reddit, personal sites |

**Minimum standard:** 2+ sources from rank 1-3 OR 3+ sources from rank 1-4 before considering a finding "verified."

**Vendor sources:** Recognize bias. If a company blog compares their product to a competitor, note the conflict of interest and seek independent sources.

## Confidence Rubric

| Level | Criteria |
|-------|----------|
| High | 2+ sources from rank 1 agree, or 3+ from rank 1-3 |
| Medium | 2+ sources from rank 2-4 agree |
| Low | Single source or only rank 5-6 sources |
| Unknown | No reliable sources found — flag as open question |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Answering from memory without verification | Search anyway — verify even what you "know" |
| Stopping at the first source | Apply the Stop Rule — 2+ authoritative sources minimum |
| Presenting forum opinions as fact | Use Source Hierarchy — rank every source |
| One-and-done search | Run the Deepen loop — change keywords/angles each iteration |
| Skipping synthesis | Phase 4 is not optional — connect the dots |
| Overconfident conclusions | Use confidence rubric — be explicit about uncertainty |
| Treating search snippets as full content | Fetch full articles before citing |
| Not checking for vendor bias | Cross-reference company blogs with independent sources |

## Quick Reference

### Stop Rule Check
- [ ] Can I answer the question with 2+ authoritative sources?
- [ ] Did my last 2 deepen iterations find 0 new facts that materially change the answer?
- [ ] Both YES — stop. Otherwise — keep deepening.

### Source Evaluation
- [ ] What rank is this source in the hierarchy?
- [ ] Is this a vendor source with bias?
- [ ] Do other sources agree/disagree?
- [ ] Is the information current?

### Report Variants
- Use **Variant A (Decision Report)** for "which to choose" questions
- Use **Variant B (Explainer)** for "how does X work" questions
- Use **Variant C (Comparison)** for "X vs Y" questions
- Use **Variant D (Detailed Research Report)** for comprehensive deep-dives requiring per-subtopic findings, synthesis, and actionable recommendations
