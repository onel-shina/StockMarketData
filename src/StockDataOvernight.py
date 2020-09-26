import pandas as pd
import datetime
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt;
import matplotlib.ticker as mtick

plt.rcdefaults()


def process_row(row):
    if (row['Percentage_Overnight'] > 0) and (row['Percentage'] > 0):
        return "Gap Up, Green close"
    elif (row['Percentage_Overnight'] > 0) and (row['Percentage'] < 0):
        return "Gap Up, Red close"
    elif (row['Percentage_Overnight'] < 0) and (row['Percentage'] > 0):
        return "Gap Down, Green close"
    elif (row['Percentage_Overnight'] < 0) and (row['Percentage'] < 0):
        return "Gap Down, Red close"



df = pdr.get_data_yahoo("SPY", start=datetime.datetime(1994, 1, 1), end=datetime.datetime.today()).reset_index()
df["Day"] = df['Date'].apply(lambda x: x.strftime('%A'))
df["Percentage"] = ((df['Close'] - df['Open']) / df['Open']) * 100
df["Percentage_Overnight"] = ((df['Open'] - df['Close'].shift()) / df['Close'].shift()) * 100

df["Percentage_Total"] = df["Percentage"].cumsum()
df["Percentage_Overnight_Total"] = df["Percentage_Overnight"].cumsum()
df['Situation'] = df.apply(lambda row: process_row(row), axis=1)

overall = df['Situation'].value_counts(normalize=True).reset_index().rename(columns={"index": "Situation", "Situation": "Count"})

plt.style.use('ggplot')
overall.sort_values("Situation").plot.barh(x='Situation', y = 'Count', rot = 0, color = 'blue')
plt.show()
plt.close()