# %%
import pytrends
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

# %%
# Initialize pytrends
pytrends = TrendReq(hl='en-GB', tz=0)

# Set up the search term
kw_list = ['head lice']

# Set the start year and end year
start_year = 2004
end_year = datetime.now().year

# Initialize an empty DataFrame to store the results
results = pd.DataFrame(columns=['date', 'head lice'])

# Fetch data year by year
for year in range(start_year, end_year + 1):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    timeframe = f'{start_date.strftime("%Y-%m-%d")} {end_date.strftime("%Y-%m-%d")}'
    
    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='GB', gprop='')
    data = pytrends.interest_over_time()
    
    if not data.empty:
        data = data.reset_index()
        data['date'] = data['date'].dt.strftime('%Y-%m-%d')
        results = pd.concat([results, data[['date', 'head lice']]], ignore_index=True)

# Sort the results by date and reset the index
results = results.sort_values('date').reset_index(drop=True)

# Display the first few rows of the results
print(results.head())

# Display the date range of the collected data
print(f"Data collected from {results['date'].iloc[0]} to {results['date'].iloc[-1]}")

# Save the results to a CSV file
output_file = 'head_lice_trends_uk_weekly_by_year.csv'
results.to_csv(output_file, index=False)
print(f"Data saved to '{output_file}'")

# %%
results['year'] = pd.to_datetime(results['date']).dt.year
results['isoweek'] = pd.to_datetime(results['date']).dt.isocalendar().week
results.drop_duplicates(['isoweek','year']).pivot(index='isoweek', columns='year',values='head lice').to_csv('head_lice_trends_uk_weekly_by_year_pivot.csv')

# %%
