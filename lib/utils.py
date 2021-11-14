#  lib/utils.py
#  - module for miscellaneous utilities
from typing import Any, Dict


def combine_counters(
    dictionary: Dict[Any, int],
    other_dictionary: Dict[Any, int],
    multiplicity: int = 1,
    other_multiplicity: int = 1,
) -> Dict[Any, int]:
    """
    Apply multiplicites and sum values of two dictionaries.

    example: `combine_counters({2: 1, 5: 2}, {2: 4}, 3, 1) ~> {2: 7, 5: 6}`
    """
    keys = set(dictionary.keys()) | set(other_dictionary.keys())

    def value(key):
        return sum(
            [
                multiplicity * dictionary.get(key, 0),
                other_multiplicity * other_dictionary.get(key, 0),
            ]
        )

    return {key: value(key) for key in keys}
