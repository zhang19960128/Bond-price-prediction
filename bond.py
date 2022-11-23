#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:05:09 2022

@author: jiahaozhang
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
font={'size':30, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
class Bond:
    def __init__(self, year, fn, principle, InterestR, Recovery):
        self.year = year; # How many years are there for the payment exist;
        self.fn = fn; # How many times each year pays the Coupon.
        self.principle = principle; # Principle part of the Bond
        self.InterestR = InterestR; # interest Rate in the capital market.
        self.Recovery = Recovery; # Recovery Rate when bond got defaulted.
        self.Paytimes = int( self.year * self.fn ); # How many times it should pay the coupon.
        self.paygrid = np.arange(1, self.Paytimes + 1, 1) / self.fn; # the time grid of payment.

    def update_InterestR(self, r):
        self.InterestR = r;

    def paycoupon(self, AnnualC):
        self.AnnualC = AnnualC;

    def calculateV(self, IR = None):
        if IR is None:
            IR = self.InterestR;
        Qgrid = self.predictQ(self.paygrid);
        term1 = self.principle * np.exp( -1 * IR * self.year) * Qgrid[-1];
        term2 = self.AnnualC / self.fn * np.exp( -1 * IR * self.paygrid ) * Qgrid;
        term2 = np.sum(term2);
        Qi_1 = np.array( [1] + list(Qgrid[0 : (self.Paytimes - 1)] ) );
        term3 = np.exp(-1 * IR * self.paygrid) * (Qi_1 - Qgrid);
        term3 = np.sum(term3) * self.Recovery * self.principle;
        return term1 + term2 + term3;

    def loadQ(self, filename):
        self.Q = np.loadtxt(filename);
        xgrid = self.Q[:, 0];
        ygrid = self.Q[:, 1];
        lnxgrid = xgrid;
        lnygrid = np.log(ygrid);
        length = len(ygrid);
        regx = np.reshape( lnxgrid, (length, 1) );
        regy = np.reshape( lnygrid, (length, 1) );
        self.regQ = LinearRegression(fit_intercept = False).fit(regx, regy);
        self.r_squared = self.regQ.score(regx, regy)

    def predictQ(self, year):
        yearinput = np.array(year).flatten();
        yearinput = np.array(year).reshape((len(yearinput), 1));
        ygrid = self.regQ.predict( yearinput );
        return np.exp( ygrid.flatten() );

    def plotQ(self):
        plt.scatter(self.Q[:, 0], self.Q[:, 1], marker='o', s = 100, label = "Raw data");
        xgrid_p = np.linspace(0, np.max(self.Q[:, 0]), 100);
        ygrid_p = self.predictQ(xgrid_p);
        plt.plot(xgrid_p, ygrid_p, '-r', label = 'Fit')
        plt.legend()
        plt.xlabel("Time (year)")
        plt.ylabel("Prob")
if __name__=='__main__':
    bond1 = Bond(1, 2, 100, 0.03, 0.4);
    bond1.loadQ("./Qdat.dat")
    #bond1.plotQ();
    bond1.paycoupon( bond1.principle * 0.03 );
    re1 = bond1.calculateV();
    print(re1)
    bond5 = Bond(5, 4, 100, 0.03, 0.4);
    bond5.loadQ("./Qdat.dat")
    bond5.paycoupon( bond5.principle * 0.05 );
    re2 = bond5.calculateV();
    print(re2)
    bond5 = Bond(5, 12, 100, 0.03, 0.4);
    bond5.loadQ("./Qdat.dat")
    bond5.paycoupon( bond5.principle * 0.05 );
    re2 = bond5.calculateV();
    print(re2)
