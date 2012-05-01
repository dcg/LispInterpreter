'''
Created on 21.04.2012

@author: dominik
'''
from IDE import repl
def read(file,env):
    input = repl.Input(env)
    for line in file:
     #   print line
        input.add(line)