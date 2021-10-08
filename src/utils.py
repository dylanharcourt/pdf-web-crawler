from typing import List
from collections import deque

import itertools


class Utils:
    @staticmethod
    def replace_from_match(match_str: str, old_list: List[str], new="") -> str:
        for old in old_list:
            match_str = match_str.replace(old, new)
        return match_str

    @staticmethod
    def trim_and_split(match_str: str):
        return [x.strip() for x in match_str.split("\n") if x and not x.isspace()]

    @staticmethod
    def map_list_to_cols(data: List[str], row_schema: dict) -> List[List[str]]:
        row_schema = dict(row_schema)
        while len(data):
            d = deque()
            while Utils.replace_from_match(data[len(data) - 1], [",", "(", ")"]).isnumeric():
                d.appendleft(data.pop())
            if data[len(data) - 1] not in row_schema:
                raise Exception(f"Row schema not defined properly! - {data[len(data) - 1]}")
            row_schema[data[len(data) - 1]] = d
            data.pop()
        return list(map(list, itertools.zip_longest(*row_schema.values(), fillvalue=0)))

    @staticmethod
    def parse_match_into_table_rows(data: List[str], schema_len: int) -> List[List[str]]:
        return [data[x : x + schema_len] for x in range(0, len(data), schema_len)]
