#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 11:22:50 2022

@author: jiahaozhang
"""
import matplotlib.pyplot as plt
import matplotlib
from bond import Bond
from sklearn.linear_model import LinearRegression
import autograd.numpy as np
from autograd import grad
from autograd import elementwise_grad as egrad
font={'size':30, 'family':'Times New Roman'};
plt.rcParams['figure.figsize']=(10, 8);
matplotlib.rc('font', **font);
class bondsensive(Bond):
    def fivestencil(self, x, h= 0.0001):
        fx_2h = self.calculateV(x - 2*h);
        fx_h = self.calculateV(x - h);
        fxph = self.calculateV(x + h);
        fxp2h = self.calculateV(x + 2*h);
        return (-1*fxp2h + 8 * fxph - 8 * fx_h + fx_2h) / 12 / h;

    def calculateV(self, IR):
        Qgrid = self.predictQ(self.paygrid);
        term1 = self.principle * np.exp( -1 * IR * self.year) * Qgrid[-1];
        term2 = self.AnnualC / self.fn * np.exp( -1 * IR * self.paygrid ) * Qgrid;
        term2 = np.sum(term2);
        Qi_1 = np.array( [1] + list(Qgrid[0 : (self.Paytimes - 1)] ) );
        term3 = np.exp(-1 * IR * self.paygrid) * (Qi_1 - Qgrid);
        term3 = np.sum(term3) * self.Recovery * self.principle;
        return term1 + term2 + term3;
    
    def calculateV2(self, IR):
        Qgrid = self.predictQ(self.paygrid);
        term1 = self.principle * (1/(1 + IR))**(self.paygrid[-1]) * Qgrid[-1];
        term2 = self.AnnualC / self.fn * (1/(1 + IR))**(self.paygrid) * Qgrid;
        term2 = np.sum(term2);
        Qi_1 = np.array( [1] + list(Qgrid[0 : (self.Paytimes - 1)] ) );
        term3 = (1/(1 + IR))**(self.paygrid) * (Qi_1 - Qgrid);
        term3 = np.sum(term3) * self.Recovery * self.principle;
        return term1 + term2 + term3;    

    def automaticgrad(self, x):
        gradV = egrad(self.calculateV);
        return gradV(x);

if __name__ == "__main__":
    bond1 = bondsensive(1, 2, 100, 0.03, 0.4);
    bond1.loadQ("./Qdat.dat");
    bond1.paycoupon(bond1.principle * 0.03)
    print(bond1.fivestencil(0.03))
    print(bond1.automaticgrad(0.03))
    bond5 = bondsensive(5, 4, 100, 0.03, 0.4);
    bond5.loadQ("./Qdat.dat")
    bond5.paycoupon( bond5.principle * 0.05 );
    print(bond5.fivestencil(0.03));
    print(bond5.automaticgrad(0.03));
