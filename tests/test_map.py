
"""
Tests for Mapper Logic

Verifies:

1. WordCount Map
2. Inverted Index Map
3. Grep Map
4. Edge Cases

Run:

pytest tests/test_map.py
"""

from jobs.wordcount import WordCountJob
from jobs.inverted_index import InvertedIndexJob
from jobs.grep import GrepJob


# ==================================================
# WORDCOUNT TESTS
# ==================================================

def test_wordcount_single_word():

    result = list(
        WordCountJob.map(
            "hello"
        )
    )

    assert result == [
        ("hello", 1)
    ]


def test_wordcount_multiple_words():

    result = list(
        WordCountJob.map(
            "hello world hello"
        )
    )

    assert result == [
        ("hello", 1),
        ("world", 1),
        ("hello", 1)
    ]


def test_wordcount_case_insensitive():

    result = list(
        WordCountJob.map(
            "Hello HELLO hello"
        )
    )

    assert result == [
        ("hello", 1),
        ("hello", 1),
        ("hello", 1)
    ]


def test_wordcount_punctuation():

    result = list(
        WordCountJob.map(
            "hello, world!"
        )
    )

    assert result == [
        ("hello", 1),
        ("world", 1)
    ]


# ==================================================
# INVERTED INDEX TESTS
# ==================================================

def test_inverted_index_single_line():

    result = list(
        InvertedIndexJob.map(
            "AI is amazing",
            "doc1.txt"
        )
    )

    assert result == [
        ("ai", "doc1.txt"),
        ("is", "doc1.txt"),
        ("amazing", "doc1.txt")
    ]


def test_inverted_index_case_insensitive():

    result = list(
        InvertedIndexJob.map(
            "AI ai Ai",
            "doc1.txt"
        )
    )

    assert result == [
        ("ai", "doc1.txt"),
        ("ai", "doc1.txt"),
        ("ai", "doc1.txt")
    ]


# ==================================================
# GREP TESTS
# ==================================================

def test_grep_match_found():

    result = list(
        GrepJob.map(
            line="AI is changing the world",

            line_number=1,

            search_term="AI",

            document_id="doc1.txt"
        )
    )

    assert len(result) == 1

    assert result[0][0] == "MATCH"


def test_grep_no_match():

    result = list(
        GrepJob.map(
            line="Python is great",

            line_number=1,

            search_term="AI",

            document_id="doc1.txt"
        )
    )

    assert result == []


def test_grep_case_insensitive():

    result = list(
        GrepJob.map(
            line="Artificial Intelligence",

            line_number=10,

            search_term="artificial",

            document_id="wiki.txt"
        )
    )

    assert len(result) == 1


# ==================================================
# VALIDATION TESTS
# ==================================================

def test_wordcount_empty_line():

    result = list(
        WordCountJob.map("")
    )

    assert result == []


def test_inverted_index_empty_line():

    result = list(
        InvertedIndexJob.map(
            "",
            "doc.txt"
        )
    )

    assert result == []


# ==================================================
# LARGE INPUT TEST
# ==================================================

def test_large_wordcount_input():

    text = "hello " * 1000

    result = list(
        WordCountJob.map(text)
    )

    assert len(result) == 1000


# ==================================================
# SPECIAL CHARACTER TEST
# ==================================================

def test_special_characters_removed():

    result = list(
        WordCountJob.map(
            "hello!!! world???"
        )
    )

    assert result == [
        ("hello", 1),
        ("world", 1)
    ]
