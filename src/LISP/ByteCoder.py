'''
Created on 12.05.2012

@author: dominik
'''
from LISP.LispClasses import LispAtom, LispCons, new, LispSymbol, LispNull,\
    UserFunction, LispInteger
from LISP.BuildInFunctions import GetParam, BuildInFunction, Lambda, If

class Literals(list):
    pass
    
class Bytecode:
    def __init__(self):
        self.bytecode=[]
        self.bytecode_txt=[]
        
    def __str__(self):
        tex =""
        tex+= "#### ByteCode #### \n"
        for txt in self.bytecode_txt:
            tex +="%s \n" % txt 
        tex+= "---- ByteCode-----"
        return tex
     
    def reverse(self):
        self.bytecode.reverse()
        self.bytecode_txt.reverse()
        return self
     
def getByteCode(bytecode,literals,optcode,env):
    byte,lit = _getByteCode(bytecode,literals,optcode,env)
    return byte.reverse(),lit
def _getByteCode(bytecode,literals,optcode,env):
    
    if isinstance(optcode ,LispNull):
        return bytecode,literals
    if isinstance(optcode,LispInteger):
        bytecode.bytecode_txt.append("PUSH-INT %s" % optcode.value)
        return bytecode,literals
    if isinstance(optcode,LispAtom):
        literals.append(optcode)
        bytecode.bytecode_txt.append("PUSH-CONSTANT %s" % (len(literals)-1))
        return bytecode,literals
    if isinstance(optcode.first, LispCons):
        
        if isinstance(optcode.first.first, LispSymbol):
            inst = optcode.first
            if inst.first.value =='getParam':
                push = "PUSH-PARAM %s"
                real_value = env.get_parameter_by_index(inst.rest.first.value)
                    
            if inst.first.value =='getGlobal':
                push = "PUSH-GLOBAL %s"
                real_value = env.get_global_by_index(inst.rest.first.value)
                    
            if inst.first.value =='getLocal':
                push = "PUSH-LOCAL %s"
                real_value = env.get_local_by_index(inst.rest.first.value)
                
            if inst.first.value =='getSuperLocal':
                bytecode.bytecode_txt.append(inst.third())
                push = "PUSH-SUPER-LOCAL %s"
                real_value = env.get_super_local_by_index(inst.second().value,inst.third().value)
                
            if inst.first.value =='getSuperParam':
                bytecode.bytecode_txt.append(inst.third())
                push = "PUSH-SUPER-PARAM %s"
                real_value = env.get_super_parameter_by_index(inst.second().value,inst.third().value)
                
                
            skip =False;
            if isinstance(real_value,Lambda):
                literals.append(optcode.rest)
                call_count=len(optcode.rest)
#                bytecode.bytecode_txt.append("CALL %s "%call_count)
                bytecode.bytecode_txt.append("CALL 2")
                #symbols = env.getParameterSymbols()
                pushes=[]
                #for i,_ in enumerate(symbols):
                  #  pushes.append("PUSH-PARAM %s" %i)
                pushes.append("PUSH-CONSTANT %s" % (len(literals)-1))
                skip=True
            elif isinstance(real_value,If):
                make_if_bytecode(optcode,bytecode,literals,env)
                return bytecode,literals
            elif _isFunctionCallNeeded(real_value):
                bytecode.bytecode_txt.append("CALL %s"%len(optcode.rest))
                
            bytecode.bytecode_txt.append(push %inst.rest.first.value)
            if not skip:
                _getByteCode(bytecode, literals, optcode.rest, env)
            else:
                for push2 in pushes:
                    bytecode.bytecode_txt.append(push2)
            return bytecode,literals
    
    if isinstance(optcode,LispCons):
        _getByteCode(bytecode,literals,optcode.first,env)
        _getByteCode(bytecode,literals,optcode.rest,env)
        return bytecode,literals
        
  
def _isFunctionCallNeeded(real_value):
    if isinstance(real_value,UserFunction):
        return True
    if isinstance(real_value,BuildInFunction):
        return True


def label_generator():
    i = 11111111111111111
    while(True):
        yield i
        i+=11111111111111111 
labels = label_generator()
def make_if_bytecode(optcode,bytecode,literals,env):
    body = optcode.rest
    cond = body.first
    false_branch = body.third()
    true_branch = body.second()
    l_endif=labels.next()
    l_false=labels.next()
    bytecode.bytecode_txt.append("LABEL %s"%l_endif)
    _getByteCode(bytecode,literals,false_branch,env)
    bytecode.bytecode_txt.append("LABEL %s"%l_false)
    bytecode.bytecode_txt.append("JUMP %s"%l_endif)
    _getByteCode(bytecode,literals,true_branch,env)
    bytecode.bytecode_txt.append("JUMP_IF_FALSE %s" %l_false)
    _getByteCode(bytecode,literals,cond,env)
    
    pass;