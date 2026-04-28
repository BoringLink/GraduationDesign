# API Limits and Configuration Guide

## arXiv API

### Rate Limits
- **Requests per second**: ~2 requests/second (polite user-agent)
- **Recommended delay**: 3 seconds between requests (conservative)
- **Authentication**: Not required
- **No API key needed**: Works with public access

### Best Practices
- Include `User-Agent` header identifying your application
- Implement exponential backoff for failed requests
- Cache results locally to avoid redundant queries
- Respect the service: don't hammer the API

### Query Syntax
- arXiv uses OAI-PMH protocol with `feedparser` library
- Query format: `search_query=...&start=N&max_results=M`
- URL encoding required for special characters

### Limitations
- Maximum results per request: Often 100-1000 depending on endpoint
- Feed format: Atom 1.0 (parsed automatically by feedparser)
- No JSON API (RSS/Atom feeds only)

## Semantic Scholar API

### Rate Limits
**Free Tier (No API Key)**
- ~100 requests per minute
- Limited fields available
- No access to some endpoints

**With API Key**
- 1 request per second (default)
- Full field access
- Higher limits possible (request increase from Allen Institute)

### Authentication
```python
headers = {
    "x-api-key": your_api_key
}
response = requests.get(url, headers=headers)
```

### Endpoints and Limits

| Endpoint | Method | Rate Limit | Notes |
|----------|--------|-----------|-------|
| `/paper/search/bulk` | GET | 1 RPS | Primary search endpoint |
| `/paper/{paperId}` | GET | 1 RPS | Single paper details |
| `/author/batch` | POST | 1 RPS | Batch author lookup |
| `/recommendations/v1/papers` | POST | 1 RPS | Recommendations |
| `/author/{authorId}` | GET | 1 RPS | Single author details |

### Available Fields

**Paper Fields**
```
paperId, title, abstract, year, citationCount, referenceCount,
isOpenAccess, publicationVenue, publicationDate, url, authors,
externalIds, tldr, venue, journal
```

**Author Fields**
```
authorId, name, url, paperCount, hIndex, papers
```

### Response Structure

**Paper Object**
```json
{
  "paperId": "string",
  "title": "string",
  "authors": [
    {
      "authorId": "string",
      "name": "string"
    }
  ],
  "year": 2024,
  "citationCount": 42,
  "abstract": "...",
  "url": "https://semanticscholar.org/paper/...",
  "isOpenAccess": true
}
```

### Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Process results |
| 400 | Bad request | Check query syntax |
| 401 | Unauthorized | Verify API key |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Server error | Retry with delay |

## Combined Search Strategy

### Choosing Sources

**Use arXiv when:**
- Looking for recent preprints
- Need comprehensive CS coverage
- Working in fast-moving research areas
- Want raw access without publisher gate

**Use Semantic Scholar when:**
- Need citation metrics
- Want published papers only
- Researching established topics
- Building citation networks

**Use both when:**
- Doing comprehensive literature review
- Combining breadth (arXiv) + depth (citations)
- Validating findings across sources

### Rate Limit Coordination

```python
# Conservative timing for combined search
ARXIV_DELAY = 3.0  # seconds between requests
SEMANTIC_DELAY = 1.0  # seconds between requests

# If querying both in sequence:
# - Query arXiv: 1 request takes 0s + 3s delay = 3s
# - Query Semantic: 1 request takes 0s + 1s delay = 1s
# - Total per query: ~4 seconds
# - For 10 parallel searches: ~4 seconds (concurrent) or ~40 seconds (sequential)
```

## Configuration for Your Skill

### Default Parameters (in combined_search.py)

```python
DEFAULT_CONFIG = {
    "arxiv": {
        "enabled": True,
        "delay_seconds": 3.0,
        "max_results": 50,
        "timeout_seconds": 15,
    },
    "semantic": {
        "enabled": True,
        "api_key": None,  # Set from environment or parameter
        "delay_seconds": 1.0,
        "max_results": 50,
        "timeout_seconds": 15,
    },
    "output": {
        "default_format": "markdown",
        "default_dir": "./outputs",
        "auto_save": True,
    }
}
```

### Environment Variables

```bash
# Set Semantic Scholar API key
export SEMANTIC_SCHOLAR_KEY="your-api-key-here"

# Optional: Set output directory
export LITERATURE_SEARCH_OUTPUT="~/papers"
```

## Caching Strategy

To minimize API calls:

```python
CACHE_DIR = ".literature_cache"
CACHE_DURATION = 86400  # 24 hours in seconds

# Cache keys: hash(keywords + filters)
# Stored as: keywords_HASH.json
```

### When to Invalidate Cache
- User explicitly requests fresh results
- More than 24 hours old
- Filters changed (year range, category, etc.)

## Troubleshooting Guide

### arXiv Issues

**Problem**: Connection timeout
- **Solution**: Increase `timeout_seconds` to 30
- **Cause**: arXiv servers slow; respect rate limit

**Problem**: Empty results with valid keywords
- **Solution**: Try different keywords or broader search
- **Cause**: arXiv may not have papers in that exact category

### Semantic Scholar Issues

**Problem**: 401 Unauthorized
- **Solution**: Check API key is correct and non-expired
- **Action**: Request new API key from Semantic Scholar

**Problem**: 429 Too Many Requests
- **Solution**: Implement exponential backoff (1s → 2s → 4s...)
- **Cause**: Exceeded rate limit; wait and retry

**Problem**: Missing fields in response
- **Solution**: Check `fields` parameter includes desired fields
- **Cause**: Requesting fields not available for free tier

## Monitoring

### Logs to Implement
```
[TIMESTAMP] [SOURCE] [KEYWORDS] [STATUS] [COUNT] [DURATION]
[2024-04-21 14:30:22] [arXiv] ["deep learning"] [OK] [47] [2.1s]
[2024-04-21 14:30:24] [Semantic] ["deep learning"] [OK] [51] [1.3s]
```

### Metrics to Track
- API response times
- Results per query
- Rate limit hit count
- Cache hit rate
- Error frequency

## Security Notes

### API Key Protection
- Never commit API keys to version control
- Use environment variables or `.env` files (git-ignored)
- Rotate keys periodically
- Monitor usage for unusual patterns

### Data Privacy
- Results contain only published metadata
- No personal data beyond author names
- Suitable for academic research purposes

## Future Capacity Planning

If you expand this skill:
- Implement connection pooling for concurrent requests
- Add persistent caching (Redis/SQLite)
- Consider batch processing for large searches
- Request higher rate limits from both services
