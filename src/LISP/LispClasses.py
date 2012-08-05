import LISP
from LISP.Helper import lispList
import Eval
import copy
from Tkinter import *

from LISP import BCMachine
class SingletonException(Exception):
    def __init__(self,singleton):
        self.singleton = singleton
        

def new(clazz,*args):
    ### this is just for perfomance ###
    if clazz == LispNull:
        if LispNull._instance != None:
            return LispNull._instance
    if clazz == LispTrue:
        if LispTrue._instance != None:
            return LispTrue._instance
    if clazz == LispFalse:
        if LispFalse._instance != None:
            return LispFalse._instance
    if clazz == LispSymbol:
        try:
            return LispSymbol._symbols[args[0]]
        except:
            pass
    ### end of perfomance block ###
    ret = None;
    try:
        ret = clazz(*args);
    except SingletonException as obj:
        ret = obj.singleton;
    return ret;



class LispTyp(object):
    pass


        
class LispAtom(LispTyp):
    def __str__(self):
        return str(self.value)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.value == other.value
        return False


class LispInteger(LispAtom):
    def __init__(self, integer):
        super(LispInteger, self).__init__()
        self.value = int(integer)
        
    def __eq__(self, other):
        if other == None:
            return False
        return self.value == other.value
    def __repr__(self):
        return str(self.value)

class LispSymbol(LispAtom):
    _symbols = {}
    def __init__(self, symbol):
        self.value = symbol
        if len(LispSymbol._symbols)==0:
            LispSymbol._symbols = {"NULL":new(LispNull), "TRUE":new(LispTrue), "FALSE":new(LispFalse)}
            print "init symbols"
        try:
            symbl  = LispSymbol._symbols[symbol]
            raise SingletonException(symbl)
        except KeyError:
            LispSymbol._symbols[symbol] = self
    

    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)


class LispNull(LispSymbol):
    _instance = None
    def __init__(self):
        self.value='()'
        if LispNull._instance:
            raise SingletonException(LispNull._instance)
        LispNull._instance= self
    def __unicode__(self):
        return "NULL"
    
class LispTrue(LispSymbol):
    _instance = None
    def __init__(self):
        self.value='TRUE'
        if LispTrue._instance:
            raise SingletonException(LispTrue._instance)
        LispTrue._instance= self
    def __str__(self):
        return "TRUE"
    
class LispFalse(LispSymbol):
    _instance = None
    def __init__(self):
        self.value='FALSE'
        if LispFalse._instance:
            raise SingletonException(LispFalse._instance)
        LispFalse._instance= self
    def __unicode__(self):
        return "FALSE"

class LispString(LispAtom):
    def __init__(self,value):
        self.value=value
    def __repr__(self):
        return '"%s"'%self.value
    def __str__(self):
        return '"%s"'%self.value
    

class LispCons(LispTyp):
    def __init__(self, first, rest=new(LispNull)):
        self.first=first
        self.rest=rest
    def addLastList(self,_list):
        element = self
        while element.rest != new(LispNull):
            element = element.rest
        element.rest=_list
    def __repr__(self):
        from LISP import Printer
        return Printer.printLisp(self)
    def second(self):
        return self.rest.first
    def third(self):
        return self.rest.rest.first
    def fourth(self):
        return self.rest.rest.rest.first
    def __len__(self):
        element = self
        i=1
        while element.rest != new(LispNull):
            element = element.rest
            i+=1
        return i
        

class UserFunction(LispTyp):
    def __init__(self,parameter,body,env):
        self.parameter = parameter
        self.param_list = Eval._lispList2PythonList(parameter)
        self.body = copy.copy(body)
        self.env = LISP.Enviroment(env)
        self.env.setParameterSymbols(self.param_list)
        print "-------- ---------"
        print "body: %s" % self.body
    #    if not self.body.first == new(LispSymbol,"lambda"):
        self.optcode = LISP.OptCoder.getOptCode(body,self.env,self.param_list)
        self.bytecode,self.literals = LISP.ByteCoder.getByteCode(LISP.ByteCoder.Bytecode(),LISP.ByteCoder.Literals(),self.optcode,self.env)
        print "optcode: %s"% self.optcode
        print "bytecode :%s"%self.bytecode
        print "-----------------"
        
    def execute_ea(self,*evalArgs):
        stack =[]
        for arg in evalArgs:
            if(arg == new(LispSymbol,"++bc++")):
                bc =""
                for b in self.bytecode.bytecode_txt:
                    bc+=(str(b)+"\n")
                return new(LispString,bc)
            if(arg == new(LispSymbol,"++op++")):
                return self.optcode
            stack.append(arg)
        return BCMachine.executeBC(self.bytecode, self.literals, stack, self.env)
    def execute(self,env, *unEvalArgs): 
        stack=[]
        param= []
        for i in range(len(unEvalArgs)):
            evalParam = LISP.Eval.evall(unEvalArgs[i],env)
            if(evalParam == new(LispSymbol,"++bc++")):
                bc =""
                for b  in self.bytecode.bytecode_txt:
                    bc+=(str(b)+"\n")
                return new(LispString,bc)
            if(evalParam == new(LispSymbol,"++op++")):
                return self.optcode
            param.append(evalParam)
            i=i+1
        self.env.setParameterList(param)
        for p in param:
            stack.append(p)
        return BCMachine.executeBC(self.bytecode,self.literals,stack, self.env)   
    def execute_opt(self,env, *unEvalArgs):
#        return self.execute_body(env, *unEvalArgs)
        param= []
        for i in range(len(unEvalArgs)):
            evalParam = LISP.Eval.evall(unEvalArgs[i],env)
            param.append(evalParam)
            i=i+1
        self.env.setParameterList(param)
        return LISP.Eval.evall(self.optcode,self.env)

    def execute_body(self,env, *unEvalArgs):
        paramList = LISP.Eval._lispList2PythonList(self.parameter)
        newEnv = LISP.Enviroment(self.env)
        for i in range(len(unEvalArgs)):
            evalParam = LISP.Eval.evall(unEvalArgs[i],env)
            newEnv.put(paramList[i],evalParam)
            i=i+1
        return LISP.Eval.evall(self.body,newEnv)
    
    def __repr__(self):
        return "(lambda %s %s)" % (self.parameter, self.body)
    
    
''' GUI STUFF'''
   
class LispTKClass(LispAtom):
    def __init__(self):
        self.value=Tk()
        self.value.title("SELF BUILDING LISP-GUI")
    def __repr__(self):
        return '"%s"'%self.value
    def __str__(self):
        return '"%s"'%self.value   
    def execute(self,env, *unEvalArgs):
        arg = Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"mainloop")):
            self.value.mainloop()
            

