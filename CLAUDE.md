# CLAUDE.md

## Repository Structure

```
data/         Raw data (RDS files, local only, .gitignore)
scripts/      Python analysis scripts
knowledge/    Promptotyping documents (see below)
docs/         GitHub Pages output (HTML, plots, CSVs)
```

**Workflow:**
1. Python scripts process `data/` locally
2. Results exported to `docs/`
3. `docs/` published via GitHub Pages
4. Raw data never committed (synthetic data only for development)

## Promptotyping Methodology

This project follows the Promptotyping method, a four-phase iterative context engineering workflow for developing research artifacts with frontier LLMs.

### Phases

**Preparation** collects raw materials before technical decisions. Data files, documentation, research questions, and domain knowledge.

**Exploration and Mapping** probes the interface between data and research context. Central question: Can research questions be mapped onto the data structure? Negative findings are equally valuable.

**Destillation** compresses the acquired context into Markdown documents (Promptotyping Documents). Core principle is context compression, meaning maximum information with minimal tokens.

**Implementation** hands the documents to the LLM and begins iterative development. The critical expert validates results. New knowledge flows back into documentation.

### Promptotyping Documents

The `knowledge/` folder contains the project's knowledge base.

| Document | Purpose |
|----------|---------|
| `data.md` | Data structure, variables, limitations, quality notes |
| `research.md` | Domain knowledge, research questions, methodological decisions |
| `requirements.md` | User stories, acceptance criteria, technology stack |
| `journal.md` | Process documentation, decisions, dead ends, insights |

Before generating code, read the relevant documents in `knowledge/`. When implementation produces new insights, update the documentation. The documents are the source of truth, code is a disposable artifact.

## Working Principles

Read `knowledge/` documents before writing code.

Document decisions and findings in `journal.md`.

Update `data.md` when discovering new data characteristics.

Save scripts to `scripts/`, outputs to `docs/` for GitHub Pages publication.

When uncertain about research context, consult `research.md` or ask.

The documents are the source of truth. Code is a disposable artifact.