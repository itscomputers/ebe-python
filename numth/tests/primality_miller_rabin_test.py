#   numth/tests/primality_miller_rabin_test.py
#===========================================================
from hypothesis import assume, example, given, strategies as st
from random import choice

from ..basic import is_prime__naive
from ..primality_miller_rabin import *
from ..primality_miller_rabin import _generate_witnesses
#===========================================================

@given(
    st.integers(min_value=3),
    st.integers(min_value=1, max_value=50)
)
def test_miller_rabin_witnesses(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)
    single_results = set(miller_rabin_witness(number, witness) for witness in witnesses)
    combined_result = miller_rabin_witnesses(number, witnesses)
    if single_results == set(['probable prime']):
        if number < miller_rabin_max_cutoff():
            assert( combined_result == 'prime' )
        else:
            assert( combined_result == 'probable prime' )
    else:
        assert( combined_result == 'composite' )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**6))
def test_miller_rabin_test(number):
    mr_primality = miller_rabin_test(number, 20)
    number_is_prime = is_prime__naive(number)
    if mr_primality in ['prime', 'probable prime']:
        assert( number_is_prime )
    else:
        assert( not number_is_prime )

#-----------------------------

@given(
    st.integers(min_value=3),
    st.integers(min_value=1, max_value=50)
)
def test_generate_witnesses(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)

    for w in witnesses:
        assert( 2 <= w < number )

    if number > miller_rabin_max_cutoff() and num_witnesses > number:
        assert( len(witnesses) == number - 3 )
    
    elif number <= miller_rabin_max_cutoff():
        assert( witnesses <= set(p for (val, p) in miller_rabin_cutoffs()) )

    else:
        assert( len(witnesses) == num_witnesses )

