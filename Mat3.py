#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Vec3 import Vec3

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

def dotproduct(self, other):
        '''
        get dot product with self and other whoever is Vec3 or Mat3,
        self is the left operand.
        '''
        return self.dot(other)

if __name__ == "__main__":

    import unittest
    import pickle
    from random import random

    def randVec3():
        return Vec3(random(), random(), random())

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

