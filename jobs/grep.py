
"""
CrashReduce Distributed Grep Job

Purpose
--------------------------------------------------

Distributed text search.

Searches large datasets in parallel.

Inspired by:

grep
distributed log analysis
search systems

--------------------------------------------------

Input:

Wikipedia partitions

Search Term:

"artificial intelligence"

Output:

All matching lines and locations.

--------------------------------------------------

Map Phase

Search each line.

Emit only matches.

--------------------------------------------------

Reduce Phase

Combine all matches.
"""

import re

from typing import Iterator
from typing import Tuple
from typing import List
from typing import Dict


class GrepJob:
    """
    Distributed Grep MapReduce Job.
    """

    @staticmethod
    def map(
        line: str,
        line_number: int,
        search_term: str,
        document_id: str
    ) -> Iterator[
        Tuple[str, Dict]
    ]:
        """
        Map Function

        Searches line for term.

        Emits only matching lines.
        """

        if not search_term:
            return

        line_lower = line.lower()

        search_lower = (
            search_term.lower()
        )

        if search_lower in line_lower:

            yield (
                "MATCH",
                {
                    "document_id":
                        document_id,

                    "line_number":
                        line_number,

                    "line":
                        line.strip()
                }
            )

    @staticmethod
    def reduce(
        key: str,
        values: List[Dict]
    ):
        """
        Combine all matches.

        Input:

        MATCH

        [
            {...},
            {...}
        ]

        Output:

        MATCH
        [
            {...},
            {...}
        ]
        """

        return (
            key,
            values
        )

    @staticmethod
    def combine(
        key: str,
        values: List[Dict]
    ):
        """
        Local combiner.

        Grep doesn't benefit much,
        but included for framework
        consistency.
        """

        return (
            key,
            values
        )

    @staticmethod
    def validate_search_term(
        search_term: str
    ) -> bool:
        """
        Ensure search term exists.
        """

        return bool(
            search_term.strip()
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
    def get_job_name():
        """
        Job identifier.
        """

        return "GREP"

    @staticmethod
    def count_matches(
        values: List[Dict]
    ):
        """
        Number of matches found.
        """

        return len(values)

    @staticmethod
    def sort_matches(
        values: List[Dict]
    ):
        """
        Deterministic ordering.

        Useful for testing.
        """

        return sorted(
            values,
            key=lambda match: (
                match["document_id"],
                match["line_number"]
            )
        )

    @staticmethod
    def format_result(
        match: Dict
    ):
        """
        Pretty-print helper.

        Example:

        wiki_part_1.txt:42:
        AI is changing the world
        """

        return (
            f"{match['document_id']}:"
            f"{match['line_number']}: "
            f"{match['line']}"
        )

    @staticmethod
    def regex_map(
        line: str,
        line_number: int,
        pattern: str,
        document_id: str
    ):
        """
        Future enhancement.

        Supports regex search.

        Example:

        r"AI.*world"
        """

        if re.search(
            pattern,
            line,
            re.IGNORECASE
        ):

            yield (
                "MATCH",
                {
                    "document_id":
                        document_id,

                    "line_number":
                        line_number,

                    "line":
                        line.strip()
                }
            )