#!/usr/bin/env python

#------------------------------------------
# This script reads a IONEX file and retrieves
# the height of the Ionosphere
#------------------------------------------

import numpy

def calcionheight(filename): 

	# opening and reading the IONEX file into memory
	linestring = open(filename, 'r').read()
	LongList = linestring.split('\n')
	################################################

	for i in range(len(LongList)-1):
		if LongList[i].split()[-1] == 'DHGT':
			IonH = float(LongList[i].split()[0])

	return IonH



		
		




