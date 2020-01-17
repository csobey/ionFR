#!/usr/bin/env python

#-----------------------------------------------------------
# The following is a wrapper that calls several functions
# written in python (and other languages) in order to estimate 
# the RM produced by the Ionosphere for a given date/time and 
# a line of sight.
# @version 1.0
# @author carlos <sotomayor@astro.rub.de>
# Updates of IGRF and angles by Charlotte Sobey 
# The source transits the sky, changing its coordinates of
# latitude and longitude every sec, min, hr, etc. As a 
# consequence of this the coordinates of the intersection 
# of the line of sight direction with thin Ionospheric shell 
# also changes.
#
# This program calculates the coordinates at the piercing 
# point during 24 hr, one point per every hour.
# Each coordinate is then used to calulate the TEC and B values 
# for every hour. Remember that there should be 25 coordinates,
# each one corresponding to every hour during a day (from 00~24).
#
# NOTE: Actually due to problems with the 'sidereal' package we only
# obtain 24 RM values (from 00~23)
#-----------------------------------------------------------

path='/Users/sob017/Python/ionFR/ionFR-master/'

#-----------------------------------------------------------

import sys
import os
sys.path.append(""+str(path)+"SiderealPackage")
sys.path.append(""+str(path)+"PunctureIonosphereCoord")
sys.path.append(""+str(path)+"IONEX")
import rdalaz
import ippcoor_v1 as ippcoor
import teccalc
import tecrmscalc
import ionheight
from scipy import *

# Defining some variables for further use
TECU = pow(10,16)
TEC2m2 = 0.1*TECU
EarthRadius = 6371000.0 # in meters
Tesla2Gauss = pow(10,4)

# Cheking the arguments are given correctly
argList  =  sys.argv[1:]
if  len(argList) != 5:
	usage ("Incorrect command line argument count.")
else:
	rawRAscencionDeclination, rawLatitude, rawLongitude, rawDTime, nameIONEX  =  argList

# predict the ionospheric RM for every hour within a day 
for h in range(24):
	if h < 10:
		rawtime = str(rawDTime.split('T')[0]+'T0'+str(h)+':00:00')
	else:
		rawtime = str(rawDTime.split('T')[0]+'T'+str(h)+':00:00')
	
	hour = rawtime.split('T')[1].split(':')[0]
	date = rawtime.split('T')[0].split('-')
	year = rawtime.split('T')[0].split('-')[0]
	month = rawtime.split('T')[0].split('-')[1]
	day = rawtime.split('T')[0].split('-')[2]

	# RA and Dec (of the source in degrees) to Alt and Az (radians)
	AzS,AlS,HA,LatO,LonO = rdalaz.alaz(rawtime)
	ZenS = (pi/2.0) - AlS

	# output data only when the altitude of the source is above 0 degrees
	if AlS*(180.0/pi) > 0: 

		# Reading the altitude of the Ionosphere in km (from IONEX file)
		AltIon = ionheight.calcionheight(nameIONEX)
		AltIon = AltIon*1000.0 # km to m

		# Alt and AZ coordinates of the Ionospheric piercing point
		# Lon and Lat distances wrt the location of the antenna are also 
		# calculated (radians)
		offLat,offLon,AzPunct,ZenPunct = ippcoor.PuncIonOffset(LatO,AzS,ZenS,AltIon)
		AlSPunct = (pi/2.0) - ZenPunct

		# Calculation of TEC path value for the indicated 'hour' and therefore 
		# at the IPP
		if rawLatitude[-1] == 's':
			if rawLongitude[-1] == 'e':
				TECarr = teccalc.calcTEC(-(LatO + offLat)*180.0/pi,(LonO + offLon)*180.0/pi,nameIONEX)
			if rawLongitude[-1] == 'w':
				TECarr = teccalc.calcTEC(-(LatO + offLat)*180.0/pi,-(LonO + offLon)*180.0/pi,nameIONEX)
		if rawLatitude[-1] == 'n':
			if rawLongitude[-1] == 'e':
				TECarr = teccalc.calcTEC((LatO + offLat)*180.0/pi,(LonO + offLon)*180.0/pi,nameIONEX)
			if rawLongitude[-1] == 'w':
				TECarr = teccalc.calcTEC((LatO + offLat)*180.0/pi,-(LonO + offLon)*180.0/pi,nameIONEX)
		VTEC = TECarr[int(hour)]
		TECpath = VTEC*TEC2m2/math.cos(ZenPunct) # from vertical TEC to line of sight TEC

		# Calculation of RMS TEC path value (same as the step above)
 		if rawLatitude[-1] == 's':
			if rawLongitude[-1] == 'e':
				RMSTECarr = tecrmscalc.calcRMSTEC(-(LatO + offLat)*180.0/pi,(LonO + offLon)*180.0/pi,nameIONEX)
			if rawLongitude[-1] == 'w':
				RMSTECarr = tecrmscalc.calcRMSTEC(-(LatO + offLat)*180.0/pi,-(LonO + offLon)*180.0/pi,nameIONEX)
		if rawLatitude[-1] == 'n':
			if rawLongitude[-1] == 'e':
				RMSTECarr = tecrmscalc.calcRMSTEC((LatO + offLat)*180.0/pi,(LonO + offLon)*180.0/pi,nameIONEX)
			if rawLongitude[-1] == 'w':
				RMSTECarr = tecrmscalc.calcRMSTEC((LatO + offLat)*180.0/pi,-(LonO + offLon)*180.0/pi,nameIONEX)
		VRMSTEC = RMSTECarr[int(hour)]
		RMSTECpath = VRMSTEC*TEC2m2/math.cos(ZenPunct) # from vertical RMS TEC to line of sight RMS TEC

		# Calculation of the total magnetic field along the line of sight at the IPP
		f = open(''+str(path)+'IGRF/geomag70_linux/input.txt', 'w')
		if rawLatitude[-1] == 's':
			if rawLongitude[-1] == 'e':
				f.write(''+str(year)+','+str(month)+','+str(day)+' C K'+str((EarthRadius+AltIon)/1000.0)+' '+str(-(LatO + offLat)*180.0/pi)+' '+str((LonO + offLon)*180.0/pi)+'')
			if rawLongitude[-1] == 'w':
				f.write(''+str(year)+','+str(month)+','+str(day)+' C K'+str((EarthRadius+AltIon)/1000.0)+' '+str(-(LatO + offLat)*180.0/pi)+' '+str(-(LonO + offLon)*180.0/pi)+'')
		if rawLatitude[-1] == 'n':
			if rawLongitude[-1] == 'e': 
				f.write(''+str(year)+','+str(month)+','+str(day)+' C K'+str((EarthRadius+AltIon)/1000.0)+' '+str((LatO + offLat)*180.0/pi)+' '+str((LonO + offLon)*180.0/pi)+'')
			if rawLongitude[-1] == 'w':
				f.write(''+str(year)+','+str(month)+','+str(day)+' C K'+str((EarthRadius+AltIon)/1000.0)+' '+str((LatO + offLat)*180.0/pi)+' '+str(-(LonO + offLon)*180.0/pi)+'')
		f.close()
		os.system(''+str(path)+'IGRF/geomag70_linux/geomag70.exe '+str(path)+'ionFR_2018/IGRF/geomag70_linux/IGRF12.COF f '+str(path)+'ionFR_2018/IGRF/geomag70_linux/input.txt '+str(path)+'ionFR_2018/IGRF/geomag70_linux/output.txt')
		g = open(''+str(path)+'IGRF/geomag70_linux/output.txt', 'r')
		data = g.readlines()
		g.close()

		Xfield = abs(float(data[1].split()[10]))
		Yfield = abs(float(data[1].split()[11]))
		Zfield = abs(float(data[1].split()[12]))
		Xfield = Xfield*pow(10,-9)*Tesla2Gauss
		Yfield = Yfield*pow(10,-9)*Tesla2Gauss
		Zfield = Zfield*pow(10,-9)*Tesla2Gauss
		Totfield = Zfield*math.cos(ZenPunct) + Yfield*math.sin(ZenPunct)*math.sin(AzPunct) - Xfield*math.sin(ZenPunct)*math.cos(AzPunct)

		# Saving the Ionosheric RM and its corresponding
		# rms value to a file for the given 'hour' value
		IFR = 2.6*pow(10,-17)*Totfield*TECpath
		RMSIFR = 2.6*pow(10,-17)*Totfield*RMSTECpath
		f = open(''+str(os.getcwd())+'/IonRM.txt', 'a')
		f.write(''+str(hour)+' '+str(TECpath)+' '+str(Totfield)+' '+str(IFR)+' '+str(RMSIFR)+'\n')

