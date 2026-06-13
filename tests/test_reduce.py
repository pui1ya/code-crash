
"""
Tests for Reducer Logic

Verifies:

1. WordCount Reduce
2. Inverted Index Reduce
3. Grep Reduce
4. Edge Cases

Run:

pytest tests/test_reduce.py
"""

from jobs.wordcount import WordCountJob
from jobs.inverted_index import InvertedIndexJob
from jobs.grep import GrepJob


# ==================================================
# WORDCOUNT TESTS
# ==================================================

def test_wordcount_reduce_single_value():

    result = WordCountJob.reduce(
        "hello",
        [1]
    )

    assert result == (
        "hello",
        1
    )


def test_wordcount_reduce_multiple_values():

    result = WordCountJob.reduce(
        "hello",
        [1, 1, 1]
    )

    assert result == (
        "hello",
        3
    )


def test_wordcount_reduce_large_count():

    values = [1] * 1000

    result = WordCountJob.reduce(
        "hello",
        values
    )

    assert result == (
        "hello",
        1000
    )


def test_wordcount_reduce_empty_values():

    result = WordCountJob.reduce(
        "hello",
        []
    )

    assert result == (
        "hello",
        0
    )


# ==================================================
# WORDCOUNT COMBINER TESTS
# ==================================================

def test_wordcount_combiner():

    result = WordCountJob.combine(
        "python",
        [1, 1, 1, 1]
    )

    assert result == (
        "python",
        4
    )


# ==================================================
# INVERTED INDEX TESTS
# ==================================================

def test_inverted_index_reduce_unique_documents():

    result = InvertedIndexJob.reduce(
        "ai",
        [
            "doc1.txt",
            "doc2.txt"
        ]
    )

    assert result == (
        "ai",
        [
            "doc1.txt",
            "doc2.txt"
        ]
    )


def test_inverted_index_reduce_duplicate_documents():

    result = InvertedIndexJob.reduce(
        "ai",
        [
            "doc1.txt",
            "doc1.txt",
            "doc2.txt"
        ]
    )

    assert result == (
        "ai",
        [
            "doc1.txt",
            "doc2.txt"
        ]
    )


def test_inverted_index_reduce_many_duplicates():

    result = InvertedIndexJob.reduce(
        "machine",
        [
            "doc1",
            "doc1",
            "doc1",
            "doc2",
            "doc2",
            "doc3"
        ]
    )

    assert result == (
        "machine",
        [
            "doc1",
            "doc2",
            "doc3"
        ]
    )


# ==================================================
# INVERTED INDEX COMBINER
# ==================================================

def test_inverted_index_combiner():

    result = InvertedIndexJob.combine(
        "ai",
        [
            "doc1",
            "doc1",
            "doc2"
        ]
    )

    key, docs = result

    assert key == "ai"

    assert set(docs) == {
        "doc1",
        "doc2"
    }


# ==================================================
# GREP TESTS
# ==================================================

def test_grep_reduce_single_match():

    matches = [
        {
            "document_id":
                "doc1.txt",

            "line_number":
                1,

            "line":
                "AI is changing the world"
        }
    ]

    result = GrepJob.reduce(
        "MATCH",
        matches
    )

    assert result == (
        "MATCH",
        matches
    )


def test_grep_reduce_multiple_matches():

    matches = [
        {
            "document_id":
                "doc1.txt",

            "line_number":
                1,

            "line":
                "AI is changing the world"
        },
        {
            "document_id":
                "doc2.txt",

            "line_number":
                50,

            "line":
                "Artificial Intelligence"
        }
    ]

    result = GrepJob.reduce(
        "MATCH",
        matches
    )

    assert len(
        result[1]
    ) == 2


def test_grep_count_matches():

    matches = [
        {"line": "one"},
        {"line": "two"},
        {"line": "three"}
    ]

    assert (
        GrepJob.count_matches(
            matches
        )
        == 3
    )


# ==================================================
# SORTING TESTS
# ==================================================

def test_grep_sort_matches():

    matches = [

        {
            "document_id":
                "doc2",

            "line_number":
                5,

            "line":
                "B"
        },

        {
            "document_id":
                "doc1",

            "line_number":
                1,

            "line":
                "A"
        }
    ]

    sorted_matches = (
        GrepJob.sort_matches(
            matches
        )
    )

    assert (
        sorted_matches[0]
        ["document_id"]
        == "doc1"
    )


# ==================================================
# FORMATTER TEST
# ==================================================

def test_grep_formatter():

    result = (
        GrepJob.format_result(
            {
                "document_id":
                    "doc1.txt",

                "line_number":
                    42,

                "line":
                    "AI is amazing"
            }
        )
    )

    assert (
        result
        ==
        "doc1.txt:42: AI is amazing"
    )


# ==================================================
# STRESS TEST
# ==================================================

def test_wordcount_stress_reduce():

    values = [1] * 100000

    result = WordCountJob.reduce(
        "stress",
        values
    )

    assert result == (
        "stress",
        100000
    )
