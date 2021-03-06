'''
Created on 30.03.2012

@author: dominik
'''
from LISP.LispClasses import LispAtom, LispNull, new, LispCons, UserFunction
def printLisp(lispTyp):
    null = new(LispNull)
    if lispTyp==None:
        return ""
    if isinstance(lispTyp, LispAtom):
        return str(lispTyp.value)
    elif isinstance(lispTyp, UserFunction):
        return lispTyp.__repr__()
    else:
        string = '('
        while (not lispTyp.rest is null):
            string+=__getString(lispTyp," ")
            lispTyp = lispTyp.rest;

        string += __getString(lispTyp,"")+")"
        return string
         
         
def __getString(lispTyp, whitespace):
    string =""
    if isinstance(lispTyp.first, LispAtom):
        string += str(lispTyp.first.value) + whitespace;
    elif isinstance(lispTyp.first, LispCons):
        string += printLisp(lispTyp.first) +whitespace   
    return string      
