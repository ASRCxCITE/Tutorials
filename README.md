# Tutorials
## Reading NetCDF with Python
Network Common Data Form (NetCDF) is a set of interfaces for array-oriented data access and a freely distributed collection of data access libraries for C, Fortran, C++, Java, and other languages. The netCDF libraries support a machine-independent format for representing scientific data. Together, the interfaces, libraries, and format support the creation, access, and sharing of scientific data.  More information on NetCDF can be found [here](https://www.unidata.ucar.edu/software/netcdf/).

This tutorial will provide the basics with reading weather data, which is formatted as NetCDF. The data comes from the Weather Research and Forecasting (WRF) Model.

>We will being using Python 3 via Anaconda

Open your favorite text editor for Python, and create a new python file, e.g., netcdf.py
Import the netCDF4 library into your python script.

```
from netCDF4 import Dataset          #import dataset library from netCDF pkg
```
Let's make sure that this works so far. Execute the script in your terminal:

```
$python netcdf.py
```
Oh wait, the library does not exist?? Let's install it! While there are some hefty instructions for [installation](https://unidata.github.io/netcdf4-python/netCDF4/index.html), we will use a lovely package manager called [conda](https://anaconda.org/anaconda/netcdf4), which does all the work for us:
```
$conda install -c anaconda netcdf4
```
Now try to run the script again. The errors should be gone (hopefully!) and nothing printed to the terminal, since we have not coded anything yet!

Now, let's open the file that we want to read.  Download the file [here](https://drive.google.com/file/d/1RwpuNtBKxo1-yLsjfpt0W0KMSd9-trlR/view?usp=sharing). Untar and unzip it:
```
$gunzip wrfout2.tar.gz
$tar -xvf wrfout2.tar
```
Out should come
```
wrfout_d01_0001-01-01_00:00:00
```
IMPORTANT: This file is almost 4GB large. Therefore, if you try to push this to GitHub, you will be stopped and then end up falling down a "large file" rabbit hole from which it is very difficult to emerge!  Thus, either save this file to a directory OUTSIDE of your github repository (and just include the path in the python script), OR you can add this filename to your ```.gitignore``` so that it is never added to you repository, but you may still use it locally.

This is a NetCDF formatted file with output generated from WRF (wrfout), for domain 1 (d01), at 00:00:00 UTC on January (01) 1 (01), 0001. Yes, these date and time are ridiculous. This is just an "idealized" case study that I ran in WRF -- in other words, I was only simulating a specific Atmospheric phenomenon, and not simulating weather that has actually happened. Running idealized cases are a common way to test new code to ensure proper functionality. You do not need to worry about this. Just know how to parse the file name, as you will come across this again. If you have NetCDF linux commands installed on your computer (sometimes automatically installed, sometimes not), you can view the contents of the file via command line: ``` ncdump wrfout_d01_0001-01-01_00:00:00 ```.

Now, add the next line of code to your script to read the filename, and open it.
```
filename = 'wrfout_d01_0001-01-01_00:00:00'  #assign vaarible filename to the file name!
fh = Dataset(filename,mode='r')              #use the NetCDF library (which we called Dataset) to store the data from filename into fh
```
The file has now been opened and stored in fh in read ('r') mode. Let's see what variables exist in the file.
```
print(fh.variables.keys())
```
and then run the code.  This will print out all the variable names. Printing just ```print(fh.variables)``` provides even more information. Let's print out that information to see what we are dealing with.

Now that we have an idea of the variables that exist, let's store some so that we can use them later. Let's start with time. How would we read that?  Well, as you can see above, I was able to access ALL the variables as an object of the file, fh, and the variable names could be specified as keys.  This means that 'variables' is a dictionary object of fh. We can access specific dictionary attributes by specifying the key, and then indicating how much of that value (in the key,value pair) we want. We want it all.

So, which variable do we want? Eventually, we will want a lot, but for now we will just get one. Let's start with a basic weather variable: Temperature, T.
```
t = numpy.transpose(fh.variables['T'][:])
```
Okay. Temperature is read in and store in "t". Run that script again. Any issues?  Probably.  Maybe we're missing numpy? Import it! 
```
import numpy
```
Now, what do we do with it? Let's plot it!

First, I know I said let's start with the basics. Unfortunately, it gets more complicated starting NOW. Temperature actually is not a variable output in WRF, so what did we just read in? Print out the information of T to see!
```
print(fh.variables['T'])
```
Answer: perturbation potential temperature. I won't make you understand this variable, I will just show you how to convert it to temperature! You're welcome. Add the next lines of code:
```
p = numpy.transpose(fh.variables['P'][:])
pb = numpy.transpose(fh.variables['PB'][:])
press = p + pb
temp = (t + 300.)*(press/100000.)**(287.5/1005.)
```
Now we have temperature. But wait, what are the units? Check the 'T' information again... Kelvin! Kelvin is great for calculations, but not great for really conceptualizing. Let's convert to Celsius:
```
Temp = temp-273.15
```
Now we have temperature in ºC. Add ```print(Temp)``` and run your program to make sure we are free of errors and we have some numbers!

To plot, we now have our variable we want to visualize, but on what axes? We can determine this by checking the dimensions (coordinates) of the variable we want to plot. Once again, print the 'T' information.

The coordinates for temperature are XLONG, XLAT, and XTIME, or longitude, latitude, and time. There is actually a fourth dimension as well: height. This means that temperature is a 4-dimensional variable (x,y,z,t), but let's just start with one dimension, time. Reading in the time variable is a tad complicated, so we will skip that for now. Instead, we will just plot relative to time-step. How many time steps are there? Let's store that value. Actually, let's just store all 4 for future use.
```
numi = Temp.shape[0]
numj = Temp.shape[1]
numk = Temp.shape[2]
numt = Temp.shape[3]
```
Shape is a method that you can call for a multi-dimensional array that tells you the size of all the dimensions (```print(Temp.shape)``` to see all 4). We want to store the length of each dimension in its own separate variable, so we access the 0th, 1st, 2nd, and 3rd dimensions, respectively.

Now that we have stored the length of the time dimension, we have a variable that tells us how many time steps there are! Let's plot!
```
x=list(range(numt))
y=Temp[0,0,0,:]

plt.plot(x,y)
plt.show()
```
What a beautiful line! Kind of boring, though.  Let's make something fancier.  How about a cross-section (x-z view) at one point in time? (Be sure to comment out those last two lines that you just added above)
```
# plt.plot(x,y)
# plt.show()

xx = np.zeros((numi,numj,numk,numt))
yy = np.zeros((numi,numj,numk,numt))
for i in range(numi):
    xx[i,:,:,:] = i
for k in range(numk):
    yy[:,:,k,:] = k

x=xx[:,0,:,1]
y=yy[:,0,:,1]
z=Temp[:,0,:,1]

plt.contourf(x,y,z)
plt.colorbar()
plt.show()
```
Let's try one more. A cloud!
```
# plt.contourf(x,y,z)
# plt.colorbar()
# plt.show()

qi = np.transpose(fh.variables['QICE'][:])
z=qi[:,0,:,1]

import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
gs = gridspec.GridSpec(1,2,width_ratios=[15,1],hspace=0.25,wspace=0.25)

ax = plt.subplot(gs[0])
logmin = -8
logmax = 2
it = 40
n_levels = logmax - logmin
C = ax.contourf(x,y,z,norm=LogNorm(),levels=np.logspace(logmin,logmax,it))

ax1 = plt.subplot(gs[1])
cblvls = np.linspace(10**logmin,10**(logmin+1),it)

for E in range(1,n_levels):
    cblvls = np.concatenate((cblvls[:-1],np.linspace(10**(logmin+E),10**(logmin+E+1),it)))
XC = [np.zeros(len(cblvls)),np.ones(len(cblvls))]
YC = [cblvls,cblvls]
CM = ax1.contourf(XC,YC,YC,levels=cblvls,norm=LogNorm())
ax1.set_yscale('log')

plt.show()
```
This is just the tip of the iceberg with the things we can do with NetCDF weather variables and Python, but it is a good place to start!





