'''
Created on 12.05.2012

@author: dominik
'''
import unittest
from LISP.Eval import evall
from LISP.Reader import readLisp
from LISP.Enviroment import Enviroment


class Test(unittest.TestCase):


    def testByteCode(self):
        env = Enviroment()
        #func = evall(readLisp("(define a 5)"),env)
        
       # func = evall(readLisp("(define (foo x) (+ 5 x))"),env)
        lisp = readLisp("(define asd (lambda (x y z a) (+ x y z a x)))")
        func = evall(lisp,env)
        lisp = readLisp("(define foo (lambda (x) (asd x 2 3 4)))")
        func = evall(lisp,env)
        foo= evall(readLisp("(foo 1)"),env)
    #    result = evall(readLisp("(foo 3)"),env)
        print func
      #  print func.optcode
       # print func.bytecode
        #print func.literals
        print foo
      #  print result
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()