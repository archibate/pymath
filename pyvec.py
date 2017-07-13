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

class Mat3(Vec3):
    '''
    transfromation matrix for Vec3. contains 3x3 element.
    '''

    def __init__(self, x=(Vec3(1,0,0), Vec3(0,1,0), Vec3(0,0,1)), y=None, z=None):
        super(Mat3, self).__init__(x, y, z)

    def get_rx(self):
        return Vec3(self.x.x, self.y.x, self.z.x)

    def get_ry(self):
        return Vec3(self.x.y, self.y.y, self.z.y)

    def get_rz(self):
        return Vec3(self.x.z, self.y.z, self.z.z)

    def __set_rx(self, value):
        self.x.x, self.y.x, self.z.x = value

    def __set_ry(self, value):
        self.x.y, self.y.y, self.z.y = value

    def __set_rz(self, value):
        self.x.z, self.y.z, self.z.z = value

    rx = property(get_rx, __set_rx, None, "row 1 of the reversed matrix.")
    ry = property(get_ry, __set_ry, None, "row 2 of the reversed matrix.")
    rz = property(get_rz, __set_rz, None, "row 3 of the reversed matrix.")

    def get_rev(self):
        return Mat3(self.rx, self.ry, self.rz)

    def __set_rev(self, value):
        self.rx, self.ry, self.rz = value

    rev = property(get_rev, __set_rev, None, "get/set the reversed matrix.")

    def irev(self):
        '''
        in-place reverse matrix.
        '''
        self.x.y, self.z.y = self.z.y, self.x.y
        self.y.x, self.y.z = self.y.z, self.y.x
        self.z.x, self.x.z = self.x.z, self.z.x
        return self

    def __repr__(self):
        '''
        representation, convert Mat3 into string, useful in debugging.
        '''
        return "Mat3(\t%s,\n\t%s,\n\t%s)" % (self.x, self.y, self.z)

    def trans(self, v):
        '''
        in-place transform the vector.
        '''
        return Vec3(self.x.dot(v), self.y.dot(v), self.z.dot(v))

    def transi(self, v):
        '''
        get transformed vector.
        '''
        v.x, v.y, v.z = self.trans(v)

    def dot(self, other):
        '''
        get product with self and other, self is the left operand.
        '''
        return Mat3(Vec3(self.x.dot(other.rx),self.x.dot(other.ry),self.x.dot(other.rz)),
                Vec3(self.y.dot(other.rx),self.y.dot(other.ry),self.y.dot(other.rz)),
                Vec3(self.z.dot(other.rx),self.z.dot(other.ry),self.z.dot(other.rz)))

    def doti(self, other):
        self.x, self.y, self.z = self.dot(other)

#def dotproduct(self, other):
        #'''
        #get dot product with self and other whoever is Vec3 or Mat3,
        #self is the left operand.
        #'''
        #return self.dot(other)

if __name__ == "__main__":

    import unittest
    import pickle
    from random import random

    def randVec3():
        return Vec3(random(), random(), random())

    ####################################################################
    class UnitTestMat(unittest.TestCase):
        '''
        unit test for Mat3 and Vec3.
        '''

        def setUp(self):
            pass

        def testTrans(self):
            v = randVec3()
            T = Mat3(randVec3(), randVec3(), randVec3())
            M = Mat3(randVec3(), randVec3(), randVec3())
            I = Mat3()

            v0 = T.trans(v)
            v1 = T.trans(v0)
            T.doti(T)
            v2 = T.trans(v)
            self.assertAlmostEqual(v1, v2)
            TI = T.dot(I)
            self.assertEqual(TI, T)
            self.assertEqual(T.rev.rev, T)
            T.rev = M.rev
            self.assertEqual(T, M)

        def testPickle(self):
            testvec = randVec3()
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEqual(testvec, loaded_vec)

    ####################################################################
    unittest.main()

    input("Press Enter to exit.")



#self.tranther.ry,=`= (*_*param v*_*) =`=jedi=`=
#               x   y   z
#  [ x']     [ m11 m12 m13 ]   [ x ]
#  [ y']  =  [ m21 m22 m23 ] * [ y ]
#  [ z']     [ m31 m32 m33 ]   [ z ]
#
#            [ x*m11 x*m12 x*m13 ]
#         =  [ y*m21 y*m22 y*m23 ]
#            [ z*m31 z*m32 z*m33 ]
#
#               x   y   z
#  [ x']     [ m11 m12 m13 ]   [ n11 n12 n13 ]
#  [ y']  =  [ m21 m22 m23 ] * [ n21 n22 n23 ]
#  [ z']     [ m31 m32 m33 ]   [ n31 n32 n33 ]

#
#  vector transformation for matrix T is:
#
#    V' = sum(TV)  where N is the old vector, V' is the transformed one
#
#      (temporary forget the rotation of multiply)
#
#  [ x']           [ m11 m12 ]   [ x ]
#  [ y']  =  sum ( [ m21 m22 ] * [ y ] )
#
#                  [ x*m11 x*m12 ]
#         =  sum ( [ y*m21 y*m22 ] )  =  [ x*m11+y*m21 x*m12+y*m22 ]
#
#         (x*m11+y*m21)*n11 + (x*m12+y*m22)*n21
#    =  x*(m11*n11+m12*n21) + y*(m21*n11+m22*n21)
#
#   MN  =  [ m11*n11+m12*n21 m21*n11+m22*n21 ]
#          [ m21*n11+m22*n21 m21*n12+m22*n22 ]

#
#
#  matrix transformation for matrix T is:
#
#    N' = sum(TN)  where N is the old matrix, N' is the transformed one
#
#  [ r11 r12 ]     [ m11 m12 ]   [ n11 n12 ]
#  [ r21 r22 ]  =  [ m21 m22 ] * [ n21 n22 ]
#
#                  [ m11 m12 ] * [ n11 n12 ]
#               =  [ m21 m22 ] * [ n21 n22 ]
#
#                  [ m11*n11 m12*n12 ]
#               =  [ m21*n21 m22*n22 ]
#
#  so that:
#                  [ m11*n11+m12*n21 ]
#    sum(T*`N)  =  [ m21*n12+m22*n22 ]
#
#  correction, this is incorrect:
#
#                  [ m11*[n11 n12]  m12*[n11 n12] ]
#               =  [ m21*[n21 n22]  m12*[n21 n22] ]
#
#                  [ [m11*n11 m11*n12]  [m12*n11 m12*n12] ]
#               =  [ [m21*n11 m21*n12]  [m22*n11 m22*n12] ]
#
#               ==sum&rev=>  [ m11*n11+m21*n11  m11*n12+m21*n12 ]
#                            [ m12*n11+m22*n11  m12*n12+m22*n12 ]
