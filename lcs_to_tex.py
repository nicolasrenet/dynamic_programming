#!/usr/bin/python3

import sys
import lcs

x =  sys.argv[1] 
y =  sys.argv[2] 

print( lcs.lcs_to_tikz( list(x), list(y) ))
