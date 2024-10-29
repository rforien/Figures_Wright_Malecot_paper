#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 10:47:09 2022

@author: raphael
"""

import numpy as np
import matplotlib.pyplot as plt
# import palettable.colorbrewer.diverging as palet
import palettable.cmocean.sequential as palet
import SLFV as slfv

# files = ["/home/raphael/Recherche/SLFV_two_radii/slfv_onetail_b_2", "/home/raphael/Recherche/SLFV_two_radii/slfv_onetail_b_0p5"]
files = ["/home/rforien/Recherche/CLT_infinite_alleles/Bastian's project/long_range_paper/slfv_onetail_b_2", 
         "/home/rforien/Recherche/CLT_infinite_alleles/Bastian's project/long_range_paper/slfv_onetail_b_0p5"]

b_values = [2, 0.5]

X0 = 5
Y0 = 1
R = 4

figsize = (11, 5)
# cmap = palet.RdBu_11.mpl_colormap
cmap = palet.Deep_20.mpl_colormap.reversed()

cbar_width = 0.1
cbar_padding = 0.025
cbar_height = 0.85

subtitle_fontsize = 14

freqs = []

for file in files:
    try:
        freqs.append(slfv.frequency.load_freq_from_file(file + '.json', file + '.npy', d = 2))
    except Exception as e:
        print("Error while loading frequency: ", e)
    
    
plt.style.use('ggplot')
fig, ax = plt.subplots(1, len(freqs), figsize = figsize)

def draw_init_circle(axis, X, Y, R, *args, **kwargs):
    xlim = axis.get_xlim()
    ylim = axis.get_ylim()
    theta = np.linspace(0, 2*np.pi, 500)
    x = X + R*np.cos(theta)
    y = Y + R*np.sin(theta)
    axis.plot(x, y, *args, **kwargs)
    axis.set_xlim(xlim)
    axis.set_ylim(ylim)

for (i, freq) in enumerate(freqs):
    freq.colorbar = cmap
    freq.plot(ax[i], colorbar = False)
    draw_init_circle(ax[i], X0, Y0, R, linestyle = 'dashed', color = 'white', linewidth = 1.5)
    ax[i].set_xticks([])
    ax[i].set_yticks([])
    ax[i].set_aspect(1)
    for pos in ['top', 'bottom', 'left', 'right']:
        ax[i].spines[pos].set_color('black')
    ax[i].set_title("b = %.1f" % b_values[i], fontsize = subtitle_fontsize)

fig.tight_layout()
fig.subplots_adjust(right=1-cbar_width-cbar_padding)
cbar_ax = fig.add_axes([1-cbar_width, (1-cbar_height)/2, 0.02, cbar_height])
cbar = fig.colorbar(freqs[0].lines, cax = cbar_ax, label = 'Proportion of allele 1')
cb_ticks = np.linspace(0, 1, 11)
cbar.set_ticks(cb_ticks)
cbar.set_ticklabels(cb_ticks.round(1))
