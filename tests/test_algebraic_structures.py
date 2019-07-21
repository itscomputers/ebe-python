#   tests/algebraic_structures_test.py
#===========================================================
import env
from hypothesis import given, assume, strategies as st

from numth.algebraic_structures import ModularRing
from numth.basic import gcd, jacobi, mod_power
from numth.modular import euler_phi
from numth.primality import next_prime
#===========================================================

@given(
    st.integers(min_value=2, max_value=10**3),
    st.integers(),
    st.integers(),
    st.integers()
)
def test_modular_ring(modulus, a, b, c):
    Zm = ModularRing(modulus)
    
    assert( Zm._factorization is None )
    assert( Zm.factorization() )
    assert( Zm._factorization == Zm.factorization() )

    assert( Zm._euler is None )
    assert( Zm.euler() is not None )
    assert( Zm._euler == Zm.euler() )
    
    assert( Zm._carmichael is None )
    assert( Zm.carmichael() is not None )
    assert( Zm._carmichael == Zm.carmichael() )
    
    assert( Zm._carmichael_factorization is None )
    assert( Zm.carmichael_factorization() is not None )
    assert( Zm._carmichael_factorization == Zm.carmichael_factorization() )
    
    assert( Zm._multiplicative_group is None )
    assert( Zm.multiplicative_group() is not None )
    assert( Zm._multiplicative_group == Zm.multiplicative_group() )

    if modulus == 2:
        assert( Zm.orders == {1: 1} )
    else:
        assert( Zm.orders == {1: 1, modulus - 1: 2} )

    if len(Zm.factorization().keys()) == 1:
        if 2 in Zm.factorization().keys():
            assert( Zm.is_cyclic() == (Zm.factorization()[2] < 3) )
        else:
            assert( Zm.is_cyclic() )
    elif len(Zm.factorization().keys()) == 2:
        assert( Zm.is_cyclic() == ((2, 1) in Zm.factorization().items()) )
    else:
        assert( not Zm.is_cyclic() )

    if not Zm.is_cyclic():
        assert( Zm.generator() is None )
        assert( Zm.as_cyclic_group() is None )
        assert( Zm.discrete_log() is None )
        assert( Zm.all_generators() == [] )
    else:
        assert( Zm._generator is None )
        assert( Zm._as_cyclic_group is None )
        assert( Zm._discrete_log is None )

    assert( Zm.elem(a) == a % modulus )
    assert( Zm.add(a, b, c) == (a + b + c) % modulus )
    assert( Zm.mult(a, b, c) == (a * b * c) % modulus )

    x = Zm.multiplicative_group()[a % Zm.euler()]
    assert( Zm.power_of(x, b) == mod_power(x, b, modulus) )
    assert( Zm.mult(x, Zm.inverse_of(x)) == 1 )
    order = Zm.order_of(x)
    assert( len(Zm.cyclic_subgroup_from(x).keys()) == order )
    
    Zm.all_orders()
    assert( Zm.orders == Zm.all_orders() )
    assert( max(Zm.orders.values()) == Zm.carmichael() )

    prime = next_prime(modulus)
    Zp = ModularRing(prime)
    assert( Zp.is_cyclic() )
    Zp.all_orders()

    gens = [x for x in Zp.multiplicative_group() if Zp.orders[x] == prime - 1]
    assert( len(gens) == euler_phi(prime - 1) )
    for x in gens:
        assert( gcd(Zp.discrete_log()[x], prime - 1) == 1 )
    
    assert( Zp.elem(a) == a % prime )
    assert( Zp.add(a, b, c) == (a + b + c) % prime )
    assert( Zp.mult(a, b, c) == (a * b * c) % prime )

    for x in (y for y in map(Zp.elem, (a, b, c)) if y != 0):
        assert( Zp.power_of(x, b) == mod_power(x, b, prime) )
        assert( Zp.mult(x, Zp.inverse_of(x)) == 1 )
        assert( len(Zp.cyclic_subgroup_from(x).keys()) == Zp.order_of(x) )
        if jacobi(x, prime) == 1:
            for y in Zp.sqrt_of(x):
                assert( Zp.power_of(y, 2) == x )

