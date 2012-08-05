'''
Created on 05.08.2012

@author: dominik
'''
import unittest
import unittest
from LISP.Reader import readLisp
from LISP.Eval import evall
from LISP.Enviroment import Enviroment, SymbolNotFound
from LISP.LispClasses import *

class Test(unittest.TestCase):

    def setUp(self):
        self.env = Enviroment();
        self.env.put(new(LispSymbol,"a"),LispInteger(5))

    def testeval_if_in_function(self):
        lisp = readLisp("((lambda (x) (if TRUE 5 6)))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(5))
        
    def testeval_if_in_function_F(self):
        lisp = readLisp("((lambda (x) (if FALSE 5 6)))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(6))
        
    def testeval_if_in_function_with_cond(self):
        lisp = readLisp("((lambda (x) (if (<? 4 3) (+ 3 5) (+ 3 6))))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(9))
    def testeval_if_in_function_with_cond_F(self):
        lisp = readLisp("((lambda (x) (if (>? 4 3) (+ 3 5) (+ 3 6))))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(8))
        
    def testeval_if_in_function_with_complex_cond(self):
        lisp = readLisp("((lambda (x) (if (>? 4 3) (if (>? 3 5) (+ 3 2) (+ 5 9)) (+ 3 6))))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(14))
        
    def testeval_begin_in_function(self):
        lisp = readLisp("((lambda (x) (begin (+ 4 3) (+ 2 3))))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(5))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()