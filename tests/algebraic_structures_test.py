#   tests/algebraic_structures_test.py
#===========================================================
import env
from hypothesis import given, assume, strategies as st

from numth.algebraic_structures import ModularRing
from numth.basic import gcd, jacobi, mod_power
from numth.modular import euler_phi
from numth.primality import is_prime, next_prime
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
        assert( Zm.cyclic_group_dict() is None )
        assert( Zm.discrete_log_dict() is None )
        assert( Zm.all_generators() == [] )
    else:
        assert( Zm._generator is None )
        assert( Zm._cyclic_group_dict is None )
        assert( Zm._discrete_log_dict is None )

    assert( Zm.elem(a) == a % modulus )
    assert( Zm.add(a, b, c) == (a + b + c) % modulus )
    assert( Zm.mult(a, b, c) == (a * b * c) % modulus )

    x = Zm.multiplicative_group()[a % Zm.euler()]
    assert( Zm.power_of(x, b) == mod_power(x, b, modulus) )
    order = Zm.order_of(x)
    assert( len(Zm.cyclic_subgroup_from(x).keys()) == order )
    
    Zm.all_inverses()
    inverse_pairs = set(sorted(x) for x in Zm.inverses.items())
    for (x, y) in inverse_pairs:
        assert( Zm.mult(x, y) == 1 )

    Zm.all_orders()
    assert( Zm.orders == Zm.all_orders() )
    assert( max(Zm.orders.values()) == Zm.carmichael() )

    if Zm.is_cyclic():
        gens = set(x for x in Zm.multiplicative_group() if Zm.orders[x] == Zm.euler())
        gens2 = set(x for i, x in Zm.cyclic_group_dict().items() if gcd(i, Zm.euler()) == 1)
        assert( gens == gens2 )
    
    if Zm.is_field() and Zm.modulus > 2:
        assert( is_prime(Zm.modulus) )
        for x in (Zm.elem(y) for y in (a, b, c) if Zm.elem(y) != 0):
            if jacobi(x, Zm.modulus) == 1:
                for y in Zm.sqrt_of(x):
                    assert( Zm.power_of(y, 2) == x )
                    assert( Zm.log_of(x) == (Zm.log_of(y) * 2) % (Zm.euler()) )

