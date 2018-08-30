
##  itscomputers/number_theory/modular.py

import number_theory as nt
import primality as pr
import factorization as fac
import root_D as rtD

##############################

def small_remainder( a, m ):
    """allows negative remainders
    (a, m) -> (a % m) but allows negative result"""

    result = a % m
    if result > m//2:
        result -= m

    return result

##############################

def inverse( a, m, cyc_gr=None ):
    """inverse of a number relative to a modulus
    (a, m) -> x with (a*x % m) == 1"""

    if nt.gcd(a,m) != 1:
        raise ValueError(a, 'is not invertible modulo', m)
    
    if cyc_gr != None:
        for k, x in cyc_gr.items():
            if x == a:
                return cyc_gr[ (-k) % len(cyc_gr) ]

    x = nt.bezout(a,m)[0]
    if x > 0:
        return x
    else:
        return x + m

##############################

def power( a, e, m, cyc_gr=None ):
    """power (positive or negative) of a number for a given modulus
    (a, e, m) ->  a^e modulo m"""

    if cyc_gr != None:
        for k, x in cyc_gr.items():
            if x == a:
                return cyc_gr[ (a*e) % len(cyc_gr) ]

    if e == 0:
        return 1
    
    result = pow( a, abs(e), m )
    if e > 0:
        return result
    else:
        if nt.gcd(a,m) != 1:
            raise ValueError(a, 'is not invertible modulo', m)
        return inverse( result, m )

##############################

def group( m, F=None, method=None ):
    """multiplicative group of given modulus
    m -> list of x between 1, m-1 with gcd(x,m) == 1"""

    if method == 'gcd':
        gr = []
        for x in range(1, m//2 + 1):
            if nt.gcd( x, m ) == 1:
                gr += [ x, m-x ]
        return sorted( gr )

    else:
        if F == None:
            F = fac.factor(m)

        gr = pr.prime_to(F)

        return gr

##############################

def cyclic_group( m, F=None, gen=None ):
    """multiplicative group as powers of a generator
    m -> { k : g^k } where g is a generator modulo m"""

    if F == None:
        F = fac.factor(m)

    max_order = carmichael_lambda(m, F)
    group_order = euler_phi(m, F)
    if max_order != group_order:
        raise ValueError( 'group not cyclic' )

    if gen == None:
        gen = generator(m, F)

    cyc_gr = { 0 : 1 }
    for k in range(1, max_order):
        cyc_gr[k] = (cyc_gr[k-1] * gen) % m

    if len( set(cyc_gr.values()) ) != max_order:
        raise ValueError( gen, 'is not a generator modulo', m )

    return cyc_gr

##############################

def euler_phi( m, F=None ):
    """euler's totient function phi
    m -> phi(m) = order of multiplicative group"""

    if F == None:
        F = fac.factor(m)

    result = 1
    for p, e in fac.multiplicity( None, F ).items():
        result *= ( p-1 )
        for i in range(e-1):
            result *= p

    return result

##############################

def carmichael_lambda( m, F=None ):
    """Carmichael's function lambda
    m -> lambda( m ) = smallest power k 
    such that x^k = 1 mod m for all x in multiplicative group"""

    if F == None:
        F = fac.factor(m)

    result = 1
    for p, e in fac.multiplicity(None, F ).items():
        result *= ( p-1 ) // nt.gcd( result, p-1 )
        if p == 2:
            if e == 2:
                result *= p
            elif e > 2:
                result *= p**(e-2)
        else:
            result *= p**(e-1)

    return result

##############################

def order( a, m, cyc_gr=None, F=None, method=None ):
    """order in multiplicative group of given modulus
    (a, m) -> order of a modulo m"""

    if nt.gcd(a,m) != 1:
        raise ValueError( 'not invertible' )

    if a % m == 1:
        return 1
    elif a % m == m-1:
        return 2

    if cyc_gr != None:
        for k, x in cyc_gr.items():
            if x == a:
                break
        return len(cyc_gr) // nt.gcd( len(cyc_gr), k )

    if method == 'brute force':
        result = a
        exp = 1
        while result != 1:
            result = (result * a) % m
            exp += 1
        return exp
    
    if F == None:
        F = fac.factor(m)

    max_order = carmichael_lambda(m, F)
    
    primes = fac.factor( max_order )
    results = [ a ]
    exp = [ 1 ]
    for p in primes:
        new_results = [ power( results[ exp.index(e) ], p, m )\
                        for e in exp if p*e not in exp ]
        new_exp = [ p*e for e in exp if p*e not in exp ]
        if 1 in new_results:
            return new_exp[ new_results.index(1) ]
        else:
            results += new_results
            exp += new_exp
            
##############################

def generator( m, F=None, gr=None ):
    """find a generator of multiplicative group (if possible)
    m -> g such that (Z_m)* = { g^k for k=0..m-1 }"""

    if F == None:
        F = fac.factor(m)
    max_order = carmichael_lambda(m, F)
    group_order = euler_phi(m, F)
    if max_order != group_order:
        raise ValueError( 'group not cyclic' )

    if gr == None:
        for x in range(2,m):
            if nt.gcd(x,m) == 1:
                if order(x,m) == max_order:
                    break
    else:
        for x in gr:
            if order(x,m) == max_order:
                break

    return x

##############################

def jacobi( a, n, method=None ):
    """compute Jacobi symbol
    (a, n) -> (a|n), which equals
        0 if gcd(a,n) != 1,
        +/- 1 if gcd(a,n) = 1.
    it is a generalization of the legendre symbol"""

    if n % 2 == 0:
        raise ValueError(\
                'jacobi symbol (%s|%s) is undefined for %s even',\
                (a,n,n) )

    if n == 1:
        return 1
    
    if nt.gcd(a,n) != 1:
        return 0

    l, a = nt.padic( a % n, 2 )
    l %= 2
    if (l == 1) and (n % 8 in [3, 5]):
        sgn = -1
    else:
        sgn = 1

    if a == 1:
        return sgn
    else:
        if (n % 4 == 1) or (a % 4 == 1):
            qr_sgn = 1
        else:
            qr_sgn = -1
        return sgn * qr_sgn * jacobi( n, a )

##############################

def legendre( a, p, method='Jacobi' ):
    """compute legendre symbol
    (a, p) -> (a|p), which equals
        1 if a is a square modulo p
        -1 if a is not a square modulo p
        0 if a is congruent to 0 modulo p"""

    if p % 2 == 0:
        raise ValueError(\
                'legendre symbol (%s|%s) is undefined for %s even',\
                (a,p,p) )

    if method == 'Jacobi':
        return jacobi( a, p )

    if a % p == 0:
        return 0

    if method == 'euler criterion':
        return small_remainder( power(a, (p-1)//2, p), p )

##############################

def sqrt_minus_one( p, method='legendre' ):
    """compute square root of -1 modulo a prime
    p -> x such that x^2 = -1 modulo p
    (possible if and only if p % 4 == 1)"""

    if pr.is_prime(p) == False:
        error_message = str(p) + ' is not prime'
        raise ValueError( error_message )
    if p % 4 == 3:
        return None
    if p == 2:
        return 1

    if method == 'legendre':
        for x in range(2, p-1):
            if legendre(x, p) == -1:
                break

        val = power(x, (p-1)//4, p)

        return sorted( [val, p - val] )

    if method == 'wilson':
        val = 1
        for x in range(2, (p-1)//2 + 1):
            val = (val * x) % p
        return sorted( [val, p - val]  )

##############################

def sqrt( a, p, method=None, cyc_gr=None ):
    """compute a square root modulo a prime
    (a, p) -> x such that x^2 = a modulo p
    (possible if and only if (a|p) == 1)"""

    if pr.is_prime(p) == False:
        error_message = str(p) + ' is not prime'
        raise ValueError( error_message )
    if a % p == 0:
        return 0
    if legendre(a,p) != 1:
        return None

    if a % p == p-1:
        return sqrt_minus_one( p )

    if p % 4 == 3:
        val = power(a, (p+1)//4, p)
        return sorted( [val, p - val] )

    if cyc_gr:
        for k, x in cyc_gr.items():
            if x == a:
                val = cyc_gr[k//2]
                return sorted( [val, p - val] )

    S, Q = nt.padic(p-1, 2)
    m = len( '{0:b}'.format(p) )

    if (method == 'cipolla') or (S*(S - 1) > 8*m + 20):
        for y in range(2,p-1):
            D = (y**2 - a) % p
            if legendre(D,p) == -1:
                break
        val, B = rtD.QuadraticRing(D,p).power( [y, 1], (p+1)//2 )
        return sorted( [val, p - val] )

    if (method == 'tonelli-shanks') or (S*(S - 1) <= 8*m + 20):
        for z in range(1,p):
            if legendre(z, p) == -1:
                break
        M = S
        c = power(z, Q, p)
        t = power(a, Q, p)
        val = power(a, (Q+1)//2, p)
        if t == 0:
            return 0
        while t != 1:
            _t = t
            for i in range(1,M):
                _t = power(_t, 2, p)
                if _t == 1:
                    break
            b = c
            for j in range(M-i-1):
                b = power(b, 2, p)
            M = i
            c = power(b, 2, p)
            t = (t * c) % p
            val = (val * b) % p

        return sorted( [val, p - val] )

##################################################################

class MultiplicativeGroup:

    def __init__(self):
        print('group instance created')

    def populate(self, modulus=None, factorization=None):

        if factorization:
            m = 1
            for p in factorization:
                m *= p
            if modulus:
                if modulus != m:
                    raise ValueError('factorization does not match modulus')
                else:
                    self.modulus = modulus
            else:
                self.modulus = m
            self.factorization = factorization

        elif modulus:
            self.modulus = modulus
            self.factorization = fac.factor( modulus )

        else:
            raise ValueError('populate() requres modulus or factorization')

        self.elements = pr.prime_to( self.factorization )
        self.cardinality = euler_phi( self.modulus, self.factorization )
        self.max_order = carmichael_lambda( self.modulus, self.factorization )

        if self.cardinality == self.max_order:
            self.is_cyclic = True
        else:
            self.is_cyclic = False

    def order(self, element):
        if element in self.elements:
            return order( element, self.modulus, F=self.factorization )

    def inverse(self, element):
        return inverse( element, self.modulus )

    def power(self, element, exponent):
        if exponent > self.max_order:
            return self.power( element, exponent % self.max_order )
        else:
            return power( element, exponent, self.modulus )

    def find_generator(self):
        if self.is_cyclic:
            return generator( self.modulus, self.factorization, self.elements )

    def all_generators(self):
        if self.is_cyclic:
            g = self.find_generator()
            for j in range(1, self.max_order):
                if nt.gcd(j, self.max_order) == 1:
                    yield self.power(g, j)

    def __repr__(self):
        return 'group of invertible elements under multiplication ' +\
                'modulo ' + str(self.modulus)

##################################################################

class CyclicGroup( MultiplicativeGroup ):

    def __init__(self, modulus, gen=None):
        print('hi')
