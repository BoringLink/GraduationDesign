# Literature Search Skill

Comprehensive academic paper discovery tool for thesis writing and research using arXiv and Semantic Scholar APIs.

## Quick Start

### Installation

1. **Prerequisites**
   ```bash
   pip install requests feedparser
   ```

2. **Optional: Semantic Scholar API Key**
   ```bash
   export SEMANTIC_SCHOLAR_KEY="your-api-key-here"
   # Get your key from: https://www.semanticscholar.org/product/api
   ```

### Basic Usage

```python
from scripts.combined_search import LiteratureSearcher

searcher = LiteratureSearcher(
    output_dir="./outputs",
    semantic_api_key="your-key-here"  # or None for free tier
)

# Simple search
results = searcher.search(
    keywords="deep learning",
    year_min=2020,
    year_max=2024,
    output_format="markdown"
)
```

### Command Line Usage

```bash
# Search for papers
python scripts/combined_search.py "deep learning" \
    --year-min 2020 \
    --year-max 2024 \
    --category cs.AI \
    --format markdown \
    --output-dir ./papers

# Search with author filter
python scripts/combined_search.py "federated learning" "privacy" \
    --authors "Yann LeCun" \
    --format json

# Search with Semantic Scholar only (for citation metrics)
python scripts/combined_search.py "transformer" \
    --sources semantic \
    --semantic-key "your-key" \
    --max-results 100
```

## Features

### Multi-Source Search
- **arXiv**: Fast, comprehensive preprint coverage in CS and physics
- **Semantic Scholar**: Citation metrics and influence scores
- **Combined**: Cross-reference for most complete results

### Flexible Filtering
- Keyword-based search (single or multiple)
- Author filtering
- Year range constraints
- Category/domain selection
- Source preference

### Multiple Output Formats
- **Markdown**: Human-readable, thesis-friendly
- **JSON**: Structured data with metadata
- **CSV**: Spreadsheet import
- **BibTeX**: Citation manager compatible

### Agent-Friendly Design
- Clear parameter interfaces
- Structured error handling
- Progress reporting
- Automatic local caching
- Designed for autonomous execution

## File Structure

```
literature-search/
├── SKILL.md                          # Main skill documentation
├── README.md                         # This file
├── scripts/
│   ├── combined_search.py            # Main orchestrator
│   ├── arxiv_searcher.py            # arXiv API client
│   ├── semantic_searcher.py         # Semantic Scholar client
│   └── result_formatter.py           # Output formatting
├── references/
│   ├── arxiv_categories.md          # Category reference
│   ├── query_examples.md            # Usage examples
│   └── api_limits.md                # Rate limits & configuration
├── evals/
│   └── evals.json                   # Test cases for skill
└── outputs/                         # Default directory for saved results
```

## Key Concepts

### Query Keywords
- Use specific, domain-relevant terms
- Combine multiple keywords with AND logic
- Examples: `["transformer", "attention"]`, `["federated learning", "privacy"]`

### Author Filtering
- Provide full or partial author names
- Case-insensitive matching
- Works across both API sources

### Category Selection
- arXiv uses hierarchical categories (e.g., `cs.AI`, `cs.LG`, `cs.CV`)
- See `references/arxiv_categories.md` for complete list
- Semantic Scholar uses general domains

### Output Formats
- **Markdown**: Best for thesis integration, human reading
- **JSON**: Best for programmatic use, citation analysis
- **CSV**: Best for spreadsheet applications
- **BibTeX**: Best for reference managers (Zotero, Mendeley)

## Examples

### Example 1: Thesis Literature Review

```python
searcher = LiteratureSearcher()

# Search for recent papers in your field
results = searcher.search(
    keywords=["neural networks", "deep learning"],
    category="cs.AI",
    year_min=2020,
    output_format="markdown",
    save_to_file=True
)

# Results saved to: outputs/papers_neural_networks_*.md
```

Output: Markdown file ready to integrate into thesis background section.

### Example 2: Author Publication History

```python
# Find all papers by a specific author
results = searcher.search(
    keywords=["machine learning"],  # Optional
    authors="Geoffrey Hinton",
    year_min=2010,
    sources=["semantic"],  # Semantic Scholar better for author discovery
    output_format="json",
    max_results=100
)
```

Output: JSON with structured author publication data.

### Example 3: Multi-Keyword Systematic Review

```python
# Comprehensive search on a topic
queries = [
    ["reinforcement learning", "policy gradient"],
    ["reinforcement learning", "Q-learning"],
    ["reinforcement learning", "actor-critic"],
]

all_results = []
for kw in queries:
    results = searcher.search(
        keywords=kw,
        category="cs.LG",
        year_min=2015,
        output_format="json"
    )
    all_results.extend(results["results"])

# Combine and deduplicate
# (deduplication handles in combined_search automatically)
```

## API Rate Limits

### arXiv
- ~2 requests/second (polite)
- 3-second delay enforced by default
- No API key required
- Free and unlimited

### Semantic Scholar
- 1 request/second (with API key)
- 100 requests/5 minutes (free tier)
- Optional API key for higher limits
- Free tier available

### Strategy
- Use both sources for comprehensive coverage
- arXiv for recent preprints
- Semantic Scholar for citation metrics
- Built-in caching minimizes redundant queries

## Error Handling

### Common Issues

**"No results found"**
- Try broader keywords
- Check spelling
- Remove or loosen year constraints
- Try different API sources

**"Rate limit exceeded"**
- Implemented automatic backoff
- Wait before retrying
- Consider API key for Semantic Scholar

**"Missing citations data"**
- Some papers may not have citation counts
- Use Semantic Scholar source for full metrics
- Check if paper is indexed in Semantic Scholar

## Customization

### Modify Default Settings

Edit `combined_search.py`:
```python
DEFAULT_CONFIG = {
    "arxiv": {
        "delay_seconds": 3.0,
        "max_results": 50,
    },
    "semantic": {
        "delay_seconds": 1.0,
        "max_results": 50,
    },
}
```

### Add New Output Formats

Add method to `ResultFormatter`:
```python
@staticmethod
def to_custom_format(papers: List[Dict]) -> str:
    # Your formatting logic
    return formatted_string
```

## Integration with Reference Managers

### Zotero
1. Search using `output_format="bibtex"`
2. Copy BibTeX output
3. Paste into Zotero as new collection

### Mendeley
1. Export as CSV
2. Import CSV file into Mendeley
3. Mendeley auto-fetches metadata

## Data Privacy & Ethics

- Results contain only published metadata
- No personal information beyond author names
- Complies with arXiv and Semantic Scholar ToS
- Suitable for academic research purposes

## Performance Tips

### Speed Up Searches
1. Use specific keywords (avoid very broad terms)
2. Limit year range
3. Use category filters
4. Set lower `max_results` if appropriate

### Reduce API Calls
1. Leverage built-in caching
2. Batch multiple searches
3. Reuse previous results when possible

### Memory Usage
1. Process results in batches if searching >500 papers
2. Enable file saving (auto-saves to disk)
3. Clear cache periodically

## Troubleshooting

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Configuration

```bash
python -c "from scripts import combined_search; print('Config OK')"
```

### Test Individual APIs

```bash
python scripts/arxiv_searcher.py --test
python scripts/semantic_searcher.py --test
```

## Contributing & Improvements

Future enhancements:
- [ ] Google Scholar integration (if permitted)
- [ ] PDF metadata extraction
- [ ] Citation network visualization
- [ ] Local SQLite caching for large result sets
- [ ] Batch processing for high-volume searches
- [ ] Integration with reference manager APIs

## License & Attribution

- Uses open APIs: arXiv, Semantic Scholar
- Respects API ToS and rate limits
- Suitable for academic and research use

## Support

For issues or questions:
1. Check `references/` documentation
2. Review error logs
3. Test with simple queries first
4. Verify API keys and network connectivity

## Links

- arXiv API: https://arxiv.org/help/api/
- Semantic Scholar API: https://www.semanticscholar.org/product/api
- feedparser docs: https://pythonhosted.org/feedparser/
