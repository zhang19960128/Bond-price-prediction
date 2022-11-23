#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 21:57:10 2022

@author: jiahaozhang
"""
from bond import Bond
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
font={'size':30, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
plt.subplots_adjust(left=0.18, right=0.95, top=0.95, bottom=0.18);
class calibration(Bond):
    def plotr(self):
        xgrid = np.linspace(-0.1, 0.1, 100);
        ygrid = np.zeros(len(xgrid));
        for i in range(len(xgrid)):
            self.update_InterestR(xgrid[i]);
            ygrid[i] = self.calculateV();
        plt.plot(xgrid, ygrid)
        plt.xlabel("Interest Rate")
        plt.ylabel("Market Price")

    def bisect(self, xleft, xright, target, precision):
        self.update_InterestR(xleft);
        dvl = self.calculateV() - target;
        self.update_InterestR(xright);
        dvr = self.calculateV() - target;
        if dvl * dvr > 0:
            print("Bad Initial Guess");
            return np.inf;
        def bi(x1, x2):
            nonlocal target;
            middle = (x1 + x2) / 2;
            if np.abs(x1 - x2) < precision:
                return (x1 + x2) / 2;
            self.update_InterestR(middle);
            dvm = self.calculateV() - target;
            self.update_InterestR(x1);
            dvl = self.calculateV() - target;
            if dvm * dvl < 0:
                return bi(x1, middle);
            else:
                return bi(middle, x2);
        return bi(xleft, xright);
if __name__ == "__main__":
    cal = calibration(1, 2, 100, 0.03, 0.4);
    cal.loadQ("./Qdat.dat");
    cal.paycoupon(3)
    cal.plotr();
    print(cal.bisect(-1, 1, 102, 1e-6))
    plt.plot(np.linspace(-0.1, 0.1, 100),np.linspace(102, 102, 100), '--')
    plt.show()
    '''
    cal = calibration(5, 4, 100, 0.03, 0.4);
    cal.loadQ("./Qdat.dat");
    cal.paycoupon(5)
    cal.plotr();
    print(cal.bisect(-1, 1, 98, 1e-6))
    plt.show()
    '''
