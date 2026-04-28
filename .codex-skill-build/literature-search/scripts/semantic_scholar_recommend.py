#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from typing import Any

from common import build_url, compact_text, emit_output, make_headers, post_json

SEMANTIC_SCHOLAR_RECOMMEND_URL = "https://api.semanticscholar.org/recommendations/v1/papers"
DEFAULT_FIELDS = "title,url,citationCount,authors"


def normalize_author(author: dict[str, Any]) -> dict[str, Any]:
    return {
        "author_id": author.get("authorId"),
        "name": compact_text(author.get("name")),
    }


def normalize_paper(paper: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "semantic_scholar",
        "paper_id": paper.get("paperId"),
        "title": compact_text(paper.get("title")),
        "url": paper.get("url"),
        "citation_count": paper.get("citationCount"),
        "authors": [normalize_author(author) for author in paper.get("authors") or []],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Semantic Scholar Recommendations",
        "",
        f"- Positive seed IDs: `{', '.join(payload['request'].get('positivePaperIds', []))}`",
        f"- Negative seed IDs: `{', '.join(payload['request'].get('negativePaperIds', []))}`",
        f"- Returned: `{len(payload.get('results', []))}`",
        "",
    ]

    for index, paper in enumerate(payload.get("results", []), start=1):
        authors = ", ".join(author["name"] for author in paper.get("authors", [])) or "Unknown authors"
        lines.extend(
            [
                f"## {index}. {paper.get('title', 'Untitled')}",
                "",
                f"- Paper ID: `{paper.get('paper_id', '')}`",
                f"- Authors: {authors}",
                f"- Citation count: {paper.get('citation_count', '')}",
                f"- URL: {paper.get('url', '')}",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Get Semantic Scholar paper recommendations from seed paper IDs."
    )
    parser.add_argument(
        "--positive-paper-id",
        action="append",
        default=[],
        help="Positive seed paperId. Repeat this flag for multiple seeds.",
    )
    parser.add_argument(
        "--negative-paper-id",
        action="append",
        default=[],
        help="Negative seed paperId. Repeat this flag for multiple seeds.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of recommendations to request. The tutorial notes a max of 500.",
    )
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help="Comma-separated response fields")
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
        help="Print the request URL, headers, and JSON body without calling the API",
    )
    args = parser.parse_args()

    if not args.positive_paper_id:
        parser.error("at least one --positive-paper-id is required")
    if not 1 <= args.limit <= 500:
        parser.error("--limit must be between 1 and 500")

    request_body = {
        "positivePaperIds": args.positive_paper_id,
        "negativePaperIds": args.negative_paper_id,
    }
    request_params = {
        "fields": args.fields,
        "limit": args.limit,
    }
    headers = make_headers(api_key=args.api_key, api_key_env="SEMANTIC_SCHOLAR_API_KEY")
    url = build_url(SEMANTIC_SCHOLAR_RECOMMEND_URL, request_params)

    if args.dry_run:
        emit_output(
            {
                "source": "semantic_scholar",
                "endpoint": "recommendations/v1/papers",
                "url": url,
                "request": request_body,
                "query": request_params,
                "header_keys": sorted(headers.keys()),
                "has_api_key": "x-api-key" in headers,
            },
            output_path=args.output,
            output_format=args.format,
            markdown_renderer=lambda payload: (
                "# Semantic Scholar Recommendation Dry Run\n\n"
                f"- URL: `{payload['url']}`\n"
                f"- Positive IDs: `{', '.join(payload['request']['positivePaperIds'])}`\n"
                f"- Negative IDs: `{', '.join(payload['request']['negativePaperIds'])}`\n"
            ),
        )
        return 0

    try:
        response = post_json(url, request_body, headers=headers)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = {
        "source": "semantic_scholar",
        "endpoint": "recommendations/v1/papers",
        "request": request_body,
        "query": request_params,
        "url": url,
        "results": [normalize_paper(paper) for paper in response.get("recommendedPapers", [])],
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
