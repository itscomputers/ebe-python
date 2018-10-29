
#   numth/factorization_alt.py
#   this module is for testing alternative methods for factorization

def get_num(d, r):
    from numth.primality import next_prime
    from functools import reduce
    from operator import mul
    primes = [ next_prime(randint(10**d, 10**(d+1))) for i in range(r) ]
    return reduce(mul, primes)

def find_good_seeds(d, r, k, rs, rp, ms):
    nums = [get_num(d, r) for j in range(k)]
    seeds = dict()
    
#   with ProcessPoolExecutor() as pool:
#       futures = []
#       for j in range(k):
#           futures.append(pool.submit( get_num, d, r ))
#       wait(futures)
#       for x in futures:
#           nums.append(x.result())

    with ProcessPoolExecutor() as pool:
        futures = []
        for n in nums:
            futures.append(pool.submit(find_divisor_w_gen, n, rs, rp, ms, True))
        wait(futures)
        for x in futures:
            i, s, d = x.result()
            if isinstance(s, int):
                s, p = s, tuple()
            else:
                s, p = s
            if s in seeds:
                seeds[s] = seeds[s] + (p, i)
            else:
                seeds[s] = (p, i)
    
    return seeds 

def seeds_to_check():
    rs = [2, 3, 4, 5, 6, 7, 8, 9]
    rp = [(1,0,1), (1,0,0,1), (1,0,0,0,1)]
    ms = [2]

    return rs, rp, ms

############################################################
############################################################
#       Factorization w/ iterators
############################################################
############################################################

def rho_gen(num, s, p):
    def f(x):
        return polyn(p).mod_eval(x, num)
    xi = f(s % num)
    x2i = f(xi)
    while True:
        d = gcd(x2i - xi, num)
        yield d
        xi = f(xi)
        x2i = f( f(x2i) )

##############################

def p_minus_one_gen(num, s):
    if gcd(s, num) > 1:
        yield gcd(s, num)

    xi = s % num
    index = 1
    while True:
        d = gcd(xi - 1, num)
        yield d
        index += 1
        xi = pow(xi, index, num)

##############################

def find_divisor_w_gen(num, rs, rp, ms, extra=False):
    rg = [ [(s,p), rho_gen(num, s, p)] for s, p in itertools.product(rs, rp) ]
    mg = [ [s, p_minus_one_gen(num, s)] for s in ms ]
    gens = rg + mg
    d = 1
    if extra:
        i = 0
    while True:
        for seed, gen in gens:
            if extra:
                i += 1
            d = next(gen)
            if d > 1:
                if d == num:
                    gens.remove(gen)
                else:
                    if extra:
                        return i, seed, d 
                    return d

############################################################
############################################################
#       Factorization w/ multiprcoessing #1
############################################################
############################################################

def find_divisor_mp(num, rs=[], rp=[], ms=[], mw=4, to=None):
    """
    Find a divisor of a number using multiprocessing.
    
    Args:   int:    num, to, mw         to: timeout value
                                        mw: max workers
            list:   rs, rp, ms

    Return: int:    divisor of num or num itself if timeout occurs
    """
    if rs == []:
        rs = _default_values('rho seeds')
    if rp == []:
        rp = _default_values('rho polyns')
    if ms == []:
        ms = _default_values('p-1 seeds')

    d = num
    futures = []
    with pebble.ProcessPool(max_workers=mw) as pool:
        for p, s in itertools.product(rp, rs):
            futures.append(pool.schedule( pollard_rho, (num, s, p) ))
        for s in ms:
            futures.append(pool.schedule( pollard_p_minus_one, (num, s) ))
        while d == num:
            wait(futures, timeout=to, return_when='FIRST_COMPLETED')
            for x in futures:
                if x.done():
                    if x.result() < num:
                        d = x.result()
                    futures.remove(x)
        if d < num:
            for x in futures:
                x.cancel()
    return d

##############################

def nontrivial_divisors_mp(num, rs=[], rp=[], ms=[], mw=4, to=None):
    """
    Find nontrivial prime divisors of a number.

    Args:   int:    num
            list:   rs, rp, ms

    Return: list:   primes      prime divisors of num
    """
    if is_prime(num):
        return [num]
    sqrt = integer_sqrt(num)
    if sqrt**2 == num:
        primes = nontrivial_divisors_mp(sqrt, rs, rp, ms, mw, to)
        return 2*primes
    else:
        divisor = find_divisor_mp(num, rs, rp, ms, mw, to)
        primes = []
        for n in [divisor, num // divisor]:
            primes = primes + nontrivial_divisors_mp(n, rs, rp, ms, mw, to)
        
        return primes

##############################

def factor_mp(num, pb=None, rs=[], rp=[], ms=[], mw=4, to=None):
    if num < 2:
        return None
    if is_prime(num):
        return [num]

    if pb is None:
        pb = _default_values('prime base')
    small_primes, num = trivial_divisors(num, pb)
    if num == 1:
        return sorted(small_primes)

    return sorted(small_primes +\
            nontrivial_divisors_mp(num, rs, rp, ms, mw, to))

############################################################
############################################################
#       Factorization w/ multiprocessing #2
############################################################
############################################################

class PollardRho:

    def __init__(self, num, s, p):
        self.num = num
        self.s = s
        self.p = p
        self.interrupted = False

    def __repr__(self):
        return 'seed {}, polynomial {}'.format(self.s, self.p)

    def __call__(self):
        num = self.num
        s = self.s
        p = self.p
        def f(x):
            return polyn(p).mod_eval(x, num)
        xi = f(s % num)
        x2i = f(xi)
        d = gcd(x2i - xi, num)

        while d == 1:
            if self.interrupted:
                print('interrupted: {}'.format(self))
                break
            xi = f(xi)
            x2i = f( f(x2i) )
            d = gcd(x2i - xi, num)

        if d == 1:
            print('got interrupted')
            return num
        return d

    def interrupt(self):
        print('received interrupt call: {}'.format(self))
        self.interrupted = True

def find_divisor_mp2(num, rs=[], rp=[], to=None):
    from time import time
    d = num
    print(num)
    with ProcessPoolExecutor() as pool:
        tasks = [ PollardRho(num, s, p) for s, p in itertools.product(rs, rp) ]
        t0 = time()
        futures = [ pool.submit(x) for x in tasks ]
        done, not_done = wait(\
                futures, timeout=to, return_when='FIRST_COMPLETED')
        while len(not_done) > 0:
            t1 = time()
            print('elapsed {}, done = {}, not done = {}'\
                    .format(t1-t0, len(done), len(not_done)))
            for x in done:
                d = x.result()
                if d < num:
                    print('found one! {}'.format(d))
                    stop_process_pool(pool)
            done, not_done = wait(\
                not_done, timeout=to, return_when='FIRST_COMPLETED')
    return d

def test(d, rs, rp, to):
    from numth.primality import next_prime
    p = next_prime(randint(10**d, 10**(d+1)))
    q = next_prime(randint(10**d, 10**(d+1)))
    n = p * q
    return find_divisor_mp2(n, rs, rp, to)
