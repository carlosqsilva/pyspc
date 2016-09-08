# PySpc
Statistical Process Control Charts Library for Humans

PySpc is a Python library aimed to make Statistical Process Control Charts as easy as possible.

## Control Charts Available

Control Charts by Variables
* Mean and Amplitude
* Mean and Standard Deviation
* Individual Values and Moving Range
* Individual values with subgroups
* Exponentially Weighted Moving Average (EWMA)
* Cumulative Sum (CUSUM)

Control Charts by Attributes
* P Chart
* NP Chart
* C Chart
* U Chart

Multivariate Control Charts
* T Square Hotelling
* T Square Hotelling with SubGroup
* Multivariate Exponentially Weighted Moving Average (MEWMA)

## Usage
```python
from pyspc import *

a = spc(pistonrings) + ewma()
print(a)
```
![alt text](screenshots/1-screen.png "My First Chart")

adding rules highlighting...
```python
a + rules()
```
![alt text](screenshots/2-screen.png "With Basic Rules")

adding more control charts to he mix...
```python
a + cusum() + xbar_sbar() + sbar()
```
![alt text](screenshots/3-screen.png "More Control Charts...")

it comes with 18 sample datasets to play with, avaiable in *./pyspc/sampledata*, you can use your own data (of course), your data can be nested lists, numpy array or pandas DataFrame.

## Gtk Gui
Its also available a python gui aplication for those who do not like to mess with code.
![alt text](screenshots/4-screen.png "Gui Application")

