#!/usr/bin/python3
from pyspc import *
import numpy as np
import pandas as pd

#df = pd.read_clipboard().values
#df = df[:,1]
#a = spc(newproduct) + ewma(target=30)+ xmr()+ mr()+ rules()
#print(a)
#a = spc(sandbox) + p() + rules()
#print(a)
#a = spc(chemical) + cusum(target=0.16) + ewma(target=0.16) + rules()
#print(a)
c = spc(pistonrings) + xbar_sbar() + sbar() + rules()
print(c)
b = spc(viscosidade) + mr()+ xmr() + cusum() +rules()
print(b)
##a = spc(plastic) + hotelling() + variation() + rules()
##print(a)
#a = spc(pistonrings) + cusum() + ewma() + rules()
#print(a)
#b = spc(pistonrings) + xbar_sbar() + sbar() + rules()
#print(b)
#c = spc(viscosidade) + imr()+ xmr() + cusum() +rules()
#print(c)
#d = spc(plastic) + hotelling() + variation() + rules()
#print(d)
#samples = dict()
#for n, value in Thickness:
#    if n in samples:
#        samples[n].append(value)
#    else:
#        samples[n] = [value]
#
#sample_size = len(samples[1])
#num_samples = len(samples)
#
#sample_mean = []
#sample_mr = []
#sample_std = []
#sample_r = []
#
#for key in samples:
#    assert sample_size == len(samples[key])
#    sample_mean.append(np.mean(samples[key]))
#    sample_std.append(np.std(samples[key], ddof=1))
#    sample_r.append(max(samples[key])-min(samples[key]))
#    
#    try:
#        v1, v2 = sample_mean[-2:]
#        sample_mr.append(abs(v1-v2))
#    except:
#        sample_mr.append(np.nan)
#
#xbar = np.mean(sample_mean)
#sbar = np.mean(sample_std)
#rbar = np.mean(sample_r)
#
## moving range graph
#mrbar = np.nanmean(sample_mr) #CENTER
#ucl_mr = D4[2] * mrbar
#lcl_mr = D3[2] * mrbar
#
## xbar graph
#ucl_xbar = xbar + 3*(mrbar/d2[2])
#lcl_xbar = xbar - 3*(mrbar/d2[2])
#
## std graph
#ucl_std = B4[sample_size] * sbar
#lcl_std = B3[sample_size] * sbar
#
## rbar graph
#ucl_rbar = D4[sample_size] * rbar
#lcl_rbar = D3[sample_size] * rbar
#
#print(xbar, sbar, rbar, mrbar)
## std estimative I-MR-R
#std_in = rbar / d2[sample_size]
#std_mr = mrbar / d2[2]
#std_between = np.sqrt(max([0, pow(std_mr, 2)-pow(std_in, 2)/sample_size]))
#std_total = np.sqrt(pow(std_between, 2)+pow(std_in, 2))
#print(std_total)
#
## std estimative I-MR-S
#std_in = sbar / c4[sample_size]
#std_mr = mrbar / d2[2]
#std_between = np.sqrt(max([0, pow(std_mr, 2)-pow(std_in, 2)/sample_size]))
#std_total = np.sqrt(pow(std_between, 2)+pow(std_in, 2))
#print(std_total)
#
###############################################################################

##data = np.array(data)
#data = experiment
#sizes = data[:,0]
#sample = data[:,1:]
#
#samples = dict()
#for n, value in zip(sizes, sample):
#    if n in samples:
#        samples[n] = np.vstack([samples[n], value])
#    else:
#        samples[n] = value
#
#square = np.array([np.var(xs, ddof=1, axis=0) for xs in samples.values()])
