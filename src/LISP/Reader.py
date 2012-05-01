import re
from LISP.LispClasses import LispInteger, LispSymbol, LispCons, LispNull, LispAtom, new,\
    LispString
 
null = new(LispNull)  
   
def findClosingBracket(inp, index):
    _open = 0;
    for i in range(index,len(inp)):
        if inp[i]=='(':
            _open=_open+1
        elif inp[i]==')':
            if _open == 1:
                return i
            else:
                _open=_open-1
   
def _splitCommands(inp):   
    cmds = [];
    cmd =""
    i=0
    string_mode = False
    while(i <len(inp)):
        if string_mode:
            if inp[i] == "'" or inp[i] == '"':
                string_mode = False
                cmd+=inp[i]
                cmds.append(cmd)
                cmd = ""
            else:
                cmd+=inp[i]
        elif inp[i] == '(':
            closingBracket = findClosingBracket(inp, i);
            cmds.append(inp[i:closingBracket+1])
            i=closingBracket+1
        elif inp[i] == "'" or inp[i] == '"':
            cmd+=inp[i]
            string_mode=True
        elif not inp[i].isspace():
            cmd+=inp[i]
        else:
            if cmd != "":
                cmds.append(cmd)
            cmd = ""
        i+=1
    if len(cmd)>0:
        cmds.append(cmd)
    return cmds

def _readListContent(inp):
    inp = inp.strip()
    if isQuote(inp):
        return _readLisp("(quote "+inp[1:len(inp)]+")")
    if isZahl(inp):
        return new(LispInteger,inp)
    if isString(inp):
        return new(LispString,inp[1:len(inp)-1])
    if isSymbol(inp):
        return new(LispSymbol,inp)
    else:
        cmds = _splitCommands(inp)
        last = None;
        first = None;
        for cmd in cmds:
            element = _readLisp(cmd)
            cons = new(LispCons,element)
            if last:
                last.rest=cons
            else:
                first = cons
            last=cons     
        return first;
    
def _readLisp(inp):
  #  print inp
    inp = inp.strip()
    if inp[0] == '(':
        lastBracket = findClosingBracket(inp,0)
        if lastBracket+1 >= len(inp):
            content= _readListContent(inp[1:lastBracket])
            if isinstance(content,LispAtom):
                    content = new(LispCons,content)
            return content;
     #   else:
     #      return LispCons(_readLisp(inp[1:lastBracket]), _readLisp(inp[lastBracket+1:len(inp)]) )
    else:
        return _readListContent(inp)
    
def readLisp(inp):
    return _readLisp(inp)


def isString(inp):
    if re.match("^'[^'.]*'$",inp) != None:
        return True
    if re.match('^"[^".]*"$',inp)!= None:
        return True
def isZahl(inp):
  #  print inp
    return re.match("[0-9]+$", inp) != None
           
def isSymbol(inp):
  #  print inp
    return  re.search("[(,), ,\n,\t,\\.]+", inp) == None
def isQuote(inp):
    return re.match("^'.*",inp) != None          


