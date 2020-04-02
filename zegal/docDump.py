import os
import json
import sys
import pandas as pd
import numpy as np


docDumpFile = "/home/jugs/Documents/zegal/docdumpCsv/filter_docdump.csv"
conversationFile = "/home/jugs/PycharmProjects/ExperimentalProjects/zegal/zegalchatlogProcess.csv"

docData = pd.read_csv(docDumpFile, skiprows=0, delimiter=',', encoding='cp1252')
# print(docData.head())

convData = pd.read_csv(conversationFile, skiprows=0, delimiter='\t')

# convData = convData.head(200)
# docData = docData.head(200)

for i, row in convData.iterrows():
    for j, drow in docData.iterrows():
        if (row['datetimestamp'] == drow['date_created']) & (row['User_x'] == drow['login']):
            print(drow['documents'])