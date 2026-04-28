#!/usr/bin/env python3
"""
Test and verification script for literature-search skill.
Run evals and verify API integrations.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from combined_search import LiteratureSearcher


def test_basic_search():
    """Test basic arXiv search without Semantic Scholar."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic arXiv Search")
    print("=" * 60)

    searcher = LiteratureSearcher(output_dir="./outputs")

    results = searcher.search(
        keywords=["deep learning"],
        year_min=2023,
        year_max=2024,
        max_results=10,
        sources=["arxiv"],
        output_format="markdown",
        save_to_file=True,
    )

    print(f"\n✓ Search completed")
    print(f"  Found: {results['total_found']} papers")
    if results.get("saved_to"):
        print(f"  Saved to: {results['saved_to']}")

    return results["total_found"] > 0


def test_author_search():
    """Test search with author filtering."""
    print("\n" + "=" * 60)
    print("TEST 2: Author-Filtered Search")
    print("=" * 60)

    searcher = LiteratureSearcher(output_dir="./outputs")

    results = searcher.search(
        keywords=["machine learning"],
        authors="Geoffrey Hinton",
        year_min=2015,
        year_max=2024,
        max_results=20,
        sources=["arxiv"],
        output_format="json",
        save_to_file=True,
    )

    print(f"\n✓ Search completed")
    print(f"  Found: {results['total_found']} papers")
    if results.get("saved_to"):
        print(f"  Saved to: {results['saved_to']}")

    return results["total_found"] > 0


def test_multi_keyword_search():
    """Test search with multiple keywords and category filter."""
    print("\n" + "=" * 60)
    print("TEST 3: Multi-Keyword Category-Filtered Search")
    print("=" * 60)

    searcher = LiteratureSearcher(output_dir="./outputs")

    results = searcher.search(
        keywords=["federated learning", "privacy"],
        category="cs.LG",
        year_min=2020,
        year_max=2024,
        max_results=15,
        sources=["arxiv"],
        output_format="markdown",
        save_to_file=True,
    )

    print(f"\n✓ Search completed")
    print(f"  Found: {results['total_found']} papers")
    if results.get("saved_to"):
        print(f"  Saved to: {results['saved_to']}")

    return results["total_found"] > 0


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("LITERATURE SEARCH SKILL - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Search", test_basic_search),
        ("Author Search", test_author_search),
        ("Multi-Keyword Search", test_multi_keyword_search),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results[test_name] = "✓ PASS" if passed else "✗ FAIL"
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results[test_name] = f"✗ ERROR: {str(e)[:50]}"

    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    for test_name, status in results.items():
        print(f"  {test_name}: {status}")

    passed_count = sum(1 for s in results.values() if s.startswith("✓"))
    total_count = len(results)
    print(f"\nPassed: {passed_count}/{total_count}")

    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
