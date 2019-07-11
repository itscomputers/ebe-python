#   numth/tests/continued_fraction.py
#===========================================================
from hypothesis import assume, given, strategies as st

from ..basic import is_square
from ..types import Quadratic, Rational
from ..continued_fraction.quadratic import *
#===========================================================

def to_quadratic(quadratic_rational):
    return Quadratic(
        Rational(quadratic_rational.real, quadratic_rational.denom),
        Rational(quadratic_rational.imag, quadratic_rational.denom),
        quadratic_rational.root
    )

#=============================

@given(
    st.integers(),
    st.integers(),
    st.integers(min_value=1),
    st.integers(min_value=2).filter(lambda x: not is_square(x)),
    st.integers()
)
def test_quadratic_rational_class(real, imag, denom, root, integer):
    assume( (real, imag) != (0, 0) )
    qr = QuadraticRational(real, imag, denom, root)
    q = Quadratic(Rational(real, denom), Rational(imag, denom), root)
    assert( to_quadratic(qr) == q )
    assert( to_quadratic(qr.inverse()) == q.inverse() )
    assert( to_quadratic(qr.minus(integer)) == q - integer )

#-----------------------------

@given(
    st.integers(min_value=2, max_value=10**6).filter(lambda x: not is_square(x))
)
def test_continued_fractions(root):
    cf_data = continued_fraction_all(root)
    assert( cf_data['complete'] )
    first_beta = cf_data['table'][0][2]
    last_beta = cf_data['table'][-1][2]
    assert( last_beta == first_beta )

    quotients = continued_fraction_quotients(root)
    convergents = continued_fraction_convergents(root)
    pell_numbers = continued_fraction_pell_numbers(root)
    table = continued_fraction_table(root)
    assert( cf_data['quotients'] == quotients )
    assert( cf_data['convergents'] == convergents )
    assert( cf_data['pell_numbers'] == pell_numbers )
    assert( cf_data['table'] == table )

    assert( pell_numbers[-1] == (-1)**(cf_data['period'] % 2) )
    assert( quotients[-1] == 2 * quotients[0] )

#-----------------------------

@given(
    st.integers(min_value=2, max_value=10**6).filter(lambda x: not is_square(x)),
    st.integers(min_value=1, max_value=30)
)
def test_continued_fractions_with_max(root, max_length):
    cf_data = continued_fraction_all(root, max_length)
    period = cf_data['period']

    if cf_data['complete']:
        assert( period <= max_length )
    else:
        assert( cf_data['period'] == max_length )

    assert( len(cf_data['quotients']) == period + 1 )
    assert( len(cf_data['convergents']) == period )
    assert( len(cf_data['pell_numbers']) == period )
    assert( len(cf_data['table']) == period + 1 )

