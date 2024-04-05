import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np
import datetime

# Read the JSON file into a Pandas DataFrame
aus = pd.read_json('data/sentiment/aus.json')
nz = pd.read_json('data/sentiment/nz.json')
canada = pd.read_json('data/sentiment/canada.json')

# Calculate daily averages
aus_daily = aus.groupby(pd.Grouper(key='date', freq='D'))['score'].mean().reset_index()
nz_daily = nz.groupby(pd.Grouper(key='date', freq='D'))['score'].mean().reset_index()
canada_daily = canada.groupby(pd.Grouper(key='date', freq='D'))['score'].mean().reset_index()
#weekly = aus.groupby(pd.Grouper(key='date', freq='W'))['score'].mean().reset_index()
#monthly = aus.groupby(pd.Grouper(key='date', freq='M'))['score'].mean().reset_index()

# Merge daily averages
daily = pd.merge(aus_daily, nz_daily, on='date', how='outer', suffixes=('_aus', '_nz'))
daily = pd.merge(daily, canada_daily, on='date', how='outer')

# Do some cleaning
daily = daily.rename(columns={'score': 'score_canada'})
daily.set_index('date', inplace=True)

# Calculate exponentially weighted moving average
daily['ewma_aus'] = daily['score_aus'].ewm(alpha=0.002, adjust=True, ignore_na=True).mean()
daily['ewma_nz'] = daily['score_nz'].ewm(alpha=0.002, adjust=True, ignore_na=True).mean()
daily['ewma_canada'] = daily['score_canada'].ewm(alpha=0.002, adjust=True, ignore_na=True).mean()

# Remove the first 90 ewma values, which are unstable
daily['ewma_aus'] = np.where(daily['ewma_aus'].shift(90).isnull(), np.nan, daily['ewma_aus'])
daily['ewma_nz'] = np.where(daily['ewma_nz'].shift(90).isnull(), np.nan, daily['ewma_nz'])
daily['ewma_canada'] = np.where(daily['ewma_canada'].shift(90).isnull(), np.nan, daily['ewma_canada'])

# Standardise start from July 2017
filtered_daily = daily.loc[daily.index > '2017-07-01']

# Set theme
plt.style.use("seaborn-v0_8-talk")

# Australia annotated plot
plt.plot(filtered_daily['ewma_aus'], label='Australia')
# Add vertical lines and annotations for events
# events = {'A': '2018-02-15', 'B': '2018-05-15', 'C': '2019-01-15', 'D': '2019-07-15', 'E': '2021-03-15'}
# for event, date in events.items():
#     date_num = dates.date2num(pd.to_datetime(date))
#     plt.axvline(x=date_num, color='black', linestyle='--', label=f'Event {event}')
#     plt.annotate(f'Event {event}', (date_num, filtered_daily.loc[date, 'ewma_aus']), textcoords="offset points", xytext=(0,10), ha='center')

# Independent COVID Inquiry
plt.axvline(x=dates.date2num(datetime.datetime.strptime('01/04/2020', "%d/%m/%Y")), color='gray', linestyle='-', linewidth=1, label='_nolegend_')
plt.annotate(text = 'COVID-19 Inquiry', xy = (dates.date2num(datetime.datetime.strptime('01/04/2020', "%d/%m/%Y")) - 370, -0.17), alpha = 0.9, fontsize=9)

# AUKUS Announced
plt.axvline(x=dates.datestr2num('16/09/2021'), color='gray', linestyle='-', linewidth=1, label='_nolegend_')
plt.annotate(text = 'AUKUS Announced', xy = (dates.datestr2num('16/09/2021') - 400, -0.17), alpha = 0.9, fontsize=9)

# New election
plt.axvline(x=dates.datestr2num('21/05/2022'), color='gray', linestyle='-', linewidth=1, label='_nolegend_')
plt.annotate(text = 'Federal Election', xy = (dates.datestr2num('21/05/2022') + 15 , -0.17), alpha = 0.9, fontsize=9)

# Formatting
plt.xlabel('Date')
plt.ylabel('Sentiment')
plt.title('Aggregated Sentiment of Articles Mentioning Australia')
plt.show()

# Create a scatter plot
plt.plot(filtered_daily['ewma_aus'], label='Australia')
plt.plot(filtered_daily['ewma_nz'], label='New Zealand')
# We fill between to show the freezer, but only from 2020 for reliability
fill_in = filtered_daily.loc[filtered_daily.index > '2020-04-01']

plt.fill_between(x = fill_in.index, y1 = fill_in['ewma_aus'], y2 = fill_in['ewma_nz'], color = '#87c7ff')

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Sentiment')
plt.title('Aggregated Headline Sentiment of Chinese State Media')
plt.legend()

# Show the plot
plt.show()
