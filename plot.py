import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
daily['ewma_aus'] = daily['score_aus'].ewm(alpha=0.003, adjust=True, ignore_na=True).mean()
daily['ewma_nz'] = daily['score_nz'].ewm(alpha=0.003, adjust=True, ignore_na=True).mean()
daily['ewma_canada'] = daily['score_canada'].ewm(alpha=0.003, adjust=True, ignore_na=True).mean()

# Remove the first 90 ewma values, which are unstable
daily['ewma_aus'] = np.where(daily['ewma_aus'].shift(90).isnull(), np.nan, daily['ewma_aus'])
daily['ewma_nz'] = np.where(daily['ewma_nz'].shift(90).isnull(), np.nan, daily['ewma_nz'])
daily['ewma_canada'] = np.where(daily['ewma_canada'].shift(90).isnull(), np.nan, daily['ewma_canada'])

# Assuming 'date' and 'score' are the column names in your DataFrame
# Replace them with the actual column names in your JSON file
x_column = 'date'
y_column = 'ewma_nz'

# Create a scatter plot
plt.plot(daily['ewma_aus'], label='Australia')
plt.plot(daily['ewma_nz'], label='New Zealand')
plt.plot(daily['ewma_canada'], label='Canada')

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Sentiment')
plt.title('Headline Sentiment Trend Over Time')
plt.legend()

# Show the plot
plt.show()
