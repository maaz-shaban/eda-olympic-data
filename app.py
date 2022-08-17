import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor
import helper
import plotly.figure_factory as ff

st.set_page_config(page_title='Olympic Data Analysis')

df = pd.read_csv('./data/athlete_events.csv')
df_regions = pd.read_csv("./data/noc_regions.csv")

df = preprocessor.preprocessor(df, df_regions)
st.sidebar.title("Olympic Data Analysis")
user_menu = st.sidebar.radio('Select any option', ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Wise Analysis'))



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header("Overall Tally")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header(f"{selected_country} Overall Performance")

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header(f"Medal Tally in {selected_year} Olympics")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(f"{selected_country} perfomrance in {selected_year} Olympics")

    st.table(helper.fetch_medal_tally(selected_year, selected_country, df))
elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athelets = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Editions")
        st.header(editions)
        st.subheader("Events")
        st.header(events)

    with col2:
        st.subheader("Cities")
        st.header(cities)
        st.subheader("Athelets")
        st.header(athelets)

    with col3:
        st.subheader("Sports")
        st.header(sports)
        st.subheader("Nations")
        st.header(nations)

    st.header("Participating Nations over time")
    nations_over_time = helper.participating_nations(df, 'region')
    fig = px.line(nations_over_time, x='year', y='count',)
    st.plotly_chart(fig)

    st.header("No. of Events over time in Olympics")
    events_over_time = helper.participating_nations(df, 'Event')
    fig = px.line(events_over_time, x='year', y='count')
    st.plotly_chart(fig)

    st.header('No. of Athletes over time in Olympics')
    athlete_over_time = helper.participating_nations(df, 'Name')
    fig = px.line(athlete_over_time, x='year', y='count')
    st.plotly_chart(fig)

    st.header("No. of Events(Every Sport) over time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.header('Most successful Athletes')
    sports = df['Sport'].unique().tolist()
    sports.insert(0, 'Overall')
    selected_sport = st.selectbox("Select Sport", sports)
    all_athletes = helper.get_athletes(df, selected_sport)
    st.table(all_athletes)
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    region = df.dropna(subset=['region'])['region'].unique().tolist()
    region.sort()
    region.insert(0, 'Overall')
    selected_country = st.sidebar.selectbox('Select Country', region)
    years = helper.yearwise_medal_tally(df, selected_country)
    if selected_country == 'Overall':
        st.header('Overall Medal Tally of all countries over years')
    else:
        st.header(f"Medal Tally of {selected_country} over years")


    fig = px.line(years, x='Year', y='Medal')
    st.plotly_chart(fig)


    years = helper.yearwise_medal_pivot(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(years, annot=True)
    st.pyplot(fig)

    st.header("Top 10 athletes of " + selected_country)
    athletes = helper.most_successful_countrywise(df, selected_country)
    st.table(athletes)

elif user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)

    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    y = []
    famous_sports = ['Basketball',
 'Judo',
 'Football',
 'Tug-Of-War',
 'Athletics',
 'Swimming',
 'Badminton',
 'Sailing',
 'Gymnastics',
 'Art Competitions',
 'Handball',
 'Weightlifting',
 'Wrestling',
 'Water Polo',
 'Hockey',
 'Rowing',
 'Fencing',
 'Equestrianism',
 'Shooting',
 'Boxing',
 'Taekwondo',
 'Cycling',
 'Diving',
 'Canoeing',
 'Tennis',
 'Modern Pentathlon',
 'Softball',
 'Archery',
 'Volleyball',
 'Synchronized Swimming',
 'Table Tennis',
 'Baseball',
 'Rhythmic Gymnastics',
 'Rugby Sevens',
 'Rugby',
 'Lacrosse',
 'Polo',
 'Cricket']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        y.append(sport)

    fig = ff.create_distplot(x, y, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

    sports = athlete_df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sports)
    if selected_sport != 'Overall':
        athlete_df = athlete_df[athlete_df['Sport'] == selected_sport]
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.scatterplot(x='Weight', y='Height', data=athlete_df, hue='Medal', style='Sex')
    st.header('Height vs Weight')
    st.pyplot(fig)

    st.header("Male vs Female Participation over Years")
    sex_data = df.groupby(['Year', 'Sex']).count()['Name'].reset_index()
    sex_data = sex_data.rename(columns={'Name':'count'})
    male = sex_data[sex_data['Sex'] == 'M'].drop('Sex', axis=1)
    female = sex_data[sex_data['Sex'] == 'F'].drop('Sex', axis=1)
    male = male.rename(columns={'count':'Male'})
    sex_data = male.merge(female, how='left', left_on='Year', right_on='Year')
    sex_data = sex_data.rename(columns={'count':'Female'})
    sex_data['Female'].fillna(0, inplace=True)
    sex_data['Female'] = sex_data['Female'].astype('int')
    fig = px.line(sex_data, x='Year', y=['Male', 'Female'])

    st.plotly_chart(fig)