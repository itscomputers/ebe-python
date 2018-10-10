
#############################

if __name__ == '__main__':

    from rational import *

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
    assert( b * b == b**2 and b / b == 1 )
    assert( a.inverse() * a == 1 )
    assert( b.inverse() * b == 1 )
    assert( c.inverse() * c == 1 )
    assert( int(a) == 0 and int(b) == 0 )
    assert( round(a) == 1 and round(b) == 0 )
    assert( float(a) == .75  and float(b) == .4 )
    assert( -a == frac(-3,4) and -b == frac(-.4) )
    assert( abs(-a) == a and abs(-b) == b )
    assert( b < a and a < c and b < c )
    assert( -b > -a and -a > -c and -b > -c )
    assert( a % 13 == 4 and b % 13 == 3 )
    assert( frac(.599).decimal(2) == '0.60' )
    assert( frac(100,49).sqrt() == frac(10,7) )
