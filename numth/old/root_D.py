
#  ~/itscomputers/number_theory/root_D.py

import number_theory as nt
import primality as pr
import factorization as fac
import modular as mod

##################################################################

class QuadraticRing:
    """ring R[ sqrt(D) ] 
    where R is ring of integers or integers modulo m"""

    def __init__(self, D, modulus=None):
        self.D = D
        self.modulus = modulus

    def reduction(self, A):
        if self.modulus:
            if isinstance(A,list):
                return [ x % self.modulus for x in A ]
            elif isinstance(A,int):
                return A % self.modulus
        else:
            return A

    def addition(self, A, B):
        return self.reduction( [ A[i] + B[i] for i in range(len(A)) ] )

    def multiplication(self, A, B):
        a1, a2 = A
        b1, b2 = B
        ab1 = a1*b1 + a2*b2*self.D
        ab2 = a1*b2 + a2*b1
        return self.reduction( [ ab1, ab2 ] )

    def conjugate(self, A):
        return self.reduction( [ A[0], -A[1] ] )

    def norm(self, A):
        return self.reduction( self.multiplication(A, self.conjugate(A))[0] )

    def inverse(self, A):
        N = self.norm(A)
        if self.modulus and (nt.gcd(N, self.modulus) == 1):
            return self.reduction([
                x*mod.inverse(N, self.modulus)
                for x in self.conjugate(A)      ])
        elif N in [1, -1]:
            return [ x*N for x in self.conjugate(A) ]

    def power(self,A, n):
        if n < 0:
            return self.inverse( self.power(A, -n) )
        elif n == 0:
            return [1,0]
        elif n % 2 == 0:
            return self.power(self.multiplication(A, A), n//2 )
        else:
            return self.multiplication(\
                    A, self.power(self.multiplication(A,A), (n-1)//2) )

    def print_(self, A):
        print( str(A[0]) + ' + ' + str(A[1]) + ' \u221A' + str(self.D) )



