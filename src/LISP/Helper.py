'''
Created on 29.04.2012

@author: dominik
'''
import LispClasses

def lispList(*elements):
    ret = None
    start= None
    for e in elements:
        if ret == None:
            start = LispClasses.LispCons(e)
            ret = start
        else:
            ret.rest = LispClasses.LispCons(e)
            ret = ret.rest
    return start