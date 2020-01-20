#!/usr/bin/env python

# Slight modified version of rdaa.py
#================================================================
# rdaa: Convert right ascension/declination to azimuth/altitude
#   For documentation, see:
#     http://www.nmt.edu/tcc/help/lang/python/examples/sidereal/ims/
#----------------------------------------------------------------
#================================================================
# Imports
#----------------------------------------------------------------
from __future__ import print_function

import sys, re
import sidereal
from math import *
#================================================================
# Manifest consants
#----------------------------------------------------------------

SIGN_PAT  =  re.compile ( r'[\-+]' )
# - - - - -   m a i n

def alaz(tim):
    """Main program for rdaa.
    """

    #-- 1 --
    # [ if sys.argv contains a valid set of command line
    #   arguments ->
    #     raDec  :=  the right ascension and declination as
    #                a sidereal.RADec instance
    #     latLon  :=  the observer's location as a
    #                 sidereal.LatLon instance
    #     dt  :=  the observer's date and time as a
    #             datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    raDec, latLon, dt  =  checkArgs(tim)
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
    #############print "Equatorial coordinates:", raDec
    #############print "Observer's location:", latLon
    #############print "Observer's time:", dt
    #############print "Local sidereal time is", lst
    #-- 4 --
    # [ h  :=  hour angle for raDec at time (utc) and longitude
    #          (latLon.lon) ]
    h  =  raDec.hourAngle ( utc, latLon.lon )

    #############print "Hour Angle:", h*180.0/pi,"d"

    #-- 5 --
    # [ aa  :=  horizon coordinates of raDec at hour angle h
    #           as a sidereal.AltAz instance ]
    aa  =  raDec.altAz ( h, latLon.lat )

    #-- 6 --
    #############print "Horizon coordinates:", aa
# - - -   c h e c k A r g s

    # changing latitude of the observer in degrees to radians
    latdeg = latLon.__str__().split()[0].split('d')[0].split('[')[1]
    latmin = latLon.__str__().split()[1].split("'")[0]
    latsec = latLon.__str__().split()[2].split('"')[0]
    latdegrees = float(latdeg) + float(latmin)/60.0 + float(latsec)/3600.0
    latradians = latdegrees*pi/180.0
    # changing longitude of the observer in degrees to radians
    londeg = latLon.__str__().split()[5].split('d')[0]
    lonmin = latLon.__str__().split()[6].split("'")[0]
    lonsec = latLon.__str__().split()[7].split('"')[0]
    londegrees = float(londeg) + float(lonmin)/60.0 + float(lonsec)/3600.0
    lonradians = londegrees*pi/180.0
    # changing azimuth  of the source in degrees to radians
    azdeg = aa.__str__().split()[1].split('d')[0]
    azmin = aa.__str__().split()[2].split("'")[0]
    azsec = aa.__str__().split()[3].split('"')[0]
    azdegrees = float(azdeg) + float(azmin)/60.0 + float(azsec)/3600.0
    azradians = azdegrees*pi/180.0	
    # changing elevation or altitude of the source in degrees to radians
    aldeg = aa.__str__().split()[5].split('d')[0]
    almin = aa.__str__().split()[6].split("'")[0]
    alsec = aa.__str__().split()[7].split('"')[0]
    aldegrees = float(aldeg) + float(almin)/60.0 + float(alsec)/3600.0
    alradians = aldegrees*pi/180.0

    # all the values are returned in radians!
    return azradians, alradians, h, latradians, lonradians


def checkArgs(ti):
    """Process all command line arguments.

      [ if sys.argv[1:] is a valid set of command line arguments ->
          return (raDec, latLon, dt) where raDec is a set of
          celestial coordinates as a sidereal.RADec instance,
          latLon is position as a sidereal.LatLon instance, and
          dt is a datetime.datetime instance
        else ->
          sys.stderr  +:=  error message
          stop execution ]
    """
    #-- 1 --
    # [ if sys.argv[1:] has exactly four elements ->
    #     rawRADec, rawLat, rawLon, rawDT  :=  those elements
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    argList  =  sys.argv[1:]
    if  len(argList) != 5:
        usage ("Incorrect command line argument count." )
    else:
        rawRADec, rawLat, rawLon, rawDT, fileIONEXTEC  =  argList
        rawDT = str(ti)
	
    #-- 2 --
    # [ if rawRADec is a valid set of equatorial coordinates ->
    #     raDec  :=  those coordinates as a sidereal.RADec instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    raDec  =  checkRADec ( rawRADec )

    #-- 3 --
    # [ if rawLat is a valid latitude ->
    #     lat  :=  that latitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lat  =  sidereal.parseLat ( rawLat )
    except SyntaxError as detail:
        usage ( "Invalid latitude: %s" % detail )

    #-- 4 --
    # [ if rawLon is a valid longitude ->
    #     lon  :=  that longitude in radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        lon  =  sidereal.parseLon ( rawLon )
    except SyntaxError as detail:
        usage ( "Invalid longitude: %s" % detail )

    #-- 5 --
    # [ if rawDT is a valid date-time string ->
    #     dt  :=  that date-time as a datetime.datetime instance
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        dt  =  sidereal.parseDatetime ( rawDT )
    except SyntaxError as detail:
        usage ( "Invalid timestamp: %s" % detail )

    #-- 6 --
    latLon  =  sidereal.LatLon ( lat, lon )
    return  (raDec, latLon, dt)
# - - -   u s a g e

def usage ( *L ):
    """Print a usage message and stop.

      [ L is a list of strings ->
          sys.stderr  +:=  (usage message) + (elements of L,
                           concatenated)
          stop execution ]
    """
    print("*** Usage:", file=sys.stderr)
    print("***   rdaa RA+dec lat lon datetime", file=sys.stderr)
    print("*** Or:", file=sys.stderr)
    print("***   rdaa RA-dec lat lon datetime", file=sys.stderr)
    print("*** Error: %s" % "".join(L), file=sys.stderr)
    raise SystemExit
# - - -   c h e c k R A D e c

def checkRADec ( rawRADec ):
    """Check and convert a pair of equatorial coordinates.

      [ rawRADec is a string ->
          if rawRADec is a valid set of equatorial coordinates ->
            return those coordinates as a sidereal.RADec instance
          else ->
            sys.stderr  +:=  error message
            stop execution ]
    """
    #-- 1 --
    # [ if rawRADec contains either a '+' or a '-' ->
    #     m  :=  a re.match instance describing the first matching
    #            character
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    m  =  SIGN_PAT.search ( rawRADec )
    if  m is None:
        usage ( "Equatorial coordinates must be separated by "
                "'+' or '-'." )
    #-- 2 --
    # [ rawRA  :=  rawRADec up to the match described by m
    #   sign  :=  characters matched by m
    #   rawDec  :=  rawRADec past the match described by m ]
    rawRA  =  rawRADec[:m.start()]
    sign  =  m.group()
    rawDec  =  rawRADec[m.end():]
    #-- 3 --
    # [ if rawRA is a valid hours expression ->
    #     ra  :=  rawRA as radians
    #   else ->
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        raHours  =  sidereal.parseHours ( rawRA )
        ra  =  sidereal.hoursToRadians ( raHours )
    except SyntaxError as detail:
        usage ( "Right ascension '%s' should have the form "
                "'NNh[NNm[NN.NNNs]]'." % rawRA )
    #-- 4 --
    # [ if rawDec is a valid angle expression ->
    #     absDec  :=  that angle in radians
    #     sys.stderr  +:=  error message
    #     stop execution ]
    try:
        absDec  =  sidereal.parseAngle ( rawDec )
    except SyntaxError as detail:
        usage ( "Right ascension '%s' should have the form "
                "'NNd[NNm[NN.NNNs]]'." % rawDec )
    #-- 5 --
    if  sign == '-':   dec  =  - absDec
    else:              dec  =  absDec

    #-- 6 --
    return sidereal.RADec ( ra, dec )
#================================================================
# Epilogue
#----------------------------------------------------------------

if  __name__ == "__main__":
    main()
