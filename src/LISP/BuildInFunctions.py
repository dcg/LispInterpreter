'''
Created on 10.04.2012

@author: dominik
'''

from LISP.LispClasses import LispInteger, LispSymbol, LispNull, new, LispTrue,\
    LispFalse, UserFunction, LispCons, LispString
import LISP
from LISP import Reader
from LISP.Printer import printLisp

class BuildInFunction(object):
    def __init__(self,name):
        self.value="<<BuildInFunction "+name+">>"
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value

class Plus(BuildInFunction):
    def __init__(self):
        super(Plus, self).__init__("Plus")
    def execute(self,env,*unEvalArgs):
        ret = 0;
        for unEvalArg in unEvalArgs:
            evalArg =LISP.Eval.evall(unEvalArg,env)
            ret = ret + evalArg.value
        return LispInteger(ret)
 
class Minus(BuildInFunction):
    def __init__(self):
        super(Minus, self).__init__("Minus")
    def execute(self,env,*unEvalArgTuple):
        unEvalArgs = list(unEvalArgTuple)
        ret = LISP.Eval.evall(unEvalArgs.pop(0),env).value;
        for unEvalArg in unEvalArgs:
            evalArg =LISP.Eval.evall(unEvalArg,env)
            ret = ret - evalArg.value
        return LispInteger(ret)
    
class Define(BuildInFunction):
    def __init__(self):
        super(Define,self).__init__("Define")
        
    def execute(self,env,*unEvalArgTuple):
        symbol = unEvalArgTuple[0]
        if isinstance(symbol, LispCons):
            func = Lambda().execute(env,symbol.rest,*unEvalArgTuple[1:len(unEvalArgTuple)])
            return self.execute(env,symbol.first,func)
        
        if not isinstance(symbol, LispSymbol):
            print "first argument was not a symbol"
            return new(LispNull)
        
        value = LISP.evall(unEvalArgTuple[1],env)
        env.put(symbol,value)
        return new(LispNull)
 
class If(BuildInFunction):
    def __init__(self):
        super(If,self).__init__("If")
    
    def execute(self,env,*unEvalArgTuple):
        condition = LISP.evall(unEvalArgTuple[0],env)
        if condition is new(LispTrue):
            return LISP.evall(unEvalArgTuple[1],env)
        else:
            return LISP.evall(unEvalArgTuple[2],env)

class Eq(BuildInFunction):
    def __init__(self):
        super(Eq,self).__init__("Eq?")
        
    def execute(self,env,*unEvalArgs):
        arg1 = LISP.Eval.evall(unEvalArgs[0],env)
        arg2= LISP.Eval.evall(unEvalArgs[1],env)
        if arg1 == arg2:
            return new(LispTrue)
        return new(LispFalse)
    
class Begin(BuildInFunction):
    def __init__(self):
        super(Begin,self).__init__("Begin")
        
    def execute(self,env,*unEvalArgs):
        arg=None;
        for uneval in unEvalArgs:
            arg = LISP.evall(uneval,env)
        return arg
    
class Lambda(BuildInFunction):
    def __init__(self):
        super(Lambda,self).__init__("Lambda")
    def execute(self,env, *unEvalArgs):
        body = unEvalArgs[1];
        if len(unEvalArgs) > 2:
            body = LispCons(new(LispSymbol,"begin"))
            element = body
            for i in range(1,len(unEvalArgs)):
                element.rest=LispCons(unEvalArgs[i])
                element=element.rest     
        return UserFunction(unEvalArgs[0],body,env)
    
class Write(BuildInFunction):
    def __init__(self):
        super(Write,self).__init__("Write")
    def execute(self,env, *unEvalArgs):
        evalArg = LISP.evall(unEvalArgs[0],env)
        print printLisp(evalArg)
        
class Print(BuildInFunction):
    def __init__(self):
        super(Print,self).__init__("Print")
    def execute(self,env, *unEvalArgs):
        evalArg = LISP.evall(unEvalArgs[0],env)
        if isinstance(evalArg, LispString):
            print "\"%s\"" % evalArg.value
        else:
            print printLisp(evalArg)
            
class Set(BuildInFunction):
    def __init__(self):
        super(Set,self).__init__("Set!")
    def execute(self,env, *unevalArgs):
        env.set(unevalArgs[0],LISP.evall(unevalArgs[1],env))

class Quote(BuildInFunction):
    def __init__(self):
        super(Quote,self).__init__("Quote")
    def execute(self,env, *unevalArgs):
        return unevalArgs[0]
    
class GetParam(BuildInFunction):
    def __init__(self):
        super(GetParam,self).__init__("GetParam")
    def execute(self,env, *args):
        index = args[0].value
        return env.getParameter(index)
            
        