#   tests/rational_approximation_test.py
#===========================================================
import env
from hypothesis import assume, given, strategies as st

from lib.basic import is_square
from lib.continued_fraction import continued_fraction_pell_numbers
from lib.types import Polynomial
from lib.rational_approximation import *
#===========================================================

def assert_convergence_and_advance(curr, diff, gen):
    prev, curr = curr, next(gen)
    next_diff = abs(curr - prev)
    assert( next_diff <= diff )
    return curr, next_diff

#-----------------------------

def approx_sqrt(number):
    gen = halley_sqrt_gen(number)
    next(gen)
    return next(gen)

#===========================================================
#   general
#===========================================================

@given(st.integers(min_value=-1, max_value=100))
def test_newton_gen(x_coeff):
    p = Polynomial({3:1, 1:x_coeff, 0:-5})
    gen = newton_gen(p, 1)
    for i in range(5):
        next(gen)
    assert( p.eval(next(gen)).approx_equal(0, 3) )

#-----------------------------

@given(st.integers(min_value=-1, max_value=100))
def test_halley_gen(x_coeff):
    p = Polynomial({3:1, 1:x_coeff, 0:-5})
    gen = halley_gen(p, 1)
    for i in range(3):
        next(gen)
    assert( p.eval(next(gen)).approx_equal(0, 3) )

#===========================================================
#   pi
#===========================================================

pi_string = '3.14159265358979323846264338327950288419716939937510' \
            + '58209749445923078164062862089986280348253421170679' \
            + '82148086513282306647093844609550582231725359408128' \
            + '48111745028410270193852110555964462294895493038196' \
            + '44288109756659334461284756482337867831652712019091' \
            + '45648566923460348610454326648213393607260249141273' \
            + '72458700660631558817488152092096282925409171536436' \
            + '78925903600113305305488204665213841469519415116094' \
            + '33057270365759591953092186117381932611793105118548' \
            + '07446237996274956735188575272489122793818301194912' \
            + '98336733624406566430860213949463952247371907021798' \
            + '60943702770539217176293176752384674818467669405132' \
            + '00056812714526356082778577134275778960917363717872' \
            + '14684409012249534301465495853710507922796892589235' \
            + '42019956112129021960864034418159813629774771309960' \
            + '51870721134999999837297804995105973173281609631859' \
            + '50244594553469083026425223082533446850352619311881' \
            + '71010003137838752886587533208381420617177669147303' \
            + '59825349042875546873115956286388235378759375195778' \
            + '18577805321712268066130019278766111959092164201989'

def test_pi():
    for digits in [1, 10, 50, 100, 500, 1000]:
        assert( pi(digits).decimal(digits)[:-2] == pi_string[:digits] )

#-----------------------------

def test_ramanujan_hardy():
    gen = ramanujan_hardy(50)
    prev = next(gen)
    curr = next(gen)

    for i in range(20):
        assert( prev.approx_equal(curr, 8*i) )
        prev, curr = curr, next(gen)

#===========================================================
#   sqrt
#===========================================================

@given(st.integers(min_value=1))
def test_babylonian(number):
    gen = babylonian_gen(number)
    prev = next(gen)
    curr = next(gen)
    diff = abs(curr - prev)

    for i in range(5):
        curr, diff = assert_convergence_and_advance(curr, diff, gen)

    assert( (curr**2).approx_equal(number, 30) )

#-----------------------------

@given(st.integers(min_value=1))
def test_halley_sqrt(number):
    gen = halley_sqrt_gen(number)
    prev = next(gen)
    curr = next(gen)
    diff = abs(curr - prev)

    for i in range(3):
        curr, diff = assert_convergence_and_advance(curr, diff, gen)

    assert( (curr**2).approx_equal(number, 30) )

#-----------------------------

@given(st.integers(min_value=1))
def test_bakshali(number):
    bak = bakhshali_gen(number)
    bab = babylonian_gen(number)
    for i in range(4):
        assert( next(bab) == next(bak) )
        next(bab)

#-----------------------------

@given(
    st.integers(
        min_value=2,
        max_value=10**5
    ).filter(lambda x: not is_square(x))
)
def test_continued_fraction_convergent(number):
    gen = continued_fraction_convergent_gen(number)
    pell_numbers = continued_fraction_pell_numbers(number)
    last = pell_numbers[-1]
    period = len(pell_numbers)

    prev = next(gen)
    curr = next(gen)
    diff = abs(curr - prev)
    counter = 1

    for i in range(50):
        pell = curr.numer**2 - number * curr.denom**2
        expected = last**(counter // period) * pell_numbers[counter % period]
        assert( pell == expected )
        prev, curr = curr, next(gen)
        next_diff = abs(curr - prev)
        counter += 1
        assert( next_diff < diff )

#-----------------------------

@given(st.integers(min_value=1).filter(lambda x: not is_square(x)))
def test_goldschmidt(number):
    assume( number != 3 )
    gen = goldschmidt_gen(number)

    for i in range(2):
        next(gen)

    for i in range(3):
        x, y = next(gen)
        assert( (x * y).approx_equal(1, i) )

#-----------------------------

@given(st.integers(min_value=1))
def test_ladder_arithmetic(number):
    gen = ladder_arithmetic_gen(number, approx_sqrt(number))
    prev = next(gen)
    curr = next(gen)
    diff = abs(curr - prev)

    for i in range(5):
        curr, diff = assert_convergence_and_advance(curr, diff, gen)

    assert( (curr**2).approx_equal(number, 10) )

#-----------------------------

@given(st.integers(min_value=1))
def test_linear_fractional_transformation(number):
    gen = linear_fractional_transformation_gen(number, approx_sqrt(number))
    prev = next(gen)
    curr = next(gen)
    diff = abs(curr - prev)

    for i in range(5):
        curr, diff = assert_convergence_and_advance(curr, diff, gen)

    assert( (curr**2).approx_equal(number, 10) )

