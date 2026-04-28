---
name: literature-search
description: Search, screen, and compare research papers with arXiv and Semantic Scholar APIs. Use when Codex needs to do literature review, 论文检索, related-work discovery, survey scoping, seed-paper expansion, paper metadata collection, or reproducible academic search workflows for a topic, author, venue, or research question.
---

# Literature Search

## Overview

Use this skill to turn an open-ended paper request into a reproducible search workflow. Prefer arXiv for recent preprints and category filters. Prefer Semantic Scholar for citation-aware metadata and recommendation expansion from seed papers.

## Workflow

1. Define the search target before calling any API.
   Capture the topic, synonyms, year range, must-have constraints, exclusions, preferred venues, and expected number of papers.
2. Choose the right source first.
   Use arXiv when the request emphasizes recent work, preprints, categories, or direct PDF access.
   Use Semantic Scholar bulk search when the request emphasizes broader recall, structured filters, or citation metadata.
   Use Semantic Scholar recommendations only after identifying 2-5 good seed papers.
3. Run a broad pass, then narrow.
   Start with a high-recall query.
   Refine with field filters, date ranges, category filters, or author constraints after inspecting the first batch.
4. Normalize the output immediately.
   Keep title, authors, year, venue or category, abstract, canonical URL, PDF URL, citation count, and source-specific IDs.
   Deduplicate by DOI first, then by Semantic Scholar paperId or arXiv ID, then by normalized title.
5. Synthesize the result set for the user.
   Separate seminal papers, recent papers, and obvious follow-up queries.
   Record the exact query text, API, date, and filters so the search is reproducible.

## Query Strategy

- Expand the topic into synonyms before searching.
  Example: "RAG" should usually also search "retrieval-augmented generation" and "retrieval augmented generation".
- Use exact phrases when a concept is easily diluted by broad keyword matching.
- For arXiv, prefer explicit field prefixes such as `ti`, `au`, `abs`, `cat`, and `all`.
- For Semantic Scholar bulk search, start with `query` plus only the fields you actually need; add `year`, `venue`, `fieldsOfStudy`, or `minCitationCount` later.
- Run recommendation expansion only after the first screening pass, otherwise the graph will amplify noisy seeds.

## Output Expectations

Return a concise search log and a ranked paper list. If the user asks for a mini-survey or related-work section, group papers by subtopic, method family, or chronology instead of returning a flat dump.

## Scripts

### `scripts/arxiv_search.py`

Query the arXiv Atom API and emit normalized JSON or Markdown.

Example:

```bash
python3 scripts/arxiv_search.py \
  --query 'ti:"retrieval augmented generation" AND cat:cs.CL' \
  --max-results 10 \
  --sort-by submittedDate \
  --sort-order descending \
  --format markdown
```

### `scripts/semantic_scholar_search.py`

Query Semantic Scholar paper bulk search. This is the default Semantic Scholar entry point in this skill because the official tutorial recommends bulk search for most discovery tasks.

Example:

```bash
python3 scripts/semantic_scholar_search.py \
  '"retrieval augmented generation"' \
  --year 2023- \
  --sort publicationDate:desc \
  --fields 'title,year,abstract,url,authors,citationCount,publicationDate,openAccessPdf'
```

### `scripts/semantic_scholar_recommend.py`

Expand from seed papers with positive and optional negative paper IDs.

Example:

```bash
python3 scripts/semantic_scholar_recommend.py \
  --positive-paper-id 649def34f8be52c8b66281af98ae884c09aef38b \
  --positive-paper-id 02138d6d094d1e7511c157f0b1a3dd4e5b20ebee \
  --limit 20 \
  --format markdown
```

## References

- Read `references/arxiv-api.md` when you need field prefixes, pagination limits, or Atom response details.
- Read `references/semantic-scholar-api.md` when you need query parameters, authentication guidance, pagination differences, or usage restrictions.

## Guardrails

- Re-check the official docs before editing the scripts if an endpoint starts returning validation errors. These APIs evolve.
- Keep requested field lists small on Semantic Scholar to reduce latency and rate-limit pressure.
- Avoid huge arXiv slices. Prefer refined queries over brute-force harvesting.
- Respect licensing and usage rules, especially for Semantic Scholar public or commercial usage.
