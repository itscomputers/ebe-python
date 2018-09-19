
#   numth/primality.py

from random import randint
from concurrent.futures import ProcessPoolExecutor, wait
if __name__ == '__main__':
    from numth import padic, mod_power, gcd, jacobi
else:
    from .numth import padic, mod_power, gcd, jacobi

##############################

def default_values(kind):
    if kind is 'mr_wit':
        return 20
    elif kind is 'l_wit':
        return 20

##############################

def naive_primality_test(num: int) -> str:
    """
    Naive primality test.

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

############################################################
############################################################
#       Miller-Rabin primality testing
############################################################
############################################################

def miller_rabin_witness(num: int, wit: int) -> str:
    """
    Miller-Rabin witness for primality.

    Return:
    'composite' -- if wit detects that num is composite
    'probable prime' -- otherwise
    """
    exp, init = padic(num - 1, 2)
    x = mod_power(wit, init, num)

    if x in [1, num-1]:
        return 'probable prime'

    for j in range(exp):
        x = (x*x) % num
        if x == num - 1:
            return 'probable prime'
        elif x == 1:
            return 'composite'

    return 'composite'

##############################

def miller_rabin_cutoffs() -> tuple:
    """Cutoff values for witnesses needed in Miller-Rabin primality test"""
    return ((1, 2),
            (2047, 3),
            (1373653, 5),
            (25326001, 7),
            (3215031751, 11),
            (2152302898747, 13),
            (3474749660383, 17),
            (341550071728321, None))

##############################

def _generate_miller_rabin_witnesses(num: int, num_wit=None) -> list:
    """Generate a list of witnesses for Miller-Rabin primality test"""
    cutoffs = miller_rabin_cutoffs()
    max_val = cutoffs[-1][0]
    if num > max_val:
        if num_wit is None:
            num_wit = default_values('mr_wit')
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

def miller_rabin_test(num: int, num_wit=None) -> str:
    """
    Miller-Rabin primality test.

    Return:
    'composite' -- if any of the witnesses returns 'composite'
    'prime' -- if all of the pre-determined witnesses return 'probable prime'
    'strong probable prime' -- if all of the witnesses return 'probable prime'

    Comment:
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

############################################################
############################################################
#       Lucas sequence primality testing
############################################################
############################################################

def _lucas_double_index(
        U: int, V: int, Q: int, num: int) -> tuple:
    """Shortcut to double the index of a Lucas sequence."""
    return (
        (U*V) % num,
        (V*V - 2*Q) % num,
        (Q**2) % num
    )

##############################

def _lucas_index_plus_one(
        U: int, V: int, P: int, Q: int, Q1: int, num: int) -> tuple:
    """Shortcut to increase the index of a Lucas sequence by one."""
    return (
        ((P*U + V) * (num + 1)//2) % num,
        (((P**2 - 4*Q1)*U + P*V) * (num + 1)//2) % num,
        (Q*Q1) % num
    )

##############################

def _lucas_sequence_by_index(
        k: int, P: int, Q: int, num: int) -> tuple:
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

##############################

def _lucas_sequence(k: int, P: int, Q: int, num: int) -> list:
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

def lucas_witness(num: int, P: int, Q: int) -> str:
    """
    Lucas sequence witness for primality.

    Return:
    'composite' -- if Lucas pair U(P,Q), V(P,Q) detects num is composite
    '(strong) probable prime' -- otherwise

    Comment:
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

def _generate_lucas_witness_pairs(num: int, num_wit=None) -> list:
    """Generate a list of witnesses for Miller-Rabin primality test"""
    if num_wit is None:
        num_wit = default_values('l_wit')
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

def lucas_test(num: int, num_wit=None) -> str:
    """
    Lucas test for primality.

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

############################################################
############################################################
#       Primality functions
############################################################
############################################################

def is_prime(num: int, 
        mr_wit=None, 
        l_wit=None, 
        multiprocess=True, 
        timeout=None) -> bool:
    """
    Primality test (with multiprocessing).

    Keyword arguments:
    num -- any integer
    mr_wit -- number of Miller-Rabin witnesses for primality testing
    l_wit -- number of Lucas witness pairs for primality testing
    multiprocess -- bool
    timeout -- any positive number

    Return:
    bool True or False

    Comments:
    1. For num < 341_550_071_728_321:
        a. only pre-designated Miller-Rabin witnesses are used.
        b. the result is completely accurate.
    2. Otherwise:
        a. The default values are:
                mr_wit = 20
                l_wit = 20
        b. the result is probabalistic, with probability of incorrect
                < ( (1/4)**mr_wit ) * ( (4/15)**l_wit )
        c. for the default values , the probability of an incorrect result is
                < 3.01 * 10**-24
    3. If multiprocess is False, Lucas tests are slower than Miller-Rabin
        tests, so it is prudent to use a smaller l_wit.
    """
    if num < 2:
        return False
    prime = ('prime', 'probable prime', 'strong probable prime')
    if num < miller_rabin_cutoffs()[-1][0]:
        return (miller_rabin_test(num, mr_wit) in prime)
    else:
        if multiprocess:
            with ProcessPoolExecutor() as pool:
                futures = [
                    pool.submit( miller_rabin_test, num, mr_wit ),
                    pool.submit( lucas_test, num, l_wit )
                ]
                wait(futures, timeout=timeout)
            mr, l = (x.result() for x in futures)
        else:
            mr = miller_rabin_test(num, mr_wit)
            l = lucas_test(num, l_wit)
        return (mr in prime) and (l in prime)

##############################

def prime_to(nums: tuple, mr_wit=None, l_wit=None) -> list:
    """
    List of numbers relatively prime to a given list of numbers.

    Keyword arguments:
    nums -- list of numbers greater than 1 (preferrably primes)

    Return:
    list of all numbers up to the product of nums
    which are relatively prime to the the numbers in nums
    """
    nums = sorted(nums)
    val = nums[0]
    already_used = [val]
    if is_prime(val, mr_wit, l_wit):
        result = [ x for x in range(1, val) ]
    else:
        result = [ x for x in range(1, val) if gcd(x, val) == 1 ]
    
    for num in nums[1:]:
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

def _choose_primes(num: int) -> list:
    """Choose primes to be used in creating blocks."""
    if num < 6:
        return [2]
    elif num < 30:
        return [2,3]
    elif num < 210:
        return [2,3,5]
    else:
        return [2,3,5,7]

##############################

def _generate_block(primes: list) -> tuple:
    """Generate a block of offsets for prime searching."""
    diam = 1
    for p in primes:
        diam *= p
    
    return prime_to(primes, mr_wit=5, l_wit=1), diam

##############################

def _shift_block(num: int, block: list, diam: int) -> list:
    """Shift a block of offsets for prime searching."""
    block_min = num - num % diam
    
    return [ block_min + x for x in block ]

##############################

def _restrict_block(block: list, l_bd=None, u_bd=None) -> list:
    if l_bd:
        block = [ x for x in block if x >= l_bd ]
    if u_bd:
        block = [ x for x in block if x < u_bd ]
    
    return block

##############################

def _next_block(block: list, diam: int) -> list:
    return [ x + diam for x in block ]

##############################

def _prev_block(block: list, diam: int) -> list:
    return [ x - diam for x in block ]

##############################

def next_prime_gen(num: int,
        block_primes=None, mr_wit=None, l_wit=None):
    """Generate the next primes."""
    if num < 1:
        num == 1
    if block_primes is None:
        block_primes = _choose_primes(num)
    block, diam = _generate_block(block_primes)
    block = _shift_block(num, block, diam)
    preblock = _restrict_block(block, l_bd=num+1)
    if preblock:
        for x in preblock:
            if is_prime(x, mr_wit, l_wit):
                yield x
    while True:
        block = _next_block(block, diam)
        for x in block:
            if is_prime(x, mr_wit, l_wit):
                yield x

##############################

def next_prime(num: int,
        block_primes=None, mr_wit=None, l_wit=None) -> int:
    """Find the next prime."""
    gen = next_prime_gen(num, block_primes, mr_wit, l_wit)
    return next(gen)

##############################

def next_primes(num: int, num_primes: int,
        block_primes=None, mr_wit=None, l_wit=None) -> list:
    """Find the next primes."""
    if num < 2:
        primes = [2]
        num = 2
    else:
        primes = []

    gen = next_prime_gen(num, block_primes, mr_wit, l_wit)
    while len(primes) < num_primes:
        primes.append( next(gen) )

    return primes

##############################

def prev_prime_gen(num: int,
        block_primes=None, mr_wit=None, l_wit=None):
    """Generate the previous primes."""
    if block_primes is None:
        block_primes = _choose_primes(num)
    block, diam = _generate_block(block_primes)
    block = _shift_block(num, block, diam)
    preblock = _restrict_block(block, u_bd=num)
    if preblock:
        for x in reversed(preblock):
            if is_prime(x, mr_wit, l_wit):
                yield x
    while True:
        block = _prev_block(block, diam)
        for x in reversed(block):
            if block[0] == 1 and x < max(block_primes):
                for y in reversed(block_primes):
                    yield y
                raise StopIteration('Iterator is empty')
            elif is_prime(x, mr_wit, l_wit):
                yield x

##############################

def prev_prime(num: int, 
        block_primes=None, mr_wit=None, l_wit=None) -> int:
    """Find the previous prime."""
    if num < 3:
        return None
    elif num == 3:
        return 2
    else:
        gen = prev_prime_gen(num, block_primes, mr_wit, l_wit)
        return next(gen)

##############################

def prev_primes(num: int, num_primes: int,
        block_primes=None, mr_wit=None, l_wit=None) -> list:
    """Find the previous primes."""
    if num < 6:
        return [ x for x in [5, 3, 2] if x < num ]
    gen = prev_prime_gen(num, block_primes, mr_wit, l_wit)
    
    primes = []
    while len(primes) < num_primes and 2 not in primes:
        primes.append( next(gen) )
    
    return primes

##############################

def primes_in_range(l_bd: int, u_bd: int,
        block_primes=None, mr_wit=None, l_wit=None) -> list:
    """
    Find primes in a range.

    Return:
    list of primes between l_bd (inclusive) and u_bd (exclusive)
    """
    if block_primes is None:
        block_primes = _choose_primes( u_bd - l_bd )
    gen = next_prime_gen(l_bd - 1, block_primes, mr_wit, l_wit)
    
    primes = [ p for p in block_primes if p >= l_bd and p < u_bd ]
    while True:
        p = next(gen)
        if p < u_bd:
            primes.append(p)
        else:
            break
    
    return primes

##############################

def next_twin_primes(num: int, mr_wit=None, l_wit=None) -> tuple:
    """
    Find next pair of twin primes.

    Comments:
    1. if num is in between or part of a twin prime pair,
        then that pair will be returned.
    2. this is a 'dangerous' function until Twin Prime Conjecture is proved. ;]
    """

    if num < 4:
        return 3, 5
    p = next_prime(num - 2, mr_wit, l_wit)
    while not is_prime(p+2):
        p = next_prime(p+2, mr_wit, l_wit)

    return p, p+2

##############################

def prev_twin_primes(num: int, mr_wit=None, l_wit=None) -> tuple:
    """
    Find previous pair of twin primes.

    Comment:
    if num is in between or part of a twin prime pair,
        then that pair will be returned.
    """

    if num < 4:
        return None
    p = prev_prime(num + 2, mr_wit, l_wit)
    while not is_prime(p-2):
        p = prev_prime(p-2, mr_wit, l_wit)

    return p-2, p

##############################

def prime_count(yield_values, mr_wit=None, l_wit=None):
    """
    The prime-counting function pi(x).
    
    Return:
    the number of primes less than or equal to each of yield_values

    Comment:
    yield_values should be a tuple or generator
    """
    start = 1
    count = 0

    if isinstance(yield_values, tuple):
        yield_values = (y for y in yield_values)

    end = next(yield_values)
    yield_ability = True
    while True:
        if not yield_ability:
            yield None
        else:
            count += len(primes_in_range(
                start, end, mr_wit=mr_wit, l_wit=l_wit))
            try:
                yield end, count
                start, end = end, next(yield_values)
            except StopIteration:
                print('Iterator is empty')
                yield_ability = False





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
    #   test next_primes
    for j in range(5):
        num = randint(2,10**6)
        num_primes = randint(1,11)
        primes = next_primes(num, num_primes)
        for p in primes:
            assert( is_prime(p) )
        for x in range(num + 1 + num%2, max(primes)+1,2):
            if x not in primes:
                assert( not is_prime(x) )
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for i in range(9):
        assert( next_prime(small_primes[i]) == small_primes[i+1] )

    ##########################
    #   test prev_primes
    for j in range(5):
        num = randint(40,10**6)
        num_primes = randint(1,11)
        primes = prev_primes(num, num_primes)
        for p in primes:
            assert( is_prime(p) )
        for x in range(min(primes) + 2, num - num%2, 2):
            if x not in primes:
                assert( not is_prime(x) )
    assert( prev_prime(2) is None )
    small_primes = [29, 23, 19, 17, 13, 11, 7, 5, 3, 2]
    for i in range(3,31):
        assert( prev_primes(i,10) == [x for x in small_primes if x < i] )

    ##########################
    #   test primes_in_range
    l_bd = randint(1, 10**10)
    u_bd = randint(l_bd, l_bd + 10**4)
    assert( primes_in_range(l_bd, u_bd)\
            ==\
            [ x for x in range(l_bd, u_bd) if is_prime(x) ] )
