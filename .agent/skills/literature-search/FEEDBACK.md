# Literature Search Skill - Iteration Feedback Template

## Pre-Evaluation Checklist

Before running evals, verify these aspects work correctly:

### ✅ arXiv Integration
- [ ] API connectivity (test with simple query)
- [ ] Atom feed parsing works correctly
- [ ] Rate limiting (3-second delay) is enforced
- [ ] Date filtering works (submittedDate parameter)
- [ ] Category filtering returns correct papers
- [ ] Results include all expected fields (title, authors, abstract, url)

### ✅ Semantic Scholar Integration  
- [ ] API connectivity with provided key
- [ ] JSON response parsing works
- [ ] Citation counts are retrieved correctly
- [ ] Author filtering works with partial names
- [ ] Results deduplicate across sources correctly

### ✅ Output Formatting
- [ ] Markdown output is human-readable
- [ ] JSON output has correct structure
- [ ] Timestamps are accurate in filenames
- [ ] File saving works to specified directory
- [ ] Results summary is accurate

### ✅ Error Handling
- [ ] Empty result handling (useful message)
- [ ] API timeout handling (graceful degradation)
- [ ] Malformed response handling (skip entry, continue)
- [ ] Missing optional parameters (sensible defaults)

---

## Post-Evaluation Feedback Form

After running `bash run_evals.sh`, use this template to provide feedback:

### Test Results

**Test 1: Basic Keyword Search**
- Expected: 30+ papers in Markdown
- Actual: [__] papers found
- Status: [ ] PASS [ ] FAIL
- Issues: [describe any problems]

**Test 2: Author-Filtered Search**
- Expected: 10-30 papers with citations
- Actual: [__] papers found
- Status: [ ] PASS [ ] FAIL
- Issues: [describe any problems]

**Test 3: Multi-Keyword Literature Review**
- Expected: 50+ combined papers
- Actual: [__] papers found
- Status: [ ] PASS [ ] FAIL
- Issues: [describe any problems]

### Quality Assessment

**Relevance**: Results match query intent
- [ ] Highly relevant (95%+)
- [ ] Mostly relevant (75-95%)
- [ ] Somewhat relevant (50-75%)
- [ ] Poor relevance (<50%)
- Comments: _______

**Completeness**: Search covers expected papers
- [ ] Very complete (found major papers)
- [ ] Reasonably complete (found most papers)
- [ ] Incomplete (missed significant papers)
- [ ] Very incomplete (significant gaps)
- Comments: _______

**Usability**: Output format and quality
- [ ] Excellent (ready to use directly)
- [ ] Good (minor reformatting needed)
- [ ] Acceptable (usable with edits)
- [ ] Poor (needs significant work)
- Comments: _______

### API Performance

**arXiv Search Speed**
- Average time: [__] seconds
- Acceptable: [ ] Yes [ ] No

**Semantic Scholar Speed**
- Average time: [__] seconds
- Acceptable: [ ] Yes [ ] No

**Rate Limiting**
- Delays respected: [ ] Yes [ ] No
- Issues: _______

### Improvement Suggestions

**High Priority** (blocking use):
1. [describe issue and suggested fix]
2. [describe issue and suggested fix]

**Medium Priority** (improves usability):
1. [describe issue and suggested fix]
2. [describe issue and suggested fix]

**Low Priority** (nice-to-have):
1. [describe issue and suggested fix]
2. [describe issue and suggested fix]

### Feature Requests

Any missing features needed for your use case?
1. [feature description]
2. [feature description]

### Documentation Feedback

- [ ] SKILL.md is clear and complete
- [ ] README.md covers all use cases
- [ ] QUICKSTART.md is truly quick
- [ ] Code comments are helpful
- [ ] Examples are practical and relevant

Suggestions for documentation improvements:
- [suggestion]
- [suggestion]

---

## Common Issues & Solutions

### Issue: "No results found"
**Possible Causes**:
1. Keywords too specific → Try broader terms
2. Year range too narrow → Expand date range
3. Category filter too restrictive → Remove or broaden
4. API connectivity issue → Check internet connection

**Solution Steps**:
1. Test with known-good query: `"machine learning" 2023-2024`
2. Progressively add filters back one at a time
3. Check API status pages if still failing

### Issue: "Search is very slow"
**Possible Causes**:
1. Large result set → Reduce max_results or narrow query
2. API rate limiting → Expected behavior, 3sec min between requests
3. Network latency → Test with simpler query

**Solution Steps**:
1. Try with max_results=10 first
2. Add year constraint to reduce noise
3. Use single keyword instead of multiple

### Issue: "Duplicate results across sources"
**Expected Behavior**: Deduplication happens automatically
**If Still Seeing Duplicates**: Report with query details

### Issue: "JSON format is malformed"
**Check**:
1. Quotes properly escaped
2. Arrays are properly formatted
3. No trailing commas

**Solution**: Try Markdown format instead, JSON structure is verified

---

## Version 1.1 Improvement Roadmap

Based on typical user feedback:

### Likely v1.1 Additions
- [ ] Batch processing multiple queries
- [ ] Result caching to minimize API calls
- [ ] CSV export format
- [ ] BibTeX export for reference managers
- [ ] Citation graph exploration
- [ ] Advanced boolean query builder

### Likely v1.2 Additions
- [ ] Google Scholar integration (if permitted)
- [ ] PDF abstract extraction
- [ ] Local SQLite database for large result sets
- [ ] Web UI for search (instead of CLI)
- [ ] Email digest of new papers in saved searches

---

## How to Report Issues

When reporting issues, include:

1. **Exact command used**: `python combined_search.py "query" --args`
2. **Query that failed**: Keywords, filters, year range
3. **Expected vs actual results**: What you wanted vs what happened
4. **Error message/output**: Full error text or logs
5. **Environment**: Python version, OS, installed packages
6. **Files created**: Check outputs/ directory for error logs

Example issue report:
```
Query: "federated learning" 2023-2024 cs.LG
Expected: 50+ papers
Actual: 0 results
Error: [error message from test_skill.py]
Environment: Python 3.10, macOS, requests 2.28.1, feedparser 6.0.10
```

---

## Next Steps After v1.0

1. **Week 1**: Collect feedback from evaluation tests
2. **Week 2**: Implement high-priority fixes
3. **Week 3**: Add most-requested features
4. **Week 4**: v1.1 release with new features

Expected v1.1 features:
- CSV/BibTeX output
- Batch query processing
- Result caching
- Improved author matching

---

Generated: 2026-04-21
For: literature-search skill v1.0
Status: Ready for evaluation feedback
