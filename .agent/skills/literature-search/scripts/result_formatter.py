#!/usr/bin/env python3
"""
Result formatting module for literature search results.
Converts paper data to Markdown, JSON, and other formats.
"""

import json
from typing import List, Dict, Any
from datetime import datetime


class ResultFormatter:
    """Handles conversion of search results to various output formats."""

    @staticmethod
    def to_markdown(
        papers: List[Dict[str, Any]],
        title: str = "Literature Search Results",
        search_params: Dict[str, Any] = None,
    ) -> str:
        """Convert papers to Markdown format."""

        lines = [f"# {title}", ""]

        if search_params:
            lines.extend(
                [
                    f"**Search Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    f"**Keywords**: {search_params.get('keywords', [])}",
                    f"**Results Found**: {len(papers)}",
                    "",
                ]
            )

            if search_params.get("year_min") or search_params.get("year_max"):
                year_range = f"{search_params.get('year_min', '?')}-{search_params.get('year_max', '?')}"
                lines.append(f"**Year Range**: {year_range}")

            if search_params.get("authors"):
                lines.append(f"**Authors**: {search_params['authors']}")

            lines.append("")

        lines.extend(["## Results", ""])

        for i, paper in enumerate(papers, 1):
            lines.extend(ResultFormatter._paper_to_markdown(paper, i))
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _paper_to_markdown(paper: Dict[str, Any], index: int) -> List[str]:
        """Convert single paper to Markdown lines."""

        lines = [f"### {index}. {paper.get('title', 'Untitled')}"]
        lines.append("")

        # Authors
        if paper.get("authors"):
            authors = paper["authors"]
            if isinstance(authors, list):
                if len(authors) > 3:
                    author_str = (
                        ", ".join(authors[:3]) + f", et al. (+{len(authors) - 3})"
                    )
                else:
                    author_str = ", ".join(authors)
            else:
                author_str = str(authors)
            lines.append(f"**Authors**: {author_str}")

        # Year
        if paper.get("year"):
            lines.append(f"**Year**: {paper['year']}")

        # Source identifiers
        if paper.get("arxiv_id"):
            lines.append(
                f"**arXiv**: [{paper['arxiv_id']}](https://arxiv.org/abs/{paper['arxiv_id']})"
            )
        elif paper.get("source_id"):
            url = f"https://semanticscholar.org/paper/{paper['source_id']}"
            lines.append(f"**Semantic Scholar**: [{paper['source_id']}]({url})")

        # Citation metrics
        if paper.get("citations") is not None:
            lines.append(f"**Citations**: {paper['citations']}")

        if paper.get("references") is not None:
            lines.append(f"**References**: {paper['references']}")

        # Venue/Journal
        if paper.get("venue"):
            lines.append(f"**Venue**: {paper['venue']}")

        # Abstract (truncated)
        if paper.get("abstract"):
            abstract = paper["abstract"]
            if len(abstract) > 300:
                abstract = abstract[:297] + "..."
            lines.append(f"\n**Abstract**:\n{abstract}\n")

        # URL
        if paper.get("url"):
            lines.append(f"**Link**: {paper['url']}")

        # Source attribution
        if paper.get("source"):
            lines.append(f"*Source: {paper['source']}*")

        return lines

    @staticmethod
    def to_json(
        papers: List[Dict[str, Any]],
        search_params: Dict[str, Any] = None,
        pretty: bool = True,
    ) -> str:
        """Convert papers to JSON format."""

        result = {
            "search_timestamp": datetime.now().isoformat(),
            "search_params": search_params or {},
            "total_results": len(papers),
            "papers": papers,
        }

        indent = 2 if pretty else None
        return json.dumps(result, indent=indent, ensure_ascii=False)

    @staticmethod
    def to_csv(papers: List[Dict[str, Any]]) -> str:
        """Convert papers to CSV format."""

        import csv
        from io import StringIO

        if not papers:
            return ""

        output = StringIO()

        fieldnames = [
            "title",
            "authors",
            "year",
            "arxiv_id",
            "source_id",
            "citations",
            "abstract",
            "url",
            "source",
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            row = {key: paper.get(key, "") for key in fieldnames}
            if isinstance(row["authors"], list):
                row["authors"] = "; ".join(row["authors"])
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def to_bibtex(papers: List[Dict[str, Any]]) -> str:
        """Convert papers to BibTeX format."""

        lines = []

        for i, paper in enumerate(papers, 1):
            citekey = ResultFormatter._generate_citekey(paper, i)

            entry_lines = [f"@article{{{citekey},"]

            if paper.get("title"):
                entry_lines.append(f'  title = "{{{paper["title"]}}}",')

            if paper.get("authors"):
                authors = paper["authors"]
                if isinstance(authors, list):
                    author_str = " and ".join(authors)
                else:
                    author_str = str(authors)
                entry_lines.append(f'  author = "{{{author_str}}}",')

            if paper.get("year"):
                entry_lines.append(f"  year = {{{paper['year']}}},")

            if paper.get("arxiv_id"):
                entry_lines.append(f'  eprint = "{{{paper["arxiv_id"]}}}",')
                entry_lines.append(f"  archivePrefix = {{arXiv}},")

            if paper.get("abstract"):
                abstract = paper["abstract"].replace('"', '\\"')
                entry_lines.append(f'  abstract = "{{{abstract}}}",')

            if paper.get("url"):
                entry_lines.append(f'  url = "{{{paper["url"]}}}",')

            entry_lines[-1] = entry_lines[-1].rstrip(",")
            entry_lines.append("}")

            lines.extend(entry_lines)
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _generate_citekey(paper: Dict[str, Any], index: int) -> str:
        """Generate BibTeX citation key."""

        authors = paper.get("authors", [])
        year = paper.get("year", "xxxx")

        if isinstance(authors, list) and authors:
            first_author = authors[0].split()[-1].lower()
        else:
            first_author = "unknown"

        return f"{first_author}{year}_{index}"

    @staticmethod
    def summary(papers: List[Dict[str, Any]]) -> str:
        """Generate a summary of results."""

        if not papers:
            return "No papers found."

        lines = [
            f"## Summary",
            f"- **Total papers**: {len(papers)}",
        ]

        years = [p.get("year") for p in papers if p.get("year")]
        if years:
            lines.append(f"- **Year range**: {min(years)}-{max(years)}")

        sources = {}
        for paper in papers:
            source = paper.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1

        if sources:
            lines.append(f"- **By source**:")
            for source, count in sorted(sources.items()):
                lines.append(f"  - {source}: {count}")

        citations = [
            p.get("citations", 0) for p in papers if p.get("citations") is not None
        ]
        if citations:
            avg_citations = sum(citations) / len(citations)
            lines.append(f"- **Average citations**: {avg_citations:.1f}")
            lines.append(f"- **Most cited**: {max(citations)}")

        return "\n".join(lines)
