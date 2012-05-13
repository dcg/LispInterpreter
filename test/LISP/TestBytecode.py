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
        func = evall(readLisp("(define a 5)"),env)

        func = evall(readLisp("(lambda (x) (+ x 2 a))"),env)
        print func
        print func.optcode
        print func.bytecode


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()