
##  ~/itscomputers/number_theory/factorization.py

import number_theory as nt
import modular as mod
import primality as pr
import approximation as apx
from random import randint
import itertools as it
from concurrent.futures import ProcessPoolExecutor, wait
import pebble
from time import time

##############################

def array_to_polyn( array, modulus=None ):
    """convert an array to a polynomial
    array -> f(x)
    where f(x) = array[0] + array[1]*x + array[2]*x**2 + ..."""

    if modulus:
        return lambda x :\
                sum([ array[i] * x**i for i in range(len(array)) ]) % modulus
    else:
        return lambda x :\
                sum([ array[i] * x**i for i in range(len(array)) ])

##############################

def pollard( number, seed, polyn, EXTRA=False ):
    """find factor using Pollard's rho method
    (number, seed, polyn) -> divisor d of number 
    using the sequence
    x0, x1, x2, ...
    where next x is the polynomial 
    evaluated at previous x modulo the number.
    Use the 'EXTRA=True' flag to return the divisor 
    along with the seed and polynomial"""

    f = array_to_polyn(polyn, number)
    xi = f(seed % number)
    x2i = f(xi)
    d = nt.gcd(x2i - xi, number)

    while d == 1:
        xi = f(xi)
        x2i = f( f(x2i) )
        d = nt.gcd(x2i - xi, number)

    if EXTRA == True:
        return {
            'seed'      :   seed, 
            'polyn'     :   polyn,
            'divisor'   :   d,
        }
    else:
        return d

##############################

def pollard_mp( number, seeds_and_polyns, timeout=None, EXTRA=False ):
    """for each seed, polyn in an array of seeds/polynomials,
    schedule pollard( number, seed, polyn ) in a ProcessPool.
    Cancel all threads once one of the threads successfully
    finds a divisor.
    Use 'timeout=NUM' to specify a timeout,
    and 'EXTRA=True' to provide the seed/polynomial that was successful.
    """
    
    divisor = None
    futures = []
    
    with pebble.ProcessPool() as pool:
        for seed, polyn in seeds_and_polyns:
            futures.append( pool.schedule(\
                pollard, (number, seed, polyn, EXTRA)\
            ))
        
        while divisor == None:
            wait(futures, timeout=timeout, return_when='FIRST_COMPLETED')
            for x in futures:
                if x.done() and (x.result != number):
                    divisor = x.result()
        
        for x in futures:
            if not x.done():
                x.cancel()

    return divisor

##############################

def random_seed_and_polyn(max_degree=None, max_coeff=None, max_seed=None):
    """generate a random polynomial.
    Use 'max_degree', 'max_coeff', and 'max_seed' to
    specify upper bounds on degree, coefficients, and seed."""

    if max_degree == None:
        max_degree = 5
    if max_coeff == None:
        max_coeff = 5
    if max_seed == None:
        max_seed = 10

    seed = randint(2, max_seed)
    deg = randint(2, max_degree)
    const = randint(1, max_coeff)
    polyn = [const]
    while len(polyn) < deg:
        polyn.append( randint(0, max_coeff) )
    polyn.append(1)

    return [seed, polyn]

##############################

def test_scenario(fixed_polyns ,lower_digits, upper_digits, number_per):
    times = []
    seeds = [2, 3] + [randint(4,1000) for j in range(1)]
    polyns = []
    numbers = []
    for i in range(lower_digits, upper_digits):
        for j in range(number_per):
            n = 1
            for j in range(3):
                n *= pr.next_prime(randint(10**i, 10**(i+1)))
            numbers.append(n)

    for p in fixed_polyns:
        for s in seeds:
            print('\nseed {}'.format(s))
            pp = p + [[randint(3,100),randint(0,100),1]\
                    for j in range(4-len(p))]
            print(pp)
            pp_dict = [ {'polyn' : x, 'count' : 0} for x in pp ]
            s_and_p = [ [s, x] for x in pp ]
            print('\npolyns {}'.format(pp))
            t0 = time()
            for n in numbers:
                d = pollard_mp(n, s_and_p, EXTRA=True)
                print('number {}, seed {} -- polyn {}'\
                        .format(n, d['seed'], d['polyn']))
                for y in pp_dict:
                    if y['polyn'] == d['polyn']:
                        y['count'] += 1
            t1 = time()
            print('elapsed time : {}'.format(t1-t0))
            times.append(t1-t0)
            polyns.append(pp_dict)

    print()
    for x in times:
        print(x)

    for s in seeds:
        print('\n\nseed {}'.format(s))
        for x in polyns:
            print()
            for y in x:
                print('{} : {}'.format(y['polyn'], y['count']))



    

        

def pollard_find_divisor(
        number,
        to=None,
        max_threads=None,
        seed_num=None,
        polyn_num=None,
        polyn_max_deg=None,
        polyn_max_coeff=None,
        extra=False             ):
    """use randomly generated polynomials and seeds to look for a divisor
    (number, timeout) -> divisor of number or TimeoutError"""

    if not seed_num:
        seed_num = 5
    if not polyn_num:
        polyn_num = 5
    if not polyn_max_deg:
        polyn_max_deg = 5
    if not polyn_max_coeff:
        polyn_max_coeff = 10

    seeds = [2, 3]
    while len(seeds) < seed_num:
        seed = randint(2, min(number,1000))
        if seed not in seeds:
            seeds.append(seed)
    polyns = [ [1,0,1] ]
    while len(polyns) < polyn_num:
        deg = randint(2,polyn_max_deg)
        p = [1] + [ randint(0, polyn_max_coeff) for i in range(deg) ]
        if p[-1] == 0:
            p[-1] = 1
        if p not in polyns:
            polyns.append(p)

    pool = pebble.ProcessPool()
    futures = []
    inputs = []
    t0 = time()
    for x in seeds:
        for p in polyns:
            inputs.append( [x, p] )
            futures.append(\
                    pool.schedule(pollard, (number, x, p, extra)) )
    wait(futures, timeout=to, return_when='FIRST_COMPLETED')
    t1 = time()
    divisors = []
    completed = []
    for x in futures:
        if x.done():
            divisors.append( x.result() )
            completed.append( x )
        else:
            x.cancel()

    print('\nsuccessful:')
    for d in divisors:
        a,b,c = d
        print('divisor : {}, from seed: {}, polynomial: {}'.format(c,a,b))
    print('\ntime elapsed:', t1-t0, end=', ')
    print('number of threads completed = {}'.format(len(divisors)))

    print('\nseeds:\n', seeds)
    print('\npolyns:\n', polyns)
    return divisors

##############################

def test_pollard( num_primes, size_primes, time_out ):
    number = 1
    primes = []
    for i in range( num_primes ):
        prime = pr.next_prime( randint(10**(size_primes-1), 10**size_primes) )
        primes.append(str(prime))
        number *= prime
    print('\n' + ' * '.join(primes) + ' =', number, '\n')
    
    pollard_find_divisor(
            number, 
            to=time_out, 
            extra=True )



##############################

def pollard_with_yield( number, seed, polyn, extra=False ):

    f = lambda x : sum([\
            polyn[i] * x**(i+1)\
            for i in range( len(polyn) )
        ]) % number

    r = f( seed % number )
    R = f(r)
    d = nt.gcd( R-r, number )

    while True:
        if extra == True:
            yield (d, seed, polyn)
        else:
            yield d
        r = f(r)
        R = f( f(R) )
        d = nt.gcd( R-r, number )

##############################

def simultaneous_pollard( number, seeds=None, lin_coeff=None, const=None ):
    if seeds == None:
        seeds = [2, 3, 5, 6, 8]
    elif isinstance(seeds,int):
        seeds = [ randint(2,1000) for i in range(seeds) ]
    if lin_coeff == None:
        lin_coeff = [0, 1]
    elif isinstance(lin_coeff,int):
        lin_coeff = [ randint(0,1000) for i in range(lin_coeff) ]
    if const == None:
        const = [1, 2]
    elif isinstance(const,int):
        const = [ randint(0,1000) for i in range(const) ]
    
    arms = it.product(seeds, lin_coeff, const)
    pollard_generators = { (x0, b, c) :\
            pollard_with_yield(number, x0, b, c)\
            for x0, b, c in arms
            }

    factor_found = False

    while not factor_found:
        dd = { x : next(pollard_generators[x]) for x in pollard_generators }
        for x, d in dd.items():
            if d > 1:
                if d < number:
                    print('found factor with {}'.format(x))
                    factor_found = True
                    factor = d
                    break
                else:
                    print('deleting {}'.format(x))
                    del pollard_generators[x]

    if factor_found:
        return factor
    else:
        print("factor not found")
    






##########################

def find_divisor( number, seeds=[2,3,5,6,8], consts=[1,2,-1] ):
    """find factor using various seeds/polynomials in pollard
    number -> d, where d | number and d > 1"""

    for n in consts:
        for x0 in seeds:
            d = pollard( number, x0, [1,0,n] )
            if d != number:
                return d

    return number

##########################

def factor( number, L=100, seeds=[2,3,5,6,8], consts=[1,2,-1] ):
    """prime factorization
    number -> list of prime factors of number
    (keeps track of nonprime factors that were not factored)"""

    a = abs( number )
    if a < 2:
        return None
    
    result = []
    for prime in pr.prime_range( 2, L ):
        if a % prime == 0:
            e, a = nt.padic( a, prime )
            result += e * [ prime ]
            if a == 1:
                return result 

    unfactored = [ a ]
    bad = []

    while unfactored != []:
        b = unfactored[0]
        unfactored.remove( b )
        if pr.is_prime( b ):
            result.append( b )
        else:
            d = find_divisor(b,seeds,consts)
            if d == b:
                bad.append( b )
                result.append( b )
            else:
                for x in [ d, b//d ]:
                    if pr.is_prime( x ):
                        result.append( x )
                    else:
                        unfactored.append( x )

    if bad != []:
        raise ValueError( 'factorization failed' )

    return result

##########################
            
def multiplicity( number=None, factorization=None ):
    """factorization with multiplicity
    F -> { p1:e1, p2:e2, ... }""" 

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    return { prime : factorization.count(prime) \
                for prime in sorted( set(factorization) ) }
    
##########################

def print_factorization( number=None, factorization=None ):
    """prints factorization from list of prime divisors
    F -> p1^e1 * p2^e2 * ..."""

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    result = []
    for prime, exp in sorted( multiplicity(None,factorization).items() ):
        if exp == 1:
            result.append( str(prime) )
        else:
            result.append( str(prime) + '^' + str(exp) )

    return ' * '.join( result )

##########################

def divisors( number=None, factorization=None ):
    """extracts list of divisors from list of prime divisors
    F -> [ d1, d2, ... ]"""

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    result = [ 1 ]
    for prime in factorization:
        result += [ prime*d for d in result if prime*d not in result ]

    return sorted( result )

##########################
##########################
##########################
##########################

if __name__ == '__main__':

    print('\n\n\n')
    t0 = time()
    test_pollard( 3, 10, 5 )
    print('\n\n')
    t1 = time()
    sleep(2)
    t2 = time()
    test_pollard( 6, 11, 8 )
    print('\n\n')
    t3 = time()
    sleep(2)
    t4 = time()
    test_pollard( 10, 12, 10 )
    t5 = time()

    print('\n\n\nelapsed times:', t1-t0, t3-t2, t5-t4, '\n\n')
