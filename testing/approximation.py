
#   ~/itscomputers/number-theory-library/approx.py

from decimal import Decimal
import number_theory as nt

##############################

def newton_iteration( value, f, df ):
    
    value = Decimal(value)
    return value - f(value) / df(value)

##############################

def newton_method( initial, f, df, error ):
    """approximates the square root of a number up to given error threshold"""

    value = Decimal(initial)
    new_value = newton_iteration(value, f, df)
    
    while abs(new_value - value) > error:
        value = new_value
        new_value = newton_iteration(value, f, df)

    return new_value

##############################

def newton_indefinite( initial, f, df ):

    value = Decimal(initial)
    while True:
        value = newton_iteration(value, f, df)
        yield value

##############################

def halley_iteration( value, f, df, d2f ):

    value = Decimal(value)
    f_div_df = f(value) / df(value)
    
    return value - f_div_df\
            / (Decimal(1)\
            - f_div_df * d2f(value) / df(value) / Decimal(2))

##############################

def halley_method( initial, f, df, d2f, error ):
    """approximates the square root of a number up to a given error threshold"""

    value = Decimal(initial)
    new_value = halley_iteration(value, f, df, d2f)

    while abs(new_value - value) > error:
        value = new_value
        new_value = halley_iteration(value, f, df, d2f)

    return new_value

##############################

def halley_indefinite( initial, f, df, d2f ):

    value = Decimal(initial)
    while True:
        value = halley_iteration(value, f, df, d2f)
        yield value

##############################

def sqrt( number, n=2, precision=None, digits=28):

    number = Decimal(number)
    f = lambda t : t**n - number
    df = lambda t : n*t**(n-1)
    d2f = lambda t : n*(n-1)*t**(n-2)
    error = Decimal(10)**(-Decimal(digits))

    gen = halley_indefinite(1, f, df, d2f)
    pair = (Decimal(1), next(gen))
    while abs(pair[1] - pair[0]) > error:
        if round(pair[1])**n == number:
            return round(pair[1])
        if (float(pair[1]**n) == number) and not precision:
            return float(pair[1])
        else:
            pair = (pair[1], next(gen))

    if precision == 'Decimal':
        return pair[1]
    else:
        return float(pair[1])

##############################

def ramanujan_hardy():

    k = Decimal(0)
    multiplier = Decimal(2) / Decimal(9801) * sqrt(2, 2, 'Decimal')
    value = Decimal(0)
    factorial_4k = Decimal(1)
    factorial_k = Decimal(1)
    while True:
        adjustment =\
                factorial_4k\
                * Decimal(1103 + 26390*k)\
                / factorial_k**4\
                / Decimal(396)**(4*k)
        value += adjustment
        k += 1
        j = factorial_4k + 1
        while j < 4*k:
            factorial_4k = factorial_4k * j
            j += 1
        factorial_k = factorial_k * k
        yield multiplier*value

##############################

def Pi( precision=None ):

    rh = ramanujan_hardy()
    for i in range(3):
        next(rh)
    pi = Decimal(1) / next(rh)
    if precision == 'Decimal':
        return pi
    else:
        return float(pi)

##############################

class ContinuedFractionRootD:

    def __init__(self, D):
        self.D = D
        self.representation = self.get_representation()

    def get_representation(self):
        m = int( sqrt(self.D,2,None) )
        if m**2 == self.D:
            return [m]

        representation = []
        fraction = [1, 0, 1]

        while fraction != [1, m, 1]:

            a, b, c = fraction
            q = int( (a*m + b) / c )
            x = q*c - b
            d = nt.gcd(c, self.D*a**2 - x**2)
            
            fraction = [ a*c/d, x*c/d, (self.D*a**2 - x**2)/d ]
            representation.append( q )

        representation.append( 2*m )

        return representation

    def convergents_generator(self):
        Q = self.representation
        numers = [1, Q[0]]
        denoms = [0, 1]
        counter = 0
        while True:
            yield [ numers[1], denoms[1] ]
            counter += 1
            if counter >= len(Q):
                counter = 1
            numers = [ numers[1], Q[counter]*numers[1] + numers[0] ]
            denoms = [ denoms[1], Q[counter]*denoms[1] + denoms[0] ]

    def convergents_range(self, lower, upper):
        c = self.convergents_generator()
        convergents = []
        for i in range(lower):
            next(c)
        for i in range(upper-lower):
            convergents.append( next(c) )
        return convergents

    def convergents_range_print(self, lower, upper):
        convergents = self.convergents_range(lower, upper)
        for convergent in convergents:
            print('\u221a{} \u2248 {} \u2248 {} / {}'\
                    .format(
                        self.D,
                        Decimal(convergent[0]) / Decimal(convergent[1]),
                        convergent[0],
                        convergent[1],
                    ))
