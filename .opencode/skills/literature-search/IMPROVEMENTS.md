# Literature Search Skill - v1.0 Quality Improvements

## Rationale

This document captures potential quality improvements based on API best practices and common user feedback patterns for academic search tools. These are recommendations for v1.1 and beyond, not blockers for v1.0.

## Priority Matrix

### MUST FIX (Blocking v1.0 release)
- ✅ Both APIs functional and tested
- ✅ Error handling for common failures
- ✅ Rate limits respected
- ✅ Documentation complete and accurate

**Status**: All addressed in v1.0

### SHOULD FIX (For v1.0 or v1.1)

#### 1. Query Validation & Suggestions

**Current State**: Queries are sent directly to APIs without validation

**Improvement**: Add query validator before API calls
```python
class QueryValidator:
    def validate_keywords(keywords: List[str]) -> bool:
        # Check for empty keywords
        # Check for very short keywords (1-2 chars)
        # Warn about overly specific queries
        # Suggest alternatives
```

**Benefit**: Better error messages, faster feedback to users

**Effort**: 2-3 hours

---

#### 2. Result Deduplication Enhancement

**Current State**: Basic deduplication by arxiv_id + title matching

**Improvement**: Add fuzzy matching for titles (handles minor variations)
```python
from fuzzywuzzy import fuzz
def deduplicate_with_fuzzy(results, threshold=0.9):
    # Group similar titles together
    # Merge metadata from duplicate sources
    # Keep best (most cited) version
```

**Benefit**: Cleaner results, better data quality

**Effort**: 3-4 hours

---

#### 3. Advanced Filtering

**Current State**: Basic filters (year, category, author)

**Improvements**:
- Min/max citation count
- Peer-reviewed vs preprint
- Venue/conference filtering
- Impact factor ranges

**Example**:
```python
results = searcher.search(
    keywords=["deep learning"],
    min_citations=10,      # Only highly cited papers
    peer_reviewed=True,    # Skip preprints
    venues=["NeurIPS", "ICML", "ICLR"]
)
```

**Benefit**: More targeted literature reviews

**Effort**: 4-5 hours

---

#### 4. Batch Processing Mode

**Current State**: One search at a time

**Improvement**: Support multiple queries in one call
```python
queries = [
    {"keywords": ["federated learning"], "year_min": 2020},
    {"keywords": ["privacy preserving"], "year_min": 2019},
    {"keywords": ["distributed ML"], "year_min": 2018},
]
results = searcher.batch_search(queries)
```

**Benefit**: Process literature reviews faster, combine related searches

**Effort**: 2-3 hours

---

#### 5. Local Caching Layer

**Current State**: No caching, every search hits APIs

**Improvement**: SQLite cache with TTL
```python
class SearchCache:
    def get(query_hash: str) -> Optional[Results]:
        # Check cache expiry (e.g., 30 days)
        # Return cached results if fresh
    
    def put(query_hash: str, results: Results) -> None:
        # Store with timestamp
        # Automatically clean up old entries
```

**Benefit**: 
- Faster repeated searches
- Reduced API load
- Works offline for cached queries

**Effort**: 4-5 hours

**Note**: Requires SQLite dependency

---

#### 6. Citation Graph Exploration

**Current State**: Linear result list

**Improvement**: Traverse citation relationships
```python
results = searcher.search(...)
# Find papers that cite these results
citations_of = searcher.find_citations_of(results[0])
# Find papers cited by these results  
cited_by = searcher.find_cited_by(results[0])
```

**Benefit**: Discover related work and impact chains

**Effort**: 6-8 hours (requires graph algorithm knowledge)

**Note**: Semantic Scholar has citation API

---

### NICE-TO-HAVE (v1.2+)

#### 7. Web UI

Build simple web interface (Flask/FastAPI) for non-CLI users

#### 8. Google Scholar Integration

Add Google Scholar as third source (if ToS permits)

#### 9. PDF Metadata Extraction

Extract full-text metadata from papers for deeper analysis

#### 10. Email Digest Service

Subscribe to papers in topics, receive daily/weekly digest

---

## Recommended v1.1 Feature Set

Based on effort vs. impact analysis:

**High Impact, Low Effort** (DO THESE):
1. ✅ Query validation & suggestions
2. ✅ Batch processing
3. ✅ CSV/BibTeX export formats

**High Impact, Medium Effort** (CONSIDER):
1. Advanced filtering (citation count, venue, peer-reviewed)
2. Local caching layer
3. Better deduplication

**Medium Impact, High Effort** (DEFER):
1. Citation graph exploration
2. Web UI
3. Third-party API integrations

---

## v1.0 Known Limitations (By Design)

These are acceptable for v1.0, target for v1.1:

| Limitation | Workaround | v1.1 Plan |
|-----------|-----------|----------|
| Sequential searches only | Run searches manually one at a time | Batch processing |
| No result caching | Re-search takes full API time | SQLite cache with 30-day TTL |
| Author matching is fuzzy | Refine results manually | Semantic Scholar author IDs |
| arXiv lacks citation data | Use Semantic Scholar source | Merge both sources' data |
| Large result sets are slow | Use stricter filters | Add pagination support |
| No offline mode | Requires internet | Cache + offline mode |

---

## Code Quality Checklist for v1.1

Before releasing v1.1, ensure:

- [ ] 90%+ type hint coverage
- [ ] All public methods have docstrings with examples
- [ ] Unit test coverage >80%
- [ ] Error handling covers >95% of failure modes
- [ ] Documentation has worked examples for every feature
- [ ] Benchmark: search completes in <5 seconds
- [ ] Memory usage <100MB for typical search
- [ ] API rate limits never exceeded
- [ ] Circular imports resolved
- [ ] Dependencies pinned to specific versions

---

## Backward Compatibility

Changes for v1.0 → v1.1:

**Breaking Changes** (None expected)
- All new features are additive
- Existing parameter interfaces unchanged
- Default behavior identical

**Deprecated** (None)

**New in v1.1**:
- Batch processing (new method)
- Caching (transparent, opt-in)
- New filters (optional parameters)
- New output formats (optional)

This means v1.0 code will work unchanged with v1.1 library.

---

## Testing Strategy for v1.1

Add these test categories:

```
tests/
├── unit/
│   ├── test_arxiv_searcher.py
│   ├── test_semantic_searcher.py
│   ├── test_result_formatter.py
│   ├── test_query_validator.py    # NEW
│   └── test_search_cache.py       # NEW
├── integration/
│   ├── test_combined_search.py
│   ├── test_batch_processing.py   # NEW
│   └── test_caching_integration.py # NEW
└── e2e/
    ├── test_thesis_workflow.py     # NEW
    └── test_literature_review.py   # NEW
```

Target: 120+ test cases, all with realistic queries

---

## Timeline Estimate

- **v1.0 release**: 2026-04-21 ✅
- **v1.0 feedback period**: 2 weeks (user testing)
- **v1.1 development**: 3-4 weeks (new features)
- **v1.1 release**: ~2026-05-19 (target)

---

## Success Metrics for v1.1

| Metric | Target |
|--------|--------|
| User satisfaction | 4.5+/5 stars |
| Search speed | <3 sec avg |
| Result quality | 95%+ relevant |
| Error rate | <1% API calls |
| Documentation coverage | 100% of public APIs |
| Code maintainability | 8+/10 (by SonarQube) |

---

## Architecture Evolution

### v1.0 Architecture
```
combined_search.py (orchestrator)
├── arxiv_searcher.py
├── semantic_searcher.py
└── result_formatter.py
```

### v1.1 Planned Architecture
```
combined_search.py (orchestrator)
├── arxiv_searcher.py
├── semantic_searcher.py
├── result_formatter.py
├── query_validator.py        # NEW
├── search_cache.py           # NEW
├── deduplicator.py           # NEW
└── citation_explorer.py      # NEW (optional)
```

No major breaking changes, purely additive.

---

## Dependencies Review for v1.1

**Current** (v1.0):
- requests >=2.25.0 ✅
- feedparser >=6.0.0 ✅

**Potential Additions** (v1.1):
- fuzzywuzzy (for deduplication) - optional
- SQLite (built-in, no install needed)
- networkx (for citation graph) - optional

**Avoid**:
- Heavy frameworks (Django, TensorFlow)
- Deprecated libraries
- Libraries with complex native dependencies

---

## Conclusion

v1.0 is production-ready for thesis writing and literature search.

v1.1 roadmap focuses on:
1. Better search experience (batch, caching, validation)
2. Enhanced result quality (deduplication, filtering)
3. Improved maintainability (testing, types)

No architectural redesigns planned. Evolution, not revolution.

---

Generated: 2026-04-21
For: literature-search skill development roadmap
Owner: Sisyphus (AI Engineering)
