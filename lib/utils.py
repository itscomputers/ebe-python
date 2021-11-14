#   lib/utils.py
#   - module for miscellaneous utilities

# ===========================================================
__all__ = [
    "combine_counters",
]
# ===========================================================


def combine_counters(d1, d2, m1=1, m2=1):
    """
    Apply multiplicites and sum values of two dictionaries.

    example: `combine_counters({2: 1, 5: 2}, {2: 3}, 3, 1) ~> {2: 6, 5: 6}`

    + d1: Dict[Any, int]
    + d2: Dict[Any, int]
    + m1: int
    + m2: int
    ~> Dict[Any, int]
    """
    return dict(
        (key, (m1 * d1[key] if key in d1 else 0) + (m2 * d2[key] if key in d2 else 0))
        for key in set(d1.keys()) | set(d2.keys())
    )
