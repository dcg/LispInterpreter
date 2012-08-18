'''
Created on 21.04.2012

@author: dominik
'''
import IDE.repl 
import IDE.file
from optparse import OptionParser
from LISP import Enviroment
if __name__ == '__main__':
    env = Enviroment()
    parser = OptionParser()
    parser.add_option("-f","--file", dest="filename", help="The Lisp file", action="append", metavar="FILE")
    (options, args) = parser.parse_args()
    print type(options)
    files = options.filename
    if(files ==None):
        files=["IDE/startGui.lsp"]
    if files != None:
        for file in files:
            f = open(file,'r')
            IDE.file.read(f,env)
    IDE.repl.start_repl(env)