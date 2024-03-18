import streamlit as st
import pandas as pd
import altair as alt
st.set_page_config(page_title="Gun Violence in America" ,layout="wide")

class PolicePresenceBarChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        year_range = st.slider('Select Year Range:', min_value=2012, max_value=2014, value=(2012, 2014), key='year_range_slider')
        
        location_options = ['All'] + list(self.data['place'].unique())
        selected_location = st.selectbox('Select Location:', location_options, index=0, key='location_selectbox')

        # Filter data based on selected filters
        filtered_data = self.data.copy()
        filtered_data = filtered_data[(filtered_data['year'] >= year_range[0]) & (filtered_data['year'] <= year_range[1])]
        if selected_location != 'All':
            filtered_data = filtered_data[filtered_data['place'] == selected_location]

        # Aggregate data by police presence
        police_counts = filtered_data['police'].value_counts().reset_index()
        police_counts.columns = ['Police Presence', 'Count']

        # Create the bar chart using Altair
        bar_chart = alt.Chart(police_counts).mark_bar().encode(
            x=alt.X('Police Presence:N', title='Police Presence'),
            y=alt.Y('Count:Q', title='Count'),
            color=alt.Color('Police Presence:N', scale=alt.Scale(scheme='set1'), legend=None),
            tooltip=['Police Presence', 'Count']
        ).properties(
            width=600,
            height=400,
            title='Gun Violence Incidents by Police Presence'
        )

        return bar_chart

class GenderDistributionChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        year_range = st.slider('Select Year Range:', min_value=2012, max_value=2014, value=(2012, 2014), key='gender_year_range_slider')
        
        location_options = ['All'] + list(self.data['place'].unique())
        selected_location = st.selectbox('Select Location:', location_options, index=0, key='gender_location_selectbox')

        # Filter data based on selected filters
        filtered_data = self.data.copy()
        filtered_data = filtered_data[(filtered_data['year'] >= year_range[0]) & (filtered_data['year'] <= year_range[1])]
        if selected_location != 'All':
            filtered_data = filtered_data[filtered_data['place'] == selected_location]

        # Count the number of victims by gender
        gender_distribution = (
            filtered_data['sex'].value_counts().reset_index()
        )
        gender_distribution.columns = ['gender', 'count']

        # Create Altair chart
        chart = alt.Chart(gender_distribution).mark_bar().encode(
            x='gender:N',
            y='count:Q',
            color=alt.Color('gender:N', legend=None),
            tooltip=['gender:N', 'count:Q']
        ).properties(
            title='Gender Distribution of Victims'
        )

        return chart
    
class GunDeathDistributionByIntentAndRace:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        intent_options = ['All'] + list(self.data['intent'].unique())
        selected_intent = st.multiselect('Select Intent:', intent_options, default='All', key='intent_filter_grouped_bar')

        race_options = ['All'] + list(self.data['race'].unique())
        selected_race = st.multiselect('Select Race:', race_options, default='All', key='race_filter_grouped_bar')

        # Apply filters to the dataset
        filtered_df = self.data.copy()
        if 'All' not in selected_intent:
            filtered_df = filtered_df[filtered_df['intent'].isin(selected_intent)]
        if 'All' not in selected_race:
            filtered_df = filtered_df[filtered_df['race'].isin(selected_race)]

        # Aggregate data by intent, race, and gender
        intent_race_counts = filtered_df.groupby(['intent', 'race']).size().reset_index(name='count')

        # Create grouped bar chart
        grouped_bar_chart = alt.Chart(intent_race_counts).mark_bar().encode(
            x=alt.X('count:Q', title='Count'),
            y=alt.Y('race:N', sort='-x', title='Race'),
            color=alt.Color('intent:N', title='Intent', scale=alt.Scale(scheme='set2')),
            tooltip=['intent', 'race', 'count']
        ).properties(
            width=700,
            height=400
        )

        return grouped_bar_chart

class TrendByIntentAndEducationChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        intent_options = ['All'] + list(self.data['intent'].unique())
        selected_intent = st.multiselect('Select Intent:', intent_options, default='All', key='intent_filter')
        
        education_options = ['All'] + list(self.data['education'].unique())
        selected_education = st.multiselect('Select Education Level:', education_options, default='All', key='education_filter')

        # Apply filters to the dataset
        filtered_df = self.data.copy()
        if 'All' not in selected_intent:
            filtered_df = filtered_df[filtered_df['intent'].isin(selected_intent)]
        if 'All' not in selected_education:
            filtered_df = filtered_df[filtered_df['education'].isin(selected_education)]

        # Combine 'year' and 'month' columns into a single datetime column
        filtered_df['Date'] = pd.to_datetime(filtered_df['year'].astype(str) + '-' + filtered_df['month'].astype(str), format='%Y-%m')

        # Calculate the count of gun violence incidents over time
        trend_data = filtered_df.groupby(['Date', 'intent', 'education']).size().reset_index(name='count')

        # Create line chart
        line_chart = alt.Chart(trend_data).mark_line().encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('count:Q', title='Count'),
            color=alt.Color('intent:N', scale=alt.Scale(scheme='category10'), title='Intent'),
            tooltip=['Date', 'intent', 'count']
        ).properties(
            width=800,
            height=400,
            title='Trend of Gun Violence Incidents by Intent and Education Level Over Time'
        )

        return line_chart

class AgeVictimsScatterPlot:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        year_range = st.slider('Select Year Range:', min_value=2012, max_value=2014, value=(2012, 2014), key='age_victims_year_range_slider')
        
        intent_options = ['All'] + list(self.data['intent'].unique())
        selected_intent = st.multiselect('Select Intent:', intent_options, default='All', key='age_victims_intent_multiselect')

        # Apply filters to the dataset
        filtered_df = self.data.copy()
        filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
        if 'All' not in selected_intent:
            filtered_df = filtered_df[filtered_df['intent'].isin(selected_intent)]

        # Scatter plot showing the relationship between age and number of victims, colored by race
        scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x=alt.X('age:Q', title='Age'),
            y=alt.Y('num_victims:Q', title='Number of Victims'),
            color=alt.Color('race:N', scale=alt.Scale(scheme='category10'), title='Race'),
            tooltip=['age', 'num_victims', 'race']
        ).properties(
            width=700,
            height=400,
            title='Relationship between Age and Number of Victims, Colored by Race'
        )

        return scatter_plot

class IntentBarChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        year_range = st.slider('Select Year Range:', min_value=2012, max_value=2014, value=(2012, 2014), key='intent_bar_year_range_slider')
        
        location_options = ['All'] + list(self.data['place'].unique())
        selected_location = st.selectbox('Select Location:', location_options, index=0, key='intent_bar_location_selectbox')

        # Apply filters to the dataset
        filtered_df = self.data.copy()
        filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['place'] == selected_location]

        # Calculate the count of incidents by intent
        intent_counts = filtered_df['intent'].value_counts().reset_index()
        intent_counts.columns = ['Intent', 'Count']

        # Create the bar chart using Altair
        bar_chart = alt.Chart(intent_counts).mark_bar().encode(
            x=alt.X('Intent:N', title='Intent'),
            y=alt.Y('Count:Q', title='Count'),
            color=alt.Color('Intent:N', scale=alt.Scale(scheme='set1'), legend=None),
            tooltip=['Intent', 'Count']
        ).properties(
            width=600,
            height=400,
            title='Gun Violence Incidents by Intent'
        )

        return bar_chart

# Load the cleaned dataset
df = pd.read_csv('guns_cleaned.csv')

# Preprocess the data to calculate the number of victims
victim_counts = df.groupby('age').size().reset_index(name='num_victims')
df = pd.merge(df, victim_counts, on='age')

col1, col2 = st.columns(2)

with col1:
    # Display the chart using Streamlit
    police_presence_chart = PolicePresenceBarChart(df)
    st.caption('Gun Violence Incidents by Police Presence')
    bar_chart = police_presence_chart.generate_chart()
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    gender_chart = GenderDistributionChart(df)
    st.caption("Gender Distribution of Victims")
    gender_chart = gender_chart.generate_chart()
    st.altair_chart(gender_chart, use_container_width=True)

distribution_chart2 = GunDeathDistributionByIntentAndRace(df)
st.caption('Gun Death Distribution by Intent and Race')
distribution_chart2 = distribution_chart2.generate_chart()
st.altair_chart(distribution_chart2, use_container_width=True)

trend_by_intent_education_chart = TrendByIntentAndEducationChart(df)
st.caption('Trend of Gun Violence Incidents by Intent and Education Level Over Time')
line_chart = trend_by_intent_education_chart.generate_chart()
st.altair_chart(line_chart, use_container_width=True)

intent_chart = IntentBarChart(df)
st.caption('Gun Violence Incidents by Intent')
bar_chart = intent_chart.generate_chart()
st.altair_chart(bar_chart, use_container_width=True)

scatter_plot = AgeVictimsScatterPlot(df)
st.caption('Relationship between Age and Number of Victims, Colored by Race')
scatter_chart = scatter_plot.generate_chart()
st.altair_chart(scatter_chart, use_container_width=True)

