'''
Created on 30.03.2012

@author: dominik
'''
import unittest
from LISP.Reader import *
from LISP.Printer import *
from LISP.LispClasses import LispTrue, LispString

class Test(unittest.TestCase):



    def testReader(self):
        tests = (
                  "4",
                  "(4)",
                  "(4 5)",
                  "(4 5 6)",
                  "(abc def geh)",
                  "()",
                  "(4 5 (5 6) 4)",
                  "(4 (4 5) (4 5) (4 (4 5 (4 5 (6 7 9 0)))))");
        for test in tests:
            self.assert_(printLisp(readLisp(test))==test, "read: "+printLisp(readLisp(test))+"\n expected: "+test)
        print(readLisp("TRUE"))
        self.assert_(readLisp("TRUE") is new(LispTrue))

    def testNewLineRead(self):
        foo='''(4 
        5
        6
        7
        )'''
        readLisp(foo)
    
    def testReadString(self):
        lisp1= readLisp("'foo'")
        lisp2= readLisp("\"foo\"")
        self.assert_(lisp2==LispString("foo"))
        self.assert_(lisp1==LispString("foo"))
        lisp2= readLisp("('foo' 'baar')")
        self.assert_(lisp2.first==LispString("foo"))
        self.assert_(lisp2.rest.first==LispString("baar"))
        lisp3=readLisp('(a "fooo")')
        self.assert_(lisp3.first==new(LispSymbol,"a"))
        self.assert_(lisp3.rest.first==LispString("fooo"))
        
        lisp4 = readLisp("(lambda (x) (write 'fooo'))")
        self.assert_(lisp4.rest.rest.first.rest.first==LispString("fooo"))

        lisp5 = readLisp("((lambda (x) (write 'fooo')) 5)")
        print lisp5.first.rest.rest.first.rest.first
        print type(lisp5.first.rest.rest.first.rest.first)
        self.assert_(lisp5.first.rest.rest.first.rest.first==LispString("fooo"))

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
