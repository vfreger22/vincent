"""
Name: Vincent Freger
CS230: Section 6
Data: Blue Bikes
URL: I attempted, could not figure out how to publish to streamlit cloud.
Description: This program gives an overall summary of the bluebikes.csv spreadsheet from Analyze Boston.
Users are able to look at various aspects of bike station distribution, deployments, and statistics. There are
various key features, such as filtering stations by available docks, deployment trends per year, visuals and counts.
Users are able to actively explore Blue Bikes information, and it is a comprehensive way to understand it as a whole.
"""
# Import Necessary Packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
# Loads the dataset
data = pd.read_csv('bluebikes.csv')
#Sets streamlit page configuration
st.set_page_config(page_title="Blue Bikes Analysis", page_icon=":bike:")
st.title("Vincent Freger's CS 230 Final Project")
st.subheader("Analyzing Blue Bikes Data")
st.markdown("Explore the distribution of bike stations and their statistics.")
# Function creates a pie chart that shows the distributions of bike stations by city
def stations_by_town_pie_chart(data):
    town_counts = data['District'].value_counts()
    st.subheader('Distribution of Bike Stations by Town')
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(town_counts, labels=town_counts.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(fig)
# Function creates a bar chart, showing the number of blue bike stations in each districy
def stations_by_district_bar_chart(data):
    district_counts = data['District'].value_counts().reset_index()
    district_counts.columns = ['District', 'Station Count']
    # Create a Plotly bar chart
    fig = px.bar(district_counts, x='District', y='Station Count')
    fig.update_layout(
        title='Number of Bike Stations in Each District',
        xaxis_title='District',
        yaxis_title='Station Count')
    st.plotly_chart(fig)
# Function displays a map, filtering bike stations based on city input in select box
def stdmap(data):
    # Sidebar filters stations by district
    dictlist = data['District'].astype(str)
    district = sorted(dictlist.unique())
    global location
    st.sidebar.title('Filter Stations')
    location = st.sidebar.selectbox('Choose a City:',district)
    df_filtered = data[data['District'] == location][['Name','District', 'LATITUDE','LONGITUDE']]
    st.write('Check out the', location,'blue bike stations')
    st.dataframe(df_filtered.sort_values('District', ascending= True))
    st.subheader('Where can you find them?')
    st.map(df_filtered, size=1,color='#0044ff')
 #Function for filtering stations by district
def filter_by_district(selected_district):
    filtered_data = data[data['District'] == selected_district]
    return filtered_data
# Function for filtering stations by available docks
def filter_by_docks(min_docks):
    filtered_data = data[data['Total docks'] >= min_docks]
    return filtered_data
# Function for deploying stations per year
def stations_deployed_per_year():
    deploy_year_counts = data['Deployment Year'].value_counts().sort_index()
    return deploy_year_counts
# Function counts stations in each district
def district_station_counts(data):
    district_counts = {district: len(data[data['District'] == district]) for district in data['District'].unique()}
    return district_counts
# Function sorts data by a specific column
def sort_data_by_column(column_name):
    sorted_data = data.sort_values(by=column_name)
    return sorted_data
def main():
    # Streamlit Elements
    st.title('Bike Station Analysis')
    st.sidebar.title('Filter Stations')
    min_docks = st.sidebar.slider('Minimum Available Docks', min_value=0, max_value=data['Total docks'].max(), value=0)
    stdmap(data)
    selected_district = location
    st.subheader(f'Bike Stations in {selected_district}')
    # Filters stations by available docks
    filtered_by_docks = filter_by_docks(min_docks)
    st.write(filtered_by_docks)
    # Displays number of stations deployed per year
    st.subheader('Number of Stations Deployed per Year')
    deploy_year_counts = stations_deployed_per_year()
    st.bar_chart(deploy_year_counts)
    st.subheader(f'Plot of locations of Stations available with at least {min_docks} docks')
    plt.figure(figsize=(20, 50))
    plt.title('Stations Deployed per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Stations')
    fig, ax = plt.subplots()
    ax.scatter(filtered_by_docks['LONGITUDE'], (filtered_by_docks['LATITUDE']))
    st.pyplot(fig)
    # Visualizations
    stations_by_town_pie_chart(data)
    district_counts = district_station_counts(data)
    st.write('District-wise Station Counts:')
    st.write(district_counts)
    sorted_data = sort_data_by_column('Deployment Year')
    st.write('Sorted data by Deployment Year:')
    st.write(sorted_data)
    stations_by_district_bar_chart(data)
# Execution of the main function
if __name__ == '__main__':
    main()