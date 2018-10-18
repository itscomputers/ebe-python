
##############################

if __name__ == '__main__':
    
    from numth.primality import *
    from random import choice

    ##########################
    #   test miller_rabin_test
    for j in range(10):
        num = randint(2,10**5)
        num += 1 - num%2
        assert( naive_primality_test(num) == miller_rabin_test(num) )

#   ##########################
#   #   test lucas_sequence
#   for j in range(10):
#       num = randint(2,10**6)
#       num += (1 - num%2)
#       P, Q = (choice([-1,1]) * randint(1,10) for i in range(2))
#       UV = _lucas_sequence(100, P, Q, num)
#       for k in range(30):
#           uvk = _lucas_sequence_by_index(k, P, Q, num)
#           assert( uvk == UV[k] )

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
