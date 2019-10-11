from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

filename = 'wrfout_d01_0001-01-01_00:00:00'
fh = Dataset(filename,mode='r')

# print(fh.variables.keys())
# print(fh.variables['T'])

t = np.transpose(fh.variables['T'][:])
p = np.transpose(fh.variables['P'][:])
pb = np.transpose(fh.variables['PB'][:])
press = p + pb
temp = (t + 300.)*(press/100000.)**(287.5/1005.)
Temp = temp-273.15

numi = Temp.shape[0]
numj = Temp.shape[1]
numk = Temp.shape[2]
numt = Temp.shape[3]

x=list(range(numt))
y=Temp[0,0,0,:]

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
riables['HGT'][:])