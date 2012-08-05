'''
Created on 17.05.2012

@author: dominik
'''
from LISP.LispClasses import LispSymbol, LispInteger,new, LispCons, LispNull
from LISP.Helper import lispList
from LISP.BuildInFunctions import Plus
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

def getOptCode(body,env, param_list):
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
        first = getOptCode(func.first, env, param_list)
        return LispCons(first,func.rest)
    if func.first == new(LispSymbol,"define"):
        env.put(func.rest.first,None)
        return func
    if func.first == new(LispSymbol,"+"):
        func = _normalizeFunction(func)
        print func
    first = getOptCode(func.first, env, param_list)
    rest = getOptCode(func.rest, env, param_list)
    return LispCons(first,rest)
    
def _normalizeFunction(func):
    if func.rest.rest.rest == new(LispNull):
        return func
    else:
        return _normalizeFunction(lispList(func.first, func.second(), _normalizeFunction(LispCons(func.first,func.rest.rest))))
