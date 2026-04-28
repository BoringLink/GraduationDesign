# Semantic Scholar API Notes

Official references:

- https://www.semanticscholar.org/product/api
- https://www.semanticscholar.org/product/api/tutorial
- https://api.semanticscholar.org/api-docs/graph
- https://api.semanticscholar.org/api-docs/recommendations
- https://api.semanticscholar.org/license/

## Endpoints Used by This Skill

- Paper bulk search: `https://api.semanticscholar.org/graph/v1/paper/search/bulk`
- Paper recommendations: `https://api.semanticscholar.org/recommendations/v1/papers`

## Authentication

- Most Semantic Scholar endpoints can be called without authentication.
- The official overview recommends including an API key whenever possible.
- This skill reads `SEMANTIC_SCHOLAR_API_KEY` by default and sends it as the `x-api-key` header.
- The official overview states that API keys start at `1 RPS` across endpoints.
- Unauthenticated traffic is shared and may be throttled more aggressively during heavy use.

## Bulk Search Parameters

The official tutorial lists these bulk-search query parameters:

- `query`: required search text
- `token`: pagination token returned by the previous response
- `fields`: comma-separated response fields
- `sort`: sort by `paperId`, `publicationDate`, or `citationCount`
- `publicationTypes`
- `openAccessPdf`
- `minCitationCount`
- `publicationDateOrYear`
- `year`
- `venue`
- `fieldsOfStudy`

The response includes:

- `total`: estimated match count
- `token`: token for the next page
- `data`: result list

## Recommendations Parameters

- Query parameters:
  - `fields`
  - `limit`
- JSON body:
  - `positivePaperIds`
  - `negativePaperIds`

The response includes `recommendedPapers`.

## Practical Guidance

- Use bulk search for most paper discovery tasks.
- Keep `fields` narrow to reduce latency and limit pressure.
- Use recommendation expansion only after screening seed papers.
- Save both the search query and the returned token if you need to continue a large search later.

## Usage Restrictions

Read the current license before public or commercial use.

The public API license currently states that default access is limited to internal, non-commercial, research or educational use, and that broader or commercial usage requires contacting Semantic Scholar for expanded access.
