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
font={'size':20, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
fn = 2;
coupon = 0.08;
xgrid = np.arange(1, 50);
sensprice = np.zeros(len(xgrid));
for i in range(len(xgrid)):
    bd = bondsensive(xgrid[i], fn, 100, 0.03, 0.4);
    bd.paycoupon( bd.principle * coupon );
    bd.loadQ("./Qdat.dat");
    sensprice[i] = bd.automaticgrad( 0.03 )# / bd.calculateV(0.03);
plt.plot(xgrid, sensprice,'-d')
plt.xlabel("Mature Year")
plt.ylabel("Sensitivity")
plt.show();
