'''
Created on 21.04.2012

@author: dominik
'''
from IDE import repl
def read(file,env):
    input = repl.Input(env)
    for line in file:
        line = line.replace("\n\n","\n")
        print line
        input.add(line)