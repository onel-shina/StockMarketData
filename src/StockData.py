import pandas as pd
import datetime
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt;

plt.rcdefaults()


stock_symbol = input("Enter Stock Symbol >> \n")

start_date_input = input("Enter starting date in yyyy-mm-dd format >> \n")
start_date = datetime.datetime.strptime(start_date_input, '%Y-%m-%d')

end_date_input = input("Enter ending date in yyyy-mm-dd format, or enter CURRENT for today's date >> \n")
if 'CURRENT' in end_date_input:
    end_date = datetime.datetime.today()
else:
    end_date = datetime.datetime.strptime(end_date_input, '%Y-%m-%d')

df = pdr.get_data_yahoo(stock_symbol, start=start_date, end=end_date).reset_index()

df["Day"] = df['Date'].apply(lambda x: x.strftime('%A'))
df["Percentage"] = ((df['Close'] - df['Open']) / df['Close']) * 100
df['Daily_Candle_Color'] = df['Percentage'].apply(lambda x: "red" if x < 0 else 'green')

days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
days_of_the_week_dfs = []
'''
days_of_the_week_dfs[0] = Monday Data
days_of_the_week_dfs[1] = Tuesday Data
days_of_the_week_dfs[2] = Wednesday Data
days_of_the_week_dfs[3] = Thursday Data
days_of_the_week_dfs[4] = Friday Data

'''
for day in days_of_the_week:
    days_of_the_week_dfs.append(df[df['Day'].str.match(day)])

days_of_the_week_mean = []
days_of_the_week_volatility = []

for df in days_of_the_week_dfs:
    days_of_the_week_mean.append(df['Percentage'].mean())
    days_of_the_week_volatility.append(df['Percentage'].std())

#   Will store the number of the green daily candles vs red daily candles in this variable
#   Green candle: Close Price > Open Price
#   Red candle: Close Price < Open Price
days_of_the_week_tables = []
for df in days_of_the_week_dfs:
    days_of_the_week_tables.append(df.pivot_table(index=['Daily_Candle_Color'], aggfunc='size'))


def display_average_daily_gain():
    plt.style.use('ggplot')
    x = days_of_the_week
    average_daily_gain = [round(i, len(x)) for i in days_of_the_week_mean]
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, average_daily_gain, color='black')

    plt.xlabel("Day of the week")
    plt.ylabel("Average Percentage gain (Close - Open)")
    plt.title("{0} data from {1} to {2}".format(stock_symbol, start_date.date(), end_date.date()))

    plt.xticks(x_pos, x)

    plt.show()
    plt.close()


def display_average_daily_volatility():
    plt.style.use('ggplot')
    x = days_of_the_week
    average_daily_volatility = [round(i, len(x)) for i in days_of_the_week_volatility]
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, average_daily_volatility, color='blue')

    plt.xlabel("Day of the week")
    plt.ylabel("Average Volatility")
    plt.title("{0} data from {1} to {2}".format(stock_symbol, start_date.date(), end_date.date()))

    plt.xticks(x_pos, x)

    plt.show()
    plt.close()


def display_daily_candle_distribution():
    x = days_of_the_week
    n = len(x)

    green_daily_candles = [i['green'] for i in days_of_the_week_tables]
    red_daily_candles = [i['red'] for i in days_of_the_week_tables]

    ind = np.arange(n)
    width = 0.35
    plt.bar(ind, green_daily_candles, width, label='Green Daily Candles (Close Price > Open Price)', color='green')
    plt.bar(ind + width, red_daily_candles, width, label='Red Daily Candles (Close Price < Open Price)', color='red')

    plt.ylabel('Number of days')
    plt.title("{0} data from {1} to {2}".format(stock_symbol, start_date.date(), end_date.date()))

    plt.xticks(ind + width / 2, x)
    plt.legend(loc='best')

    plt.show()
    plt.close()


display_average_daily_gain()
display_average_daily_volatility()
display_daily_candle_distribution()