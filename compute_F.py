#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 15:08:07 2022

@author: raphael
"""

import numpy as np
import scipy.integrate as integrate
import scipy.special as special
import pandas as pd
import sys, getopt


try:
    opts, args = getopt.getopt(sys.argv[1:], "d:a:b:o:", ["dimension=", "alpha=", "beta=", "output="])
except getopt.GetoptError:
    print("compute_F.py -d <dimension> -a <alpha> -b <beta> -o <output file>")
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-d', "--dimension"):
        d = int(arg)
    elif opt in ('-a', "--alpha"):
        alpha = float(arg)
    elif opt in ('-b', "--beta"):
        beta = float(arg)
    elif opt in ('-o', '--output'):
        filename = str(arg)

#try:
#    d
#except:
#    d = 2
#try:
#    alpha
#except:
#    alpha = 2
#try:
#    beta
#except:
#    beta = 2
#try:
#    filename
#except:
#    filename = 'test'

    
params = pd.Series(index = ["d", "alpha", "beta"])
params['d'] = d
params['alpha'] = alpha
params['beta'] = beta

params.to_csv(filename + "params.csv", sep = ',')
# sys.exit(0)

verbose = False

zeta = 1
gamma = 1
sigma2 = 1
mu = 0.2

xmax = 3
nx = 2

max_error = 3e-2

assert (beta >= d and alpha > d-1) or (beta < d and d - beta + alpha > d-1), 'Integrals will diverge'

if alpha > 2:
    print("Warning, alpha cannot be larger than 2. Setting alpha = 2.")
    alpha = 2

# function to compute sum of terms of alternating signs up to a given precisions
def compute_alternate_sum(general_term, rel_error, *args, **kwargs):
    assert rel_error > 0 and rel_error < 1
    i = 0
    a = [general_term(i, *args, **kwargs)]
    while np.abs(a[-1]/np.sum(a)) > rel_error or np.mod(i, 2) == 1:
        i = i + 1
        a.append(general_term(i, *args, **kwargs))
    return np.sum(a)

def sphere_surface(r, d):
    return (d+1) * np.pi**((d+1)/2) * r**d / special.gamma((d+3)/2)

# compute c1
if alpha == 2:
    c1 = 2*np.pi**2*sigma2
else:
    if d == 1:
        def I(u):
            return 2/u**(d+alpha)
    elif d == 2:
        def I(u):
            return 4 * integrate.quad(lambda r: 1/(u**2 + r**2)**((d + alpha)/2), 0, np.inf)[0]
    else:
        def I(u):
            return 2 * integrate.quad(lambda r: 1/(u**2 + r**2)**((d+alpha)/2) * sphere_surface(r, d-2), 0, np.inf)[0]
    
    V1 = np.pi**(d/2)/special.gamma(d/2+1)
    c1 = (zeta / (V1 * (d+alpha))) * integrate.quad(lambda u: I(u) * (1-np.cos(2*np.pi*u)), 0, np.inf)[0]

# compute c2
if beta >= d:
    c2 = 1
else:
    if d == 1:
        def H(u):
            return 2/u**beta
    elif d == 2:
        def H(u):
            return 4 * integrate.quad(lambda r: 1/(u**2 + r**2)**(beta/2), 0, np.inf)[0]
    else:
        def H(u):
            return 2 * integrate.quad(lambda r: 1/(u**2 + r**2)**(beta/2) * sphere_surface(r, d-2), 0, np.inf)[0]
    
    def compute_b(i):
        return (-1)**i * integrate.quad(lambda u: H(0.5*i + u) * np.cos(2*np.pi*u), 0, 1/2)[0]
    
    c2 = compute_alternate_sum(compute_b, max_error)
    

if beta >= d:
    power = 0
    c3 = 1
else:
    power = d - beta
    c3 = c2**(1/power)

# define integrands
def g(r):
    return 0.5*gamma/((mu + c1 * r**alpha)*(r/c3)**power)
    
if d==1:
    def G(u,x):
        return 2*g(u/x)/x
elif d==2:
    def G(u,x):
        return (4/x) * integrate.quad(lambda r: g(np.sqrt((u/x)**2+r**2)), 0, np.inf)[0]
else:
    def G(u,x):
        return (2/x) * integrate.quad(lambda r : g(np.sqrt((u/x)**2 + r**2)) * sphere_surface(r, d-2), 0, np.inf)[0]

# function to compute each term of the summation
def compute_a(i, x):
    return (-1)**i * integrate.quad(lambda u: G(0.5*i + u, x) * np.cos(2*np.pi*u), 0, 1/2)[0]

# compute the value of F at one point
def compute_F(x, max_rel_error = 1e-2):
    return compute_alternate_sum(compute_a, max_rel_error, x = x)

x_values = np.linspace(0, xmax, nx+1)[1:]
F_values = pd.Series(index = x_values, dtype = np.float64)

for (i,x) in enumerate(x_values):
    F_values[x] = compute_F(x, max_error)
    if verbose:
        print("Computed %d of %d entries" % (i+1, nx))

F_values.to_csv(filename + ".csv", sep = ',')
params.to_csv(filename + "params.csv", sep = ',')


