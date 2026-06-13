
"""
CrashReduce Inverted Index Job

Purpose
--------------------------------------------------

Creates a searchable inverted index.

Input:

Document

↓

Words

Output:

Word → Document List

--------------------------------------------------

Example

doc1.txt:

AI is amazing

doc2.txt:

AI is growing

Output:

{
    "ai":
        ["doc1.txt", "doc2.txt"],

    "is":
        ["doc1.txt", "doc2.txt"],

    "amazing":
        ["doc1.txt"],

    "growing":
        ["doc2.txt"]
}

--------------------------------------------------

Used to demonstrate that
CrashReduce can build
search-engine style indexes.
"""

import re

from typing import Iterator
from typing import Tuple
from typing import List


class InvertedIndexJob:
    """
    Inverted Index MapReduce Job.
    """

    @staticmethod
    def map(
        line: str,
        document_id: str
    ) -> Iterator[
        Tuple[str, str]
    ]:
        """
        Map Function

        Input:

        line:
            AI is amazing

        document_id:
            doc1.txt

        Output:

        ("ai", "doc1.txt")

        ("is", "doc1.txt")

        ("amazing", "doc1.txt")
        """

        line = line.lower()

        words = re.findall(
            r"\b\w+\b",
            line
        )

        for word in words:

            yield (
                word,
                document_id
            )

    @staticmethod
    def reduce(
        key: str,
        values: List[str]
    ):
        """
        Reduce Function

        Input:

        ai

        [
            doc1,
            doc1,
            doc2
        ]

        Output:

        (
            "ai",
            [
                "doc1",
                "doc2"
            ]
        )
        """

        unique_documents = sorted(
            list(
                set(values)
            )
        )

        return (
            key,
            unique_documents
        )

    @staticmethod
    def combine(
        key: str,
        values: List[str]
    ):
        """
        Optional Combiner.

        Removes duplicates locally
        before shuffle.

        Useful for huge datasets.
        """

        return (
            key,
            list(
                set(values)
            )
        )

    @staticmethod
    def validate_input(
        line: str
    ) -> bool:
        """
        Ignore empty lines.
        """

        return bool(
            line.strip()
        )

    @staticmethod
    def normalize_word(
        word: str
    ) -> str:
        """
        Standardize word format.
        """

        return word.lower()

    @staticmethod
    def get_job_name():
        """
        Job identifier.
        """

        return "INVERTED_INDEX"

    @staticmethod
    def count_unique_documents(
        values: List[str]
    ):
        """
        Useful for analytics.

        Example:

        AI appears in 500 docs.
        """

        return len(
            set(values)
        )

    @staticmethod
    def sort_document_list(
        documents: List[str]
    ):
        """
        Keeps output deterministic.

        Important for testing.
        """

        return sorted(
            list(
                set(documents)
            )
        )
