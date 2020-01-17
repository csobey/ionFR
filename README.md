# ionFR
A code that allows you to predict the ionospheric Faraday rotation for a specific line-of-sight, geographic location, and epoch

# Introduction
ionFR is a software package that provides an estimate the ionospheric Faraday rotation along a given line-of-sight (LOS) at a specific geographic location. 
The software uses the International Geomagnetic Reference Field (IGRF12; available at https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html) and global ionospheric maps given in the IONosphere map EXchange format (IONEX) that provide global TEC values (available at ftp://cddis.nasa.gov/pub/gps/products/ionex/). 

ionFR has been written almost entirely in Python. This software package has been proven to work well under the Ubuntu operating system.

Users are encouraged to report bugs or flaws. Suggestions or comments that the users think will improve this code are also welcomed.

# Installation
You will need the following modules from python intalled in your machine:
- numpy
- scipy
You also need the gcc compiler

The following are a few steps to get this code working:

0) extract and open the ionFR/ folder

1) open the file 'ionFRM.py' and modify the variable 'path' in the first line to <your_path> (the location of the directory on your machine).
   Example: /home/carlos/Documents/

2) compile and create an executable of the software that has version 12 of the IGRF. Go to <your_path>/ionFR/IGRF/geomag70_linux/
   and type the following:
   
   <code>gcc -lm geomag70.c -o geomag70.exe</code>

3) add to your PATH variable in your .bashrc or profile file the following:
<code> export PATH=$PATH:<your_path>/ionFR </code>

4) make the ionFRM.py script located in <your_path>/ionFR executable:
   <code>chmod +x ionFRM.py </code>

5) That's it! Have fun :-)

# Getting started and testing the code
One you have installed ionFR in your computer, you will be able to run it from the terminal.

To test the package, open a terminal and copy the IONEX file codg2930.11i in the directory ionFR/test, to your current working directory. Then, execute the following command:

<code>ionFRM.py 08h37m05.6s+06d10m14.5s 52d54m54.6sn 6d52m11.7se 2011-10-20T00:00:00 codg2930.11i</code>

ionFR should produce a text file, IonRM.txt, which will contain ionospheric Faraday rotation values and uncertainties along the given LOS in steps of 1 hour during an entire day. For more on the outputs see "ionFR output" below.

# Input arguments
<code> ionFRM.py Source_RA±DEC Telescope_Latitude Telescope_Longitude Date Ionex_file </code>

- Source_RA±DEC (string)
Right Ascencion and Declination for a given LOS. 
Examples: 16h50m04.0s+79d11m25.0s (positive dec.); 16h50m04.0s-79d11m25.0s (negative dec.)

- Telescope_Latitude (string)
Latitude of the location where a given LOS is being observed. 
Examples: 52d54m54.64sn (lat. north); 52d54m54.64ss (lat. south)

- Telescope_Longitude (string)
Longitude of the location where a given LOS is being observed. 
Examples: 6d52m11.7se (lon. east); 6d52m11.7sw (lon. west)

- Date (string)
Date when you want to predict the Ionospheric Faraday rotation in format YYYY-MM-DDT00:00:00. 
Examples: 2004-05-19T00:00:00; 2011-10-20T00:00:00

- IONEX_file (string)
Name of the IONEX file needed. Note: the IONEX file should be from the same date specified above. 
Example: codg2930.11i; igsg1130.19i

The python script ftpdownload.py allows you to download the correct IONEX file from the website.

<code> ftpdownload.py -d DATE (format YYYY-MM-DD) -t IONEX_file_type (string e.g. igsg, codg, etc.) </code>

Example: <code> ftpdownload.py -d 2011-10-20 -t codg </code>

The IONEX files are downloaded as compressed .Z files. These can be unpacked using e.g. gunzip or other suitable command.
Note that ionFR is compatible with IONEX files with 2-hr time resolution.
CODE IONEX files (codg) have changed format and will not be immediately compatible with ionFR after ~2014.

# ionFR Output
A file called IonRM.txt will be created in the folder where you ran the test. This file contains
five columns:

1) Hour of the day in Universal Time (UT)
2) TEC along the LOS
3) Geomagnetic field along the LOS
4) Ionospheric Faraday rotation along the LOS
5) Uncertainties Ionospheric Faraday rotation values in column 4.

ionFR will produce values only for source elevations higher than 0 degrees.

An example python plot showing the output is included as test/plot_ionFR_output.png.
A juypiter notebook used to create this plot is included as test/plot_ionFR_output.ipynb

For more information about the code, we refer you to:
Sotomayor-Beltran et al. 2013, Astronomy & Astrophysics, Volume 552, id.A58
https://ui.adsabs.harvard.edu/abs/2013A%26A...552A..58S
https://ui.adsabs.harvard.edu/abs/2015A%26A...581C...4S
