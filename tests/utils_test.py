#   tests/utils_test.py

# ===========================================================
from functools import reduce
from hypothesis import given, strategies as st

import env
from lib.utils import *

# ===========================================================


@given(
    st.integers(),
    st.integers(),
    st.integers(min_value=0, max_value=2),
    st.integers(min_value=0, max_value=2),
    *(4 * [st.integers()])
)
def test_combine_counters(m1, m2, only1, only2, v1, v2, v3, v4):
    values = (v1, v2, v3, v4)
    values1 = values[:only1]
    values2 = values[only1 : only1 + only2]
    values_both = values[only1 + only2 : 4]
    d1 = {
        k: v
        for k, v in list(zip(range(only1), values1))
        + list(zip(range(only1 + only2, 4), values_both))
    }
    d2 = {
        k: v
        for k, v in list(zip(range(only1, only1 + only2), values2))
        + list(zip(range(only1 + only2, 4), values_both))
    }
    result = combine_counters(d1, d2, m1, m2)
    for k in range(only1):
        assert result[k] == m1 * d1[k]
    for k in range(only1, only1 + only2):
        assert result[k] == m2 * d2[k]
    for k in range(only1 + only2, 4):
        assert result[k] == m1 * d1[k] + m2 * d2[k]
