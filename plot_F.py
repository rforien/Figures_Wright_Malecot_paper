#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 09:31:47 2022

@author: raphael
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

directory = 'out2/'

plot_dimensions = [2, 3]

files = []
for d in plot_dimensions:
    files = files + ['F_values_d-' + str(d) + '_run-' + str(i) for i in range(4)]

colour_id = np.tile(np.arange(4), len(plot_dimensions))

figsize = (9,4)
xlim_left = -0.5

first_value = 0.1

xlabel = "distance between sampled individuals"
ylabel = 'Probability of identity'

plt.style.use('ggplot')
colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

fig, ax = plt.subplots(1, len(plot_dimensions), figsize = figsize, sharey = True)

for (j, file) in enumerate(files):
    params = pd.read_csv(directory + file + 'params.csv', sep=',', index_col = 0).squeeze("columns")
    F_values = pd.read_csv(directory + file + '.csv', sep = ',', index_col = 0).squeeze("columns")
    
    F_values = first_value * F_values / F_values.values[9]
    
    i = np.where(plot_dimensions == params["d"])[0][0]
    color = colours[colour_id[j]]
    
    ax[i].plot(F_values, label = r"$\alpha$=%.1f, $\beta$=%.1f" % (params["alpha"], params["beta"]), color = color)
    
for i in range(len(plot_dimensions)):
    ax[i].set_title(r"$d$ = %d" % plot_dimensions[i])
    ax[i].set_yscale('log')
    ax[i].legend(loc='best')
    
    ax[i].yaxis.set_tick_params(labelleft="True")
    
    xlim = ax[i].get_xlim()
    ax[i].set_xlim(xlim_left, xlim[1])
    ax[i].set_xlabel(xlabel)

ax[0].set_ylabel(ylabel)

fig.tight_layout()

