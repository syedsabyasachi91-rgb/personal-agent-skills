# 🚀 Personal Agent Skills

> A collection of specialized **AI agent skills** — tested, production-ready workflows for code analysis, research, implementation review, and content generation. Each skill is a self-contained `SKILL.md` plus optional tests and evaluation data.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Skills Directory](#-skills-directory)
- [Getting Started](#-getting-started)
- [Skill Categories](#-skill-categories)
- [Repository Structure](#-repository-structure)
- [How Skills Work](#-how-skills-work)
- [Quality Assurance](#-quality-assurance)
- [Contributing](#-contributing)
- [Quick Links](#-quick-links)

---

## 🎯 Overview

This repository contains **12 specialized skills** that extend AI agent capabilities across multiple domains:

- **Code Analysis** — Search, review, and understand existing codebases
- **Research & Learning** — Efficiently gather information from web, docs, and GitHub
- **Implementation Workflows** — Structured processes for requirements gathering, implementation, and review
- **Document & Content** — Read docs systematically and turn papers into explainers
- **Skill Maintenance** — Safely edit existing skills without breaking tested behavior
- **Domain-Specific Knowledge** — Specialized API knowledge (CoinDCX Futures)

Each skill includes:
- ✅ A YAML frontmatter `description` defining precise trigger conditions
- ✅ Step-by-step workflow phases
- ✅ Red flag warnings and common-mistake tables
- ✅ Test scenarios and evaluation data where applicable

---

## 📚 Skills Directory

### Code Analysis & Understanding

| Skill | Purpose |
|-------|---------|
| **[Codebase Search Funnel](codebase-search-funnel/SKILL.md)** | Find code elements (definitions, usages, patterns, config) efficiently in any codebase using a 5-phase funnel that prevents missed results and noise. |
| **[Finding Dead Code](finding-dead-code/SKILL.md)** | Detect, score, and safely remove unused code in Python, JS/TS, and HTML (including embedded code) using `pyflakes`, `vulture`, `eslint`, etc. |
| **[Code Review](code-review/SKILL.md)** | Perform focused code reviews with structured 6-dimension feedback (correctness, security, performance, etc.) on shared snippets or PR diffs. |

### Research & Information Gathering

| Skill | Purpose |
|-------|---------|
| **[Research Funnel](research-funnel/SKILL.md)** | Conduct deep, multi-source research using iterative deepening with a strict stop rule (2+ independent sources + diminishing returns). |
| **[Web Fetching](web-fetching/SKILL.md)** | Retrieve web content reliably via `webfetch` and perform web searches using search-engine URLs (since `websearch` is not available). |
| **[GitHub Finder](github-finder/SKILL.md)** | Search GitHub (repos, code, issues, users, topics) with tiered fallback: `gh` CLI → REST API → web search. |
| **[Document Reader](document-reader/SKILL.md)** | Read documentation files completely to extract endpoints, schemas, auth, and error codes — never summarize from a partial read. |

### Implementation & Review Workflows

| Skill | Purpose |
|-------|---------|
| **[Requirements Gathering](requirements-gathering/SKILL.md)** | Clarify project needs through one-at-a-time questioning across 8 categories, then synthesize and confirm before implementation. |
| **[Reviewing Implementation](reviewing-implementation/SKILL.md)** | Verify a code change correctly implements all tasks and acceptance criteria from a plan, using a fresh subagent to avoid bias. |
| **[Modifying Skills](modifying-skills/SKILL.md)** | Edit existing skills safely using READ → INVENTORY → CHANGE → REGRESS → VERIFY — never break tested behavior. |

### Document & Content Workflows

| Skill | Purpose |
|-------|---------|
| **[Paper to Explainer](paper-to-explainer/SKILL.md)** | Turn any research paper (PDF, URL, or arXiv ID) into a structured markdown explainer with LaTeX equations, then convert to DOCX. |

### Domain-Specific Knowledge

| Skill | Purpose |
|-------|---------|
| **[CoinDCX Futures API](coindcx-api/SKILL.md)** | Perpetual futures trading via CoinDCX — REST endpoints, WebSocket connections, HMAC authentication, order management. |

---

## 🚀 Getting Started

### Using a Skill

1. **Identify the right skill** — Match your task to the skill descriptions and frontmatter `description:` blocks above
2. **Read the SKILL.md** — Each folder contains the full workflow
3. **Follow the phases** — Skills are organized into numbered steps
4. **Reference examples** — Most skills include concrete examples and templates

### Example Workflows

**Finding unused code in a Python project:**
```bash
# Trigger the "Finding Dead Code" skill
# Phase 1: Run python -m pyflakes . && vulture .
# Phase 2-4: Cross-reference, filter false positives, score confidence
# Phase 6: Safe removal with git stash backup and dry-run
```

**Researching a new technology:**
```bash
# Use the "Research Funnel" skill
# Phase 1: Frame the question precisely
# Phase 2-3: Explore 5+ sources from 3+ angles, then deepen
# Stop rule: 2+ independent sources AND diminishing returns
```

**Verifying an implementation matches its plan:**
```bash
# Use the "Reviewing Implementation" skill
# Provide plan path + BASE_SHA + HEAD_SHA
# A fresh subagent checks every plan task and acceptance criterion
```

**Turning a research paper into an explainer:**
```bash
# Use the "Paper to Explainer" skill
python skills/paper-to-explainer/extract_pdf.py "paper.pdf"          # extract text
# Edit the generated explainer in your preferred markdown editor
python skills/paper-to-explainer/convert_to_docx.py --input paper.md  # produce .docx
```

---

## 🏗️ Skill Categories

### By Use Case

**👨‍💻 For Developers:**
- Codebase Search Funnel
- Code Review
- Finding Dead Code

**🔍 For Researchers:**
- Research Funnel
- Web Fetching
- Document Reader
- GitHub Finder

**📋 For Project Management:**
- Requirements Gathering
- Reviewing Implementation
- Modifying Skills

**📄 For Content / Knowledge Work:**
- Paper to Explainer
- Document Reader

**💼 For API Integration:**
- CoinDCX Futures API
- Document Reader

### By Depth

**Quick Reference** (< 5 minutes):
- Web Fetching
- CoinDCX Futures API
- Finding Dead Code (detection phase)

**Medium Workflow** (15–30 minutes):
- Code Review
- Codebase Search Funnel
- Document Reader
- Paper to Explainer (after extraction)
- Modifying Skills (single edit)

**Deep Process** (45+ minutes):
- Research Funnel
- Requirements Gathering
- Reviewing Implementation
- Paper to Explainer (full paper)

---

## 📂 Repository Structure

```
.
├── README.md                                # This file
│
├── code-review/
│   ├── SKILL.md
│   └── test-scenarios.md
│
├── codebase-search-funnel/
│   ├── SKILL.md
│   └── tests/                               # Baseline + embedded-scenario tests
│
├── finding-dead-code/
│   └── SKILL.md
│
├── github-finder/
│   ├── SKILL.md
│   └── evals/                               # Evaluation data
│
├── document-reader/
│   ├── SKILL.md
│   └── tests/                               # Baselines, green, scenario coverage, fixtures
│
├── requirements-gathering/
│   ├── SKILL.md
│   ├── baseline-observed.md                 # Reference observations
│   └── test-scenarios.md
│
├── reviewing-implementation/
│   ├── SKILL.md
│   ├── reviewer-prompt.md                   # Template for subagent review
│   └── evals/                               # Evaluation data
│
├── modifying-skills/
│   ├── SKILL.md
│   └── test-scenarios.md
│
├── paper-to-explainer/
│   ├── SKILL.md
│   ├── extract_pdf.py                       # PDF → text extraction
│   └── convert_to_docx.py                   # Markdown → Word .docx
│
├── research-funnel/
│   └── SKILL.md
│
├── web-fetching/
│   ├── SKILL.md
│   └── test-scenarios.md
│
└── coindcx-api/
    ├── SKILL.md
    └── references/                          # API endpoint documentation
```

---

## 🎓 How Skills Work

Each skill is designed around a **frontmatter-driven trigger model**:

1. **Trigger** — YAML `description:` block defines precise conditions for when the skill fires
2. **Phases** — Step-by-step process to complete the task
3. **Tools & Patterns** — Specific techniques, commands, and templates
4. **Red Flags** — Warnings about common rationalizations that lead to failure
5. **Examples** — Real-world scenarios and worked walkthroughs

### Example: Codebase Search Funnel

```
Phase 0: Frame       → Identify search type (definition, usage, pattern, config, file, embedded)
Phase 1: Scope       → Narrow dirs, file types, include/exclude tests
Phase 2: Execute     → Pick tool (glob, rg/grep, task) and use context flags
Phase 3: Filter      → Remove noise and false positives
Phase 4: Context     → Include surrounding code (-C 3 to -C 5)
Phase 5: Verify      → Confirm results match the original intent
```

---

## ✅ Quality Assurance

Skills in this repo have been:
- ✅ Tested with multiple scenarios (see `tests/`, `test-scenarios.md`, `evals/`)
- ✅ Evaluated for effectiveness against baselines
- ✅ Documented with red-flag warnings for common rationalizations
- ✅ Structured around phase-based workflows

Before modifying any skill, run the [Modifying Skills](modifying-skills/SKILL.md) workflow — it enforces regression testing of existing behavior.

---

## 🤝 Contributing

### Adding a New Skill

1. Create a new folder: `your-skill-name/`
2. Write `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: >
     Clear, one-sentence description of when to use this skill
   ---
   ```
3. Structure with phases, examples, and red flags
4. Add test scenarios: `test-scenarios.md`
5. Include reference docs or evaluation data if applicable
6. Submit via pull request

### Modifying Existing Skills

Use the [Modifying Skills](modifying-skills/SKILL.md) skill. It enforces:
- Regression testing of existing behavior
- YAML frontmatter safety (the `description:` controls trigger conditions)
- Change inventory tracking
- No breaking changes to tested workflows

---

## 🔗 Quick Links

- **Finding code?** → [Codebase Search Funnel](codebase-search-funnel/SKILL.md)
- **Removing unused code?** → [Finding Dead Code](finding-dead-code/SKILL.md)
- **Reviewing a snippet?** → [Code Review](code-review/SKILL.md)
- **Verifying work matches a plan?** → [Reviewing Implementation](reviewing-implementation/SKILL.md)
- **Gathering requirements?** → [Requirements Gathering](requirements-gathering/SKILL.md)
- **Researching a topic?** → [Research Funnel](research-funnel/SKILL.md)
- **Fetching a URL or searching the web?** → [Web Fetching](web-fetching/SKILL.md)
- **Searching GitHub?** → [GitHub Finder](github-finder/SKILL.md)
- **Reading API docs?** → [Document Reader](document-reader/SKILL.md)
- **Explaining a research paper?** → [Paper to Explainer](paper-to-explainer/SKILL.md)
- **Editing another skill?** → [Modifying Skills](modifying-skills/SKILL.md)
- **Working with CoinDCX Futures?** → [CoinDCX API](coindcx-api/SKILL.md)

---

**Made for AI agents. Built for developers. Tested for reliability.** 🚀
