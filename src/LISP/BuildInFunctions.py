'''
Created on 10.04.2012

@author: dominik
'''

from LISP.LispClasses import LispInteger, LispSymbol, LispNull, new, LispTrue,\
    LispFalse, UserFunction, LispCons, LispString, LispAtom
import LISP
from LISP import Reader, LispClasses
from LISP.Printer import printLisp
import string
from distutils.command.build import build
from Tkinter import Text, Button, Frame, Toplevel, Label, Scrollbar
from Tkconstants import END, RIGHT, Y, BOTH, YES

class BuildInFunction(LispAtom):
    def __init__(self,name,bytecode_txt=None,symbol=None):
        self.value="<<BuildInFunction "+name+">>"
        if bytecode_txt==None:
            self.bytecode_txt=name
        else:
            self.bytecode_txt=bytecode_txt
        if symbol ==None:
            self.symbol=name.lower()
        else:
            self.symbol=symbol   
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
    def execute_ea(self,*evalArgs):
        ret = 0
        for arg in evalArgs:
            ret = ret +arg.value
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
    def execute_ea(self,*evalArgs):
        evalArgList = list(evalArgs)
        ret = evalArgList.pop(0).value
        for arg in evalArgList:
            ret = ret -arg.value
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
        return value
    def execute_ea(self,*evalArgs):
        symbol = evalArgs[0]
        env = evalArgs[-1]
        if isinstance(symbol, LispCons):
            func = Lambda().execute_ea(env,symbol.rest,*evalArgs[1:len(evalArgs)])
            return self.execute_ea(env,symbol.first,func)
        if not isinstance(symbol, LispSymbol):
            print "first argument was not a symbol"
            return new(LispNull)
        value = evalArgs[1]
        env.put(symbol,value)
        return value
 
class If(BuildInFunction):
    def __init__(self):
        super(If,self).__init__("If")
    
    def execute(self,env,*unEvalArgTuple):
        condition = LISP.evall(unEvalArgTuple[0],env)
        if condition is new(LispTrue):
            return LISP.evall(unEvalArgTuple[1],env)
        else:
            return LISP.evall(unEvalArgTuple[2],env)

    def execute_ea(self,*evalArg):
        print "halt"
        
class Eq(BuildInFunction):
    def __init__(self):
        super(Eq,self).__init__("Eq?")
        
    def execute(self,env,*unEvalArgs):
        arg1 = LISP.Eval.evall(unEvalArgs[0],env)
        arg2= LISP.Eval.evall(unEvalArgs[1],env)
        if arg1 == arg2:
            return new(LispTrue)
        return new(LispFalse)
    def execute_ea(self,*evalArgs):
        arg1=evalArgs[0]
        arg2=evalArgs[1]
        if arg1 == arg2:
            return new(LispTrue)
        return new(LispFalse)
class Grt(BuildInFunction):
    def __init__(self):
        super(Grt,self).__init__(">?")
        
    def execute(self,env,*unEvalArgs):
        arg1 = LISP.Eval.evall(unEvalArgs[0],env)
        arg2= LISP.Eval.evall(unEvalArgs[1],env)
        if arg1.value > arg2.value:
            return new(LispTrue)
        return new(LispFalse)
    def execute_ea(self,*evalArgs):
        arg1=evalArgs[0]
        arg2=evalArgs[1]
        if arg1.value > arg2.value:
            return new(LispTrue)
        return new(LispFalse)
class Lwt(BuildInFunction):
    def __init__(self):
        super(Lwt,self).__init__("<?")
        
    def execute(self,env,*unEvalArgs):
        arg1 = LISP.Eval.evall(unEvalArgs[0],env)
        arg2= LISP.Eval.evall(unEvalArgs[1],env)
        if arg1.value < arg2.value:
            return new(LispTrue)
        return new(LispFalse)
    def execute_ea(self,*evalArgs):
        arg1=evalArgs[0]
        arg2=evalArgs[1]
        if arg1.value < arg2.value:
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
    def execute_ea(self,*evalArgs):
        arg=None
        for evalArg in evalArgs:
            arg=evalArg
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
    
    def execute_ea(self, *evalArgs):
        body = evalArgs[0].rest
        param = evalArgs[0].first
        if body.rest is not new(LispNull):
            body2 = LispCons(new(LispSymbol,"begin"))
            body2.rest=body
            body=body2
      # param = evalArgs[-2]
        env=evalArgs[-1]
        return UserFunction(param,body,env)
    
class Write(BuildInFunction):
    def __init__(self):
        super(Write,self).__init__("Write")
    def execute(self,env, *unEvalArgs):
        evalArg = LISP.evall(unEvalArgs[0],env)
        print printLisp(evalArg)
        
    def execute_ea(self, *evalArg):
        print evalArg
        
class Print(BuildInFunction):
    def __init__(self):
        super(Print,self).__init__("Print")
    def execute(self,env, *unEvalArgs):
        evalArg = LISP.evall(unEvalArgs[0],env)
        if isinstance(evalArg, LispString):
            print "\"%s\"" % evalArg.value
        else:
            print printLisp(evalArg)
            
    def execute_ea(self, *evalArgs):
        evalArg=evalArgs[0];
        if isinstance(evalArg, str):
            print "\"%s\"" % evalArg
        else:
            print evalArg
            
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
    def execute_ea(self, *evalArg):
        return evalArg[0]
    
class GetParam(BuildInFunction):
    def __init__(self):
        super(GetParam,self).__init__("GetParam")
    def execute(self,env, *args):
        index = args[0].value
        return env.get_parameter_by_index(index)
    
class GetSuperParam(BuildInFunction):
    def __init__(self):
        super(GetSuperParam,self).__init__("GetSuperParam")
    def execute(self,env, *args):
        index = args[0].value
        _env = None
        for x in range(args[1].value):
            _env=env.superEnv
        return _env.get_parameter_by_index(index)
            
class GetLocal(BuildInFunction):
    def __init__(self):
        super(GetLocal,self).__init__("GetLocal")
    def execute(self,env, *args):
        index = args[0].value
        return env.get_local_by_index(index)
    
class GetSuperLocal(BuildInFunction):
    def __init__(self):
        super(GetSuperLocal,self).__init__("GetSuperLocal")
    def execute(self,env, *args):
        index = args[0].value
        _env = None
        for x in range(args[1].value):
            _env=env.superEnv
        return _env.get_local_by_index(index)
            
class GetGlobal(BuildInFunction):
    def __init__(self):
        super(GetGlobal,self).__init__("GetGlobal")
    def execute(self,env, *args):
        index = args[0].value
        return env.get_global_by_index(index)
  
class Eval(BuildInFunction):
    def __init__(self):
        super(Eval,self).__init__("Eval")
    def execute_ea(self,lispSrc,env):
        lisp = LISP.Reader.readLisp(lispSrc.value)
        ret= LISP.Eval.evall(lisp,env)
        return ret
    
class Str_Concat(BuildInFunction):
    def __init__(self):
        super(Str_Concat,self).__init__("Str_Concat")
    def execute(self,env, *unEvalArgs):
        ret =""
        for uarg in unEvalArgs:
            arg = LISP.Eval.evall(uarg,env)
            ret +=arg.value
        return new(LispString,ret)
    
    def execute_ea(self,*args):
        ret =""
        for arg in args:
            ret+=arg.value
        return new(LispString,ret)
    
class Load(BuildInFunction):
    def __init__(self):
        super(Load,self).__init__("Load")
    def execute(self,env, *unEvalArgs):
        file_name = LISP.Eval.evall(unEvalArgs[0],env)
        file = open(file_name.value,'r')
        ret =""
        for line in file:
            ret+=line
        file.close()
        return new(LispString,ret)
    def execute_ea(self,*evalArgs):
        file_name = evalArgs[0]
        file = open(file_name.value,'r')
        ret =""
        for line in file:
            ret+=line
        file.close()
        return new(LispString,ret)
    
class Type(BuildInFunction):
    def __init__(self):
        super(Type,self).__init__("Typ")
    def execute(self,env, *unEvalArgs):
        val = LISP.Eval.evall(unEvalArgs[0],env)
        ret = type(val).__name__
        ret = ret.replace("'","--")
        return new(LispString,ret)
    def execute_ea(self,*evalArgs):
        val = evalArgs[0]
        ret = type(val).__name__
        ret = ret.replace("'","--")
        return new(LispString,ret)
    
class Call(BuildInFunction):
    def __init__(self):
        super(Call,self).__init__("call")
    def execute(self,env, *unEvalArgs):
        pass #duerfte nicht gebraucht werden
    def execute_ea(self,*evalArgs):
        func = evalArgs[0]
        return func.execute_ea(*evalArgs[1:])

    
''' GUI FUNCTIONS '''
    
class LispTK(BuildInFunction):
    def __init__(self):
        super(LispTK,self).__init__("tk$")
    def execute(self,env, *args):
        return LispClasses.LispTKClass()
    
class LispTKLabel(BuildInFunction):
    def __init__(self):
        super(LispTKLabel,self).__init__("label$")
    def execute(self,env, *args):
        root = LISP.evall(args[0],env)
        text = LISP.evall(args[1],env)
        return LispTKLabelClass(root,text)
    
class LispTKText(BuildInFunction):
    def __init__(self):
        super(LispTKText,self).__init__("text$")
    def execute(self,env, *args):
        root = LISP.evall(args[0],env)
        return LispTKTextClass(root)
class LispTKFrame(BuildInFunction):
    def __init__(self):
        super(LispTKFrame,self).__init__("frame$")
    def execute(self,env, *args):
        root = LISP.evall(args[0],env)
        return LispTKFrameClass(root)
class LispTKScrollbar(BuildInFunction):
    def __init__(self):
        super(LispTKScrollbar,self).__init__("scrollbar$")
    def execute(self,env, *args):
        root = LISP.evall(args[0],env)
        return LispTKScrollbarClass(root)
    
class LispTKToplevel(BuildInFunction):
    def __init__(self):
        super(LispTKToplevel,self).__init__("toplevel$")
    def execute(self,env, *args):
        return LispToplevelClass()
    
class LispTKButton(BuildInFunction):
    def __init__(self):
        super(LispTKButton,self).__init__("button$")
    def execute(self,env, *args):
        root = LISP.evall(args[0],env)
        text = LISP.evall(args[1],env)
        command = LISP.evall(args[2],env)
        return LispTKButtonClass(root,text,command,env)
    
    
class LispTKTextClass(BuildInFunction):
    def __init__(self,root):
        super(LispTKTextClass,self).__init__("textClass")
        self.value=Text(root.value, height=24)        
    
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"pack")):
            self.value.pack(expand=YES, fill=BOTH,side="left")
        if(arg == new(LispSymbol,"getText")):
            foo= new(LispString,self.value.get(1.0,END))
            print foo
            return foo
        if(arg == new(LispSymbol,"setText")):
            text = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.delete(0.1,END)
            self.value.insert(0.1, text.value)
        if(arg ==new(LispSymbol,'setBG')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(bg=val.value)
        if(arg ==new(LispSymbol,'setFG')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(fg=val.value)
        if(arg ==new(LispSymbol,'setCursorColor')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(insertbackground=val.value)
        if(arg ==new(LispSymbol,'setScrollbar')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(yscrollcommand=val.value.set)
            
    def execute_ea(self,*evalArgs):
        if(evalArgs[0] ==new(LispSymbol,"pack")):
            self.value.pack(expand=YES, fill=BOTH,side="left")
        if(evalArgs[0] == new(LispSymbol,"getText")):
            foo= new(LispString,self.value.get(1.0,END))
            print foo
            return foo
        if(evalArgs[0]==new(LispSymbol,'setText')):
            self.value.delete(0.1,END)
            self.value.insert(0.1, printLisp(evalArgs[1]))
        if(evalArgs[0]==new(LispSymbol,'setBG')):
            self.value.configure(bg=evalArgs[1])
        if(evalArgs[0]==new(LispSymbol,'setFG')):
            self.value.configure(fg=evalArgs[1])
        if(evalArgs[0]==new(LispSymbol,'setCursorColor')):
            self.value.configure(insertbackground=evalArgs[1])
        if(evalArgs[0] ==new(LispSymbol,'setScrollbar')):
            self.value.configure(yscrollcommand=evalArgs[1].value.set)    
            
            
    def __str__(self):
        return "textClass"
    def __repr__(self):
        return "textClass"
    
    
            
class LispTKButtonClass(BuildInFunction):
    def __init__(self,root,text,command,env):
        self.value=Button(root.value,text=text.value,command=command.execute_ea)
    
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"pack")):
            self.value.pack(side="left")
        if(arg == new(LispSymbol,"setCMD")):
            arg1 = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(command=arg1.execute_ea)
        if(arg ==new(LispSymbol,'setBG')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(bg=val.value)
        if(arg ==new(LispSymbol,'setFG')):
            val = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(fg=val.value)
    def execute_ea(self,*args):
        if(args[0] == new(LispSymbol,"pack")):
            self.value.pack(side="left")
        if(args[0] == new(LispSymbol,"setCMD")):
            self.value.configure(command=args[1].execute_ea)
        if(args[0]==new(LispSymbol,'setBG')):
            self.value.configure(bg=args[1])
        if(args[0]==new(LispSymbol,'setFG')):
            self.value.configure(fg=args[1])
            
            
class LispTKFrameClass(BuildInFunction):
    def __init__(self,root):
        self.value=Frame(root.value)
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"pack")):
            self.value.pack(expand=YES, fill=BOTH)
    def execute_ea(self,*args):
        if(args[0] == new(LispSymbol,"pack")):
            self.value.pack(expand=YES, fill=BOTH)       
            
class LispToplevelClass(BuildInFunction):
    def __init__(self):
        self.value=Toplevel()
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"setTitle")):
            arg1 = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.title(arg1)
    def execute_ea(self,*args):
        if(args[0] == new(LispSymbol,"setTitle")):
            self.value.title(args[0])     
            
class LispTKLabelClass(LispAtom):
    def __init__(self,root,text):
        self.value=Label(root.value,text=text.value)        
    
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"pack")):
            self.value.pack()
            
class LispTKScrollbarClass(LispAtom):
    def __init__(self,root):
        self.value=Scrollbar(root.value)        
    
    def execute(self,env, *unEvalArgs):
        arg = LISP.Eval.evall(unEvalArgs[0], env)
        if(arg == new(LispSymbol,"pack")):
            self.value.pack(side=RIGHT, fill=Y)
        if(arg == new(LispSymbol,"setParent")):
            parent = LISP.Eval.evall(unEvalArgs[1], env)
            self.value.configure(command=parent.value.yview)
            
    def execute_ea(self,*evalArgs):
        arg=evalArgs[0]
        if(arg == new(LispSymbol,"pack")):
            self.value.pack(side=RIGHT, fill=Y)
        if(arg == new(LispSymbol,"setParent")):
            parent = evalArgs[1]
            self.value.configure(command=parent.value.yview)
