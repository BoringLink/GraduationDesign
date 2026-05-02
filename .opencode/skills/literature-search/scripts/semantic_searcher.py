#!/usr/bin/env python3
"""
Semantic Scholar API integration module.
Provides access to published papers with citation metrics and rich metadata.
"""

import requests
from typing import List, Dict, Any, Optional
import time


class SemanticSearcher:
    """
    Client for Semantic Scholar API.
    Provides access to published papers with metadata including citations.
    Free tier available without API key (limited functionality).
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        """
        Initialize Semantic Scholar searcher.

        Args:
            api_key: Optional API key for higher rate limits
            delay: Delay (seconds) between API requests
        """
        self.api_key = api_key
        self.delay = delay
        self.last_request_time = 0
        self.headers = {"User-Agent": "LiteratureSearchSkill/1.0"}
        if api_key:
            self.headers["x-api-key"] = api_key

    def search(
        self,
        keywords: List[str],
        authors: Optional[str | List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search Semantic Scholar.

        Args:
            keywords: List of search terms
            authors: Author name(s) to filter by
            year_min: Minimum publication year
            year_max: Maximum publication year
            max_results: Maximum number of results

        Returns:
            List of paper dictionaries with metadata
        """

        # Combine keywords into search query
        query = " ".join(keywords)

        # Construct request
        url = f"{self.BASE_URL}/paper/search"
        params = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": "paperId,title,authors,year,abstract,citationCount,referenceCount,isOpenAccess,publicationVenue,publicationDate,url",
        }

        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        try:
            print(f"Querying Semantic Scholar: {query}")
            response = requests.get(
                url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            self.last_request_time = time.time()
        except requests.RequestException as e:
            print(f"Warning: Semantic Scholar API error: {e}")
            return []

        data = response.json()
        papers = data.get("data", [])

        results = []
        for paper in papers:
            try:
                # Extract year
                year = paper.get("year")

                # Apply year filters
                if year_min and year and year < year_min:
                    continue
                if year_max and year and year > year_max:
                    continue

                # Extract authors
                authors_list = []
                for author in paper.get("authors", []):
                    if isinstance(author, dict):
                        authors_list.append(author.get("name", ""))
                    else:
                        authors_list.append(str(author))

                # Build paper dict
                paper_dict = {
                    "title": paper.get("title", "").strip(),
                    "authors": authors_list,
                    "year": year,
                    "abstract": paper.get("abstract", "").strip(),
                    "source_id": paper.get("paperId", ""),
                    "citations": paper.get("citationCount", 0),
                    "references": paper.get("referenceCount", 0),
                    "is_open_access": paper.get("isOpenAccess", False),
                    "venue": paper.get("publicationVenue", {}).get("name")
                    if isinstance(paper.get("publicationVenue"), dict)
                    else None,
                    "publication_date": paper.get("publicationDate"),
                    "url": paper.get("url")
                    or f"https://semanticscholar.org/paper/{paper.get('paperId', '')}",
                    "source": "Semantic Scholar",
                }

                # Apply author filter if specified
                if authors:
                    if isinstance(authors, str):
                        authors = [authors]

                    matched = False
                    for specified_author in authors:
                        if any(
                            specified_author.lower() in a.lower() for a in authors_list
                        ):
                            matched = True
                            break

                    if not matched:
                        continue

                results.append(paper_dict)

            except (KeyError, ValueError, TypeError) as e:
                print(f"Warning: Failed to parse paper: {e}")
                continue

        return results

    def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID

        Returns:
            Detailed paper metadata
        """
        url = f"{self.BASE_URL}/paper/{paper_id}"
        params = {
            "fields": "paperId,title,authors,year,abstract,citationCount,references,citations,publicationVenue",
        }

        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        try:
            response = requests.get(
                url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            self.last_request_time = time.time()
            return response.json()
        except requests.RequestException as e:
            print(f"Warning: Failed to fetch paper details: {e}")
            return {}
