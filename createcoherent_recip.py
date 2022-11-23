import numpy as np
import matplotlib.pyplot as plt
Edata=np.loadtxt("Coherent_efield.dat");
plt.subplot(221)
plt.plot(Edata[:,0],Edata[:,1]);
plt.show();
plt.subplot(222)
length=int(len(Edata[:,0]));
useful=int(length/2);
intensity=np.fft.fft(Edata[:,1]);
freq_grid=np.arange(length)/(length*Edata[1,0]-length*Edata[0,0]);
timegrid=Edata[:,0];
Egrid=np.zeros(len(timegrid),dtype=complex);
intensity[44]=1.414*(intensity[40]+intensity[50]);
intensity[34]=1.414*(intensity[30]+intensity[40]);
for i in range(len(timegrid)):
    for j in range(useful):
        Egrid[i]=Egrid[i]+intensity[j]*np.exp(1j*2*np.pi*timegrid[i]*freq_grid[j]);
    Egrid[i]=Egrid[i]/len(freq_grid);
Egrid=Egrid.real;
plt.plot(timegrid,Egrid.real);
plt.show()
f=open("design_recip.txt",'w');
for i in range(len(timegrid)):
    f.write("{0:20.10f} {1:20.10f}\n".format(timegrid[i],Egrid[i]));
f.close();
plt.subplot(223)
length=int(len(Edata[:,1]));
useful=int s(length/2);
intensity=np.fft.fft(Edata[:,1])[0:useful];
xgrid=np.arange(useful)/(length*(Edata[1,0]-Edata[0,0]));
ygrid=np.abs(intensity)**2;
plt.plot(xgrid,ygrid)
plt.show()
plt.subplot(224)
length=int(len(Edata[:,1]));
useful=int(length/2);
intensity=np.fft.fft(Egrid.real)[0:useful];
xgrid=np.arange(useful)/(length*(Edata[1,0]-Edata[0,0]));
ygrid=np.abs(intensity)**2;
plt.plot(xgrid,ygrid)
plt.show()