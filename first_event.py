#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:37:22 2022

@author: raphael
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import palettable.colorbrewer.diverging as palet
import SLFV as slfv

Lx = 10
Ly = 8
dx = 0.01

X0 = 3
spread = 3

centre_of_event = np.array([4.5, 5])
r_parent = np.array([4, 1])
r_replace = np.array([1, 3.5])
u = 0.4

parent_draw_radius = 0.8
parent_draw_angle = 2.5*np.pi/3

linewidth = 1.3
marker_size = 60
parent_color = 'white'
event_color = 'black'

legend_background_color = "#D4D4D4"

cmap = palet.RdBu_11.mpl_colormap

titles = [r'$r_1 > r_2$', r'$r_1 < r_2$']
htitle_fontsize = 16

htitles = ['Before the reproduction event', 'After the reproduction event']
vtitle_fontsize = 14

cbar_width = 0.15
cbar_padding = 0.025
cbar_height = 0.8

freq_init = slfv.Frequency2D((Lx, Ly), .01, 2)
freq1 = slfv.Frequency2D((Lx, Ly), dx, 2)
freq2 = slfv.Frequency2D((Lx, Ly), dx, 2)

freq_array = [freq1, freq2]

def freq_func(X, Y, X0):
    freq = np.zeros(freq_init.nx + (2,))
    # freq[:,:,0] = (np.sqrt((X-X0)**2+(Y-Y0)**2)<R)
    freq[:,:,0] = 0.5*(1-np.tanh((X - X0)/spread))
    freq[:,:,1] = 1-freq[:,:,0]
    return freq

for freq in [freq_init, freq1, freq2]:
    freq.set_freq(freq_func, X0=X0)
    freq.colorbar = cmap
    # freq.colorbar = palet.Bamako_10.mpl_colormap.reversed()
    
parent_x = centre_of_event[0] + r_parent * parent_draw_radius * np.cos(parent_draw_angle)
parent_y = centre_of_event[1] + r_parent * parent_draw_radius * np.sin(parent_draw_angle)

parent_allele = [0, 1]

for i in range(2):
    freq_array[i].update(centre_of_event, r_replace[i], u, parent_allele[i])

plt.style.use('ggplot')
fig, ax = plt.subplots(2, 2, figsize=(Lx/(1-cbar_width-cbar_padding), Ly))

for i in range(2):
    freq_init.plot(ax[0,i], colorbar=False)
    ax[0,i].scatter(centre_of_event[0], centre_of_event[1], marker='+', s = marker_size, color = event_color)
    parent_point = ax[0,i].scatter(parent_x[i], parent_y[i], marker= 'x', s = marker_size, color = parent_color)
    ylim, xlim = ax[0,i].get_ylim(), ax[0,i].get_xlim()
    circle_replace = plt.Circle(centre_of_event, r_replace[i], fill = False, clip_on = True, 
                                linewidth = linewidth, color = event_color)
    ax[0,i].add_patch(circle_replace)
    circle_parent = plt.Circle(centre_of_event, r_parent[i], fill = False, linestyle = '--', 
                               linewidth = linewidth, color = parent_color, clip_on = True)
    ax[0,i].add_patch(circle_parent)
    ax[0,i].set_ylim(ylim)
    ax[0,i].set_xlim(xlim)
    ax[0,i].set_title(titles[i], fontsize = htitle_fontsize)
    ax[i,0].set_ylabel(htitles[i], fontsize = vtitle_fontsize)
    
    freq_array[i].plot(ax[1,i], colorbar = False)
    
    for j in range(2):
        ax[i,j].set_aspect(1)

fig.tight_layout()
fig.subplots_adjust(right=1-cbar_width-cbar_padding)
cbar_ax = fig.add_axes([1-cbar_width, 0.95-cbar_height, 0.03, cbar_height])
cbar = fig.colorbar(freq_init.lines, cax = cbar_ax, label = 'Proportion of allele 1')
cb_ticks = np.linspace(0, 1, 11)
cbar.set_ticks(cb_ticks)
cbar.set_ticklabels(cb_ticks.round(1))
fig.legend([circle_replace, circle_parent, parent_point], ['Replacement area', 'Parent-search area', 'parent location'], 
           loc="lower right", fontsize="large", frameon=True, borderpad = 0.8, facecolor = legend_background_color, 
           shadow = True)

for i in range(2):
    for j in range(2):
        for pos in ['top', 'bottom', 'left', 'right']:
            ax[i,j].spines[pos].set_color('black')
            ax[i,j].set_xticks([])
            ax[i,j].set_yticks([])
            