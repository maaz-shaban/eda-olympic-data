

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby("region").sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']] = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']].astype('int')
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def fetch_medal_tally(year, country, df):
    medal_year = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    groupby = 'region'
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_year

    if year == 'Overall' and country != 'Overall':
        temp_df = medal_year[medal_year['region'] == country]
        groupby = 'Year'

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_year[medal_year['Year'] == year]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_year[(medal_year['Year'] == year) & (medal_year['region'] == country)]

    temp_df = temp_df.groupby(groupby).sum()[["Gold", "Silver", "Bronze"]].sort_values('Gold', ascending=False)
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df[['Gold', 'Silver', 'Bronze', 'Total']] = temp_df[['Gold', 'Silver', 'Bronze', 'Total']].astype('int')
    return temp_df

def participating_nations(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time = nations_over_time.rename(columns={'index':'year','Year':'count'})
    return nations_over_time

def get_athletes(df, sport="Overall"):
    temp_df = df
    if sport != "Overall":
        temp_df = df[df['Sport'] == sport]

    temp_df = temp_df.dropna(subset=['Medal'])
    temp_df = temp_df['Name'].value_counts().reset_index()
    temp_df = temp_df.head(15).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates(subset=['index'])
    temp_df = temp_df.rename(columns={'index': 'Name', 'Name_x': 'Medals', 'region': 'Region'})
    return temp_df.reset_index().drop('index', axis=1)

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df

def yearwise_medal_pivot(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return temp_df

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates(subset=['index'])
    x.rename(columns={'index':'Name', 'Name_x':'Medals'}, inplace=True)
    return x