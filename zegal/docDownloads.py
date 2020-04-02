import os
import sys
import pandas as pd
import numpy as np

filepath = "/home/jugs/Documents/zegal/docdumpCsv/docdump.csv"

data = pd.read_csv(filepath, delimiter=',')

# print(data.head())

for i, row in data.iterrows():
    print(row)