import LISP
from LISP.Helper import lispList
import Eval
import copy
class SingletonException(Exception):
    def __init__(self,singleton):
        self.singleton = singleton
        

def new(clazz,*args):
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
    __symbols = {}
    def __init__(self, symbol):
        self.value = symbol
        if len(LispSymbol.__symbols)==0:
            LispSymbol.__symbols = {"NULL":new(LispNull), "TRUE":new(LispTrue), "FALSE":new(LispFalse)}
            print "init symbols"
        try:
            symbl  = LispSymbol.__symbols[symbol]
            raise SingletonException(symbl)
        except KeyError:
            LispSymbol.__symbols[symbol] = self
    

    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)


class LispNull(LispSymbol):
    __instance = None
    def __init__(self):
        self.value='()'
        if LispNull.__instance:
            raise SingletonException(LispNull.__instance)
        LispNull.__instance= self
    def __unicode__(self):
        return "NULL"
    
class LispTrue(LispSymbol):
    __instance = None
    def __init__(self):
        self.value='TRUE'
        if LispTrue.__instance:
            raise SingletonException(LispTrue.__instance)
        LispTrue.__instance= self
    def __str__(self):
        return "TRUE"
    
class LispFalse(LispSymbol):
    __instance = None
    def __init__(self):
        self.value='FALSE'
        if LispFalse.__instance:
            raise SingletonException(LispFalse.__instance)
        LispFalse.__instance= self
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
    
def _getParameter(parameter,element):
    for i in range(len(parameter)):
        if element == parameter[i]:
            return i
    return -1

def _getOptCode(body,param_list):
    if isinstance(body,LispSymbol):
        index = _getParameter(param_list,body)
        if index > -1:
            return lispList(new(LispSymbol,"getParam"),LispInteger(index))
    if isinstance(body,LispCons):
        return LispCons(_getOptCode(body.first,param_list), _getOptCode(body.rest,param_list))
    return body
        

class UserFunction(LispTyp):
    def __init__(self,parameter,body,env):
        self.parameter = parameter
        self.param_list = Eval._lispList2PythonList(parameter)
        self.body = copy.copy(body)
        self.env = env
        self.optcode = _getOptCode(body,self.param_list)
        print self.body
        print self.optcode
        
    def execute(self,env, *unEvalArgs):
        #paramList = LISP.Eval._lispList2PythonList(self.parameter)
      # newEnv = LISP.Enviroment(self.env)
        param= []
        for i in range(len(unEvalArgs)):
            evalParam = LISP.Eval.evall(unEvalArgs[i],env)
            param.append(evalParam)
            i=i+1
        self.env.setParameter(param)
        return LISP.Eval.evall(self.optcode,self.env)

    def __repr__(self):
        return "(lambda %s %s)" % (self.parameter, self.body)