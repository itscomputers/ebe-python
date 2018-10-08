
#   numth/modular.py

import numth.numth as numth
import numth.primality as primality
import numth.factorization as factorization
import numth.quadratic as quadratic

##############################

def _default_values(cat):
    pass

##############################

def euler_phi(num):
    """Euler's totient/phi function."""
    return factorization.Factorize(num).euler_phi()

##############################

def carmichael_lambda(num):
    """Carmichael's lambda function."""
    return factorization.Factorize(num).carmichael_lambda()

##############################

def legendre(num, prime, EULER_CRITERION=False):
    """
    Legendre symbol.

    Args:   int:    num, prime
            bool:   EULER_CRITERION     use the Euler criterion (slower)

    Return: int:    1   <-  if num is a square modulo prime
                    0   <-  if num is divisible by prime
                    -1  <-  if num is not a square modulo prime
    """
    if not primality.is_prime(prime):
        raise ValueError('{} is not prime'.format(prime))
    else:
        return numth.jacobi(num, prime)

##############################

def sqrt_minus_one(prime, LEGENDRE=True):
    """
    Square root of -1 modulo a prime.

    Args:   int:    prime
            bool:   LEGENDRE        True    <- use Legendre's method
                                    False   <- use Wilson's method

    Return: tuple:  (val1, val2)    val**2 % prime == prime - 1
    """
    if not primality.is_prime(prime):
        raise ValueError('{} is not prime'.format(prime))
    if prime == 2:
        return (1, 1)
    if prime % 4 == 3:
        return None
    
    if METHOD == 'legendre':
        for x in range(2, prime-1):
            if jacobi(x, prime) == -1:
                val = pow(x, (prime-1)//4, prime)
                return tuple(sorted([val, prime - val]))

    else:
        val = 1
        for x in range(2, (prime-1)//2 + 1):
            val = (val * x) % prime
        return tuple(sorted([val, prime - val]))

##############################

def sqrt(num, prime, METHOD=None):
    """
    Square root of a number modulo a prime.

    Args:   int:    num, prime
            str:    METHOD          'cipolla', 'tonelli-shanks', or None

    Return: tuple:  (val1, val2)    val**2 % prime == num % prime
    """
    if not primality.is_prime(prime):
        raise ValueError('{} is not prime'.format(prime))
    if num % prime == 0:
        return (0, 0)
    elif num % prime == prime - 1:
        return sqrt_minus_one(prime)
    elif jacobi(num, prime) != 1:
        return None

    if prime % 4 == 3:
        val = pow(num, (prime+1)//4, prime)
        return tuple(sorted([val, prime - val]))

    s, q = numth.padic(prime-1, 2)
    m = len(bin(prime)[2:])
    
    if METHOD == 'cipolla' or (METHOD == None and s*(s - 1) > 8*m + 20):
        # Cipolla's method
        for y in range(2, prime-1):
            root = (y**2 - num) % prime
            if jacobi(root, p) == -1:
                break
        val = (quadratic.QuadraticInt(y, 1, root)**((p+1)//2)).real
        return tuple(sorted([val, prime - val]))

    else:
        # Tonelli-Shanks method
        for z in range(1, prime):
            if jacobi(z, prime) == -1:
                break
        m = s
        c = pow(z, q, prime)
        t = pow(num, q, prime)
        val = pow(num, (q+1)//2, prime)
        while t != 1:
            tt = t
            for i in range(1, m):
                tt = pow(tt, 2, prime)
                if tt == 1:
                    break
            b = c
            for j in range(m-i-1):
                b = pow(b, 2, prime)
            m = i
            c = pow(b, 2, prime)
            t = (t * c) % prime
            val = (val * b) % prime
        return tuple(sorted([val, prime - val]))

############################################################
############################################################
#       Modular ring class
############################################################
############################################################

class ModRing:
    """Class for modular arithmetic."""

    def __init__(self, mod):
        self.mod = mod
        self.factorize = factorization.Factorize(mod)
        self.euler = self.factorize.euler_phi()
        self.carmichael = self.factorize.carmichael_lambda()
        self.is_cyclic = self.euler == self.carmichael
        self.multiplicative_group = None
        self.generator = None
        self.all_generators = None
        self.cyclic_group = None

    ##########################

    def __repr__(self):
        return 'Ring of integers modulo {}'.format(self.mod)

    ##########################

    def get_multiplicative_group(self):
        """Populate class with group of invertible elements."""
        self.multiplicative_group =\
                (x for x in primality.prime_to(self.factorize.factorization))

    ##########################

    def get_generator(self):
        """
        Populate class with a 'generator', if possible.
        
        Return: int:    x       multiplicative group can be realized 
                                as powers of x
        """
        if not self.is_cyclic:
            raise ValueError('Multiplicative group is not cyclic')
        for x in self.multiplicative_group():
            if self.order_of(x) == self.euler:
                self.generator = x

    ##########################

    def get_all_generators(self, gen=None):
        """
        Populate class with all 'generators'.
        
        Args:   int:        gen

        Return: generator:  int         all possible 'generators'
        """
        if gen == None:
            gen = self.find_generator()
        else:
            if self.order_of(gen) != self.euler:
                raise ValueError('{} is not a generator'.format(gen))
        self.all_generators = (pow(gen, j, self.mod)\
                for j in range(1, self.euler)\
                if numth.gcd(j, self.euler) == 1)

    ##########################

    def get_cyclic_group(self, gen=None):
        """
        Populate class with a cyclic group structure.
        
        Args:   int:    gen
        
        Return: dict:   { j : gen**j }
        """
        if gen == None:
            if self.generator is None:
                gen = self.find_generator()
            else:
                gen = self.generator
        else:
            if self.order_of(gen) != self.euler:
                raise ValueError('{} is not a generator'.format(gen))
        self.cyclic_group = self.cyclic_subgroup(gen, self.euler)

    ##########################
    
    def cyclic_subgroup(self, gen, order=None):
        """
        Cyclic subgroup of multiplicative group.

        Args:   int:    gen:    generator
                        order:  order of gen

        Return: dict:   { j : gen**j }
        """
        order is None:
            order = self.order_of(gen)
        return { j : pow(gen, j, self.mod) for j in range(order) }

    ##########################

    def order_of(self, elem):
        """
        Multiplicative order of an element.

        Args:   int:    elem

        Return: int:    order       smallest positive int with 
                                    pow(elem, order, self.mod) == 1
        """
        if numth.gcd(elem, self.mod) != 1:
            raise ValueError('{} is not invertible'.format(elem))

        if num % self.mod == 1:
            return 1
        elif num % self.mod == self.mod - 1:
            return 2
 
        powers = [elem]
        exponents = [1]
        for p in factorization.factor(self.carmichael):
            new_powers = [ pow(powers[exponents.index(e)], p, self.mod)\
                            for e in exponents if p*e not in exponents ]
            new_exponents = [ p*e for e in exponents if p*e not in exponents ]
            if 1 in new_powers:
                return new_exponents[ new_powers.index(1) ]
            else:
                powers = powers + new_powers
                exponents = exponents + new_exponents

    ##########################

    def inverse_of(self, elem):
        """Multiplicative inverse of an element."""
        if elem % self.mod in [1, self.mod - 1]:
            return elem
        elif self.cylic_subgroup is None:
            return numth.mod_inverse(elem, self.mod)
        else:
            index = self.cyclic_log_of(elem, subgroup)
            return subgroup[self.mod - index]

    ##########################

    def cyclic_log_of(self, elem, subgroup):
        """
        Discrete logarithm of an element of a cyclic subgroup.

        Args:   int:    elem
                dict:   subgroup    with a 'generator' gen

        Return: int:    index       elem == gen**index % self.mod
        """
        for j in subgroup:
            if subgroup[j] == elem % self.mod:
                return j
        return None

    ##########################

    def sqrt_of(self, elem):
        """
        Square root of an element.

        Args:   int:    elem

        Return: int:    sqrt        pow(sqrt, 2, self.mod) == elem
        """
        if self.cyclic_group is None and primality.is_prime(self.mod):
            return sqrt(elem, self.mod)
        elif: self.cyclic_group is not None:
            index = self.cyclic_log_of(elem, self.cyclic_group)
            if index % 2 == 1:
                return None
            else:
                return tuple(sorted([
                    cyclic_group[index//2],
                    cyclic_group[self.mod - index//2]] ))
        else:
            ## look through all cyclic subgroups?
            return None

