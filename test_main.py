
if __name__ == '__main__':
    
    from numth.main import *
    from random import randint, choice

    ##########################
    #   test div
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        q, r = div(a, b)
        assert( a == q*b + r )
        assert( r < abs(b) )
        q, r = div(a, b, 'SMALL')
        assert( a == q*b + r )
        assert( (r <= abs(b)//2) and (r > -abs(b)//2) )

    #########################
    #   test gcd
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        d = gcd(a, b)
        assert( (a%d, b%d) == (0, 0) )
        assert( gcd(a//d, b//d) == 1 )

    ##########################
    #   test lcm
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        m = lcm(a, b)
        assert( (m%a, m%b) == (0, 0) )
        assert( gcd(m//a, m//b) == 1 )

    ##########################
    #   test bezout
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        x, y = bezout(a, b)
        d = gcd(a, b)
        assert( a*x + b*y == d )

    ##########################
    #   test padic
    for j in range(10):
        num, base = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        exp, rest = padic(num, base)
        assert( num == base**exp * rest )
        assert( rest % base != 0 )

    ##########################
    #   test mod_inverse
    for j in range(10):
        num, mod = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        while gcd(num, mod) != 1:
            num += 1
        inv = mod_inverse(num, mod)
        assert( inv > 0 and inv < mod )
        assert( (num * inv) % mod == 1 )

    ##########################
    #   test mod_power
    for j in range(10):
        num, exp, mod = (randint(1,10**4) for i in range(3))
        ans = mod_power(num, exp, mod)
        assert( (num**exp) % mod == ans )
        if gcd(num, mod) == 1:
            inv = mod_power(num, -exp, mod)
            assert( mod_inverse(ans, mod) == inv )

    ##########################
    #   test jacobi
    jacobi_row_15 = [0,1,1,0,1,0,0,-1,1,0,0,-1,0,-1,-1]
    assert( [jacobi(a, 15) for a in range(15)] == jacobi_row_15 )

