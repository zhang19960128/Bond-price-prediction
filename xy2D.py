#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 10:03:56 2022

@author: jiahaozhang
"""
from bond import Bond
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from sklearn.linear_model import LinearRegression
font={'size':30, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
fn = 2;
xgrid = np.arange(1, 10);
ygrid = np.arange(0, 0.2, 0.01);
X, Y = np.meshgrid(xgrid, ygrid);
shape = np.shape(X);
Vprice = np.zeros(shape);
for x in range(shape[0]):
    for y in range(shape[1]):
        year = X[x, y];
        coupon = Y[x, y];
        bd = Bond(year, fn, 100, 0.03, 0.4);
        bd.paycoupon( bd.principle * coupon );
        bd.loadQ("./Qdat.dat");
        Vprice[x, y] = bd.calculateV();
fig, ax = plt.subplots(constrained_layout=True);
cf = ax.contourf(X, Y, Vprice, cmap = cm.jet, levels = 20)
cs = ax.contour(X, Y, Vprice, levels = 20)
ax.clabel(cs, inline = 1, fontsize = 15, fmt = "%5.1f")
ax.set_xlabel("Years")
ax.set_ylabel("Coupon rate")
fig.colorbar(cf, ax=ax, shrink=0.7)
ax.set_title("Bond price when pay frequency = {0:d}".format(fn))
ax.locator_params(nbins=4)
'''
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Vprice, cmap=cm.coolwarm,linewidth=0, antialiased=False)
'''