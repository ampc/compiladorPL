#/bin/python

import sys
from myparser import MyParser

try:
    f = open(sys.argv[1], 'rU')
    print sys.argv[1]
    parser = MyParser()
    p = parser.parse(f.read())
    print p
except EOFError:
    print "Could not open file %s."
