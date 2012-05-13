'''
Created on 12.05.2012

@author: dominik
'''
from LISP.LispClasses import LispAtom, LispCons, new, LispSymbol, LispNull

class Bytecode:
    def __init__(self):
        self.bytecode=[]
        self.bytecode_txt=[]
        
    def __str__(self):
        tex =""
        tex+= "#### ByteCode ####"
        for txt in self.bytecode_txt:
            tex +="%s \n" % txt 
        tex+= "---- ByteCode-----"
        return tex
        
def getByteCode(bytecode,optcode):
    
    if isinstance(optcode ,LispNull):
        return bytecode
    if isinstance(optcode,LispAtom):
        bytecode.bytecode_txt.append(optcode.value)
        return bytecode.bytecode_txt
    if isinstance(optcode,LispCons):
        getByteCode(bytecode,optcode.first)
        getByteCode(bytecode,optcode.rest)
        return bytecode
        
        