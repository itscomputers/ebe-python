
#   applications/primes_in_intervals.py

##  this is broken for now
from ..primality import is_prime, primes_in_range
from ..numth import gcd

def next_interval_primes(a, H):
    """Find primes in range(a+H+1, a+2*H+1)."""
    primes = []
    if (a + H) % 2 == 0:
        start = a + H + 1
    else:
        start = a + H + 2
    end = a + 2*H + 1
    for x in range(start, end, 2):
        if is_prime(x):
            primes.append(x)
    return primes

def count_changes(a, H, num_P, P):
    """
    Find number of primes in each of the intervals
    (a, a+H], (a+1, a+H+1], ..., (a+H, a+2*H+1].
    """
    change_dict = {}
    Q = next_interval_primes(a, H)
    num_primes = num_P
    for i in range(H):
        if a + i in P:
            num_primes = num_primes - 1
        if a + H + i in Q:
            num_primes = num_primes + 1
        if num_primes in change_dict:
            change_dict[num_primes] += 1
        else:
            change_dict[num_primes] = 1
    return change_dict, a+H, len(Q), Q

def count_changes_diff_interval(a, b, H, num_P, P):
    change_dict = {}
    Q = [ x for x in range(a+H+1, b+H+1) if is_prime(x) ]
    num_primes = num_P
    for i in range(b-a):
        if a + i in P:
            num_primes = num_primes - 1
        if a + H + i in Q:
            num_primes = num_primes + 1
        if num_primes in change_dict:
            change_dict[num_primes] += 1
        else:
            change_dict[num_primes] = 1
    Q = [ x for x in Q if x > b ]
    return change_dict, b, len(Q), Q

def primes_in_intervals(N, H):
    a = 0
    P = primes_in_range(1, H+1)
    num_P = len(P)
    m_dict = {}
    while a + H < N:
        cc, a, num_P, P = count_changes(a, H, num_P, P)
        for m in cc:
            if m in m_dict:
                m_dict[m] += cc[m]
            else:
                m_dict[m] = cc[m]
    cc, a, num_P, P = count_changes_diff_interval(a, N, H, num_P, P)
    for m in cc:
        if m in m_dict:
            m_dict[m] += cc[m]
        else:
            m_dict[m] = cc[m]
    return m_dict 

def primes_in_intervals_yield(H, yield_values):
    a = 0
    P = primes_in_range(1, H+1)
    num_P = len(P)
    m_dict = {}
    for y in yield_values:
        while a + H < y:
            cc, a, num_P, P = count_changes(a, H, num_P, P)
            for m in cc:
                if m in m_dict:
                    m_dict[m] += cc[m]
                else:
                    m_dict[m] = cc[m]
        cc, a, num_P, P = count_changes_diff_interval(a, y, H, num_P, P)
        for m in cc:
            if m in m_dict:
                m_dict[m] += cc[m]
            else:
                m_dict[m] = cc[m]
        yield m_dict
