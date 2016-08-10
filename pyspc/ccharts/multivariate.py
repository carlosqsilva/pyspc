#!/usr/bin/python3
#
#Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
#This library is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .ccharts import ccharts
from.tables import B3, B4
from scipy.stats import beta
import numpy as np

class hotelling(ccharts):
    
    title = "T-square Hotelling Chart"
    
    def plot(self, ax, data, size, newdata=None):
                
        data = np.array(data)
        numsample = len(data)
        
        colmean = np.mean(data, axis=0)
        matcov = np.cov(data.T)
        matinv = np.linalg.inv(matcov)
        
        values = []
        for sample in data:
            dif = sample - colmean
            value = matinv.dot(dif.T).dot(dif)
            values.append(value)
        
        cl = ((numsample-1)**2)/numsample
        lcl = cl * beta.ppf(0.00135, size/2, (numsample-size-1)/2)
        center = cl * beta.ppf(0.5, size/2, (numsample-size-1)/2)
        ucl = cl * beta.ppf(0.99865, size/2, (numsample-size-1)/2)
        
        self.elements(ax, values, elements=[lcl, center, ucl])
        return (values, center, lcl, ucl)

class variation(ccharts):
    
    def plot(self, ax, data, size, newdata=None):
        
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0, ddof=1)
        svalues = []
        for sample in data:
            value = []
            for i in range(size):
                value.append((sample[i]-mean[i])/std[i])
            a = sum([x*x for x in value])
            b = np.mean(value)
            s = np.sqrt((a - 3*(b*b))/2)
            svalues.append(s)
        
        sbar = np.mean(svalues)
        lcl = B3[size+1] * sbar
        ucl = B4[size+1] * sbar
        
        self.elements(ax, svalues, elements=[lcl, sbar, ucl])
        return (svalues, sbar, lcl, ucl)

#class hotelling2(ccharts):
#    
#    def plot(self, ax, data, size):
#        
#        data = np.array(data)
#        sizes = data[:,0]
#        sample = data[:,1:]
#        
#        samples = dict()
#        for n, value in zip(sizes, sample):
#            if n in samples:
#                samples[n].append(value)
#            else:
#                samples[n] = [value]
#        
#        
#        
#class variation2(ccharts):
#    
#    def plot(self, ax, data, size):
#        pass