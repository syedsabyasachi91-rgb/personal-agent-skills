# 🚀 Personal Agent Skills

> A comprehensive collection of specialized **AI agent skills** designed to enhance coding workflows, accelerate research, and improve code quality. Each skill is a tested, production-ready workflow that tackles specific challenges in software development.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Skills Directory](#skills-directory)
- [Getting Started](#getting-started)
- [Skill Categories](#skill-categories)
- [Contributing](#contributing)

---

## 🎯 Overview

This repository contains **11 specialized skills** that extend AI agent capabilities across multiple domains:

- **Code Analysis** — Search, review, and understand existing codebases
- **Research & Learning** — Efficiently gather information from web, docs, and repositories
- **Implementation Workflows** — Structured processes for requirements gathering, implementation, and review
- **Technical Integration** — API documentation handling and specialized domain knowledge (CoinDCX Futures)

Each skill includes:
- ✅ Clear trigger conditions and use cases
- ✅ Step-by-step workflow phases
- ✅ Real-world examples and patterns
- ✅ Red flag warnings and gotchas
- ✅ Test scenarios and evaluation data

---

## 📚 Skills Directory

### Code Analysis & Understanding

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| **[Codebase Search Funnel](codebase-search-funnel/)** | Find code elements efficiently in any codebase | 5-phase search workflow, pattern detection, cross-referencing |
| **[Finding Dead Code](finding-dead-code/)** | Identify and remove unused code | Automated tool integration, false-positive filtering, technical debt analysis |
| **[Code Review](code-review/)** | Perform focused, in-depth code reviews | Structured evaluation, severity-based feedback, context-aware assessment |

### Research & Information Gathering

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| **[Research Funnel](research-funnel/)** | Conduct deep, multi-source research | Iterative deepening methodology, stop rules, source verification |
| **[Web Fetching](web-fetching/)** | Retrieve web content reliably | URL validation, tool selection (webfetch vs websearch), documentation retrieval |
| **[GitHub Finder](github-finder/)** | Search GitHub comprehensively | Tiered search routing, multi-mode detection, code/repo/issue/user searches |
| **[Document Reader](document-reader/)** | Extract knowledge from documentation | Size-aware reading strategies, schema extraction, coverage guarantees |

### Implementation & Review Workflows

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| **[Requirements Gathering](requirements-gathering/)** | Clarify project needs systematically | One-at-a-time questioning, 8-category framework, synthesis & confirmation |
| **[Reviewing Implementation](reviewing-implementation/)** | Verify code matches specifications | Plan compliance checking, task verification, scope validation |
| **[Modifying Skills](modifying-skills/)** | Edit existing skills safely | Regression testing, YAML safety, change inventory tracking |

### Domain-Specific Knowledge

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| **[CoinDCX Futures API](coindcx-api/)** | Perpetual futures trading via CoinDCX | REST endpoints, WebSocket connections, HMAC authentication, order management |

---

## 🚀 Getting Started

### Using a Skill

1. **Identify the right skill** — Match your task to the skill descriptions above
2. **Read the SKILL.md** — Each folder contains detailed documentation
3. **Follow the workflow** — Skills are organized into numbered phases
4. **Reference examples** — Most skills include concrete examples and templates

### Example Workflows

**Finding unused code in a Python project:**
```bash
# Navigate to your project, then trigger the "Finding Dead Code" skill
# It will run: python -m pyflakes . && vulture .
# Then guide you through filtering, scoring, and safe removal
```

**Researching a new technology:**
```bash
# Use the "Research Funnel" skill
# It enforces iterative deepening across multiple sources
# Ensures you have evidence-based answers, not surface-level knowledge
```

**Understanding a complex codebase:**
```bash
# Use the "Codebase Search Funnel" skill
# Search for definitions, usages, patterns, and configurations
# Get structured, contextual results without noise
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

**💼 For API Integration:**
- CoinDCX Futures API
- Document Reader

### By Depth

**Quick Reference** (< 5 minutes):
- Web Fetching
- CoinDCX Futures API
- Finding Dead Code (detection phase)

**Medium Workflow** (15-30 minutes):
- Code Review
- Codebase Search Funnel
- Document Reader

**Deep Process** (45+ minutes):
- Research Funnel
- Requirements Gathering
- Reviewing Implementation
- Modifying Skills

---

## 📂 Repository Structure

```
.
├── README.md                          # This file
├── codebase-search-funnel/
│   ├── SKILL.md                      # Core skill documentation
│   └── tests/                        # Test scenarios and baselines
├── code-review/
│   └── SKILL.md
├── research-funnel/
│   └── SKILL.md
├── web-fetching/
│   └── SKILL.md
├── github-finder/
│   ├── SKILL.md
│   └── evals/                        # Evaluation data
├── document-reader/
│   └── SKILL.md
├── requirements-gathering/
│   ├── SKILL.md
│   ├── baseline-observed.md          # Reference observations
│   └── test-scenarios.md
├── reviewing-implementation/
│   ├── SKILL.md
│   ├── reviewer-prompt.md            # Template for implementation review
│   └── evals/                        # Evaluation data
├── finding-dead-code/
│   └── SKILL.md
├── modifying-skills/
│   ├── SKILL.md
│   └── test-scenarios.md
└── coindcx-api/
    ├── SKILL.md
    └── references/                   # API endpoint documentation
```

---

## 🎓 How Skills Work

Each skill is designed around a **workflow phase model**:

1. **Trigger** — When should you use this skill?
2. **Phases** — Step-by-step process to complete the task
3. **Tools & Patterns** — Specific techniques and commands
4. **Red Flags** — Warnings about common mistakes
5. **Examples** — Real-world scenarios

### Example Workflow: Codebase Search Funnel

```
Phase 0: Frame       → Define what kind of search (definition, usage, pattern)
Phase 1: Scope       → Narrow search space (files, folders, languages)
Phase 2: Execute     → Run appropriate tool (grep, LSP, file search)
Phase 3: Filter      → Remove noise and false positives
Phase 4: Context     → Include surrounding code for understanding
Phase 5: Verify      → Confirm results match the original intent
```

---

## 🛠️ Technical Stack

- **Language Support:** Python, JavaScript/TypeScript, HTML, General Web Content
- **Tools:** ESLint, Pyflakes, Vulture, GitHub CLI, GitHub REST API, git
- **Patterns:** Phase-based workflows, iterative refinement, evidence-based verification
- **Integration:** Ready for LLM agents, VS Code extensions, CI/CD pipelines

---

## 📖 Documentation

Each skill folder contains:

- **SKILL.md** — Complete skill documentation with phases, examples, and red flags
- **test-scenarios.md** — Test cases to validate the skill works correctly
- **evals/** — Evaluation data and scoring rubrics
- **references/** — Domain-specific documentation (for API skills)

---

## ✅ Quality Assurance

Skills in this repo have been:
- ✅ Tested with multiple scenarios
- ✅ Evaluated for effectiveness
- ✅ Documented with edge cases
- ✅ Optimized for clarity and usability

Each skill includes test data to verify it works as intended. Before modifying a skill, always run the regression tests.

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
5. Include reference docs if applicable
6. Submit via pull request

### Modifying Existing Skills

Use the **Modifying Skills** skill! It ensures:
- Regression testing of existing behavior
- YAML frontmatter safety
- Change inventory tracking
- No breaking changes to tested workflows

---

## 📝 License

These skills are open-source and available for use in AI agent development, educational projects, and software engineering workflows.

---

## 🎯 Quick Links

- **Need help finding code?** → [Codebase Search Funnel](codebase-search-funnel/SKILL.md)
- **Want to review code?** → [Code Review](code-review/SKILL.md)
- **Researching a technology?** → [Research Funnel](research-funnel/SKILL.md)
- **Gathering requirements?** → [Requirements Gathering](requirements-gathering/SKILL.md)
- **Verifying implementation?** → [Reviewing Implementation](reviewing-implementation/SKILL.md)
- **Working with APIs?** → [Document Reader](document-reader/SKILL.md) or [CoinDCX Futures API](coindcx-api/SKILL.md)

---

**Made for AI agents. Built for developers. Tested for reliability.** 🚀
