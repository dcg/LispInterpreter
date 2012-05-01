from LISP.LispClasses import LispInteger, LispSymbol, LispCons, LispNull, new,\
    LispTrue, LispFalse, UserFunction, LispString
from LISP.BuildInFunctions import BuildInFunction
def evall(lisp, env):
    if isinstance(lisp,(LispTrue,LispNull,LispFalse)):
        return lisp;
    if isinstance(lisp, LispInteger):
        return lisp;
    if isinstance(lisp, LispString):
        return lisp;
    if isinstance(lisp, (BuildInFunction, UserFunction)):
        return lisp;
    if isinstance(lisp, LispSymbol):
        return evall(env.get(lisp),env)
    if isinstance(lisp, LispCons):
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