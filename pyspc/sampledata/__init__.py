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

paint = pd.read_csv(os.path.join(_ROOT, 'PaintMaterial.csv')).values

thickness = pd.read_csv(os.path.join(_ROOT, 'thickness.csv')).values

viscosity = pd.read_csv(os.path.join(_ROOT, 'Viscosidade.csv')).values

plastic = pd.read_csv(os.path.join(_ROOT, 'hotelling.csv')).values

experiment = pd.read_csv(os.path.join(_ROOT, 'experiment.csv')).values

mewma_example = pd.read_csv(os.path.join(_ROOT, 'dados.csv')).values
