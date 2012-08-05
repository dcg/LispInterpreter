'''
Created on 01.06.2012

@author: dominik
'''
import LISP

''' Fuehrt Bytecode aus '''
def executeBC(bytecode,literals,stack,env):
    pc=0
    #stackcounter =0
    while True:
        if len(bytecode.bytecode_txt)<=pc:
            return stack.pop()
        instr=bytecode.bytecode_txt[pc].split(" ")
        pc+=1
        cmd = instr[0]
        cmd_param = int(instr[1])
        if cmd=='PUSH-CONSTANT':
            stack.append(literals[cmd_param])
        elif cmd=='PUSH-GLOBAL':
            stack.append(env.get_global_by_index(cmd_param))
        elif cmd=='PUSH-PARAM':
            stack.append(stack[cmd_param])
        elif cmd=='PUSH-SUPER-PARAM':
            stack.append(env.get_super_parameter_by_index(cmd_param,bytecode.bytecode_txt[pc].value))
            pc+=1
        elif cmd=="PUSH-INT":
            stack.append(LISP.LispClasses.LispInteger(cmd_param))
        elif cmd=="JUMP_IF_FALSE":
            cond = stack.pop()
            if cond == LISP.LispClasses.new(LISP.LispClasses.LispSymbol,"FALSE"):
                pc=jump(cmd_param,bytecode,pc)   
        elif cmd=="JUMP":
            pc=jump(cmd_param,bytecode,pc)
            
        elif cmd=='CALL':
            func = stack.pop()
            param=[]
            for i in range(cmd_param):
                param.append(stack.pop())
            if isinstance(func, (LISP.BuildInFunctions.Lambda,LISP.BuildInFunctions.Eval)):
                param.append(env)
            stack.append(func.execute_ea(*param))
        
def jump(label,bytecode,pc):
    for i in range(len(bytecode.bytecode_txt)):
        if isinstance(bytecode.bytecode_txt[i],str):
            instr=bytecode.bytecode_txt[i].split(" ")
            if instr[0]=="LABEL" and int(instr[1]) == label:
                return i
    print "LABEL NOT FOUND!!! %s"%label
    raise LookupError("LABEL Not Found: \"%s\"" % label)
     