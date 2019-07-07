#   numth/quaternion.py
#===========================================================
from ..basic import div_with_small_remainder
from .rational import frac, Rational
#===========================================================

def quaternion(number):
    if type(number) in [int, float, Rational]:
        return Quaternion(number, 0, 0, 0)
    if type(number) is Quaternion:
        return number

#=============================

class Quaternion:
    """
    Quaternion number class.

    params
    + components = (a, b, c, d) : (int, int, int, int)

    represents
    a + b*i + c*j + d*k
    """

    def __init__(self, *components):
        self.components = components
        self.r, self.i, self.j, self.k = components

    #-------------------------

    def __repr__(self):
        representation = ' ' + ' + '.join(
            ''.join(format(y) for y in x) \
            for x in zip(self.components, ['', ' i', ' j', ' k']))

        return representation.replace(' + -', ' - ')\

    #=========================
    
    def __eq__(self, other):
        return self.components == quaternion(other).components

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.norm() < quaternion(other).norm()

    def __gt__(self, other):
        return self.norm() > quaternion(other).norm()

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def component_map(self, function, other=None):
        if other is not None:
            return Quaternion(*map(
                function,
                self.components,
                quaternion(other).components
            ))

        return Quaternion(*map(function, self.components))

    #=========================

    def norm(self):
        return sum(self.component_map(lambda x: x**2).components)

    #-------------------------

    def conjugate(self):
        return Quaternion(self.r, *map(lambda x: -x, self.components[1:]))

    #-------------------------

    def inverse(self):
        norm = self.norm()
        if abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse()

        return self.conjugate().component_map(lambda x: x * norm_inverse)

    #=========================

    def __neg__(self):
        return self.component_map(lambda x: -x)

    #-------------------------

    def round(self):
        return self.component_map(lambda x: int(x + .5))

    #=========================

    def __add__(self, other):
        return self.component_map(lambda x, y: x + y, other)

    def __radd__(self, other):
        return self + other

    #-------------------------

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    #-------------------------

    def __mul__(self, other):
        def mul_each(index, s_comp, o_comp):
            sign = [(1, -1, -1, -1),
                    (1, 1, 1, -1),
                    (1, -1, 1, 1),
                    (1, 1, -1, 1)][index]
            o_ind = [(0, 1, 2, 3),
                    (1, 0, 3, 2),
                    (2, 3, 0, 1),
                    (3, 2, 1, 0)][index]
            return sum(map(
                lambda x, y, z: x * y * z,
                sign,
                s_comp,
                (o_comp[i] for i in o_ind)
            ))
    
        return Quaternion(*[
            mul_each(index, self.components, quaternion(other).components)
            for index in range(4)
        ])

    def __rmul__(self, other):
        return self * other

    #-------------------------

    def __truediv__(self, other):
        return self * quaternion(other).inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    #-------------------------

    def __floordiv__(self, other):
        return (self * quaternion(other).conjugate()).component_map(
                lambda x: x // quaternion(other).norm())

    def __rfloordiv__(self, other):
        return (self.conjugate() * quaternion(other)) // self.norm()

    #-------------------------

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**(-other)
        if other == 0:
            return Quaternion(1, 0, 0, 0)
        if other == 1:
            return self
        if other % 2 == 0:
            return (self * self) ** (other // 2)
        
        return self * (self * self) ** (other // 2)

    #-------------------------

    def __mod__(self, other):
        if type(other) is int:
            def mod_with_small_remainder(x):
                return div_with_small_remainder(x, other)[1]
            return self.component_map(mod_with_small_remainder)
        return self - (self // other) * other

    def __rmod__(self, other):
        return quaternion(other) % self

