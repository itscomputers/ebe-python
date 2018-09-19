
##  ~/itscomputers/number_theory/primality.py

from random import randint

import number_theory as nt
import modular as mod

##########################

def miller_rabin_witness( number, witness ):
    """whether a number is composite or probably prime, according to witness
    (number, witness) -> 'composite' or 'probably prime'
    this uses the Miller-Rabin test"""

    l, m = nt.padic( number-1, 2 )
    X = mod.power( witness, m, number )

    if X % number in [ 1, number-1 ]:
        return 'pseudoprime'

    for i in range( 1, l+1 ):
        Y = pow( X, 2, number )
        if Y % number == number-1:
            return 'pseudoprime'
        if Y % number == 1:
            return 'composite'
        X = Y

    return 'composite'

##########################

def miller_rabin_test( number, MR=None ):
    """Miller-Rabin primality test
    a test that determines if a is prime or composite.
    for a < 341550071728321, the test is deteriministic.
    otherwise, the test is probabilistic and gives the
    correct result with probability > 1 - (.25)^MR
    (number, MR) -> True or False using MR witnesses"""

    if number == 2:
        return 'prime'
    elif number % 2 == 0:
        return 'composite'
    elif number < 2047:
        witnesses = [2]
    elif number < 1373653:
        witnesses = [2,3]
    elif number < 25326001:
        witnesses = [2,3,5]
    elif number < 3215031751:
        witnesses = [2,3,5,7]
    elif number < 2152302898747:
        witnesses = [2,3,5,7,11]
    elif number < 3474749660383:
        witnesses = [2,3,5,7,11,13]
    elif number < 341550071728321:
        witnesses = [2,3,5,7,11,13,17]
    else:
        if MR == None:
            MR = 10
        if MR > number:
            witnesses = [ x for x in range(2,number-1) ]
        else:
            witnesses = []
            while len(witnesses) < MR:
                x = randint( 2, number-1 )
                if x not in witnesses:
                    witnesses.append(x)
    
    for x in witnesses:
        if miller_rabin_witness(number,x) == 'composite':
            return 'composite'
    if number < 341550071728321:
        return 'prime'
    return 'strong pseudoprime'

##############################

def lucas_double_index( U, V, Q, n ):
    return [
        (U*V) % n, 
        (V*V - 2*Q) % n,
        (Q**2) % n
    ]

##############################

def lucas_index_plus_one( U, V, P, Q, Q1, n ):
    return [
        (P*U + V) * (n+1)//2 % n,
        ((P**2 - 4*Q1)*U + P*V) * (n+1)//2 % n,
        (Q * Q1) % n
    ]

##############################

def lucas_sequence( k, P, Q, n ):
    UV = [ [0, 2, 1], [1, P%n, Q] ]
    for i in range(k-1):
        U_, V_, Q_ = UV[-1]
        U__, V__, Q__ = UV[-2]
        UV.append([
            (P*U_ - Q*U__) % n, 
            (P*V_ - Q*V__) % n, (
                Q*Q_) % n 
        ])
    return UV

##############################

def lucas_sequence_by_index( k, P, Q, n ):
    if k == 0:
        return [0, 2, 1]
    elif k == 1:
        return [1, P, Q]
    elif k % 2 == 0:
        U_, V_, Q_ = lucas_sequence_by_index(k//2, P, Q, n)
        return lucas_double_index(U_, V_, Q_, n)
    else:
        U_, V_, Q_ = lucas_sequence_by_index(k-1, P, Q, n)
        return lucas_index_plus_one(U_, V_, P, Q_, Q, n)

##############################

def lucas_witness( number, P, Q ):
    """Lucas test for primality, a probabilistic test"""

    D = P**2 - 4*Q
    gcd_D_number = nt.gcd(D,number)
    if gcd_D_number > 1:
        if gcd_D_number < number:
            return 'composite'
        else:
            return None

    delta = number - mod.jacobi(D, number)
    s, d = nt.padic(delta, 2)
    strong = False
    
    U, V, Q_ = lucas_sequence_by_index(d, P, Q, number)
    if U == 0:
        strong = True

    for j in range(s-1):
        U, V, Q_ = lucas_double_index(U, V, Q_, number)
        if V == 0:
            strong = True
    U, V = lucas_double_index(U, V, Q_, number)[:2]

    if (U == 0):
        if delta - number == 1:
            if V != (2*Q) % number:
                return 'composite'
            if Q_ != (Q * mod.jacobi(Q, number) ) % number:
                return 'composite'
        else:
            if Q_ != mod.jacobi(Q, number) % number:
                return 'composite'
        if strong == True:
            return 'strong pseudoprime'
        else:
            return 'pseudoprime'

    return 'composite'

##############################

def lucas_test( number, L=None ):
    """Lucas test for primality 
    (number, L) -> 'prime', 'pseudoprime', 'strong pseudoprime', 'composite'
    using L witness pairs"""

    if number == 2:
        return 'prime'
    elif number % 2 == 0:
        return 'composite'

    if L == None:
        L = 4

    sequence_PQ = []

    D = 5
    sgn = 1
    counter = 0
    while len(sequence_PQ) < L//2 + 1:
        if mod.jacobi(D*sgn, number) == -1:
            gcd_D = nt.gcd(D*sgn, number)
            gcd_Q = nt.gcd((1-D*sgn)//4, number)
            if (gcd_D > 1) and (gcd_D < number):
                return 'composite'
            elif (gcd_Q > 1) and (gcd_Q < number):
                return 'composite'
            elif [gcd_D, gcd_Q] == [1, 1]:
                sequence_PQ.append( [1, (1-D)//4] )
        D += 2
        sgn *= -1
        counter += 1
        if counter > 2*L:
            break

    while len(sequence_PQ) < L:
        P = randint(1, 100*L)
        Q = randint(1, 100*L)
        gcd_P = nt.gcd(P, number)
        gcd_Q = nt.gcd(Q, number)
        if (gcd_P > 1) and (gcd_P < number):
            return 'composite'
        elif (gcd_Q > 1) and (gcd_Q < number):
            return 'composite'
        elif [gcd_P, gcd_Q] == [1, 1]:
            if [P, Q] not in sequence_PQ:
                sequence_PQ.append( [P, Q] )

    result = 'pseudoprime'
    for P, Q in sequence_PQ:
        witness = lucas_witness( number, P, Q )
        if witness == 'composite':
            return 'composite'
        if witness == 'strong pseudoprime':
            result = witness

    return result

##############################

def is_prime( number, MR=None, L=None ):

    mr_test = miller_rabin_test( number, MR )
    l_test = lucas_test( number, L )
    if mr_test in [ 'prime', 'strong pseudoprime' ]:
        if l_test in [ 'prime', 'pseudoprime', 'strong pseudoprime' ]:
            return True
    return False

##############################

def prime_to( prime_list, MR=None, L=None ):
    """list of numbers which are less than
    the product of the list and which are
    relatively prime to the list
    prime_list -> list of relatively prime #'s"""

    finished = []
    prime_list = sorted( prime_list )
    val = prime_list[0]
    finished.append(val)

    if is_prime(val, MR, L):
        result = [ x for x in range(1,val) ]
    else:
        result = [ x for x in range(1, val) if nt.gcd(x, val) == 1 ]
    
    for prime in prime_list[1:]:
        
        original = [ x for x in result ]
        for i in range(1, prime):
            result += [ i*val + x for x in original ]
        
        if prime not in finished:
            for x in original:
                result.remove( prime*x )

        val *= prime
        finished.append( prime )
    
    return result

##########################

def testing_block( number, P=None ):
    """block of numbers to test for primality
    number -> block"""

    if number < 6:
        P = [2]
    elif number < 30:
        P = [2,3]
    elif number < 210:
        P = [2,3,5]
    elif P == None:
        P = [2,3,5,7]
    
    length = 1
    for prime in P:
        length *= prime

    block = prime_to( P, MR=10, L=1 )

    return [ P, block, length ]

##########################

def next_prime( number, k=None, MR=None, L=None ):
    """find next primes
    (number, k=1, MR=10, L=4) -> prime or list of k primes greater than number"""

    result = []

    if number < 1:
        number = 1

    if k == None:
        k = 1

    P, block, length = testing_block( number )
    r = number % length
    preblock = [ m for m in block if m > r ]
    lower = number - r

    for m in preblock:
        if len( result ) < k:
            if is_prime( lower + m, MR, L ):
                result.append( lower + m )
    lower += length
    
    while len(result) < k:
        for m in block:
            if is_prime( lower + m, MR, L ):
                result.append( lower + m )
            if len(result) == k:
                break
        lower += length

    if k == 1:
        return result[0]
    else:
        return result

##########################

def previous_prime( number, k=None, MR=None, L=None ):
    """find previous primes
    (number, k=1, MR=10, L=4) -> primeor list of k primes less than number"""

    result = []
    if number < 3:
        return None
    if number == 3:
        return 2

    if k == None:
        k = 1

    P, block, length = testing_block( number )
    r = number % length
    preblock = [ m for m in block if m < r ]
    lower = number - r
    
    for m in reversed(preblock):
        if len( result ) < k:
            if is_prime( lower + m, MR, L ):
                result.append( lower + m )
    lower -= length
    
    while len(result) < k:
        for m in reversed(block):
            if is_prime( lower + m, MR, L ):
                result.append( lower + m )
            if len(result) == k:
                break
        if min(result) == 11:
            for prime in [ 7, 5, 3, 2 ]:
                if len(result) < k:
                    result.append( prime )
            break
        lower -= length

    if k == 1:
        return result[0]
    else:
        return result

##############################

def prime_range( lower_bound, upper_bound, P=None, MR=None, L=None ):
    """primes in a range
    (l, u) -> list of primes with l <= p < u"""

    if upper_bound - lower_bound < 2:
        return None

    P, block, length = testing_block( upper_bound, P )
    
    if lower_bound < max(P):
        result = [ x for x in P if x >= lower_bound ]
        lower_bound = max(P) + 1
    elif is_prime( lower_bound, MR, L ):
        result = [ lower_bound ]
    else:
        result = []

    r = lower_bound % length
    R = upper_bound % length
    lower = lower_bound - r
    if lower == upper_bound - R:
        return None

    preblock = [ m for m in block if m > r ]
    postblock = [ m for m in block if m < R ]

    for m in preblock:
        if is_prime( lower + m, MR, L ):
            result.append( lower + m )
    lower += length

    while lower < upper_bound - R:
        for m in block:
            if is_prime( lower + m, MR, L ):
                result.append( lower + m )
        lower += length

    for m in postblock:
        if is_prime( lower + m, MR, L ):
            result.append( lower + m )

    return result

##########################

def next_twin_primes( a, MR=None, L=None ):
    """next pair of twin primes
    a -> [p, q] with q-p = 2 and a < q
    this function is 'dangerous' 
    until the twin prime conjecture is proved :]"""

    if a < 4:
        return [3, 5]

    p = next_prime( a-2, MR, L )
    q = next_prime( p, MR, L )
    while q - p > 2:
        p, q, = q, next_prime( q, MR, L )
    
    return [ p, q ]

##########################

def previous_twin_primes( a, MR=None, L=None ):
    """previous pair of twin primes
    a -> [p, q] with q-p = 2 and a > p"""

    if a < 4:
        return None

    q = previous_prime( a+2, MR, L )
    p = previous_prime( q, MR, L )
    while q - p > 2:
        p, q = previous_prime( p, MR, L ), p

    return [ p, q ]

##########################
