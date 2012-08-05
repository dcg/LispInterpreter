'''
Created on 05.08.2012

@author: dominik
'''
import re
inp ='"fo~"obar"'
inp2 ='"fo"obar"'
inp3 ='"foobar"'
reg='^"([^".]*)"$'
print re.match(reg,inp)
print re.match(reg,inp2)
print re.match(reg,inp3)