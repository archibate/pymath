#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import math

class Vec3:
    '''
    a simple 3D vector, contains (x, y, z) coordinate.
    '''

    __slots__ = ['x', 'y', 'z']

    def __init__(self, x=(0, 0, 0), y=None, z=None):
        '''
        initialization of Vec3 with a tuple provided in x, or from (x, y, z)
        use Vec3(old_vector) you can copy and get a new vector same as the old_vector.
        '''
        if y is not None and z is not None:
            self.x, self.y, self.z = x, y, z
        else:
            self.x, self.y, self.z = x

    def __getitem__(self, i):
        '''
        get the item in Vec3, i is the index in (X, Y, Z).
        Vec3 can be used as a list, where X is the 1st item, etc.
        '''
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError("index out of range in vector")

    def __setitem__(self, i, val):
        '''
        set the item in Vec3, i is the index in (X, Y, Z).
        opposition of __getitem__, eg. use v[0] = val to set X, etc.
        '''
        if i == 0:
            self.x = val
        elif i == 1:
            self.y = val
        elif i == 2:
            self.z = val
        else:
            raise IndexError("index out of range in vector")

    def __nonzero__(self):
        '''
        check wheather a vector is not a zero vector.
        '''
        return bool(self.x or self.y or self.z)

    def __ne__(self, other):
        '''
        check wheather a vector is not equal to another vector.
        '''
        return bool(self.x != other.x or self.y != other.y or self.z != other.z)

    def __eq__(self, other):
        '''
        check wheather a vector is equal to another vector.
        '''
        return bool(self.x == other.x and self.y == other.y and self.z == other.z)

    def __len__(self):
        '''
        length of the list of Vec3. see __getitem__ and __setitem__
        the Vec3 can be use as (X, Y, Z)
        '''
        return 3

    def __repr__(self):
        '''
        represent Vec3 to string, useful in debugging
        '''
        return "Vec3(%s, %s, %s)" % (self.x, self.y, self.z)

    def _o1_of(f):
        '''
        generic handler of unary operator
        '''
        def decorated(self, other):
            if hasattr(other, "__getitem__"):
                return type(self)(
                        f(self.x), f(self.y), f(self.z))
            else:
                return type(self)(
                        f(self.x), f(self.y), f(self.z))

        return decorated

    def _o2_of(f):
        '''
        generic handler of binary operator
        '''
        def decorated(self, other):
            if hasattr(other, "__getitem__"):
                return type(self)(
                        f(self.x, other[0]),
                        f(self.y, other[1]),
                        f(self.z, other[2]))
            else:
                return type(self)(
                        f(self.x, other),
                        f(self.y, other),
                        f(self.z, other))

        return decorated

    def _ro2_of(f):
        '''
        generic handler of reverse binary operator
        '''
        def decorated(self, other):
            if hasattr(other, "__getitem__"):
                return type(self)(
                        f(other[0], self.x),
                        f(other[1], self.y),
                        f(other[2], self.z))
            else:
                return type(self)(
                        f(other, self.x),
                        f(other, self.y),
                        f(other, self.z))

        return decorated

    def _io2_of(f):
        '''
        generic handler of in-place binary operator
        '''
        def decorated(self, other):
            if hasattr(other, "__getitem__"):
                self.x = f(self.x, other[0])
                self.y = f(self.y, other[1])
                self.z = f(self.z, other[2])
            else:
                self.x = f(self.x, other)
                self.y = f(self.y, other)
                self.z = f(self.z, other)
            return self

        return decorated

    __add__ = _o2_of(operator.add)
    __radd__ = _ro2_of(operator.add)
    __iadd__ = _io2_of(operator.add)
    __sub__ = _o2_of(operator.sub)
    __rsub__ = _ro2_of(operator.sub)
    __isub__ = _io2_of(operator.sub)
    __mul__ = _o2_of(operator.mul)
    __rmul__ = _ro2_of(operator.mul)
    __imul__ = _io2_of(operator.mul)
    if hasattr(operator, "div"):
        __div__ = _o2_of(operator.div)
        __rdiv__ = _ro2_of(operator.div)
        __idiv__ = _io2_of(operator.div)
    __floordiv__ = _o2_of(operator.floordiv)
    __rfloordiv__ = _ro2_of(operator.floordiv)
    __ifloordiv__ = _io2_of(operator.floordiv)
    __truediv__ = _o2_of(operator.truediv)
    __rtruediv__ = _ro2_of(operator.truediv)
    __itruediv__ = _io2_of(operator.truediv)
    __mod__ = _o2_of(operator.mod)
    __rmod__ = _ro2_of(operator.mod)
    __divmod__ = _o2_of(divmod)
    __rdivmod__ = _ro2_of(divmod)
    __pow__ = _o2_of(operator.pow)
    __rpow__ = _ro2_of(operator.pow)
    __and__ = _o2_of(operator.and_)
    __rand__ = _ro2_of(operator.and_)
    __or__ = _o2_of(operator.or_)
    __ror__ = _ro2_of(operator.or_)
    __xor__ = _o2_of(operator.xor)
    __rxor__ = _ro2_of(operator.xor)
    __neg__ = _o1_of(operator.neg)
    __pos__ = _o1_of(operator.pos)

    def dot(self, other):
        '''
        get the dot product of self and other.
        '''
        return self.x * other[0] + self.y * other[1] + self.z * other[2]
        # or try return sum(self * other)?  but slower may be.

    def cross(self, other):
        '''
        get the cross product of self and other.
        '''
        return type(self)(
                self.y * other[2] - self.z * other[1],
                self.z * other[0] - self.x * other[2],
                self.x * other[1] - self.y * other[0])

    def mag(self):
        '''
        get the magnitude of vector.
        '''
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def sqr_mag(self):
        '''
        get the square of magnitude of vector.
        '''
        return (self.x * self.x + self.y * self.y + self.z * self.z)

    __abs__ = mag

    def __set_mag(self, mag):
        '''
        set the square of magnitude of vector, automaticly, 
        '''
        old_mag = self.mag()
        self /= old_mag
        self *= mag

    length = property(mag, __set_mag, None, None)

    def norm(self):
        '''
        return the normalized vector.
        '''
        mag = self.mag()
        return self / mag

    def inorm(self):
        '''
        in-place normalize the vector.
        '''
        mag = self.mag()
        self /= mag
        # or use self.mag = 1 better?
        return mag

