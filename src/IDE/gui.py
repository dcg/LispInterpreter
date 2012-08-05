'''
Created on 04.08.2012

@author: dominik
'''
from Tkinter import *


def foo():
    print t_input.configure(bg="RED")
    b_eval.configure(command=foo2)
def foo2():
    print t_input.configure(bg="GREEN")
    b_eval.configure(command=foo)

root = Tk()
w = Label(root, text="Hello, world")
w.pack()
t_input = Text(root)
t_input.pack(expand=YES, fill=BOTH)
b_eval =Button(root,text="Eval", bg="green", command=foo)
b_eval.pack(side="left",padx=20)
'''
frame = Frame(root)
b_bc =Button(frame,text="eval function and show bytecode")
b_bc.pack(side="left",padx=20)
b_optcode =Button(frame, text="eval function and show opt-code")
b_optcode.pack(side="left",padx=20)
frame.pack()
repl = Text(root)
repl.pack(expand=YES, fill=BOTH)
'''
root.mainloop()
w.configure(text="foo")

'''
(set! root (tk$))
(set! w (label$ root, "Hallo Welt"))
(w 'pack)
(root 'mainloop)


'''