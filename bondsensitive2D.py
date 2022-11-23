#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 12:39:26 2022

@author: jiahaozhang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 10:03:56 2022

@author: jiahaozhang
"""
from bondsensitive import bondsensive
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from sklearn.linear_model import LinearRegression
font={'size':30, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
fn = 2;
xgrid = np.arange(1, 30);
ygrid = np.arange(0, 0.2, 0.01);
X, Y = np.meshgrid(xgrid, ygrid);
shape = np.shape(X);
Vprice = np.zeros(shape);
for x in range(shape[0]):
    for y in range(shape[1]):
        year = X[x, y];
        coupon = Y[x, y];
        bd = bondsensive(year, fn, 100, 0.03, 0.4);
        bd.paycoupon( bd.principle * coupon );
        bd.loadQ("./Qdat.dat");
        Vprice[x, y] = bd.automaticgrad( 0.03 );
fig, ax = plt.subplots(constrained_layout=True);
cf = ax.contourf(X, Y, Vprice, cmap = cm.jet, levels = 15)
cs = ax.contour(X, Y, Vprice, levels = 15)
ax.clabel(cs, inline = 1, fontsize = 15, fmt = "%5.1f")
ax.set_xlabel("Years")
ax.set_ylabel("Coupon rate")
fig.colorbar(cf, ax=ax, shrink=0.7)
ax.set_title("Bond sensitivity when pay frequency = {0:d}".format(fn))
ax.locator_params(nbins=4)
plt.show();
