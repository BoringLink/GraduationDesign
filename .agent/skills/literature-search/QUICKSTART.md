# Quick Start Guide - Literature Search Skill

## One-Minute Setup

### 1. Install Dependencies

```bash
pip install requests feedparser
```

### 2. Set Semantic Scholar API Key (Optional)

```bash
export SEMANTIC_SCHOLAR_KEY="IlA3rQ62vP2P6gCYgzcG51zRTbhrAhal59RGpaY8"
```

Or add to `.bashrc`/`.zshrc` for permanent setup.

### 3. Test the Skill

```bash
cd /Users/tk/.agents/skills/literature-search
bash run_evals.sh
```

Expected output: 3 passing tests, results saved to `outputs/`

## Common Use Cases

### Search for Papers on a Topic

```python
from scripts.combined_search import LiteratureSearcher

searcher = LiteratureSearcher(output_dir="./my_papers")

results = searcher.search(
    keywords="transformer attention",
    year_min=2020,
    year_max=2024,
    output_format="markdown"
)
```

**Result**: `my_papers/papers_transformer_attention_*.md` ready for thesis

### Find Papers by Author

```python
results = searcher.search(
    keywords=["machine learning"],
    authors="Yoshua Bengio",
    year_min=2015,
    sources=["semantic"],
    output_format="json"
)
```

**Result**: JSON with structured author publication data

### Literature Review Search

```python
# Combine multiple searches for comprehensive coverage
keywords_list = [
    ["federated learning", "privacy"],
    ["federated learning", "communication"],
    ["distributed machine learning", "decentralization"],
]

for keywords in keywords_list:
    results = searcher.search(
        keywords=keywords,
        category="cs.LG",
        year_min=2019,
        output_format="markdown",
        save_to_file=True,
        output_dir="./literature_review"
    )
```

**Result**: Multiple markdown files in `literature_review/` for integration

## Output Locations

All search results are saved to the output directory with timestamps:

```
outputs/
├── papers_transformer_20240421_143022.md
├── papers_federated_learning_20240421_144015.json
└── ...
```

## Troubleshooting

### "No results found"

Try:
1. Use broader keywords: `"machine learning"` instead of `"meta-learning on graph neural networks"`
2. Remove year constraints
3. Try Semantic Scholar source: `sources=["semantic"]`

### API timeout

Add delay between searches:
```python
import time
time.sleep(5)  # Wait 5 seconds
```

### Missing Semantic Scholar data

Some papers may not be indexed in Semantic Scholar. Use both sources:
```python
sources=["arxiv", "semantic"]
```

## Next Steps

1. **Read**: `SKILL.md` for complete documentation
2. **Learn**: `references/query_examples.md` for advanced examples
3. **Configure**: `references/api_limits.md` for rate limiting details
4. **Explore**: `README.md` for integration options

## Support Resources

- arXiv API: https://arxiv.org/help/api/
- Semantic Scholar: https://www.semanticscholar.org/product/api
- Skill Documentation: See SKILL.md in this directory
