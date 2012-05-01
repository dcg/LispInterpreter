import cProfile
import pstats
import time
from LISP.Eval import evall
from LISP.Reader import readLisp
from LISP import Enviroment
env = Enviroment();

def testPlus():
    lisp = readLisp("(+ 5 4)")
    for i in range(10000):
        val = evall(lisp,env)

def testDefine():
    lisp = readLisp("(define (foo x) (+ x 3 4))")
    for i in range(10000):
        evall(lisp,env)
        
lisp = readLisp("(define (foo x) (+ x 3 4))")
evall(lisp,env)
def testSomefunction():
    lisp=readLisp("(foo 5)")
    for i in range(1):
        evall(lisp,env)
        
lisp = readLisp("(define (loop n) (if (eq? n 1) 1 (loop (- n 1))))")
evall(lisp, env)
print "start"
def testLoop():
    lisp = readLisp("(loop 100)")
    for i in range(1000):
#    for i in range(1):
        evall(lisp,env)
def val1():    
    print ("plus")
    t1=time.clock()    
    cProfile.run("testPlus()","perf_plus")
    t2=time.clock()    
    p = pstats.Stats('perf_plus')
    p.strip_dirs()
    p.sort_stats("time")
    p.print_stats(20)

    print "time:" +str(t1+t2)
    
def val2():    
    print "Define"
    t1=time.clock()    
    cProfile.run("testDefine()","perf_define")
    t2=time.clock()    
    p = pstats.Stats('perf_define')
    p.strip_dirs()
    p.sort_stats("time")
    p.print_stats(20)
    print "time:" +str(t1+t2)

def val3():    
    print "loop"
    t1=time.clock()    
    cProfile.run("testLoop()","perf_loop")
    t2=time.clock()    
    p = pstats.Stats('perf_loop')
    p.strip_dirs()
    p.sort_stats("time")
    p.print_stats(20)
    print "time:" +str(t1+t2)
    
def val4():    
    print "func"
    t1=time.clock()    
    cProfile.run("testSomefunction()","perf_func")
    t2=time.clock()    
    p = pstats.Stats('perf_func')
    p.strip_dirs()
    p.sort_stats("time")
    p.print_stats(20)
    print "time:" +str(t1+t2)

val1() 
val2()
val3()
#val4()