'''
Created on 21.04.2012

@author: dominik
'''
from LISP import Reader,Printer,Eval,Enviroment
def start_repl(env):
    input = Input(env)
    while True:
        inp = raw_input(">")
        val = input.add(inp)
        if val != None:
            print Printer.printLisp(val)
    print "foo"
    
    
class Input(object):
    def __init__(self,env):
        self.inp =""
        self.bracket = -1
        self.env=env
        
    def add(self,data):
        for c in data:
            if c == "(":
                if self.bracket == -1:
                    self.bracket=0
                self.bracket+=1
            elif c== ")":
                self.bracket-=1
            self.inp+=c
            if self.bracket==0:
                self.bracket=-1
                tmp_inp=self.inp
                self.inp=""
                return self.eval(tmp_inp,self.env)
        self.inp+="\n"
    def eval(self,inp,env):
        lisp = Reader.readLisp(inp)
        val = Eval.evall(lisp,env)
        return val   