'''
Created on 10.04.2012

@author: dominik
'''
from LISP import BuildInFunctions
from LISP.LispClasses import LispSymbol,new, LispTrue, LispFalse
from LISP.BuildInFunctions import Plus,Minus, Define, If, Eq, Lambda, Begin,\
    Write,Print, Set, Quote, GetParam, GetLocal, GetSuperParam, GetSuperLocal, GetGlobal
from compiler.ast import Print
from collections import OrderedDict
import LISP
class SymbolNotFound(LookupError):
    def __init__ (self, msg):
        self.msg=msg
    def __unicode__(self, *args, **kwargs):
        return self.msg
    def __str__(self, *args, **kwargs):
        return self.msg
    def __repr__(self, *args, **kwargs):
        return self.msg
    

class Enviroment():
    __global_env=None
    def __init__ (self, superEnv=None):
        self.map = OrderedDict()
        self.map_index = []
        self.superEnv=superEnv
        
        if superEnv==None:
            Enviroment. __global_env=self

            self.put(new(LispSymbol,"+"),Plus())
            self.put(new(LispSymbol,"-"),Minus())
            self.put(new(LispSymbol,"define"),Define())
            self.put(new(LispSymbol,"if"),If())
            self.put(new(LispSymbol,"eq?"),Eq())
            self.put(new(LispSymbol,"lambda"),Lambda())
            self.put(new(LispSymbol,"begin"),Begin())
            self.put(new(LispSymbol,"set!"),Set())
            self.put(new(LispSymbol,"quote"),Quote())
            self.put(new(LispSymbol,"write"),Write())
            self.put(new(LispSymbol,"print"),BuildInFunctions.Print())
            self.put(new(LispSymbol,"getParam"),GetParam())
            self.put(new(LispSymbol,"getLocal"),GetLocal())
            self.put(new(LispSymbol,"getSuperParam"),GetSuperParam())
            self.put(new(LispSymbol,"getSuperLocal"),GetSuperLocal())
            self.put(new(LispSymbol,"getGlobal"),GetGlobal())
        
    def set(self, key ,value):
        if key in self.map:
            self.map[key]=value
            self.map_index=self.map.values()
        else:
            raise SymbolNotFound("Key '%s' is not defined, yet"%key.value)
    def put(self, key, value):
        self.map[key] = value
        self.map_index=self.map.values()

    def get(self,key):
        env = self
        while env != None:
            try:
                return env.map[key]
            except KeyError:
                env = env.superEnv
        print "UNDEFINED SYMBOL"
        raise SymbolNotFound("Symbol Not Found: \"%s\"" % key.value)
    
    def get_local_by_index(self,index):
        return self.map_index[index]
    
    def get_global_by_index(self,index):
        return Enviroment.__global_env.map_index[index]
    
    def get_local_index(self,element):
        i=0
        for key in self.map:
            if key == element:
                return i
            i+=1
        return -1
    
    def get_global_index(self,element):
        i=0
        for key in Enviroment.__global_env.map:
            if key == element:
                return i 
            i+=1
        return -1
    def setParameterSymbols(self,symbols):
        self.parameter_symbols=symbols;
        
    def setParameterList(self, param):
        self.parameter=param
    def getParameter(self, index):
        return self.parameter[index]
    def __repr__(self):
        return  self.map.__repr__()