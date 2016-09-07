#!/usr/bin/env python3
from pyspc import *

a = spc(pistonrings) + cusum() + ewma() + rules()
#print(a)
b = spc(pistonrings) + xbar_sbar() + sbar() + rules()
#print(b)
c = spc(viscosidade) + xmr() + mr() + cusum() + rules()
#print(c)
d = spc(plastic) + Tsquare_single() + rules()
#print(d)
e = spc(experiment) + Tsquare()
#print(e)
f = spc(mewma_example) + mewma() + rules()
#print(f)
