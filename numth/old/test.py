
import number_theory as nt
import modular as mod
import factorization as fac
import primality as pr
import root_D as rtD
from random import randint, choice

###     testing         ###

# nt.div 
for i in range(100):
    a, b =\
        choice([-1,1])*randint(1,1000000),\
        choice([-1,1])*randint(1,1000000)
    q, r = nt.div(a, b)
    q_, r_ = nt.div(a, b, 'small remainder')
    if (r < 0) or (r >= abs(b)) or (a != q*b + r):
        print('nt.div error', a, b, q, r)
    if (r_ < -abs(b)/2) or (r_ >= abs(b)/2) or (a != q_*b + r_):
        print('nt.div error', a, b, q_, r_)

# nt.gcd
for i in range(100):
    a, b =\
        choice([-1,1])*randint(1,1000000),\
        choice([-1,1])*randint(1,1000000)
    d = nt.gcd(a, b)
    if ([ a%d, b%d ] != [0, 0]) or (nt.gcd(a//d,b//d) != 1):
        print('nt.gcd error', a, b, d)

# nt.bezout
for i in range(100):
    a, b =\
        choice([-1,1])*randint(1,1000000),\
        choice([-1,1])*randint(1,1000000)
    x, y = nt.bezout(a, b)
    d = nt.gcd(a, b)
    if a*x + b*y != d:
        print('nt.bezout error', a, b, x, y, d)

# nt.padic
for i in range(100):
    a, p =\
        choice([-1,1])*randint(1,1000000),\
        randint(1,1000000)
    e, b = nt.padic( a, p )
    if (a != p**e * b) or (b % p == 0):
        print('nt.padic error', a, p, e, b)

# mod.inverse
for i in range(100):
    a, m =\
        choice([-1,1])*randint(1,1000000),\
        randint(1,1000000)
    if nt.gcd(a, m) == 1:
        x = mod.inverse(a, m)
        if (a*x % m != 1) or (x < 0) or (x >= m):
            print('mod.inverse error:', a, x,  m)

# mod.power
for i in range(100):
    a, e, m =\
        choice([-1,1])*randint(1,1000000),\
        randint(1,1000),\
        randint(1,1000000)
    b = mod.power( a, e, m )
    if (a**e) % m != b:
        print('mod.power error', a, e, m)
    if nt.gcd(a,m) == 1:
        c = mod.power( a, -e, m )
        if (mod.inverse(b,m) != c) or (b*c % m != 1):
            print('mod.power error', a, -e, m)

#   # pr.is_prime
#   counter = 1
#   for i in range(3,100000003,2):
#      if i in [10**k+1 for k in range(1,10)]:
#          print(i-1, counter)
#      if prime.is_prime(i) == 'prime':
#          counter += 1

# pr.prime_to
for i in range(5):
    P = []
    while len(P) < 5:
        P.append(choice([2,3,5,7,11]))
    m = 1
    for p in P:
       m *= p
    M = 1
    for p in set(P):
        M *= p
    Z_m = [ x for x in range(1,m) if nt.gcd(x,M) == 1 ]
    ZZ_m = pr.prime_to(P)
    if Z_m != ZZ_m:
        print('pr.prime_to error', P)


# pr.next_prime
for i in range(5):
    a = randint(2,10**6)
    k = randint(1,11)
    P = pr.next_prime(a,k)
    if k == 1:
        if not pr.next_prime(P):
            print('pr.next_prime error', a, P)
    else:
        for p in P:
            if not pr.is_prime(p):
                print('pr.next_prime error', a, p)
        for x in range(a-a%2+1,max(P)+1,2):
            if x not in P:
                if pr.is_prime(x):
                    print('pr.next_prime error', a, P, 'missed this prime', x)

# pr.prime_range
L = randint(1,10**10)
U = randint(L,L+10**4)
if pr.prime_range(L,U) != [ x for x in range(L, U) if pr.is_prime(x) ]:
    print('pr.prime_range error', L, U)

# fac.factor
for i in range(10):
    a = randint(2,10**15)
    F = fac.factor( a )
    FM = fac.multiplicity( a, F )
    D = fac.divisors( a, F )
    m = 1
    for p in F:
        m *= p
    n = 1
    for e in [ FM[x] for x in FM ]:
        n *= e+1
    if (m != a) or (n != len(D)):
        print('fac.factor error', a, F, FM, D)
    for p in F:
        if not pr.is_prime( p ):
            print('fac.factor error', a, p)

import time

# mod.group
test_moduli = [ randint(2,10**5) for i in range(5) ]
Z_m = {}
ZZ_m = {}
euler = { x : mod.euler_phi( x ) for x in test_moduli }
carmichael = { x : mod.carmichael_lambda( x ) for x in test_moduli }
t0 = time.time()
for x in test_moduli:
    Z_m[x] = mod.group( x )
t1 = time.time()
for x in test_moduli:
    ZZ_m[x] = mod.group( x, method='gcd' )
t2 = time.time()
if (t2 < t1):
    print('mod.group faster with gcd method!!!')
for x in test_moduli:
    if Z_m[x] != ZZ_m[x]:
        print('mod.group error', x)
    if len(Z_m[x]) != euler[x]:
        print('mod.euler_phi error', x)
    for y in Z_m[x]:
        if mod.power( y, carmichael[x], x ) != 1:
            print('mod.carmichael_lambda error', x)
for x in test_moduli:
    test_elements = [ choice(Z_m[x]) for i in range(5) ]
    test_orders = { a : [] for a in test_elements }
    t3 = time.time()
    for a in test_elements:
        test_orders[a].append( mod.order(a, x) )
    t4 = time.time()
    for a in test_elements:
        test_orders[a].append( mod.order(a, x, method='brute force' ) )
    t5 = time.time()
    if t5-t4 < t4-t3:
        print('brute force order faster for', test_elements, 'modulo', x)
    for a in test_elements:
        if test_orders[a][0] != test_orders[a][1]:
            print('mod.order error', a, x)



