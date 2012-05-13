import LISP
from LISP.Helper import lispList
import Eval
import copy
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
    

class UserFunction(LispTyp):
    def __init__(self,parameter,body,env):
        self.parameter = parameter
        self.param_list = Eval._lispList2PythonList(parameter)
        self.body = copy.copy(body)
        self.env = LISP.Enviroment(env)
        self.env.setParameterSymbols(self.param_list)
        self.optcode = _getOptCode(body,self.env,self.param_list)
        self.bytecode = LISP.ByteCoder.getByteCode(LISP.ByteCoder.Bytecode(),self.optcode)
    # print "-------- ---------"
    #    print "body: %s" % self.body
    #    print "optcode: %s"% self.optcode
    #    print "-----------------"
    def execute(self,env, *unEvalArgs):
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
    
    
    
def _getParameter(parameter,element):
    for i in range(len(parameter)):
        if element == parameter[i]:
            return i
    return -1
def _getLocal(env,element):
    return  env.get_local_index(element)
 
def _getGlobal(env,element):
    return env.get_global_index(element)    
def _getSuperParam(env, element):
    i = 1
    _env = env.superEnv
    while _env != None:
        try:
            index = _getParameter(_env.parameter_symbols,element)
            if index > -1:
                if _env.superEnv!=None:
                    return (index,i)
        except AttributeError as e:
            pass
        _env = _env.superEnv
        i+=1
    return (-1,-1)
def _getSuperLocal(env, element):
    i = 1
    _env = env.superEnv
    while _env != None:
        index = _getLocal(_env,element)
        if index > -1:
            if _env.superEnv!=None:
                return (index,i)
        _env = _env.superEnv
        i+=1
    return (-1,-1)

def _getOptCode(body,env, param_list):
    if isinstance(body,LispSymbol):
        index = _getParameter(param_list,body)
        if index > -1:
            return lispList(new(LispSymbol,"getParam"),LispInteger(index))
        else: 
            index = _getLocal(env,body)
            if index > -1:
                return lispList(new(LispSymbol,"getLocal"),LispInteger(index))
            else:
                (index,super) =_getSuperParam(env,body)
                if index >-1:
                    return lispList(new(LispSymbol,"getSuperParam"),LispInteger(index),LispInteger(super))
                else:
                    (index,super) =_getSuperLocal(env,body)
                    if index >-1:
                        return lispList(new(LispSymbol,"getSuperLocal"),LispInteger(index),LispInteger(super))
                    else:
                        index = _getGlobal(env,body)
                        if index > -1:
                            return lispList(new(LispSymbol,"getGlobal"),LispInteger(index))
    if isinstance(body,LispCons):
        return __getOptFunction(body, env, param_list)
    return body

def __getOptFunction(func,env,param_list):
    if func.first == new(LispSymbol,"lambda"):
        return func
    if func.first == new(LispSymbol,"define"):
        env.put(func.rest.first,None)
        return func
    first = _getOptCode(func.first, env, param_list)
    rest = _getOptCode(func.rest, env, param_list)
    return LispCons(first,rest)
    
    
        
