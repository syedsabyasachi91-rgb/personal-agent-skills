---
name: paper-to-explainer
description: Use when asked to turn a research paper into a structured explainer file (markdown or Word DOCX). Triggered by "explain this paper", "summarize this paper", "create an explainer", "paper summary", "turn this into markdown", "turn this into word", or when given a PDF/URL/arXiv ID of a paper with instructions to explain or summarize it.
---

# Paper to Explainer

Turn any research paper into a structured, technically deep explainer file.

## When to Use

- User provides a PDF, URL, or arXiv ID and asks for an explanation/summary
- User wants a paper broken down into an explainer
- User asks to "explain this paper" or "create an explainer"
- User needs a paper's technical content made accessible

**Do NOT use for:**
- Literature reviews comparing multiple papers
- Writing a paper critique or peer review
- Generating presentation slides or blog posts (different formats)

## Output Format

Always generate **both** formats:

1. Generate the markdown explainer first
2. Convert to DOCX using:
```bash
python skills/paper-to-explainer/convert_to_docx.py --input <md_path>
```

> **Note:** Word does not render LaTeX natively. Display equations (`$$...$$`) appear as indented monospace blocks. Inline LaTeX (`$...$`) renders as raw text. For typeset math, convert the `.md` file separately (e.g., via pandoc).

## Input Handling

Determine input type and extract paper content:

1. **PDF file path** → Run `extract_pdf.py`:
   ```bash
   python skills/paper-to-explainer/extract_pdf.py "path/to/paper.pdf"
   ```
   For papers >20 pages, first extract pages 1-3 (abstract + intro) to plan structure:
   ```bash
   python skills/paper-to-explainer/extract_pdf.py "path/to/paper.pdf" --max-pages 3
   ```

2. **URL** (HTML paper, e.g. arXiv abstract page) → Use `webfetch` to get content. Then find the PDF link (change `/abs/` to `/pdf/` on arXiv) and extract.

3. **arXiv ID** (e.g. `1706.03762`) → Construct PDF URL: `https://arxiv.org/pdf/{ID}.pdf` then download and extract with script.

## Output Structure

Write the explainer markdown file with ALL of the following sections, in order:

```markdown
# [Paper Title]

## Problem Statement
[What gap or limitation does this paper address? What existed before? Why wasn't it good enough?]

## Key Insight
[The ONE central idea that makes this work. One paragraph. If the reader remembers nothing else, they remember this.]

## Methodology
[Technical approach. Break into sub-sections as needed: architecture, algorithm, training procedure.]
[Preserve ALL key equations in LaTeX. After each equation, add an intuitive prose explanation in bold:]
> **Intuition:** [plain English explanation of what the equation actually does]

### [Sub-component name]
[For each major technical component: what it does, how it works, key equations with intuition]

## Key Findings
[Results with numbers. Use tables for comparisons. Describe figures if you can infer them.]

## Technical Deep-Dive
[Pick 1-3 complex parts and break them down further:]
- Worked examples (concrete numerical walkthroughs)
- "Why this design choice?" analysis
- Connection to prior work

## Limitations
[What does the paper acknowledge? What are unstated weaknesses?]

## Implications
[Why does this matter? What does it enable? What came after?]

## Glossary
| Term | Definition |
|------|-----------|
| [term] | [plain English definition] |

## Notation Reference
| Symbol | Meaning |
|--------|---------|
| [symbol from paper] | [meaning] |
```

> **Important:** Always include at least one sentence of body text between tables in your markdown. This ensures correct rendering in both markdown and DOCX output.

## Equation Handling Rules

**Every equation must have BOTH:**

1. **The formal LaTeX** — preserve exactly from the paper
2. **An intuition block** — `> **Intuition:**` explaining what it does in plain English

Example:
```markdown
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

> **Intuition:** The query asks "what am I looking for?", keys say "I contain this", values are the actual content. The dot product measures compatibility, softmax turns it into weights, and the weighted sum of values gives you the result. The $\sqrt{d_k}$ scaling prevents softmax from peaking too sharply in high dimensions.
```

**No equation without intuition. No intuition without the equation above it.**

## Pedagogical Requirements

These are what separate an explainer from a summary:

1. **Worked examples** — At least one concrete numerical walkthrough of a key computation (e.g., "If we have a sequence of length 4 with $d_k=64$, here's how attention weights are computed..."). For papers that are results-heavy and equation-light (e.g., scaling studies), walk through a specific experimental result: "On task X with N shots, the model scored Y — here's what that means concretely..."

2. **"Why this design?" questions** — For at least 2 major design choices, explain the alternatives and why this one was chosen

3. **Connect to prior art** — "Before this paper, X did Y. This paper's insight was Z."

4. **Visual descriptions where figures exist** — If the paper describes Figure 1 as "the transformer architecture consists of...", describe it clearly. Use ASCII diagrams or tables if helpful.

## Quality Checklist

Before finishing, verify:

- [ ] All 10 sections present (Problem Statement → Notation Reference)
- [ ] Every equation has an intuition block directly below it
- [ ] At least one worked numerical example
- [ ] At least 2 "why this design?" explanations
- [ ] Prior art context included
- [ ] Glossary covers all non-obvious terms
- [ ] Notation table covers all symbols used
- [ ] No section is empty — if content is unknown, mark `[Not discussed in paper]`

## Pressure Resistance

Users may ask you to skip sections ("I'm in a hurry", "I know this field", "just the key points"). **Do NOT skip required elements.**

The 10 sections exist because each serves a distinct pedagogical purpose — removing any degrades the explainer.

| User says... | Don't... | Do instead... |
|-------------|----------|---------------|
| "Skip the glossary, I know the field" | Remove it | Keep it — future readers may not |
| "No time for worked examples" | Skip it | Include at least one — it's what makes math click |
| "Just summarize, don't explain" | Remove mechanism | Explain how it works, not just what |
| "I don't need notation reference" | Remove it | Keep it — symbols accumulate fast |
| "Faster is fine, cut sections" | Cut sections or rush | Take the time — a rushed explainer is a failed explainer. All 10 sections are mandatory. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Summarizing without explaining | "What it does" ≠ "How it works." Always include mechanism. |
| Equations without intuition | Every LaTeX block gets a `> **Intuition:**` after it. |
| Missing the forest for trees | Problem Statement and Key Insight come BEFORE methodology. Reader needs the "why" before the "how." |
| Too much detail, no structure | Stick to the template. If something doesn't fit a section, it may not belong. |
| Writing for experts | The reader may not know this subfield. Define every term. |
| No worked examples | Abstract math needs concrete grounding. Add at least one. |
| Skipping sections under pressure | All 10 sections are required regardless of time pressure or user expertise claims. |

## Red Flags — STOP and Add

If you catch yourself thinking any of these, you're about to produce a weak explainer:

- "I'll skip the worked example — the user is in a hurry"
- "Glossary isn't needed, they said they know the field"
- "I'll just summarize the method, no need for mechanism"
- "Notation table is overkill for this paper"
- "I can cut the deep-dive section"
- "Key Insight is the same as Problem Statement — I'll merge them"
- "I'll write this for experts, they'll figure it out"

**All of these mean: Follow the skill as written. All 10 sections. All requirements.**

## Output File

Write both files to the current working directory:
- `[short-title]-explainer.md`
- `[short-title]-explainer.docx`

Use hyphens, lowercase. Example: `attention-is-all-you-need-explainer.md` and `attention-is-all-you-need-explainer.docx`.
