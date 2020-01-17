#!/usr/bin/env python

#-------------------------------------------------------------------
# This function provides de geographic and topographic coordinates
# the Ionospheric piercing point (IPP)
# @version 1.0
# 
#
# Given the azimuth and zenith angle of the line of sight at the 
# location of the antenna, the offsets in geographic coordinates at 
# the intersection of the line of sight with the ionosphere are 
# calculated. Also, the altitude and azimuth corrdinates at the IPP
# are estimated. 
#
# The ionsphere is assumed to approximated by a thin shell at a
# uniform altitude.
#
# Input: 
#	LatObs		latitude of the antenna (radians)
#	AzSou		Azimtuh of the source (radians)
#			from antenna location
#	ZeSou		Zenith of the source (radians)
#			from antenna location
#	AltIon		height of the Ionospheric thin shell
#			(meters)
# Output: 
#	dLat		offset latitude (radians)
#	dLon		offset longitude (radians)
#	AzPunc		Azimuth of the source (radians)
#			from IPP
#	ZenPunc		Zenith of the source (radians)
#			from IPP
#-------------------------------------------------------------------

from scipy import *

def PuncIonOffset(LatObs,AzSou,ZeSou,AltIon):

	RadiusEarth = 6371000.0 # in meters

	if AzSou > pi:
		AzSou -= 2*pi

	# The 2-D sine rule gives the zenith angle at the
	# Ionospheric piercing point
	ZenPunc = math.asin((RadiusEarth*math.sin(ZeSou))/(RadiusEarth + AltIon)) 

	# Use the sum of the internal angles of a triange to determine theta
	theta = ZeSou - ZenPunc

	# The cosine rule for spherical triangles gives us the latitude
	# at the IPP
	lation = math.asin(math.sin(LatObs)*math.cos(theta) + math.cos(LatObs)*math.sin(theta)*math.cos(AzSou)) 
	dLat = lation - LatObs # latitude difference

	# Longitude difference using the 3-D sine rule (or for spherical triangles)
	dLon = math.asin(math.sin(AzSou)*math.sin(theta)/math.cos(lation))
	

	# Azimuth at the IPP using the 3-D sine rule
	sazion = math.sin(AzSou)*math.cos(LatObs)/math.cos(lation)
	AzPunc = math.asin(sazion)

	if AzSou > 0.5*pi:
		AzPunc += 2.*abs(AzPunc-pi/2.)
	elif AzSou < -0.5*pi:
		AzPunc -= 2.*abs((abs(AzPunc)-pi/2.))

	return dLat,dLon,AzPunc,ZenPunc
