#   tests/types_polynomial_test.py
# ===========================================================
from hypothesis import assume, given, strategies as st
from collections import defaultdict

import env  # noqa
from lib.basic import is_square
from lib.types import frac, Rational, Quadratic
from lib.types.polynomial import (
    Polynomial,
    polyn,
    _string_to_dict,
)

# ===========================================================


@st.composite
def polynomial(
    draw,
    num_terms,
    min_coeff=None,
    max_coeff=None,
    min_exp=0,
    max_exp=100,
    coeff_filter=lambda x: True,
):
    num_terms = min(num_terms, max_exp - min_exp + 1)
    exponents = draw(
        st.sets(
            st.integers(
                min_value=min_exp,
                max_value=max_exp,
            ),
            min_size=num_terms,
            max_size=num_terms,
        ),
    )

    return Polynomial(
        dict(
            (
                exp,
                draw(
                    st.integers(min_value=min_coeff, max_value=max_coeff).filter(
                        coeff_filter
                    )
                ),
            )
            for exp in exponents
        )
    )


@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume(numer != 0)
    return Rational(numer, denom)


def nonzero(number):
    return number != 0


# ===========================================================


@given(
    st.integers(min_value=0, max_value=500),
    st.integers(min_value=1, max_value=500),
    st.integers(min_value=1, max_value=500),
)
def test_string_to_dict(e, c, d):
    for expected_dict, string in (
        ({e: c}, "{}a^{}".format(c, e)),
        ({e: c}, "{}*b^{}".format(c, e)),
        ({e: c}, "+{}c^{}".format(c, e)),
        ({e: c}, "+{}*d^{}".format(c, e)),
        ({e: -c}, "-{}e^{}".format(c, e)),
        ({e: -c}, "-{}*f^{}".format(c, e)),
        ({e: frac(c, d)}, "{}/{}g^{}".format(c, d, e)),
        ({e: frac(c, d)}, "{}/{}*h^{}".format(c, d, e)),
        ({e: frac(c, d)}, "+{}/{}i^{}".format(c, d, e)),
        ({e: frac(c, d)}, "+{}/{}*j^{}".format(c, d, e)),
        ({e: -frac(c, d)}, "-{}/{}k^{}".format(c, d, e)),
        ({e: -frac(c, d)}, "-{}/{}*k^{}".format(c, d, e)),
        ({e: 1}, "x^{}".format(e)),
        ({e: 1}, "+y^{}".format(e)),
        ({e: -1}, "-z^{}".format(e)),
        ({1: c}, "{}A".format(c)),
        ({1: c}, "{}*B".format(c)),
        ({1: c}, "+{}C".format(c)),
        ({1: c}, "+{}*D".format(c)),
        ({1: -c}, "-{}E".format(c)),
        ({1: -c}, "-{}*F".format(c)),
        ({1: frac(c, d)}, "{}/{}G".format(c, d)),
        ({1: frac(c, d)}, "{}/{}*H".format(c, d)),
        ({1: frac(c, d)}, "+{}/{}I".format(c, d)),
        ({1: frac(c, d)}, "+{}/{}*J".format(c, d)),
        ({1: -frac(c, d)}, "-{}/{}K".format(c, d)),
        ({1: -frac(c, d)}, "-{}/{}*K".format(c, d)),
        ({e: 0}, "0U^{}".format(e)),
        ({e: 0}, "0*V^{}".format(e)),
        ({e: 0}, "+0W^{}".format(e)),
        ({e: 0}, "+0*X^{}".format(e)),
        ({e: 0}, "-0Y^{}".format(e)),
        ({e: 0}, "-0*Z^{}".format(e)),
        ({0: c}, "{}".format(c)),
        ({0: 0}, "0"),
    ):
        assert _string_to_dict(string) == expected_dict
        assert polyn(string) == Polynomial(expected_dict)
        assert polyn(string) == polyn(expected_dict)


@given(polynomial(5))
def test_from_string(a):
    assert Polynomial.from_string(repr(a)) == a
    assert polyn(repr(a)) == a


@given(*(8 * [st.integers()]))
def test_from_coeff_list(a, b, c, d, e, f, g, h):
    coeff_list = (a, b, c, d, e, f, g, h)
    p = Polynomial({0: a, 1: b, 2: c, 3: d, 4: e, 5: f, 6: g, 7: h})
    assert Polynomial.from_coeff_list(*coeff_list) == p
    assert polyn(*coeff_list) == p


# =============================


@given(polynomial(3))
def test_degree_and_leading_coeff(a):
    if a.coeffs != dict():
        assert a.degree == max(a.coeffs.items())[0]
        assert a.leading_coeff == max(a.coeffs.items())[1]
    else:
        assert a.degree == -1
        assert a.leading_coeff == 0


# =============================


@given(polynomial(3), polynomial(3))
def test_eq(a, b):
    assert a == a
    if sorted(a.coeffs.items()) == sorted(b.coeffs.items()):
        assert a == b
    else:
        assert a != b


@given(polynomial(3), st.integers())
def test_eq_int(a, b):
    if a.degree == -1 and b == 0:
        assert a == b
    elif a.degree == 0 and a.coeffs[0] == b:
        assert a == b
    else:
        assert a != b


@given(polynomial(3), rational())
def test_eq_Rational(a, b):
    if a.degree == -1 and b == 0:
        assert a == b
    elif a.degree == 0 and a[0] == b:
        assert a == b
    else:
        assert a != b


# =============================


@given(polynomial(3))
def test_neg(a):
    assert type(-a) is Polynomial
    assert -a == Polynomial({e: -c for e, c in a.coeffs.items()})
    assert a + -a == -a + a == 0
    assert -a == -1 * a == a * -1


@given(polynomial(3))
def test_canonical(a):
    assert a.canonical().leading_coeff >= 0


@given(polynomial(3, coeff_filter=nonzero), rational(nonzero=True))
def test_clear_denominators(a, b):
    assert set(
        map(lambda x: x.denom, (a * b).clear_denominators().coeffs.values())
    ) == set([1])


# =============================


@given(polynomial(2, coeff_filter=nonzero), st.integers())
def test_eval(a, b):
    (e1, c1), (e2, c2) = a.coeffs.items()
    assert a.eval(b) == c1 * b**e1 + c2 * b**e2


@given(polynomial(2, coeff_filter=nonzero), st.integers(), st.integers(min_value=2))
def test_mod_eval(a, b, m):
    (e1, c1), (e2, c2) = a.coeffs.items()
    assert a.mod_eval(b, m) == (c1 * pow(b, e1, m) + c2 * pow(b, e2, m)) % m
    assert a.mod_eval(b, m) == a.eval(b) % m


# =============================


@given(polynomial(3), polynomial(3), st.integers())
def test_derivative(a, b, c):
    assert type(a.derivative()) is Polynomial
    if a != 0:
        assert a.derivative().degree == a.degree - 1
    assert a.derivative(order=3) == a.derivative().derivative().derivative()
    assert (c + a).derivative() == a.derivative()
    assert (c * a).derivative() == c * a.derivative()
    assert (a + b).derivative() == a.derivative() + b.derivative()
    assert (a * b).derivative() == a.derivative() * b + a * b.derivative()


@given(polynomial(3), st.integers(), st.integers().filter(nonzero))
def test_integral(a, b, c):
    assert type(a.integral()) is Polynomial
    if a != 0 or b != 0:
        assert a.integral(b).degree == a.degree + 1
    assert a.integral(b).derivative() == a
    assert a.derivative().integral(0 if 0 not in a.coeffs else a.coeffs[0]) == a
    assert a.integral(b).eval(0) == b
    assert (c * a).integral() == c * a.integral()


# =============================


@given(polynomial(3), polynomial(4))
def test_add(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Polynomial
    assert result == reverse
    assert result == polyn("+".join([repr(a), repr(b)]))
    assert result == Polynomial(
        dict(
            (exp, defaultdict(int, a.coeffs)[exp] + defaultdict(int, b.coeffs)[exp])
            for exp in set(a.coeffs.keys()) | set(b.coeffs.keys())
        )
    )


@given(polynomial(3), st.integers())
def test_add_int(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == reverse
    assert result == polyn("+".join([repr(a), repr(b)]))
    assert result == Polynomial(
        dict(
            (exp, defaultdict(int, a.coeffs)[exp] + (b if exp == 0 else 0))
            for exp in set(a.coeffs.keys()) | set([0])
        )
    )


@given(polynomial(3), rational())
def test_add_Rational(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == reverse
    assert result == polyn("+".join([repr(a), repr(b)]))
    assert result == Polynomial(
        dict(
            (exp, defaultdict(int, a.coeffs)[exp] + (b if exp == 0 else 0))
            for exp in set(a.coeffs.keys()) | set([0])
        )
    )


# =============================


@given(polynomial(3), polynomial(4))
def test_sub(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Polynomial
    assert result == -reverse
    assert result == a + (-b)


@given(polynomial(3), st.integers())
def test_sub_int(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == -reverse
    assert result == a + (-b)


@given(polynomial(3), rational())
def test_sub_Rational(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == -reverse
    assert result == a + (-b)


# =============================


@given(polynomial(3), polynomial(3))
def test_mul(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == reverse
    assert result == sum(
        Polynomial(dict((ea + eb, ca * cb) for ea, ca in a.coeffs.items()))
        for eb, cb in b.coeffs.items()
    )


@given(polynomial(3), st.integers())
def test_mul_int(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == reverse
    assert result == Polynomial(dict((exp, coeff * b) for exp, coeff in a.coeffs.items()))


@given(polynomial(3), rational())
def test_mul_Rational(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Polynomial
    assert type(reverse) is Polynomial
    assert result == reverse
    assert result == Polynomial(dict((exp, coeff * b) for exp, coeff in a.coeffs.items()))


# -----------------------------


@given(polynomial(3), polynomial(4), polynomial(2), polynomial(3))
def test_distributive_law(p1, p2, p3, p4):
    assert (p1 + p2) * (p3 + p4) == p1 * p3 + p1 * p4 + p2 * p3 + p2 * p4


# =============================


@given(polynomial(3), st.integers().filter(nonzero))
def test_div_int(a, b):
    result = a / b
    assert type(result) is Polynomial
    assert result * b == a


@given(polynomial(3), rational(nonzero=True))
def test_div_Rational(a, b):
    result = a / b
    assert type(result) is Polynomial
    assert result * b == a


# =============================


@given(polynomial(3), polynomial(3, coeff_filter=nonzero))
def test_div_with_remainder(a, b):
    quotient, remainder = a.div_with_remainder(b)
    assert type(quotient) is Polynomial
    assert type(remainder) is Polynomial
    assert a == b * quotient + remainder
    assert remainder.degree < b.degree


@given(polynomial(3), st.integers().filter(nonzero))
def test_div_mod_int(a, b):
    quotient, remainder = a // b, a % b
    assert type(quotient) is Polynomial
    assert type(remainder) is Polynomial
    assert a == b * quotient + remainder


@given(polynomial(3), rational(nonzero=True))
def test_div_mod_rational(a, b):
    quotient, remainder = a // b, a % b
    assert type(quotient) is Polynomial
    assert type(remainder) is Polynomial
    assert a == b * quotient + remainder


# =============================


@given(
    polynomial(2, coeff_filter=nonzero),
    st.integers(min_value=0, max_value=5),
    st.integers(min_value=0, max_value=5),
)
def test_pow(a, m, n):
    mth_power = a**m
    nth_power = a**n
    sum_power = a ** (m + n)
    assert type(a**0) is Polynomial
    assert type(a**1) is Polynomial
    assert type(mth_power) is Polynomial
    assert a**0 == 1
    assert a**1 == a
    assert a**2 == a * a
    assert mth_power * nth_power == sum_power
    assert sum_power.div_with_remainder(mth_power) == (nth_power, 0)


# =============================


@given(
    *(4 * [rational(nonzero)]), st.integers().filter(lambda x: x < 0 or not is_square(x))
)
def test_quadratic(a1, b1, a2, b2, d):
    g1 = Quadratic(a1, b1, d)
    g2 = Quadratic(a2, b2, d)
    p1 = Polynomial({0: a1, 1: b1})
    p2 = Polynomial({0: a2, 1: b2})
    m = Polynomial({0: -d, 2: 1})
    g = g1 * g2
    p = Polynomial({0: g.real, 1: g.imag})
    assert (p1 * p2) % m == p
