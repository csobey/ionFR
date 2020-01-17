#!/usr/bin/env python
#================================================================
# aard: Convert azimuth/altitude to right ascension/declination
#   For documentation, see:
#     http://www.nmt.edu/tcc/help/lang/python/examples/sidereal/ims/
#----------------------------------------------------------------
#================================================================
# Imports
#----------------------------------------------------------------
import sys, re
import sidereal
#================================================================
# Manifest consants
#----------------------------------------------------------------

SIGN_PAT  =  re.compile ( r'[\-+]' )
# - - - - -   m a i n

def main():
    """Main program for aard.
    """

    #-- 1 --
    # [ if sys.argv contains a valid set of command line
    #   arguments ->
    #     altAz  :=  the azimuth and altitude as
    #                a sidereal.AltAz instance
    #     latLon  :=  the observer's location as a
    #                 sidereal.LatLon instance
    #     dt  :=  the observer's date and time as a
    #             datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    altAz, latLon, dt  =  checkArgs()

    #-- 2 --
    # [ if dt has no time zone information ->
    #     utc  :=  dt
    #   else ->
    #     utc  :=  the UTC equivalent to dt ]
    if  ( (dt.tzinfo is None) or
          (dt.utcoffset() is None) ):
        utc  =  dt
    else:
        utc  =  dt - dt.utcoffset()
    #-- 3 --
    # [ sys.stdout  +:=  local sidereal time for dt and latLon ]
    gst  =  sidereal.SiderealTime.fromDatetime ( utc )
    lst  =  gst.lst ( latLon.lon )
    print "Horizon coordinates:", altAz
    print "Observer's location:", latLon
    print "Observer's time:", dt
    print "Local sidereal time is", lst
    #-- 4 --
    # [ raDec  :=  equatorial coordinates of self for local
    #       sidereal time (lst) and location (latLon) ]
    raDec  =  altAz.raDec ( lst, latLon )

    #-- 5 --
    print "Equatorial coordinates:", raDec
# - - -   c h e c k A r g s

def checkArgs():
    """Process all command line arguments.

      [ if sys.argv[1:] is a valid set of command line arguments ->
          return (altAz, latLon, dt) where altAz is a set of
          horizon coordinates as a sidereal.AltAz instance,
          latLon is position as a sidereal.LatLon instance, and
          dt is a datetime.datetime instance
        else ->
          sys.stderr  +:=  error message
          stop execution ]
    """

    #-- 1 --
    # [ if sys.argv[1:] has exactly four elements ->
    #     rawAltAz, rawLat, rawLon, rawDT  :=  those elements
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    argList  =  sys.argv[1:]
    if  len(argList) != 4:
        usage ("Incorrect command line argument count." )
    else:
        rawAltAz, rawLat, rawLon, rawDT  =  argList
    #-- 2 --
    # [ if rawAltAz is a valid set of horizon coordinates ->
    #     altAz  :=  those coordinates as a sidereal.AltAz instance
    altAz  =  checkAltAz ( rawAltAz )

    #-- 3 --
    # [ if rawLat is a valid latitude ->
    #     lat  :=  that latitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lat  =  sidereal.parseLat ( rawLat )
    except SyntaxError, detail:
        usage ( "Invalid latitude: %s" % detail )

    #-- 4 --
    # [ if rawLon is a valid longitude ->
    #     lon  :=  that longitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lon  =  sidereal.parseLon ( rawLon )
    except SyntaxError, detail:
        usage ( "Invalid longitude: %s" % detail )

    #-- 5 --
    # [ if rawDT is a valid date-time string ->
    #     dt  :=  that date-time as a datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        dt  =  sidereal.parseDatetime ( rawDT )
    except SyntaxError, detail:
        usage ( "Invalid timestamp: %s" % detail )

    #-- 6 --
    latLon  =  sidereal.LatLon ( lat, lon )
    return  (altAz, latLon, dt)
# - - -   u s a g e

def usage ( *L ):
    """Print a usage message and stop.

      [ L is a list of strings ->
          sys.stderr  +:=  (usage message) + (elements of L,
                           concatenated)
          stop execution ]
    """
    print >>sys.stderr, "*** Usage:"
    print >>sys.stderr, "***   aard az+alt lat lon datetime"
    print >>sys.stderr, "*** Error: %s" % "".join(L)
    raise SystemExit
# - - -   c h e c k A l t A z

def checkAltAz ( rawAltAz ):
    """Check and convert a pair of horizon coordinates.

      [ rawAltAz is a string ->
          if rawAltAz is a valid set of horizon coordinates ->
            return those coordinates as a sidereal.AltAz instance
          else ->
            sys.stderr  +:=  error message
            stop execution ]
    """
    #-- 1 --
    # [ if rawAltAz contains either a '+' or a '-' ->
    #     m  :=  a re.match instance describing the first matching
    #            character
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    m  =  SIGN_PAT.search ( rawAltAz )
    if  m is None:
        usage ( "Equatorial coordinates must be separated by "
                "'+' or '-'." )
    #-- 2 --
    # [ rawAz  :=  rawAltAz up to the match described by m
    #   sign  :=  characters matched by m
    #   rawAlt  :=  rawAltAz past the match described by m ]
    rawAz  =  rawAltAz[:m.start()]
    sign  =  m.group()
    rawAlt  =  rawAltAz[m.end():]

    #-- 3 --
    # [ if rawAz is a valid angle ->
    #     az  :=  that angle as radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        az  =  sidereal.parseAngle ( rawAz )
    except SyntaxError, detail:
        usage ( "Azimuth '%s' should have the form "
                "'NNNd[NNm[NN.NNNs]]'." % rawAz )

    #-- 4 --
    # [ if rawAlt is a valid angle ->
    #     alt  :=  that angle as radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        absAlt  =  sidereal.parseAngle ( rawAlt )
    except SyntaxError, detail:
        usage ( "Altitude '%s' should have the form "
                "'NNd[NNm[NN.NNNs]]'." % rawAlt )

    #-- 5 --
    if  sign == '-':   alt  =  - absAlt
    else:              alt  =  absAlt

    #-- 6 --
    return  sidereal.AltAz ( alt, az )
#================================================================
# Epilogue
#----------------------------------------------------------------

if  __name__ == "__main__":
    main()