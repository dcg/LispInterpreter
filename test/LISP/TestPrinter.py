'''
Created on 30.03.2012

@author: dominik
'''
import unittest
from LISP.LispClasses import *
from LISP.Printer import printLisp


class Test(unittest.TestCase):


    def testPrint(self):
        self.assertTrue(printLisp(new(LispInteger,5)) == "5",printLisp(new(LispInteger,5)))
        self.assertTrue(printLisp(new(LispSymbol,"asd")) == "asd",printLisp(new(LispSymbol,"asd")))
        self.assertTrue(printLisp(new(LispNull)) == "()",printLisp(new(LispNull)))
        self.assertTrue(printLisp(new(LispTrue)) == "TRUE",printLisp(new(LispTrue)))
        self.assertTrue(printLisp(new(LispFalse)) == "FALSE",printLisp(new(LispFalse)))

        liste = new(LispCons,new(LispInteger,5))
        self.assertTrue(printLisp(liste)=="(5)",printLisp(liste))

        liste = new(LispCons,new(LispInteger,5),new(LispCons,new(LispInteger,6)))
        self.assertTrue(printLisp(liste)=="(5 6)",printLisp(liste))
        
        liste = new(LispCons,new(LispInteger,5),new(LispCons,new(LispTrue)))
        self.assertTrue(printLisp(liste)=="(5 TRUE)",printLisp(liste))
        
        l5 = new(LispInteger,5)
        l6 = new(LispInteger,6)
        liste = new(LispCons,l5,new(LispCons,l6))
        subListe = new(LispCons,l5,new(LispCons,l6))
        liste.rest.rest=new(LispCons,subListe,new(LispCons,l5))
        self.assertTrue(printLisp(liste)=="(5 6 (5 6) 5)",printLisp(liste))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPrint']
    unittest.main()