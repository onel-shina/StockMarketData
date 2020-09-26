import pandas as pd
import datetime
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt;
import matplotlib.ticker as mtick

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

# Add a day of the week column
df["Day"] = df['Date'].apply(lambda x: x.strftime('%A'))
# Calculating Market Hour Daily Gain/Loss percentage
df["Percentage"] = ((df['Close'] - df['Open']) / df['Open']) * 100
# Calculating Overnight Gain/Loss percentage
df["Percentage_Overnight"] = ((df['Open'] - df['Close'].shift()) / df['Close'].shift()) * 100
# Green candles: Daily Open > Daily Close, Red candle: Daily Open < Daily Close
df['Daily_Candle_Color'] = df['Percentage'].apply(lambda x: "red" if x < 0 else 'green')

# Cumulative sum of Market Hour Gains
df["Percentage_Daily_Cumulative_Sum"] = df["Percentage"].cumsum()
# Cumulative sum of Overnight Gains
df["Percentage_Overnight_Cumulative_Sum"] = df["Percentage_Overnight"].cumsum()

# Total Sum of Market Hour Gains
daily_gains_sum = df["Percentage"].sum()
# Total Sum of Overnight Gains
overnight_gains_sum = df["Percentage_Overnight"].sum()

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

for df in days_of_the_week_dfs:
    days_of_the_week_mean.append(df['Percentage'].mean())

#   Will store the number of the green daily candles vs red daily candles in this variable
#   Green candle: Close Price > Open Price
#   Red candle: Close Price < Open Price
days_of_the_week_tables = []
for df in days_of_the_week_dfs:
    days_of_the_week_tables.append(df.pivot_table(index=['Daily_Candle_Color'], aggfunc='size'))


def display_average_daily_gain():
    fig = plt.figure()
    plt.style.use('ggplot')

    ax = fig.add_subplot(111)

    x = days_of_the_week
    average_daily_gain = [round(i, len(x)) for i in days_of_the_week_mean]
    y_colors = ['green' if i > 0 else "red" for i in average_daily_gain]
    x_pos = [i for i, _ in enumerate(x)]
    ax.bar(x_pos, average_daily_gain, color=y_colors)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    plt.xlabel("Day of the week")
    plt.ylabel("Average Percentage gain (Close - Open)")
    plt.title("{0} data from {1} to {2}".format(stock_symbol, start_date.date(), end_date.date()))

    plt.xticks(x_pos, x)

    plt.show()
    plt.close()




def display_daily_candle_distribution():
    x = days_of_the_week
    n = len(x)
    plt.style.use('ggplot')

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


def display_dailygains_versus_overnightgains():
    fig = plt.figure(figsize=(12, 8))
    plt.style.use('ggplot')
    ax = fig.add_subplot(111)
    ax.plot(df["Date"], df["Percentage_Daily_Cumulative_Sum"], label='Market Hours Gains')
    ax.plot(df["Date"], df["Percentage_Overnight_Cumulative_Sum"], label='Overnight Gains')
    ax.legend()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.title("{0} Gains\nFrom {1} to {2}".format(stock_symbol, start_date.date(), end_date.date()))
    plt.ylabel('Percent Gain Overtime')
    plt.xlabel('Date')
    plt.show()
    plt.close()


def dailygains_versus_overnightgains_percentage():
    fig = plt.figure()
    plt.style.use('ggplot')
    ax = fig.add_subplot(111)

    x = ["Market Hours Gains", "Overnight Gains"]
    y = [daily_gains_sum, overnight_gains_sum]
    y_colors = ['green' if i > 0 else "red" for i in y]
    x_pos = [i for i, _ in enumerate(x)]
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.bar(x_pos, y, color=y_colors)

    plt.title("{0} Gains: market hours vs overnight\nFrom {1} to {2}".format(stock_symbol,
                                                                             start_date.date(), end_date.date()))
    plt.ylabel('Total Gain')
    plt.xticks(x_pos, x)
    plt.show()
    plt.close()


display_average_daily_gain()
display_daily_candle_distribution()
display_dailygains_versus_overnightgains()
dailygains_versus_overnightgains_percentage()
