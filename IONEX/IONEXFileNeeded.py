#!/usr/bin/env python

#------------------------------------------------------------
# This program allows you to know the name of the IONEX file
# you need for a given date.
# @version 1.0
# @author carlos
#
# HOW TO run it:
# $./IONEXFileNeeded 
#------------------------------------------------------------

import datetime

# Reading the date provided
date = raw_input('date of observation?(yyyy-mm-dd): ')
year = int(date.split('-')[0])
month = int(date.split('-')[1])
day = int(date.split('-')[2])

# datetime.datetime.now().timetuple().tm_yday  # gives the day of the current year
# gives the day of the year of any random year
dayofyear = datetime.datetime.strptime(''+str(year)+' '+str(month)+' '+str(day)+'', '%Y %m %d').timetuple().tm_yday

if dayofyear < 10:
	dayofyear = '00'+str(dayofyear)
if dayofyear < 100 and dayofyear >= 10:
	dayofyear = '0'+str(dayofyear)

# Outputing the name of the IONEX file you require
print 'file needed:', 'CODG'+str(dayofyear)+'0.'+str(list(str(year))[2])+''+str(list(str(year))[3])+'I'
