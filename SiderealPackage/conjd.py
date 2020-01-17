#!/usr/bin/env python
#================================================================
# conjd:  Convert Julian date to date and time
#   For documentation, see:
#     http://www.nmt.edu/tcc/help/lang/python/examples/sidereal/ims/
#----------------------------------------------------------------
#================================================================
# Imports
#----------------------------------------------------------------

import sys
from sidereal import *
# - - -   m a i n

def main():
    """conjd main program.
    """

    #-- 1 --
    # [ if  sys.argv[1:] is a single float ->
    #     j  :=  that float
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    argList  =  sys.argv[1:]
    if  len(argList) != 1:
        usage ( "Wrong argument count." )
    else:
        try:
            j  =  float ( argList[0] )
        except ValueError, detail:
            usage ( "Invalid argument: %s" % detail )
    #-- 2 --
    # [ jd  :=  a JulianDate instance for Julian date j ]
    jd  =  JulianDate ( j )

    #-- 3 --
    # [ dt  :=  jd as a datetime.datetime instance ]
    dt  =  jd.datetime()

    #-- 4 --
    # [ sys.stdout  +:=  dt in ISO form ]
    print str(dt)
# - - -   u s a g e

def usage ( *L ):
    """Write a usage message and stop.

      [ L is a list of strings ->
          sys.stderr  +:=  (usage message) + (joined elements of L)
          stop execution ]
    """
    print >>sys.stderr, "*** Usage:"
    print >>sys.stderr, "***   conjd NNNNNNN.NN..."
    print >>sys.stderr, "*** where NNNNNNN.NN is the Julian date."
    print >>sys.stderr, "*** Error: %s" % "".join(L)
    raise SystemExit
#================================================================
# Epilogue
#----------------------------------------------------------------

if __name__ == "__main__":
    main()