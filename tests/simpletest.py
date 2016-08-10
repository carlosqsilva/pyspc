#!/usr/bin/python3
from pyspc import *

a = spc(pistonrings) + cusum() + ewma() + rules()
print(a)
b = spc(pistonrings) + xbar_sbar() + sbar() + rules()
print(b)
c = spc(viscosidade) + imr()+ xmr() + cusum() +rules()
print(c)
d = spc(plastic) + hotelling() + variation() + rules()
print(d)
