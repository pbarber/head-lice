# %%
import pytrends
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

# %%
def get_google_trends_data(search_terms, start_year=2004, end_year=None, frequency='weekly', geo='GB'):
    """
    Fetch Google Trends data for multiple search terms.
    
    :param search_terms: List of search terms
    :param start_year: Start year for data collection (default: 2004)
    :param end_year: End year for data collection (default: current year)
    :param frequency: 'weekly' or 'monthly' (default: 'weekly')
    :return: DataFrame with data for all search terms
    """
    # Initialize pytrends
    pytrends = TrendReq(hl='en-GB', tz=0)
    
    # Set the end year to current year if not specified
    if end_year is None:
        end_year = datetime.now().year
    
    # Initialize an empty DataFrame to store the results
    results = pd.DataFrame(columns=['date'] + search_terms)
    
    # Determine the appropriate time chunk based on frequency
    if frequency == 'monthly':
        date_format = '%Y-%m-01'
        timeframe = f'{start_year}-01-01 {end_year}-12-31'

        pytrends.build_payload(search_terms, cat=0, timeframe=timeframe, geo=geo, gprop='')
        data = pytrends.interest_over_time()
        
        if not data.empty:
            data = data.reset_index()
            data['date'] = data['date'].dt.strftime(date_format)
            results = pd.concat([results, data[['date'] + search_terms]], ignore_index=True)
    else:  # weekly
        date_format = '%Y-%m-%d'
        # Fetch data year by year for weekly frequency
        for year in range(start_year, end_year + 1):
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            timeframe = f'{start_date.strftime("%Y-%m-%d")} {end_date.strftime("%Y-%m-%d")}'
            
            pytrends.build_payload(search_terms, cat=0, timeframe=timeframe, geo=geo, gprop='')
            data = pytrends.interest_over_time()
            
            if not data.empty:
                data = data.reset_index()
                data['date'] = data['date'].dt.strftime(date_format)
                results = pd.concat([results, data[['date'] + search_terms]], ignore_index=True)
    
    
    # Sort the results by date and reset the index
    results = results.sort_values('date').reset_index(drop=True)
    results['year'] = pd.to_datetime(results['date']).dt.year
    
    if frequency == 'monthly':
        results['month'] = pd.to_datetime(results['date']).dt.month
    else:  # weekly
        results['isoweek'] = pd.to_datetime(results['date']).dt.isocalendar().week
    
    return results

def output_csv_for_term(data, term, filename, frequency='weekly'):
    if frequency == 'monthly':
        data.drop_duplicates(
            ['month','year']
        ).pivot(
            index='month', columns='year', values=term
        ).to_csv(filename)
    else:  # weekly
        data.drop_duplicates(
            ['isoweek','year']
        ).pivot(
            index='isoweek', columns='year', values=term
        ).to_csv(filename)

# %%
trends_data = get_google_trends_data(['head lice', 'nits', 'lice treatment'])
trends_data.to_csv('google_trends_uk_weekly_by_year.csv', index=False)
output_csv_for_term(trends_data, 'head lice', 'head_lice_trends_uk_weekly_by_year_pivot.csv')
output_csv_for_term(trends_data, 'nits', 'nits_trends_uk_weekly_by_year_pivot.csv')
output_csv_for_term(trends_data, 'lice treatment', 'lice_treatment_trends_uk_weekly_by_year_pivot.csv')

# %%
trends_data2 = get_google_trends_data(['itchy head','bites on neck'])
output_csv_for_term(trends_data2, 'itchy head', 'itchy_head_trends_uk_weekly_by_year_pivot.csv')
output_csv_for_term(trends_data2, 'bites on neck', 'bites_on_neck_trends_uk_weekly_by_year_pivot.csv')

# %%
trends_data3 = get_google_trends_data(['head lice', 'nits', 'lice treatment'], frequency='monthly')
trends_data3.to_csv('google_trends_uk_monthly_by_year.csv', index=False)

# %%
trends_data6 = get_google_trends_data(['gym near me'])
output_csv_for_term(trends_data6, 'gym near me', 'gym_uk_weekly_by_year_pivot.csv')

# %%
