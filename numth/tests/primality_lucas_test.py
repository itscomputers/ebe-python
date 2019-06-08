#   numth/tests/test_lucas_primality.py
#===========================================================
from hypothesis import assume, example, given, strategies as st

from ..basic import is_prime__naive
from ..primality_lucas import *
from ..primality_lucas import \
    _generate_witness_pairs, \
    _good_parameters, \
    _get_quadratic_element, \
    _extract_from_quadratic, \
    _by_index, \
    _lucas_sequence
#===========================================================

@given(
    st.integers(min_value=3),
    st.integers(min_value=1,
        max_value=50)
)
def test_lucas_witnesses(number, num_witnesses):
    number += 1 - number % 2
    witness_pairs = _generate_witness_pairs(number, num_witnesses)

    results = set(lucas_witness_pair(number, *pair) for pair in witness_pairs)
    combined_result = lucas_witness_pairs(number, witness_pairs)

    if ('composite', False) in results:
        assert( combined_result == ('composite', False) )
    elif ('probable prime', True) in results:
        assert( combined_result == ('probable prime', True) )
    else:
        assert( combined_result == ('probable prime', False) )

#-----------------------------

@given(st.integers(min_value=3, max_value=10**6))
def test_lucas_test(number):
    number += 1 - number % 2
    l_primality = lucas_test(number, 20)
    number_is_prime = is_prime__naive(number)
    if l_primality in ['strong probable prime', 'probable prime']:
        assert( number_is_prime )
    else:
        assert( not number_is_prime )

#-----------------------------

@given(
    st.integers(min_value=3),
    st.integers(min_value=1, max_value=30)
)
def test_generate_witness_pairs(number, num_witnesses):
    number += 1 - number % 2
    witness_pairs = _generate_witness_pairs(number, num_witnesses)
    assert( num_witnesses == len(witness_pairs) )
    for witness_pair in witness_pairs:
        P, Q = witness_pair
        assert( _good_parameters(number, P, Q, P**2 - 4*Q) != False )

#-----------------------------

@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3)
)
def test_by_index(k, P, Q, mod):
    mod += 1 - mod % 2
    D = P**2 - 4*Q
    q = _get_quadratic_element(P, D, mod)
    U_k, V_k, Q_k = _by_index(k, P, Q, mod)
    kth_power = pow(q, k, mod)
    assert( _extract_from_quadratic(kth_power, mod) == (U_k, V_k) )
    assert( Q_k == pow(Q, k, mod) )

#-----------------------------

@given(
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3)
)
def test_lucas_sequence(P, Q, mod):
    mod += 1 - mod % 2
    UV = _lucas_sequence(P, Q, mod)
    for i in range(100):
        assert( _by_index(i, P, Q, mod) == next(UV) )

