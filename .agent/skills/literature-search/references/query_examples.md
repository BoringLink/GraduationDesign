# Query Examples and Best Practices

## For Thesis Literature Reviews

### Example 1: Finding Recent Deep Learning Papers

**Use Case**: Writing thesis on deep learning applications in computer vision

```python
search(
    keywords=["deep learning", "convolutional neural networks"],
    category="cs.CV",
    year_min=2020,
    year_max=2024,
    sources=["arxiv", "semantic"],
    max_results=100,
    output_format="markdown",
    save_to_file=True,
)
```

**Why this works**:
- Specific keywords narrow results to relevant papers
- Year range ensures recent work
- cs.CV category filters to computer vision domain
- Both sources provide complementary data (preprints + published + citations)
- Markdown output ready for thesis integration

### Example 2: Finding Papers by Specific Authors

**Use Case**: Researching work from known pioneers in your field

```python
search(
    keywords=["reinforcement learning"],
    authors="Richard Sutton",
    sources=["semantic"],  # Semantic Scholar better for author discovery
    max_results=50,
    output_format="json",
)
```

### Example 3: Multi-Keyword Literature Review

**Use Case**: Comprehensive review combining multiple concepts

```python
search(
    keywords=["federated learning", "privacy", "decentralized"],
    category="cs.LG",
    year_min=2019,
    year_max=2024,
    sources=["arxiv"],  # More preprints in this active area
    max_results=150,
)
```

Then run additional searches:

```python
search(
    keywords=["federated learning", "communication efficiency"],
    category="cs.LG",
    year_min=2019,
    year_max=2024,
    sources=["semantic"],  # Get citation metrics for second pass
    max_results=100,
)
```

Combine results manually, removing duplicates.

## API Rate Limits and Considerations

### arXiv
- **Rate Limit**: ~2 requests per second
- **Delay**: Automatically enforced (3 seconds between requests)
- **Best For**: Preprints, recent work, large result sets
- **Note**: No API key required

### Semantic Scholar
- **Rate Limit**: 100 requests per 5 minutes (free tier)
- **API Key**: Optional (improves rate limits)
- **Delay**: Automatically enforced (1 second between requests)
- **Best For**: Published papers, citation metrics, rich metadata

### Strategy
1. **First Pass**: Use arXiv for keyword discovery (broader coverage)
2. **Second Pass**: Use Semantic Scholar for citation metrics
3. **Combine**: Merge results, dedup by title

## Query Construction Tips

### Effective Keywords
✅ **Good**: "transformer architecture", "attention mechanism", "BERT"
❌ **Avoid**: "AI", "deep learning" alone (too broad)

### Boolean Operators
- **AND**: Narrow results (both terms must appear)
  - Example: `["neural networks", "graph"]` → papers on graph neural networks
- **OR**: Broaden results (at least one term)
  - Example: `["CNN", "RNN"]` → convolutional OR recurrent networks

### Year Ranges
- **Last 2 years** (2022-2024): Latest methods and improvements
- **Last 5 years** (2019-2024): Established trends with maturity
- **Since 2015**: Major paradigm shifts (if looking for historical context)

### Category Selection
- **Single category** (cs.AI): Focused results
- **Multiple categories** (cs.AI + cs.LG): Broader coverage
- **None**: Searches across all arXiv (not recommended for active areas)

## Handling Large Result Sets

If a search returns 500+ papers:

1. **Narrow keywords**: Use more specific terms or combinations
2. **Tighten year range**: Focus on most recent work
3. **Use category filters**: Reduce noise
4. **Post-process results**: Filter by citation count, author reputation

## Saving and Organizing Results

### File Naming Convention
```
papers_KEYWORDS_YYYYMMDD_HHMMSS.md  # Auto-generated
papers_federated_learning_20240421_143022.md
```

### Directory Organization
```
./outputs/
├── literature_review/
│   ├── transformer_papers_2024.md
│   ├── attention_mechanisms_2024.md
│   └── nlp_survey_2024.md
└── specific_author/
    └── lecun_papers_all.json
```

## Troubleshooting

### "No results found"
- Check keyword spelling
- Try broader keywords or remove year constraints
- Verify category exists (see arxiv_categories.md)
- Try Semantic Scholar instead (better for some domains)

### "Too many results (>1000)"
- Add more specific keywords
- Narrow the year range
- Use author filters
- Split into multiple searches

### "API timeout"
- Increase delay between requests
- Reduce max_results per search
- Run searches sequentially instead of parallel

## Semantic Scholar Citation Metrics

When using Semantic Scholar, you get citation counts:
- **High citations** (>100): Well-cited influential papers
- **Medium citations** (10-100): Solid contributions
- **Low citations** (<10): Recent or niche papers

Use this to prioritize reading for thesis background.

## Example Workflow for Thesis

1. **Identify key concepts** from your thesis topic
2. **Run initial broad search** for each concept (arXiv)
3. **Save Markdown results** for easy reference
4. **Run targeted searches** by important authors
5. **Export to JSON** and import into reference manager (Zotero, Mendeley, etc.)
6. **Review citations** in Semantic Scholar results to find "hidden" influential papers
7. **Save final curated list** as structured JSON for analysis
