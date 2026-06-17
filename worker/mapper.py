
"""
CrashReduce Mapper

Purpose
--------------------------------------------------

Generic Map execution engine.

Responsible for:

1. Reading input partition
2. Executing map function
3. Generating key-value pairs
4. Partitioning output
5. Writing intermediate files

--------------------------------------------------

Example

Input:

hello world
hello mapreduce

Output:

("hello",1)
("world",1)
("hello",1)
("mapreduce",1)

--------------------------------------------------

Mapper does NOT aggregate.

Aggregation happens in reducer.py
"""

import json
from pathlib import Path
from collections import defaultdict


class Mapper:
    """
    Generic Map execution engine.
    """

    def __init__(
        self,
        num_reducers: int = 2
    ):

        self.num_reducers = num_reducers

        self.intermediate_dir = Path(
            "storage/intermediate"
        )

        self.intermediate_dir.mkdir(
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
        Main mapper execution.

        Returns:

        list of generated files
        """

        input_file = task["input_file"]

        task_id = task["task_id"]

        job_type = task["job_type"].upper()

        print(
            f"[MAPPER] Processing "
            f"{input_file}"
        )

        key_value_pairs = self.execute_map_function(
            input_file=input_file,
            job_type=job_type
        )

        output_files = self.partition_output(
            task_id,
            key_value_pairs
        )

        return output_files

    # ==========================================
    # EXECUTE MAP FUNCTION
    # ==========================================

    def execute_map_function(
        self,
        input_file: str,
        job_type: str
    ):
        """
        Executes job-specific map logic.

        Returns:

        [
            (key,value),
            (key,value)
        ]
        """

        if job_type == "WORDCOUNT":

            return self.wordcount_mapper(
                input_file
            )

        elif job_type == "INVERTED_INDEX":

            return self.inverted_index_mapper(
                input_file
            )

        elif job_type == "GREP":

            return self.grep_mapper(
                input_file
            )

        else:

            raise ValueError(
                f"Unknown job type: {job_type}"
            )

    # ==========================================
    # WORDCOUNT MAPPER
    # ==========================================

    def wordcount_mapper(
        self,
        input_file: str
    ):
        """
        hello world

        →

        ("hello",1)
        ("world",1)
        """

        results = []

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                words = line.strip().split()

                for word in words:

                    results.append(
                        (word.lower(), 1)
                    )

        return results

    # ==========================================
    # INVERTED INDEX MAPPER
    # ==========================================

    def inverted_index_mapper(
        self,
        input_file: str
    ):
        """
        AI is great

        →

        ("AI", filename)

        ("is", filename)

        ("great", filename)
        """

        results = []

        filename = Path(
            input_file
        ).name

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                words = line.strip().split()

                for word in words:

                    results.append(
                        (
                            word.lower(),
                            filename
                        )
                    )

        return results

    # ==========================================
    # GREP MAPPER
    # ==========================================

    def grep_mapper(
        self,
        input_file: str
    ):
        """
        Emits line numbers.

        Actual filtering happens
        in reducer phase.
        """

        results = []

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

            for line_number, line in enumerate(
                file,
                start=1
            ):

                results.append(
                    (
                        line.strip(),
                        line_number
                    )
                )

        return results

    # ==========================================
    # PARTITION OUTPUT
    # ==========================================

    def partition_output(
        self,
        task_id: str,
        key_value_pairs
    ):
        """
        Assigns keys to reducers.

        hash(key) % num_reducers
        """

        partitions = defaultdict(list)

        for key, value in key_value_pairs:

            reducer_id = (
                hash(key)
                % self.num_reducers
            )

            partitions[
                reducer_id
            ].append(
                (key, value)
            )

        output_files = []

        for reducer_id, values in (
            partitions.items()
        ):

            output_file = (
                self.intermediate_dir
                /
                f"{task_id}_reduce_"
                f"{reducer_id}.json"
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    values,
                    file
                )

            output_files.append(
                str(output_file)
            )

        return output_files

    # ==========================================
    # HASH PARTITION
    # ==========================================

    def get_partition(
        self,
        key: str
    ):
        """
        Determines reducer assignment.
        """

        return (
            hash(key)
            % self.num_reducers
        )
    