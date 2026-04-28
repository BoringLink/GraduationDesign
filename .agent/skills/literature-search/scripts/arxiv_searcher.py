#!/usr/bin/env python3
"""
arXiv API integration module.
Provides direct access to arXiv preprints with flexible filtering.

Official API: https://arxiv.org/help/api/
Documentation: https://arxiv.org/help/api/user-manual.html
"""

import feedparser
from typing import List, Dict, Any, Optional
from urllib.parse import quote
import time


class ArxivSearcher:
    """
    Client for arXiv API (OAI-PMH based).
    Supports keyword search, filtering by category, year, authors.

    API Base: http://export.arxiv.org/api/query
    Reference: https://arxiv.org/help/api/user-manual.html
    """

    BASE_URL = "http://export.arxiv.org/api/query?"

    ARXIV_CATEGORIES = {
        # Computer Science (Major Categories)
        "cs.AI": "Artificial Intelligence",
        "cs.LG": "Machine Learning",
        "cs.CL": "Computation and Language (NLP)",
        "cs.CV": "Computer Vision and Pattern Recognition",
        "cs.DC": "Distributed, Parallel, and Cluster Computing",
        "cs.NE": "Neural and Evolutionary Computing",
        "cs.PL": "Programming Languages",
        "cs.DS": "Data Structures and Algorithms",
        "cs.DB": "Databases",
        "cs.IR": "Information Retrieval",
        "cs.SE": "Software Engineering",
        "cs.HC": "Human-Computer Interaction",
        "cs.CY": "Computers and Society",
        "cs.ED": "Computers and Education",
        # Physics
        "physics.comp-ph": "Computational Physics",
        "physics.ed-ph": "Physics Education",
        # Quantitative Biology
        "q-bio.NC": "Neurons and Cognition",
    }

    def __init__(self, delay: float = 3.0):
        """
        Initialize arXiv searcher.

        Args:
            delay: Delay (seconds) between API requests (respect rate limits).
                   Official recommendation: minimum 3 seconds for polite access.
        """
        self.delay = delay
        self.last_request_time = 0

    def search(
        self,
        keywords: List[str],
        category: Optional[str] = None,
        authors: Optional[str | List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search arXiv with flexible parameters.

        Uses official arXiv API query syntax:
        https://arxiv.org/help/api/user-manual.html#query_details

        Args:
            keywords: List of search terms (combined with AND logic)
            category: arXiv category code (e.g., 'cs.AI', 'cs.LG')
            authors: Author name(s) to filter by
            year_min: Minimum publication year (submittedDate filter)
            year_max: Maximum publication year (submittedDate filter)
            max_results: Maximum number of results to return

        Returns:
            List of paper dictionaries with metadata (title, authors, year, etc.)
        """

        query_parts = []

        for kw in keywords:
            query_parts.append(f'(all:"{kw}")')

        if not query_parts:
            return []

        query_str = " AND ".join(query_parts)

        if category:
            query_str += f" AND cat:{category}"

        if year_min and year_max:
            date_start = f"{year_min}0101000"
            date_end = f"{year_max}1231235"
            query_str += f" AND submittedDate:[{date_start} TO {date_end}]"
        elif year_min:
            date_start = f"{year_min}0101000"
            query_str += f" AND submittedDate:[{date_start} TO 29991231235]"
        elif year_max:
            date_end = f"{year_max}1231235"
            query_str += f" AND submittedDate:[00000101000 TO {date_end}]"

        params = {
            "search_query": query_str,
            "start": 0,
            "max_results": min(max_results, 2000),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        url = self.BASE_URL + "&".join(
            f"{k}={quote(str(v))}" for k, v in params.items()
        )

        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        print(f"Querying arXiv: {query_str[:80]}...")
        feed = feedparser.parse(url)
        self.last_request_time = time.time()

        if feed.get("status") != 200 and "bozo_exception" in feed:
            print(f"Warning: arXiv API error: {feed.get('bozo_exception')}")
            return []

        results = []
        for entry in feed.get("entries", []):
            try:
                published = entry.get("published", "")
                year = int(published[:4]) if published else None

                if year_min and year and year < year_min:
                    continue
                if year_max and year and year > year_max:
                    continue

                authors_list = [
                    author.get("name", "").strip()
                    for author in entry.get("authors", [])
                ]

                categories = []
                for tag in entry.get("tags", []):
                    if isinstance(tag, dict) and "term" in tag:
                        categories.append(tag["term"])

                primary_category = entry.get("arxiv_primary_category", {}).get(
                    "term", ""
                )

                paper = {
                    "title": entry.get("title", "").replace("\n", " ").strip(),
                    "authors": authors_list,
                    "year": year,
                    "arxiv_id": entry.get("id", "").split("/abs/")[-1],
                    "abstract": entry.get("summary", "").replace("\n", " ").strip(),
                    "published": published,
                    "categories": categories,
                    "primary_category": primary_category,
                    "url": entry.get("id", ""),
                    "pdf_url": f"https://arxiv.org/pdf/{entry.get('id', '').split('/abs/')[-1]}.pdf",
                    "source": "arXiv",
                }

                if authors:
                    author_list = [authors] if isinstance(authors, str) else authors
                    if not any(
                        any(auth.lower() in a.lower() for a in authors_list)
                        for auth in author_list
                    ):
                        continue

                results.append(paper)

            except (KeyError, ValueError, IndexError, AttributeError) as e:
                print(f"Warning: Failed to parse entry: {e}")
                continue

        return results

    @staticmethod
    def get_category_description(category: str) -> str:
        """Get human-readable description of arXiv category."""
        return ArxivSearcher.ARXIV_CATEGORIES.get(category, category)
