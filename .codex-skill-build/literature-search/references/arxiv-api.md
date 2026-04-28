# arXiv API Notes

Official references:

- https://info.arxiv.org/help/api/user-manual.html
- https://info.arxiv.org/help/api/tou.html

## Endpoint

- Base query endpoint: `https://export.arxiv.org/api/query`
- Response format: Atom XML feed

## Parameters Used by This Skill

- `search_query`: main query string
- `id_list`: comma-separated arXiv IDs
- `start`: 0-based offset
- `max_results`: page size
- `sortBy`: `relevance`, `lastUpdatedDate`, or `submittedDate`
- `sortOrder`: `ascending` or `descending`

## Search Field Prefixes

- `ti`: title
- `au`: author
- `abs`: abstract
- `co`: comment
- `jr`: journal reference
- `cat`: subject category
- `rn`: report number
- `all`: all searchable fields

Prefer `id_list` over `search_query=id:...` when targeting exact arXiv IDs.

## Date Filter

Use `submittedDate:[YYYYMMDDTTTT+TO+YYYYMMDDTTTT]` inside `search_query`.

Example:

```text
au:del_maestro AND submittedDate:[202301010600+TO+202401010600]
```

## Boolean Syntax

Combine clauses with `AND`, `OR`, and quoted phrases.

Examples:

```text
ti:"retrieval augmented generation"
au:lecun AND abs:contrastive
cat:cs.CL AND abs:"large language model"
```

## Paging and Limits

- `start` is 0-based.
- arXiv recommends a 3 second delay when making multiple calls in a row.
- A single request may return at most 30,000 results overall, in slices of at most 2,000.
- Queries returning more than about 1,000 results should usually be refined instead of harvested as-is.

## Response Notes

Common entry fields:

- `id`
- `title`
- `summary`
- `published`
- `updated`
- `author`
- `category`
- `link`
- `arxiv:primary_category`
- `arxiv:comment`
- `arxiv:journal_ref`
- `arxiv:doi`

The `link` elements usually include the abstract page and, when available, the PDF URL.
