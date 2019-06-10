# The following script uses census data from the [United States Census Bureau](http://www.census.gov)
# Counties are political and geographic subdivisions of states in the United States.
# This dataset contains population data for counties and states in the US from 2010 to 2015.
# [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf)
# for a description of the variable names.


import pandas as pd
import numpy as np
census_df = pd.read_csv('census.csv')
census_df

# The following function returns the state which has the most counties in it as a single string value


def most_counties():
    sumlev50 = census_df[(census_df['SUMLEV'] == 40)]
    data = sumlev50[['STNAME', 'CTYNAME']]
    cnt_counties = data.groupby('STNAME')['CTYNAME'].count()
    county_max = cnt_counties.sort_values(ascending=False).index[0]
    return county_max


most_counties()


# The following function returns the three most populous states by only looking
# at the three most populous counties for each state


def threemost_pop_state():
    sumlev50 = census_df[census_df['SUMLEV'] == 50]
    data = sumlev50[['CENSUS2010POP', 'STNAME', 'CTYNAME']]
    sum_countyPOP = data.sort_values(['STNAME', 'CENSUS2010POP'], ascending=True).groupby('STNAME')['CENSUS2010POP'].nlargest(3).sum(level=0)
    max3POP = pd.Series(sum_countyPOP.nlargest(3)).index.tolist()
    return max3POP


threemost_pop_state()


# The following function returns the county that has had the largest absolute change in Population
# within the period 2010-2015

def largest_abs_change():
    sumlev50 = census_df[census_df['SUMLEV'] == 50]
    data = sumlev50[['CTYNAME', 'POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']]
    max_p = data[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].max(axis=1)
    min_p = data[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].min(axis=1)
    data['MAXPOPChange'] = max_p - min_p
    max_delta = data.groupby('MAXPOPChange')['CTYNAME'].max()
    county = max_delta.iloc[-1]
    return county


largest_abs_change()


# The following function returns a 5x2 DataFrame of counties that belong to regions 1 or 2,
# whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

def counties_query():
    sumlev50 = census_df[census_df['SUMLEV'] == 50]
    data = sumlev50[['STNAME', 'CTYNAME', 'REGION', 'POPESTIMATE2014', 'POPESTIMATE2015']]
    sort = data[((data['REGION'] == 1) | (data['REGION'] == 2)) & (data['CTYNAME'].str.contains('Washington')) & (data['POPESTIMATE2015'] > data['POPESTIMATE2014'])]
    return sort[['STNAME', 'CTYNAME']]


counties_query()
