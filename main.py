#/bin/python

import sys
from myparser import MyParser
import ply.yacc as yacc

try:
    f = open(sys.argv[1], 'rU')
    print sys.argv[1]
    parser = MyParser()
    p = yacc.parse(f.read())
    
    print p
except EOFError:
    print "Could not open file %s."
