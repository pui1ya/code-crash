
"""
CrashReduce Reducer

Purpose
--------------------------------------------------

Generic Reduce execution engine.

Responsibilities

1. Read mapper output files
2. Shuffle and sort keys
3. Group values by key
4. Execute reduce function
5. Generate final output

--------------------------------------------------

Example

Mapper Output:

("hello",1)
("hello",1)
("world",1)

After Shuffle:

{
    "hello": [1,1],
    "world": [1]
}

Reducer Output:

hello 2
world 1
"""

import json
from pathlib import Path
from collections import defaultdict


class Reducer:
    """
    Generic Reduce execution engine.
    """

    def __init__(self):

        self.intermediate_dir = Path(
            "storage/intermediate"
        )

        self.output_dir = Path(
            "storage/output"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================
    # MAIN ENTRYPOINT
    # ==========================================

    def run(
        self,
        task: dict
    ):
        """
        Main reducer execution.

        Returns:
            output file path
        """

        job_type = task["job_type"]

        reducer_partition = task[
            "partition_id"
        ]

        print(
            f"[REDUCER] Starting "
            f"partition {reducer_partition}"
        )

        grouped_data = self.load_partition_data(
            reducer_partition
        )

        if job_type == "WORDCOUNT":

            reduced_data = (
                self.wordcount_reduce(
                    grouped_data
                )
            )

        elif job_type == "INVERTED_INDEX":

            reduced_data = (
                self.inverted_index_reduce(
                    grouped_data
                )
            )

        elif job_type == "GREP":

            search_term = task.get(
                "search_term",
                ""
            )

            reduced_data = (
                self.grep_reduce(
                    grouped_data,
                    search_term
                )
            )

        else:

            raise ValueError(
                f"Unknown job type: {job_type}"
            )

        output_path = self.write_output(
            task["task_id"],
            reduced_data
        )

        return output_path

    # ==========================================
    # LOAD INTERMEDIATE FILES
    # ==========================================

    def load_partition_data(
        self,
        partition_id: int
    ):
        """
        Reads all mapper outputs
        belonging to one reducer.

        Performs shuffle phase.
        """

        grouped = defaultdict(list)

        pattern = (
            f"*_reduce_{partition_id}.json"
        )

        files = list(
            self.intermediate_dir.glob(
                pattern
            )
        )

        for file_path in files:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                records = json.load(file)

                for key, value in records:

                    grouped[key].append(
                        value
                    )

        return grouped

    # ==========================================
    # WORDCOUNT REDUCE
    # ==========================================

    def wordcount_reduce(
        self,
        grouped_data
    ):
        """
        hello:[1,1,1]

        →

        hello:3
        """

        results = {}

        for key, values in (
            grouped_data.items()
        ):

            results[key] = sum(values)

        return results

    # ==========================================
    # INVERTED INDEX REDUCE
    # ==========================================

    def inverted_index_reduce(
        self,
        grouped_data
    ):
        """
        AI:
        [doc1,doc1,doc2]

        →

        AI:
        [doc1,doc2]
        """

        results = {}

        for key, values in (
            grouped_data.items()
        ):

            results[key] = sorted(
                list(set(values))
            )

        return results

    # ==========================================
    # GREP REDUCE
    # ==========================================

    def grep_reduce(
        self,
        grouped_data,
        search_term
    ):
        """
        Distributed grep.

        Returns matching lines.
        """

        results = {}

        search_term = (
            search_term.lower()
        )

        for line, positions in (
            grouped_data.items()
        ):

            if search_term in (
                line.lower()
            ):

                results[line] = positions

        return results

    # ==========================================
    # WRITE OUTPUT FILE
    # ==========================================

    def write_output(
        self,
        task_id: str,
        results
    ):
        """
        Writes reducer output.
        """

        output_file = (
            self.output_dir
            /
            f"{task_id}_result.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=4
            )

        return output_file

    # ==========================================
    # MERGE OUTPUTS
    # ==========================================

    def merge_reduce_outputs(
        self
    ):
        """
        Future enhancement.

        Merge all reducer outputs
        into one final result.
        """

        pass

    # ==========================================
    # SHUFFLE STATISTICS
    # ==========================================

    def get_shuffle_statistics(
        self,
        grouped_data
    ):
        """
        Useful for debugging.
        """

        total_keys = len(
            grouped_data
        )

        total_values = sum(
            len(values)
            for values in grouped_data.values()
        )

        return {
            "total_keys":
                total_keys,

            "total_values":
                total_values
        }