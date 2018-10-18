
#############################

if __name__ == '__main__':

    from numth.rational import *

    ##########################
    #   test Rational class
    a = frac(3,4)
    b = frac(.4)
    c = frac(3)
    assert( a + b == frac(23,20) and a + b == 1.15 )
    assert( a + c == frac(15,4) and a + c == 3.75 )
    assert( b + c == frac(17,5) and b + c == 3.4 )
    assert( a + 3 == a + c and 3 + a == a + c )
    assert( a + b == b + a and a + c == c + a and b + c == c + b )
    assert( a - b == frac(7,20) and a - b == .35 )
    assert( a - c == frac(-9,4) and a - c == -2.25 )
    assert( b - c == frac(-13,5) and b - c == -2.6 )
    assert( a - b == -b + a and a - c == -c + a and b - c == -c + b )
    assert( b - a == -a + b and c - a == -a + c and c - b == -b + c )
    assert( a - 3 == a - c and 3 - a == c - a )
    assert( a * b == frac(3,10) and a * b == .3 )
    assert( a * c == frac(9,4) and a * c == 2.25 )
    assert( b * c == frac(6,5) and b * c == 1.2 )
    assert( a * b == b * a and a * c == c * a and b * c == b * c )
    assert( a * 3 == a * c and 3 * a == c * a )
    assert( a / b == frac(15,8) and a / b == 1.875 )
    assert( a / c == frac(1,4) and a / c == .25 )
    assert( c / b == frac(15,2) and c / b == 7.5 )
    assert( a / b == 1 / (b / a)\
            and a / c == 1 / (c / a)\
            and b / c == 1 / (c / b) )
    assert( a / 3 == a / c and 3 / a == c / a )
    assert( a + a == 2 * a and a - a == 0 )
    assert( b**7 / b**6 == b and b / b == 1 )
    assert( b**3 * b**4 == b**7 and b**5 == b*b*b*b*b )
    assert( a.inverse() * a == 1 )
    assert( b.inverse() * b == 1 )
    assert( c.inverse() * c == 1 )
    assert( int(a) == 0 and int(b) == 0 )
    assert( round(a) == 1 and round(b) == 0 )
    assert( round(2*a+1) == 3 and int(2*a+1) == 2 )
    assert( float(a) == .75  and float(b) == .4 )
    assert( -a == frac(-3,4) and -b == frac(-.4) )
    assert( abs(-a) == a and abs(-b) == b )
    assert( b < a and a < c and b < c )
    assert( -b > -a and -a > -c and -b > -c )
    assert( a % 13 == 4 and b % 13 == 3 )
    assert( frac(.599).decimal(2) == '0.60' and frac(1,3).decimal(2) == '0.33' )
    assert( frac(100,49).sqrt() == frac(10,7) )
    assert( repeating_dec_to_rational(5,142857) == frac(36,7) )
    
    ##########################
    #   test sqrt approximations
    assert( integer_sqrt(5) == 2 )
    sqrt5 = sqrt(5).decimal(3)
    gens = [\
        newton_gen(2, (-5, 0, 1)),
        halley_gen(2, (-5, 0, 1)),
        babylonian_sqrt_gen(5, 2),
        halley_sqrt_gen(5),
        bakhshali_sqrt_gen(5),
        continued_fraction_sqrt_gen(5),
        generalized_continued_fraction_sqrt_gen(5),
        generalized_continued_fraction_sqrt_gen_2(5),
        ladder_arithmetic_sqrt_gen(5),
        linear_fractional_transformation_sqrt_gen(5, 2, 1),
    ]
    for i in range(5):
        for x in gens:
            next(x)
    assert( next(gens[0]) == next(gens[2]) )
    assert( next(gens[1]) == next(gens[3]) )
    approxs = [ next(x).decimal(3) for x in gens ]
    for a in approxs:
        assert( a == sqrt5 )

    ##########################
    #   test pi approximation
    #   note: the last digit is different because pi(60).decimal() rounds
    pi_60 = '3.141592653589793238462643383279502884197169399375105820974944'
    assert( pi(60).decimal(60)[:59] ==  pi_60[:59] )
