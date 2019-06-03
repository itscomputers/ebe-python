#   test_miller_rabin.py
#===========================================================
from hypothesis import assume, example, given, strategies as st
from random import choice

from ..miller_rabin import *
from ..miller_rabin import \
    _miller_rabin_cutoffs, \
    _generate_witnesses
#===========================================================

@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_generate_witnesses(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)
    cutoffs = _miller_rabin_cutoffs()

    for w in witnesses:
        assert( 2 <= w < number )

    if number > cutoffs[-1][0] and num_witnesses > number:
        assert( len(witnesses) == number - 3 )
    
    elif number <= cutoffs[-1][0]:
        assert( witnesses <= set(p for (val, p) in cutoffs[:-1]) )

    else:
        assert( len(witnesses) == num_witnesses )

#-----------------------------

@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_combined_test(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)
    single_results = set(single_test(number, witness) for witness in witnesses)
    combined_result = combined_tests(number, witnesses)
    if single_results == set(['probable prime']):
        assert( combined_result == 'probable prime' )
    else:
        assert( combined_result == 'composite' )
