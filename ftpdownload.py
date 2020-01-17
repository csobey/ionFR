#!/usr/bin/env python
'''
Script to download publicly available TEC maps
usage:
python ftpdownload.py -d yyyy-mm-dd [-t type]
-d gives date of observation
-t gives type of ionex file (codg,upcg,igsg) codg maps are default option

v0.1 Charlotte Sobey 2013 
'''

import ftplib
import datetime
import optparse as op

p=op.OptionParser()
p.add_option('--date','-d',default='NONE',type='string',help='Date (yyyy-mm-dd)')
p.add_option('--type','-t',default='codg',type='string',help='Type of ionex file (codg,upcg,igsg) [codg default]')
ops,args=p.parse_args()

# Reading the date provided
#date = raw_input('date of observation?(yyyy-mm-dd): ')
#filetype = raw_input('Type of ionex file?(codg,upcg,igsg): ')
year = int(ops.date.split('-')[0])
month = int(ops.date.split('-')[1])
day = int(ops.date.split('-')[2])

dayofyear = datetime.datetime.strptime(''+str(year)+' '+str(month)+' '+str(day)+'', '%Y %m %d').timetuple().tm_yday

if dayofyear < 10:
        dayofyear = '00'+str(dayofyear)
if dayofyear < 100 and dayofyear >= 10:
        dayofyear = '0'+str(dayofyear)

# Outputing the name of the IONEX file you require
file = str(ops.type)+str(dayofyear)+'0.'+str(list(str(year))[2])+str(list(str(year))[3])+'i.Z'
print 'FILE:', file
directory = '/pub/gps/products/ionex/'+str(year)+'/'+str(dayofyear)+'/'
print 'DIR:', directory

def download(ftp,directory,file):
    ftp.cwd(directory)
    f = open(file,"wb")
    ftp.retrbinary("RETR " + file,f.write)
    f.close()
    
ftp = ftplib.FTP("cddis.gsfc.nasa.gov")
ftp.login("anonymous", "anonymous")

# Download appropriate file via ftp
download(ftp, directory, file)

print 'done'
