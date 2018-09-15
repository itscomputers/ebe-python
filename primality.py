
#   numth/primality.py

from random import randint
from concurrent.futures import ProcessPoolExecutor, wait
from numth import padic, mod_power, gcd, jacobi

##############################

def default_values(kind):
    if kind is 'num_mr':
        return 20
    elif kind is 'num_l':
        return 20
    elif kind is 'prime_count_rate':
        return 100000

##############################

def naive_primality_test(num):
    """
    Naive primality test.

    Keyword arguments:
    num -- any integer greater than 1

    Return:
    'composite' -- if num is divisible by a prime < sqrt(num)
    'prime' -- otherwise
    """

    all_nums = [ x for x in range(2, num) if x**2 <= num ]
    while all_nums != []:
        sm = all_nums[0]
        if num % sm == 0:
            return 'composite'
        else:
            all_nums = [ x for x in all_nums if x % sm != 0 ]
    return 'prime'

##############################

def miller_rabin_witness(num, wit):
    """
    Miller-Rabin witness for primality.

    Keyword arguments:
    num, wit -- any integers greater than 1

    Return:
    'composite' -- if wit detects that num is composite
    'probable prime' -- otherwise
    
    Additional comment:
    Here, 'probable prime' means that num may or may not be prime,
    according to wit.
    """

    exp, init = padic(num - 1, 2)
    x = mod_power(wit, init, num)

    if x in [1, num-1]:
        return 'pseudoprime'

    for j in range(exp):
        x = (x*x) % num
        if x == num - 1:
            return 'probable prime'
        elif x == 1:
            return 'composite'

    return 'composite'

##############################

def miller_rabin_cutoffs():
    """Cutoff values for witnesses needed in Miller-Rabin primality test"""

    return ((1, 2),
            (2047, 3),
            (1373653, 5),
            (25326001, 7),
            (3215031751, 11),
            (2152302898747, 13),
            (3474749660383, 17),
            (341550071728321, None))

def _generate_miller_rabin_witnesses(num, num_wit=None):
    """Generate a list of witnesses for Miller-Rabin primality test"""

    cutoffs = miller_rabin_cutoffs()
    max_val = cutoffs[-1][0]
    if num > max_val:
        if num_wit is None:
            num_wit = default_values('num_mr')
        if num_wit > num:
            witnesses = [ x for x in range(2, num-1) ]
        else:
            witnesses = []
            while len(witnesses) < num_wit:
                x = randint(2, num-1)
                if x not in witnesses:
                    witnesses.append(x)
    else:
        witnesses = []
        for val, p in cutoffs[:-1]:
            if num >= val:
                witnesses.append(p)
    
    return witnesses

##############################

def miller_rabin_test(num, num_wit=None):
    """
    Miller-Rabin primality test.

    Keyword arguments:
    num -- any integer greater than 1
    num_wit -- number of witnesses (at least 1)

    Return:
    'composite' -- if any of the witnesses returns 'composite'
    'prime' -- if all of the pre-determined witnesses return 'probable prime'
    'strong probable prime' -- if all of the witnesses return 'probable prime'

    Additional comment:
    For num < 341 550 071 728 321, the test is deterministic.
    Otherwise, the test is probabilistic with probability of misdiagnosis
    provably at most (.25)**num_wit.
    """

    if num == 2:
        return 'prime'
    witnesses = _generate_miller_rabin_witnesses(num, num_wit)

    for wit in witnesses:
        if miller_rabin_witness(num, wit) == 'composite':
            return 'composite'

    if num < miller_rabin_cutoffs()[-1][0]:
        return 'prime'
    else:
        return 'strong probable prime'

##############################

def _lucas_double_index(U, V, Q, num):
    """Shortcut to double the index of a Lucas sequence."""

    return (
        (U*V) % num,
        (V*V - 2*Q) % num,
        (Q**2) % num
    )

def _lucas_index_plus_one(U, V, P, Q, Q1, num):
    """Shortcut to increase the index of a Lucas sequence by one."""
    
    return (
        ((P*U + V) * (num + 1)//2) % num,
        (((P**2 - 4*Q1)*U + P*V) * (num + 1)//2) % num,
        (Q*Q1) % num
    )

def _lucas_sequence_by_index(k, P, Q, num):
    """Explicit formula for any element of a Lucas sequence."""

    if k == 0:
        return (0, 2, 1)
    elif k == 1:
        return (1, P, Q)
    elif k % 2 == 0:
        U_, V_, Q_ = _lucas_sequence_by_index(k//2, P, Q, num)
        return _lucas_double_index(U_, V_, Q_, num)
    else:
        U_, V_, Q_ = _lucas_sequence_by_index(k-1, P, Q, num)
        return _lucas_index_plus_one(U_, V_, P, Q_, Q, num)

def _lucas_sequence(k, P, Q, num):
    """Recursive formula to generate a Lucas sequence up to some point."""

    UV = [ (0, 2, 1), (1, P, Q) ]
    for i in range(k-1):
        U_, V_, Q_ = UV[-1]
        U__, V__, Q__ = UV[-2]
        UV.append((
            (P*U_ - Q*U__) % num,
            (P*V_ - Q*V__) % num,
            (Q*Q_) % num
        ))
    return UV

##############################

def lucas_witness(num, P, Q):
    """
    Lucas sequence witness for primality.
    
    Keyword arguments:
    num -- any integer greater than 1
    P, Q -- any nonzero integers (parameters)

    Return:
    'composite' -- if Lucas pair U(P,Q), V(P,Q) detects num is composite
    '(strong) probable prime' -- otherwise

    Additional comments:
    The 'strength' of a probable prime is based on some additional conditions
    that make it more likely to be prime.
    """

    D = P**2 - 4*Q
    gcd_D = gcd(D, num)
    gcd_P = gcd(P, num)
    gcd_Q = gcd(Q, num)
    for g in (gcd_D, gcd_P, gcd_Q):
        if g == num:
            raise ValueError('Bad parameters: {}, {}'.format(P, Q))
        elif g > 1:
            return 'composite'

    delta = num - jacobi(D, num)
    s, d = padic(delta, 2)
    strong = False

    U, V, Q_ = _lucas_sequence_by_index(d, P, Q, num)
    if U == 0:
        strong = True
    for j in range(s - 1):
        U, V, Q_ = _lucas_double_index(U, V, Q_, num)
        if V == 0:
            strong = True
    U, V = _lucas_double_index(U, V, Q_, num)[:2]

    if U == 0:
        if delta == num + 1:
            if V != (2*Q) % num:
                return 'composite'
            if Q_ != (Q * jacobi(Q, num)) % num:
                return 'composite'
        else:
            if Q_ != jacobi(Q, num) % num:
                return 'composite'
        if strong:
            return 'strong probable prime'
        else:
            return 'probable prime'

    return 'composite'

##############################

def _generate_lucas_witness_pairs(num, num_wit=None):
    """Generate a list of witnesses for Miller-Rabin primality test"""

    if num_wit is None:
        num_wit = default_values('num_l')
    witnesses = []
    D = 5
    sgn = 1
    counter = 0   ## after i make a decent square root, this will be slow
    while len(witnesses) < num_wit // 2 + 1:
        if (jacobi(D*sgn, num) == -1):
            witnesses.append( (1, (1 - D)//4) )
        D += 2
        sgn *= 1
        counter += 1
        if counter > 2*num_wit:
            break

    while len(witnesses) < num_wit:
        P = randint(1, 100*num_wit)
        Q = randint(1, 100*num_wit)
        D = P**2 - 4*Q
        if (P, Q) not in witnesses:
            witnesses.append( (P, Q) )

    return witnesses

##############################

def lucas_test(num, num_wit=None):
    """
    Lucas test for primality.

    Keyword arguments:
    num -- any integer greater than 2
    num_wit -- number of witness pairs, any positive integer

    Return:
    'composite' -- if any pair returns 'composite'
    'probable prime' -- if all pairs return 'probable prime'
    'strong probable prime -- if any pair returns 'strong probable prime'
                            and the rest return 'probable prime'
    """

    if num <= 2:
        raise ValueError('Num should be at least 3')
    if num % 2 == 0:
        return 'composite'
    witnesses = _generate_lucas_witness_pairs(num, num_wit)

    strong = False
    for P, Q in witnesses:
        
        primality = lucas_witness(num, P, Q)
        if primality == 'composite':
            return 'composite'
        if primality == 'strong probable prime':
            strong = True
    if strong:
        return 'strong probable prime'
    else:
        return 'probable prime'

##############################

def is_prime(num, num_mr=None, num_l=None, multiprocess=True, timeout=None):
    """
    Primality test (with multiprocessing).

    Keyword arguments:
    num -- any integer
    num_mr -- nonnegative number of Miller-Rabin witnesses
    num_l -- nonnegative number of Lucas witness pairs
    multiprocess -- bool
    timeout -- any positive number

    Return:
    bool True or False

    Additional comments:
    1. For num < 341550071728321:
        a. only pre-designated Miller-Rabin witnesses are used.
        b. the result is completely accurate.
    2. Otherwise:
        a. The default values are:
                num_mr = 20
                num_l = 20
        b. the result is probabalistic, with probability of incorrect
                < ( (1/4)**num_mr ) * ( (4/15)**num_l )
        c. for the default values, the probability of an incorrect result is
                < 1 / (3.01 * 10**-24)
    3. If multiprocess is False, Lucas tests are slower than Miller-Rabin
        tests, so it is prudent to use a smaller num_l.
    """

    if num < 2:
        return False
    prime = ('prime', 'probable prime', 'strong probable prime')
    if num < miller_rabin_cutoffs()[-1][0]:
        return (miller_rabin_test(num, num_mr) in prime)
    else:
        if multiprocess:
            with ProcessPoolExecutor() as pool:
                futures = [
                    pool.submit( miller_rabin_test, num, num_mr ),
                    pool.submit( lucas_test, num, num_l )
                ]
                wait(futures, timeout=timeout)
            mr, l = (x.result() for x in futures)
        else:
            mr = miller_rabin_test(num, num_mr)
            l = lucas_test(num, num_l)
        return (mr in prime) and (l in prime)

##############################

def prime_to(num_list, num_mr=None, num_l=None):
    """
    List of numbers relatively prime to a given list of numbers.

    Keyword arguments:
    num_list -- list of numbers greater than 1 (preferrably primes)
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    list of all numbers up to the product of the given list
    which are relatively prime to the given list
    """

    num_list = sorted(num_list)
    val = num_list[0]
    already_used = [val]
    if is_prime(val, num_mr, num_l):
        result = [ x for x in range(1, val) ]
    else:
        result = [ x for x in range(1, val) if gcd(x, val) == 1 ]
    
    for num in num_list[1:]:
        orig = [ x for x in result ]
        for i in range(1, num):
            result += [ i * val + x for x in orig ]
        if num not in already_used:
            for x in orig:
                result.remove(num * x)
            already_used.append(num)
        val *= num

    return result

##############################

def _test_block(num, num_list=None):
    """Generate block of prime candidates."""

    if num < 6:
        num_list = [2]
    elif num < 30:
        num_list = [2,3]
    elif num < 210:
        num_list = [2,3,5]
    elif num_list is None:
        num_list = [2,3,5,7]
    
    diameter = 1
    for num in num_list:
        diameter *= num
    block = prime_to(num_list, num_mr=5, num_l=1)

    return (num_list, block, diameter)

##############################

def next_prime(num, num_primes=None, num_mr=None, num_l=None):
    """
    Find the next primes.

    Keyword arguments:
    num -- real number
    num_primes -- number of primes
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    the prime or the list of num_primes primes greater than num
    """
    
    if num < 1:
        num = 1
    if num_primes is None:
        num_primes = 1

    result = []
    num_list, block, diameter = _test_block(num)
    r = num % diameter
    preblock = [ x for x in block if x > r ]
    lower = num - r
    for x in preblock:
        if (len(result) < num_primes) and is_prime(lower + x, num_mr, num_l):
                result.append(lower + x)
    lower += diameter

    while len(result) < num_primes:
        for x in block:
            if is_prime(lower + x, num_mr, num_l):
                result.append(lower + x)
            if len(result) == num_primes:
                break
        lower += diameter

    if num_primes == 1:
        return result[0]
    else:
        return result

##############################

def prev_prime(num, num_primes=None, num_mr=None, num_l=None):
    """
    Find the previous primes.

    Keyword arguments:
    num -- real number
    num_primes -- number of primes
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    the prime or the list of num_primes primes less than num
    """

    if num_primes == None:
        num_primes = 1
    if num < 3:
        return None
    if num == 3:
        if num_primes == 1:
            return 2
        else:
            return [2]

    result = []
    num_list, block, diameter = _test_block(num)
    r = num % diameter
    preblock = [ x for x in block if x < r ]
    lower = num - r
    for x in reversed(preblock):
        if (len(result) < num_primes) and is_prime(lower + x, num_mr, num_l):
            result.append(lower + x)
    lower -= diameter

    while len(result) < num_primes:
        for x in reversed(block):
            if is_prime(lower + x, num_mr, num_l):
                result.append(lower + x)
            if len(result) == num_primes:
                break
        if min(result) <= 11:
            for p in [7, 5, 3, 2]:
                if (p < num) and (p not in result)\
                        and (len(result) < num_primes):
                    result.append(p)
            break
        lower -= diameter 

    if num_primes == 1:
        return result[0]
    else:
        return result

##############################

def primes_in_range(l_bd, u_bd, p_list=None, num_mr=None, num_l=None):
    """
    Find primems in a range.

    Keyword arguments:
    l_bd -- lower bound, any integer
    u_bd -- upper bound, any integer
    p_list -- list of small prime numbers for creating a test block
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    list of primes between l_bd (inclusive) and u_bd (exclusive)
    """

    if u_bd - l_bd < 2:
        return None
    num_list, block, diameter = _test_block(u_bd, p_list)
    if l_bd < max(num_list):
        result = [ x for x in num_list if x >= l_bd ]
        l_bd = max(num_list) + 1
    elif is_prime(l_bd, num_mr, num_l):
        result = [ l_bd ]
    else:
        result = []

    lower = l_bd - (l_bd % diameter)
    for x in block:
        if (lower + x > l_bd)\
                and (lower + x < u_bd)\
                and is_prime(lower + x, num_mr, num_l):
            result.append(lower + x)
    lower += diameter
    while lower < u_bd - (u_bd % diameter):
        for x in block:
            if is_prime(lower + x, num_mr, num_l):
                result.append(lower + x)
        lower += diameter
    for x in block:
        if (lower + x < u_bd) and is_prime(lower + x, num_mr, num_l):
            result.append(lower + x)

    return result

##############################

def next_twin_primes(num, num_mr, num_l):
    """
    Find next pair of twin primes.
    
    Keyword arguments:
    num -- any integer
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    pair of twin primes 'after' num

    Additional comments:
    1. if num is in between or part of a twin prime pair,
        then that pair will be returned.
    2. this is a 'dangerous' function until Twin Prime Conjecture is proved. ;]
    """

    if num < 4:
        return 3, 5
    p = next_prime(num - 2, num_mr, num_l)
    while not is_prime(p+2):
        p = next_prime(p+2, num_mr, num_l)

    return p, p+2

##############################

def prev_twin_primes(num, num_mr, num_l):
    """
    Find previous pair of twin primes.
    
    Keyword arguments:
    num -- any integer
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    pair of twin primes 'before' num

    Additional comment:
    if num is in between or part of a twin prime pair,
        then that pair will be returned.
    """

    if num < 4:
        return None
    p = prev_prime(num + 2, num_mr, num_l)
    while not is_prime(p-2):
        p = prev_prime(p-2, num_mr, num_l)

    return p-2, p

##############################

def prime_count(num, rate=None, num_mr=None, num_l=None):
    """
    The prime-counting function pi(x).

    Keyword arguments:
    num -- any integer
    rate -- integer dictating how often to yield partial results
    num_mr -- number of Miller-Rabin witnesses for primality testing
    num_l -- number of Lucas witness pairs for primality testing

    Return:
    the number of primes less than or equal to num

    Additional comment:
    this is computationally laborious, so it will yield values
    spaced every rate until num
    """

    if rate is None:
        rate = default_values('prime_count_rate')
    if num <= rate:
        return len(primes_in_range(2, num, num_mr=num_mr, num_l=num_l))
    else:
        curr_val = 2
        next_val = rate
        prime_count = 0
        while curr_val < num - (num % rate):
            print('number of primes up to {}'.format(next_val))
            prime_count += len(primes_in_range(\
                    curr_val, next_val, num_mr=num_mr, num_l=num_l))
            curr_val, next_val = next_val, next_val + rate
            yield prime_count

        prime_count += len(primes_in_range(\
                curr_val, num, num_mr=num_mr, num_l=num_l))
        return prime_count







############################################################
############################################################
############################################################
############################################################
############################################################

##  testing

##############################

if __name__ == '__main__':
    from random import choice

#   ##########################
#   #   test miller_rabin_test
#   for j in range(10):
#       num = randint(2,10**5)
#       num += 1 - num%2
#       assert( naive_primality_test(num) == miller_rabin_test(num) )

    ##########################
    #   test lucas_sequence
    for j in range(10):
        num = randint(2,10**6)
        num += (1 - num%2)
        P, Q = (choice([-1,1]) * randint(1,10) for i in range(2))
        UV = _lucas_sequence(100, P, Q, num)
        for k in range(30):
            uvk = _lucas_sequence_by_index(k, P, Q, num)
            assert( uvk == UV[k] )

    ##########################
    #   test lucas_test
    for j in range(10):
        num = randint(3,10**5)
        num += 1 - num%2
        primality = lucas_test(num, 4)
        if 'prime' in primality:
            primality = 'prime'
        assert( naive_primality_test(num) ==  primality )

    ##########################
    #   test is_prime
    for j in range(10):
        num = randint(2, 10**5)
        num += 1 - num%2
        naive = naive_primality_test(num) == 'prime'
        prime = is_prime(num)
        assert( naive == prime )
    naive = ['prime' == naive_primality_test(x) for x in range(2,30)]
    prime = [is_prime(x) for x in range(2,30)]
    assert( naive == prime )

    ##########################
    #   test prime_to
    test_blocks = [
            [[2],       [1]],
            [[2,3],     [1,5]],
            [[2,5],     [1,3,7,9]],
            [[3,5],     [1,2,4,7,8,11,13,14]],
            [[2,3,5],   [1,7,11,13,17,19,23,29]]
        ]
    for num_list, result in test_blocks:
        assert( prime_to(num_list) == result )

    ##########################
    #   test next_prime
    for j in range(5):
        num = randint(2,10**6)
        num_primes = randint(1,11)
        primes = next_prime(num, num_primes)
        if num_primes == 1:
            assert( is_prime(primes) )
            for x in range(num+1, primes):
                assert( not is_prime(x) )
        else:
            for p in primes:
                assert( is_prime(p) )
            for x in range(num + 1 + num%2, max(primes)+1,2):
                if x not in primes:
                    assert( not is_prime(x) )

    ##########################
    #   test prev_prime
    for j in range(5):
        num = randint(40,10**6)
        num_primes = randint(1,11)
        primes = prev_prime(num, num_primes)
        if num_primes == 1:
            assert( is_prime(primes) )
            for x in range(primes+1, num):
                assert( not is_prime(x) )
        else:
            for p in primes:
                assert( is_prime(p) )
            for x in range(min(primes) + 2, num - num%2, 2):
                if x not in primes:
                    assert( not is_prime(x) )
    assert( prev_prime(2) is None )
    small_primes = [29, 23, 19, 17, 13, 11, 7, 5, 3, 2]
    for i in range(3,31):
        assert( prev_prime(i,10) == [x for x in small_primes if x < i] )

    ##########################
    #   test primes_in_range
    l_bd = randint(1, 10**10)
    u_bd = randint(l_bd, l_bd + 10**4)
    assert( primes_in_range(l_bd, u_bd)\
            ==\
            [ x for x in range(l_bd, u_bd) if is_prime(x) ] )
