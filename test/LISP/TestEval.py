'''
Created on 10.04.2012

@author: dominik
'''
import unittest
from LISP.Reader import readLisp
from LISP.Eval import evall
from LISP.Enviroment import Enviroment, SymbolNotFound
from LISP.LispClasses import *
class Test(unittest.TestCase):

    def setUp(self):
        self.env = Enviroment();
        self.env.put(new(LispSymbol,"a"),LispInteger(5))
        
    def testevalu1(self):
        lisp = readLisp("4")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(4))
        
    def testevalu2(self):
        lisp = readLisp("5")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(5))
    
    def testevalu3(self):
        lisp = readLisp("a")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(5))
    
    def testevalu4(self):
        lisp = readLisp("(+ 5 4)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(9))
    
    def testevalu5(self):
        lisp = readLisp("(+ (+ 5 4) 4 1)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(14))
        
    def testevalu6(self):
        lisp = readLisp("(+ (+ a 4) 4 1)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(14))
    
    def testevalu7(self):
        lisp = readLisp("(- 4 1)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(3))
        
    def testevalu8(self):
        evall(readLisp("(define xxx 666)"),self.env)
        lisp = readLisp("(- xxx 1)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(665))
    
    def testevalu9(self):
        lisp = readLisp("(if TRUE (+ 5 6) (+ 4 3))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(11))
        
    def testevalu10(self):
        lisp = readLisp("(if FALSE (+ 5 6) (+ 4 3))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(7))
    
    def testevalu11(self):
        lisp = readLisp("(if (eq? 5 5) (+ 5 6) (+ 4 3))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(11))

    def testevalu12(self):
        lisp = readLisp("(lambda (a) (+ a 1))")
        val = evall(lisp,self.env)
        self.assert_(isinstance(val, UserFunction))
        
    def testevalu13(self):
        lisp = readLisp("(define add1 (lambda (a) (+ a 1)))")
        evall(lisp,self.env)
        
        lisp = readLisp("(add1 5)")
        val =  evall(lisp,self.env)
        self.assert_(val == LispInteger(6))
        
    def testevalu14(self):
        lisp = readLisp("(define addSum1 (lambda (a b) (+ a b 1)))")
        evall(lisp,self.env)
        
        lisp = readLisp("(addSum1 5 6)")
        val =  evall(lisp,self.env)
        self.assert_(val == LispInteger(12))
        
    def testevalu15(self):
        lisp = readLisp("(define somethingStrange (lambda (a b c d ) (+ a b 1 (- c b) (- c d a) (+ a (+ 1 2 c)))))")
        evall(lisp,self.env)
        
        lisp = readLisp("(somethingStrange 1 2 3 4)")
        val =  evall(lisp,self.env)
        evall(readLisp("(somethingStrange 44 33 88 8)"),self.env)
        self.assert_(val == LispInteger(10))
        
    def testevalu16(self):
        lisp = readLisp("(define (func a b) (+ a b))")
        evall(lisp,self.env)
        val= evall(readLisp("(func 10 20)"),self.env)
        self.assert_(val == LispInteger(30))

    def testBegin(self):
        lisp = readLisp("(begin (+ 3 5) (+ 3 4))")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(7))
    
    def testLambdaBegin(self):
        lisp = readLisp("(lambda (x) (- 5 x) (+ 5 x))")
        val = evall(lisp,self.env)
        self.assert_(isinstance(val,UserFunction))
        
        lisp = readLisp("(lambda (x) (print 'Foobar') 5)")
        val = evall(lisp,self.env)
        self.assert_(isinstance(val,UserFunction))

        lisp = readLisp("((lambda (x) (print 'Hallo Welt') (+ 5 x)) 5)")
        val = evall(lisp,self.env)
        self.assert_(val == LispInteger(10))
  
    def testDefineBegin(self):
        lisp = readLisp("(define (foo x) (print 'Hello World') (write (- 2 x)) (- 5 x) (+ 5 x))")
        val = evall(lisp,self.env)
        lisp2 = readLisp("(foo 5)")
        val = evall(lisp2,self.env)
        self.assert_(val==LispInteger(10))

    def testSet(self):
        lisp = readLisp("(set! a 555)")
        evall(lisp,self.env)
        self.assert_(self.env.get(new(LispSymbol,"a"))==LispInteger(555))
        lisp = readLisp("(set! ab 666)")
        try:
            evall(lisp,self.env)
            self.fail("Exception not thrown")
        except SymbolNotFound:
            pass
        
        lisp = readLisp("(set! a 'Foo')")
        evall(lisp,self.env)
        self.assert_(self.env.get(new(LispSymbol,"a"))==LispString("Foo"))
        
    def test_something_long_with_all_this_cool_set_and_closure_stuff(self):
        lispStr = '''
        (define (make-point x y)
  (define (get-x)
    x)
  (define (get-y)
    y)
  (define (set-x! newX)
    (set! x newX))
  (define (set-y! newY)
    (set! y newY))
  (define (area)
    (* x y))
  (define (error)
    (print "mist"))
    
      (define (dispatch op)
    (if (eq? op 'get-x)
        get-x
    (if (eq? op 'get-y)
        get-y
    (if (eq? op 'set-x!)
        set-x!
    (if (eq? op 'set-y!)
        set-y!
    (if (eq? op 'area)
        area
        error))))))
  
  dispatch)

        '''
        lisp= readLisp(lispStr)
        val= evall(lisp,self.env)
        val = evall(readLisp("(make-point 5 6)"),self.env)
        self.assert_(isinstance(val,UserFunction))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()