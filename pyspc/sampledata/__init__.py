# -*- coding: utf-8 -*-
import pandas as pd
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

pistonrings = pd.read_csv(os.path.join(_ROOT, 'pistonrings.csv')).values
    
diameter = pd.read_csv(os.path.join(_ROOT, 'diameter.csv')).values

parts = pd.read_csv(os.path.join(_ROOT, 'parts.csv')).values
    
sizes = pd.read_csv(os.path.join(_ROOT, 'sizes.csv')).values
    
chemical = pd.read_csv(os.path.join(_ROOT, 'chemical.csv')).values
    
newproduct = pd.read_csv(os.path.join(_ROOT, 'newproduct.csv')).values
    
waitingTime = pd.read_csv(os.path.join(_ROOT, 'waitingTime.csv')).values

sandbox = pd.read_csv(os.path.join(_ROOT, 'sandbox.csv')).values

canjuice = pd.read_csv(os.path.join(_ROOT, 'canjuice.csv')).values

circuits = pd.read_csv(os.path.join(_ROOT, 'circuits.csv')).values

inspection = pd.read_csv(os.path.join(_ROOT, 'inspection.csv')).values