'''
Created on 30.03.2012

@author: dominik
'''
import unittest
from LISP.LispClasses import *


class Test(unittest.TestCase):


    def testSome(self):
        self.assertTrue(new(LispSymbol,"aa") is new(LispSymbol,"aa"))
        self.assertFalse(new(LispSymbol,"aa") is new(LispSymbol,"aba"))
        self.assertTrue(new(LispNull) is new(LispNull))
        self.assertTrue(new(LispSymbol,"TRUE") is new(LispSymbol,"TRUE"))
        a = new(LispSymbol,"TRUE")
        b=  new(LispTrue)
        print a
        print b
        self.assert_(a is b)
        str1 = LispString("abc")
        str2 = LispString("abc")
        str3 = LispString("abcb")
        self.assert_(str1==str2)
        self.assert_(str1!=str3)
        self.assert_(str1!=new(LispSymbol,"abc"))
        self.assert_(new(LispSymbol,"abc")!=str1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSome']
    unittest.main()