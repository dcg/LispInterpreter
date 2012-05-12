'''
Created on 20.04.2012

@author: dominik
'''
import unittest
from LISP.LispClasses import LispInteger, new, LispSymbol, UserFunction
from LISP import *
class Test(unittest.TestCase):

    def setUp(self):
        self.env = Enviroment();
        self.env.put(new(LispSymbol,"a"),LispInteger(5))
        
    def testClosure(self):
        lispStr = '''  (define (make-adder x)
                          (lambda (y) (+ y x)))'''
        lisp = readLisp(lispStr)
        evall(lisp, self.env)
        val2 = evall(readLisp("(make-adder 3)"),self.env)
        self.assert_(isinstance(val2, UserFunction))
        evall(readLisp("(define add3 (make-adder 3))"),self.env)
        val3 = evall(readLisp("(add3 5)"),self.env)
        self.assert_(val3 == LispInteger(8))
        evall(readLisp("(define x 59)"),self.env)
        evall(readLisp("(define y 99)"),self.env)
        val3 = evall(readLisp("(add3 5)"),self.env)
        self.assert_(val3 == LispInteger(8))
        
    def atestClosure2(self):
        lispStr = '''  (define (make-adder a b c d e f)
                          (lambda (x y z) (print a) (print b) (print c) (print d) (print e) (print f) (print x) (print y) (print z)))'''
        lisp = readLisp(lispStr)
        evall(lisp, self.env)
        evall(readLisp("(define add3 (make-adder 1 2 3 4 5 6))"),self.env)
        val3 = evall(readLisp("(add3 7 8 9)"),self.env)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()