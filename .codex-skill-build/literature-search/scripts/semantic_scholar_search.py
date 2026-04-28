#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from typing import Any

from common import build_url, compact_text, emit_output, fetch_json, make_headers

SEMANTIC_SCHOLAR_BULK_URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
DEFAULT_FIELDS = ",".join(
    [
        "title",
        "year",
        "abstract",
        "url",
        "authors",
        "citationCount",
        "publicationTypes",
        "publicationDate",
        "openAccessPdf",
    ]
)


def normalize_author(author: dict[str, Any]) -> dict[str, Any]:
    return {
        "author_id": author.get("authorId"),
        "name": compact_text(author.get("name")),
    }


def normalize_paper(paper: dict[str, Any]) -> dict[str, Any]:
    open_access_pdf = paper.get("openAccessPdf") or {}
    return {
        "source": "semantic_scholar",
        "paper_id": paper.get("paperId"),
        "title": compact_text(paper.get("title")),
        "abstract": compact_text(paper.get("abstract")),
        "year": paper.get("year"),
        "publication_date": paper.get("publicationDate"),
        "publication_types": paper.get("publicationTypes") or [],
        "citation_count": paper.get("citationCount"),
        "url": paper.get("url"),
        "open_access_pdf_url": open_access_pdf.get("url"),
        "authors": [normalize_author(author) for author in paper.get("authors") or []],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Semantic Scholar Bulk Search Results",
        "",
        f"- Query: `{payload['request'].get('query', '')}`",
        f"- Total estimate: `{payload.get('total')}`",
        f"- Returned: `{len(payload.get('results', []))}`",
        f"- Next token: `{payload.get('token') or ''}`",
        "",
    ]

    for index, paper in enumerate(payload.get("results", []), start=1):
        authors = ", ".join(author["name"] for author in paper.get("authors", [])) or "Unknown authors"
        publication_types = ", ".join(paper.get("publication_types", [])) or "Unknown type"
        lines.extend(
            [
                f"## {index}. {paper.get('title', 'Untitled')}",
                "",
                f"- Paper ID: `{paper.get('paper_id', '')}`",
                f"- Authors: {authors}",
                f"- Year: {paper.get('year', '')}",
                f"- Publication date: {paper.get('publication_date', '')}",
                f"- Publication types: {publication_types}",
                f"- Citation count: {paper.get('citation_count', '')}",
                f"- URL: {paper.get('url', '')}",
                f"- Open-access PDF: {paper.get('open_access_pdf_url', '')}",
                "",
                paper.get("abstract", ""),
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar with the paper bulk search endpoint."
    )
    parser.add_argument("query", help="Search query string. Quote phrases when needed.")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help="Comma-separated response fields")
    parser.add_argument("--token", help="Pagination token from a previous response")
    parser.add_argument("--sort", help="Sort expression, for example publicationDate:desc")
    parser.add_argument("--publication-types", help="Publication type filter string")
    parser.add_argument(
        "--open-access-pdf",
        choices=["true", "false"],
        help="Filter for results with or without public PDFs",
    )
    parser.add_argument("--min-citation-count", type=int, help="Minimum citation count")
    parser.add_argument("--publication-date-or-year", help="Date range filter string")
    parser.add_argument("--year", help="Year range filter string, for example 2023-")
    parser.add_argument("--venue", help="Venue filter string")
    parser.add_argument("--fields-of-study", help="Field-of-study filter string")
    parser.add_argument("--api-key", help="Semantic Scholar API key override")
    parser.add_argument("--output", help="Write output to a file instead of stdout")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request URL and headers without calling the API",
    )
    args = parser.parse_args()

    if args.min_citation_count is not None and args.min_citation_count < 0:
        parser.error("--min-citation-count must be >= 0")

    request_params = {
        "query": args.query,
        "fields": args.fields,
        "token": args.token,
        "sort": args.sort,
        "publicationTypes": args.publication_types,
        "openAccessPdf": args.open_access_pdf,
        "minCitationCount": args.min_citation_count,
        "publicationDateOrYear": args.publication_date_or_year,
        "year": args.year,
        "venue": args.venue,
        "fieldsOfStudy": args.fields_of_study,
    }
    headers = make_headers(api_key=args.api_key, api_key_env="SEMANTIC_SCHOLAR_API_KEY")
    url = build_url(SEMANTIC_SCHOLAR_BULK_URL, request_params)

    if args.dry_run:
        emit_output(
            {
                "source": "semantic_scholar",
                "endpoint": "paper/search/bulk",
                "url": url,
                "request": request_params,
                "header_keys": sorted(headers.keys()),
                "has_api_key": "x-api-key" in headers,
            },
            output_path=args.output,
            output_format=args.format,
            markdown_renderer=lambda payload: (
                "# Semantic Scholar Bulk Search Dry Run\n\n"
                f"- URL: `{payload['url']}`\n"
                f"- Header keys: `{', '.join(payload['header_keys'])}`\n"
            ),
        )
        return 0

    try:
        response = fetch_json(url, headers=headers)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = {
        "source": "semantic_scholar",
        "endpoint": "paper/search/bulk",
        "request": request_params,
        "url": url,
        "total": response.get("total"),
        "token": response.get("token"),
        "results": [normalize_paper(paper) for paper in response.get("data", [])],
    }
    emit_output(
        payload,
        output_path=args.output,
        output_format=args.format,
        markdown_renderer=render_markdown,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
