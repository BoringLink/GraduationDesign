#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from typing import Any

from common import build_url, compact_text, emit_output, fetch_text, make_headers

ARXIV_QUERY_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_NS = {"arxiv": "http://arxiv.org/schemas/atom"}
OPENSEARCH_NS = {"opensearch": "http://a9.com/-/spec/opensearch/1.1/"}


def text_of(element: ET.Element, path: str, namespaces: dict[str, str]) -> str:
    found = element.find(path, namespaces)
    if found is None or found.text is None:
        return ""
    return compact_text(found.text)


def parse_int(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_entry(entry: ET.Element) -> dict[str, Any]:
    links = []
    abstract_url = ""
    pdf_url = ""

    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href", "")
        rel = link.attrib.get("rel", "")
        title = link.attrib.get("title", "")
        link_type = link.attrib.get("type", "")
        links.append(
            {
                "href": href,
                "rel": rel,
                "title": title,
                "type": link_type,
            }
        )
        if rel == "alternate" and href and not abstract_url:
            abstract_url = href
        if title == "pdf" or link_type == "application/pdf":
            pdf_url = href

    authors = [
        compact_text(name.text)
        for name in entry.findall("atom:author/atom:name", ATOM_NS)
        if name.text
    ]
    categories = [
        category.attrib.get("term", "")
        for category in entry.findall("atom:category", ATOM_NS)
        if category.attrib.get("term")
    ]

    identifier = text_of(entry, "atom:id", ATOM_NS)
    arxiv_id = identifier.rsplit("/", 1)[-1] if identifier else ""

    primary_category = ""
    primary = entry.find("arxiv:primary_category", ARXIV_NS)
    if primary is not None:
        primary_category = primary.attrib.get("term", "")

    return {
        "source": "arxiv",
        "arxiv_id": arxiv_id,
        "id": identifier,
        "title": text_of(entry, "atom:title", ATOM_NS),
        "summary": text_of(entry, "atom:summary", ATOM_NS),
        "published": text_of(entry, "atom:published", ATOM_NS),
        "updated": text_of(entry, "atom:updated", ATOM_NS),
        "authors": authors,
        "categories": categories,
        "primary_category": primary_category,
        "comment": text_of(entry, "arxiv:comment", ARXIV_NS),
        "journal_ref": text_of(entry, "arxiv:journal_ref", ARXIV_NS),
        "doi": text_of(entry, "arxiv:doi", ARXIV_NS),
        "abstract_url": abstract_url,
        "pdf_url": pdf_url,
        "links": links,
    }


def parse_feed(xml_text: str) -> dict[str, Any]:
    root = ET.fromstring(xml_text)
    entries = [parse_entry(entry) for entry in root.findall("atom:entry", ATOM_NS)]
    return {
        "feed_title": text_of(root, "atom:title", ATOM_NS),
        "updated": text_of(root, "atom:updated", ATOM_NS),
        "total_results": parse_int(text_of(root, "opensearch:totalResults", OPENSEARCH_NS)),
        "start_index": parse_int(text_of(root, "opensearch:startIndex", OPENSEARCH_NS)),
        "items_per_page": parse_int(text_of(root, "opensearch:itemsPerPage", OPENSEARCH_NS)),
        "results": entries,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# arXiv Results",
        "",
        f"- Query: `{payload['request'].get('search_query') or ''}`",
        f"- ID list: `{payload['request'].get('id_list') or ''}`",
        f"- Total results: `{payload.get('total_results')}`",
        f"- Returned: `{len(payload.get('results', []))}`",
        "",
    ]

    for index, paper in enumerate(payload.get("results", []), start=1):
        author_line = ", ".join(paper.get("authors", [])) or "Unknown authors"
        category_line = ", ".join(paper.get("categories", [])) or "No categories"
        lines.extend(
            [
                f"## {index}. {paper.get('title', 'Untitled')}",
                "",
                f"- arXiv ID: `{paper.get('arxiv_id', '')}`",
                f"- Authors: {author_line}",
                f"- Published: {paper.get('published', '')}",
                f"- Updated: {paper.get('updated', '')}",
                f"- Primary category: `{paper.get('primary_category', '')}`",
                f"- Categories: {category_line}",
                f"- Abstract URL: {paper.get('abstract_url', '')}",
                f"- PDF URL: {paper.get('pdf_url', '')}",
                "",
                paper.get("summary", ""),
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Search arXiv and emit normalized results.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="arXiv search_query string")
    group.add_argument("--id-list", help="Comma-separated arXiv IDs")
    parser.add_argument("--start", type=int, default=0, help="0-based result offset")
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Number of results to request (arXiv recommends slices of at most 2000)",
    )
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="relevance",
        help="Sort field",
    )
    parser.add_argument(
        "--sort-order",
        choices=["ascending", "descending"],
        default="descending",
        help="Sort direction",
    )
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
        help="Print the request URL without calling the API",
    )
    args = parser.parse_args()

    if args.start < 0:
        parser.error("--start must be >= 0")
    if not 1 <= args.max_results <= 2000:
        parser.error("--max-results must be between 1 and 2000")

    request_params = {
        "search_query": args.query,
        "id_list": args.id_list,
        "start": args.start,
        "max_results": args.max_results,
        "sortBy": args.sort_by,
        "sortOrder": args.sort_order,
    }
    url = build_url(ARXIV_QUERY_URL, request_params)

    if args.dry_run:
        emit_output(
            {
                "source": "arxiv",
                "url": url,
                "request": request_params,
            },
            output_path=args.output,
            output_format=args.format,
            markdown_renderer=lambda payload: f"# arXiv Dry Run\n\n`{payload['url']}`\n",
        )
        return 0

    try:
        xml_text = fetch_text(
            url,
            headers=make_headers(accept="application/atom+xml"),
        )
        feed = parse_feed(xml_text)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = {
        "source": "arxiv",
        "request": request_params,
        "url": url,
        **feed,
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
