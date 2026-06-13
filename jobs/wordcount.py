
"""
CrashReduce WordCount Job

Purpose
--------------------------------------------------

Classic MapReduce Word Count.

This is the canonical example from the
Google MapReduce paper.

Input:

hello world
hello mapreduce

Map Output:

("hello", 1)
("world", 1)
("hello", 1)
("mapreduce", 1)

Reduce Output:

hello -> 2
world -> 1
mapreduce -> 1

--------------------------------------------------

This file ONLY contains
job-specific business logic.

No file I/O.

No networking.

No worker logic.
"""


import re
from typing import Iterator
from typing import Tuple
from typing import List


class WordCountJob:
    """
    WordCount MapReduce implementation.
    """

    @staticmethod
    def map(
        line: str
    ) -> Iterator[Tuple[str, int]]:
        """
        Map Function

        Input:
            One line of text

        Output:
            (word, 1)

        Example:

        hello world

        →

        ("hello",1)

        ("world",1)
        """

        # Convert to lowercase
        line = line.lower()

        # Extract words only
        words = re.findall(
            r"\b\w+\b",
            line
        )

        for word in words:

            yield (
                word,
                1
            )

    @staticmethod
    def reduce(
        key: str,
        values: List[int]
    ):
        """
        Reduce Function

        Input:

        hello

        [1,1,1]

        Output:

        ("hello", 3)
        """

        return (
            key,
            sum(values)
        )

    @staticmethod
    def combine(
        key: str,
        values: List[int]
    ):
        """
        Optional Combiner.

        Local aggregation before shuffle.

        Same logic as reducer
        for WordCount.

        Future optimization.
        """

        return (
            key,
            sum(values)
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
        Shared normalization helper.

        Future:

        Stop words

        Stemming

        Lemmatization
        """

        return word.lower()

    @staticmethod
    def get_job_name():
        """
        Returns job identifier.
        """

        return "WORDCOUNT"