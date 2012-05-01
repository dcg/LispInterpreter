from LISP.LispClasses import LispInteger, LispSymbol, LispCons, LispNull, new,\
    LispTrue, LispFalse, UserFunction, LispString, LispAtom
from LISP.BuildInFunctions import BuildInFunction, GetLocal, GetParam, GetGlobal
getLocal = GetLocal()
getParam = GetParam()
getGlobal = GetGlobal()
getLocalSym = new(LispSymbol,"getLocal")
getParamSym = new(LispSymbol,"getParam")
getGlobalSym = new(LispSymbol,"getParam")
def evall(lisp, env):
    if isinstance(lisp, LispSymbol):
        return evall(env.get(lisp),env)
    
    if issubclass(lisp.__class__, LispAtom):
        return lisp;
#    if isinstance(lisp,(LispTrue,LispNull,LispFalse)):
#        return lisp;
#    if isinstance(lisp, LispInteger):
#        return lisp;
#    if isinstance(lisp, LispString):
#        return lisp;
#    if isinstance(lisp, (BuildInFunction, UserFunction)):
#        return lisp;

    ###perfomance shortcuts####
    if lisp.first is getLocalSym:
        return getLocal.execute(env,lisp.rest.first)
    if lisp.first is getParamSym:
        return getParam.execute(env,lisp.rest.first)
    if lisp.first is getGlobalSym:
        return getGlobal.execute(env,lisp.rest.first)
    ### end of perfomance shortcuts###
#perfomance    if isinstance(lisp, LispCons):
    evalFirst = evall(lisp.first,env)
    args = _lispList2PythonList(lisp.rest)
    return evalFirst.execute(env,*args)
        
        

def _lispList2PythonList(lispList):
    args = []
    element = lispList
    while element.rest is not new(LispNull):
        args.append(element.first)
        element = element.rest
    args.append(element.first)
    return args