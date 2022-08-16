#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 16:42:52 2022

@author: raphael
"""

import numpy as np
import SLFV as slfv
import palettable.colorbrewer.diverging as palet

Lx = 10
Ly = 10
dx = 0.01

u0 = 0.3
r0 = 0.5

a = 1.3
b = 2
c = 1

if b > 1:
    a = a*b
    # r0 = 1.2*r0

X0 = 5
Y0 = 1
R = 4
spread = 1

T = 3

event = slfv.events.OneTailRadii(u0, r0, c, b, a, 2)

slfv = slfv.SLFV((Lx, Ly), 2, event, dx = dx)

slfv.frequency.colorbar = palet.RdBu_11.mpl_colormap

def freq_func(X, Y, X0, Y0, R, spread):
    freq = np.zeros(slfv.frequency.nx + (2,))
    r = np.sqrt((X-X0)**2 + (Y-Y0)**2)
    freq[:,:,0] = 0.5*(1+np.tanh((r-R)/spread))
    freq[:,:,1] = 1-freq[:,:,0]
    return freq

slfv.set_freq(freq_func, X0 = X0, Y0 = Y0, R = R, spread = spread)
slfv.run(T)
slfv.plot()
# slfv.frequency.save("/home/raphael/Recherche/SLFV_two_radii/slfv_onetail_b_2")