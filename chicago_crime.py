import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import json
import plotly.express as px

#Load and Cache function
@st.cache_data
def load_data(filepath):
    if filepath.endswith('.csv'):
        data = pd.read_csv(filepath) 
    elif filepath.endswith('.parquet'):
        data = pd.read_parquet(filepath)
    elif filepath.endswith('.json'):
        data = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format. Supported formats are CSV, Parquet, and JSON.")
    return data

# Define the crime_analysis function
def crime_analysis():
    st.subheader('Overview of Crime in Chicago')

    st.write('''
    
    This page serves as an overview and how it is distrubted in terms of category and time.
    ''')

    #Load Data
    filepath_line_1 = 'data/data_cache/1_top_10_crimes_per_year.parquet'
    filepath_bar_1 = 'data/data_cache/1b_crime_count_total_amount.csv'
    filepath_bar_2 = 'data/data_cache/1a_average_crimes_per_hour.parquet'
    
    df_line_1 = load_data(filepath_line_1)
    df_bar_1 = load_data(filepath_bar_1)
    df_bar_2 = load_data(filepath_bar_2)

    #Bar 1
    pivot_bar1 = df_bar_1.pivot_table(index='Primary Type', values='count', aggfunc='sum')
    top_crimes1 = pivot_bar1.nlargest(35, 'count')

    # Plotting the first bar chart
    fig_bar1, ax_bar1 = plt.subplots(figsize=(10, 6))
    top_crimes1.plot(kind='bar', ax=ax_bar1, color='skyblue')
    ax_bar1.set_title('Total Crime Counts by Type (Top 15)')
    ax_bar1.set_ylabel('Total Counts')
    ax_bar1.set_xlabel('Crime Type')
    ax_bar1.tick_params(axis='x', rotation=90)
    ax_bar1.grid(True)
    ax_bar1.legend(title='Crime Type', loc='upper left', bbox_to_anchor=(1, 1))  # Places the legend outside the plot
    plt.tight_layout()

    st.pyplot(fig_bar1)

    #Bar 1 Discuss
    st.write("""
    Above we can see all the major categories that are tracked by Chicago Police Department.
    We can clearly see the majority of all crime is concentrated into just a few categories.
    Crimes such as theft current top over 1.5 million reports or roughly 20.5% of overall reports. Other crimes such as obscenity only account 
    for a very small part counting in at 786 reports, 0.0001%.

    """)

    #Bar 2
    pivot_bar2 = df_bar_2.pivot_table(index='Hour', values='Average', aggfunc='mean')

    fig_bar2, ax_bar2 = plt.subplots(figsize=(10, 6))
    pivot_bar2.plot(kind='bar', ax=ax_bar2, color='skyblue')
    ax_bar2.set_title('Average Crimes per Hour')
    ax_bar2.set_ylabel('Average Number of Crimes')
    ax_bar2.set_xlabel('Hour')
    ax_bar2.tick_params(axis='x', rotation=0)
    ax_bar2.grid(True)
    ax_bar2.legend(title='Crime Type', loc='upper left', bbox_to_anchor=(1, 1))  # Places the legend outside the plot
    plt.tight_layout()

    st.pyplot(fig_bar2)

    #Bar 2 Discuss
    st.write("""

    In the graph above we can see the distribution of crime over a 24h period. Proving all to well crime never sleeps.
    The distribution of crime throughout the day is to be expected to high's during the day and a steady drop during the evening.

    In the data we can see two spikes at 12:00 and 00:00, from the data it appears to be a software scheduling of some sort,
    or a change of shift. The data clear shows an abnormal amount of reports specifically at this two times.

    Below you can select, view the top crimes more closely.

    """)

    #Line Graph Multi Select
    crime_types_line = df_line_1['Primary Type'].unique()
    selected_types_line = st.multiselect('Select crime types to display for line graph:', crime_types_line, default=crime_types_line[:3])  # Default to top 3 types

    if selected_types_line:
        st.subheader('Crime Trend Analysis')

        filtered_data_line = df_line_1[df_line_1['Primary Type'].isin(selected_types_line)]

        pivot_data_line = filtered_data_line.pivot_table(index='Year', columns='Primary Type', values='Count', aggfunc='sum')

        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_data_line.plot(kind='line', ax=ax)
        ax.set_title('Top 10 Crimes per Year by Commited offence')
        ax.set_ylabel('Number of Crimes')
        ax.set_xlabel('Year')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        ax.legend(title='Crime Type', loc='upper left', bbox_to_anchor=(1, 1)) # <-- Legend outside anchor

        plt.tight_layout()

        st.pyplot(fig)

    #Line Graph Discuss
    st.subheader('Findings')
    st.write("""
    
    There are two interesting datapoints that are very visable. 

    1. The overall drop in drug related crime in Chicago, this is despite any amount of drugs is considered an offence. On
    further inverstigation via these articles:

    - [Article One](https://www.chicagoappleseed.org/2022/06/15/dynamics-of-drug-possession-charges-in-illinois/)
    - [Article Two](https://chicago.suntimes.com/2021/11/26/22639255/dead-end-drug-arrests-drugs-possession-chicago)
    - [Article Three](https://chicago.suntimes.com/2022/11/10/23444935/drug-possession-jail-safe-t-act-pretrial-fairness-watchdogs-law-enforcement-cook-county-editorial)
    - [Article Four](https://news.wttw.com/2021/12/07/sun-times-bga-report-reveals-costly-toll-dead-end-drug-arrests)
    """)
    st.write("""         
    We can conclude:
             
    1. The majority off all drug arrests are dropped roughly 86%.
    2. The opiod crisis, led to prescription drugs, making it harder for the police to take it away from you.
    3. Marijuana is now legal in Chicago 2022. It is by far the most used drugs by the overall population.
    4. Data also suggests the African Americans prefer marijuana over opiods, leading to less arrests as it's lower class drug.

    In short, it's just not worth the effort to persue misdemeanor offence, in a city where crime is just so high.

    2. Secondly we can look at the spike in "Motor Vehicle Theft"  during and after 2020, the USA saw an increase 
    in car prices as high as 63% over Manufacturer's Suggested Retail Price (MSRP). It's estimated car used car prices
    still sit at roughly 32% above the norm. This can be attributed to the decrease in newer cars being produced as shortages 
    in crucial car parts become unavailable. Car manufacturers started producing less featured cars as a response but were unable to meet demand.

    """)


def crime_covid():
    filepath_bar_1 = 'data/data_cache/3_crime_counts_covid_19.csv'
    filtered_df = load_data(filepath_bar_1)

    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

    filtered_df.set_index('Date', inplace=True)

    lockdown_date = pd.to_datetime('2020-03-31')
    end_lockdown_date = pd.to_datetime('2022-03-31')

    lockdown_count = filtered_df.loc[lockdown_date, 'Count']
    end_lockdown_count = filtered_df.loc[end_lockdown_date, 'Count']

    # Plotting using Streamlit's plotting capabilities
    st.write("## Number of Reports per Month")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_df.index, filtered_df['Count'], marker='o')
    ax.set_title('Number of Reports per Month')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Reports')

    #Lockdown start
    ax.annotate('Lockdown', xy=(lockdown_date, lockdown_count), xytext=(lockdown_date, lockdown_count + 4100),
                arrowprops=dict(arrowstyle='-', linestyle=' ', color='red'), ha='left')
    ax.axvline(x=lockdown_date, color='red', linestyle='--', linewidth=1)

    #Lockdown end
    ax.annotate('Lockdown Ended', xy=(end_lockdown_date, end_lockdown_count), xytext=(end_lockdown_date, end_lockdown_count + 2700),
                arrowprops=dict(arrowstyle='-', linestyle=' ', color='green'), ha='right')
    ax.axvline(x=end_lockdown_date, color='green', linestyle='--', linewidth=1)

    ax.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

    st.subheader('Findings Discussion')
    st.write("""
             
    Overall drop and recovery during and after Covid:
             
        Percentage Change During Lockdown: -39.77%
        Percentage Change After Lockdown: 24.87%
             
    The graph clearly demonstrates that covid had a massive effect on crime rates in Chicago dropping to an all time low.

    In a study by published the College of the Holy Cross by Olivia DiMonte, Advisor: Professor Baumann. On a study of covid in Chicago, Houston, they were able to
    conclude that for every one case of covid in Chicago crime reports fell by 0.25. It should be noted this applies to overall crime
    however there were noticable increases in crime such as domestic abuse and acts of non-consensual sex.
    """)


def add_tooltip(feature, layer):
    community_area = feature['properties']['Community Area']
    total_crimes = feature['properties']['Total Crimes'] if 'Total Crimes' in feature['properties'] else 'N/A'
    layer.add_child(folium.Popup(f"Community Area: {community_area}<br>Total Crimes: {total_crimes}"))


def community_crime_overview():

    st.subheader('Visual Overview of Crime')

    st.write("""
    Here we are just looking at exploring the overl distrubtion of crime throught the city. In the bar graph below, we can see a general distrubtion across all 76
    communities, with several communities being the outliers with abnormally high reports rates. Community area 25, soars over all other areas.

    """)

    #Load Data
    filepath_crimes_by_community = 'data/data_cache/2_crimes_by_community_area.parquet'
    filepath_crimes_by_count_yearly = 'data/data_cache/2b_crime_counts_every_year_community.parquet'
    
    crimes_by_year = load_data(filepath_crimes_by_count_yearly)
    crimes_by_community_area = load_data(filepath_crimes_by_community)

    st.subheader('Crime Across City')

    #Bar 1
    pivot_data_community = crimes_by_community_area.pivot_table(index='Community Area', values='Total Crimes', aggfunc='sum')

    fig_community, ax_community = plt.subplots(figsize=(12, 8))
    pivot_data_community.plot(kind='bar', ax=ax_community, color='skyblue')
    ax_community.set_title('Crime Counts by Community Area')
    ax_community.set_ylabel('Total Counts')
    ax_community.set_xlabel('Community Area')
    ax_community.tick_params(axis='x', rotation=90)
    ax_community.grid(True)
    plt.tight_layout()

    st.pyplot(fig_community)

    #Map 1
    st.title("Chicago Crime Map by Community Area")

    boundary_gdf = gpd.read_file('data/data_cache/chicago_boundaries.geojson')
    crimes_by_community_area['Community Area'] = crimes_by_community_area['Community Area'].astype(int)
    boundary_gdf['area_num_1'] = boundary_gdf['area_num_1'].astype(int)
    merged_gdf = boundary_gdf.merge(crimes_by_community_area, left_on='area_num_1', right_on='Community Area', how='left')

    map_chicago_1 = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

    choropleth_layer = folium.Choropleth(
        geo_data=merged_gdf.to_json(),
        name='choropleth',
        data=merged_gdf,
        columns=['area_num_1', 'Total Crimes'],
        key_on='feature.properties.area_num_1',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Crimes per Community Area'
    ).add_to(map_chicago_1)

    choropleth_layer.geojson.add_child(folium.features.GeoJsonTooltip(['Community Area', 'Total Crimes'], aliases=['Community Area', 'Total Crimes']))

    folium_static(map_chicago_1)

    st.write('''
    
    Below you can explore the data year for year, however it quickly becomes evident that despite the dataset
    spanning over 20+ years, there are several key communities responisble for nearly all crime.

    ''')

    #Map 2 user select
    selected_year = st.selectbox("Select Year", sorted(crimes_by_year.columns[:-1], reverse=True), index=1)
    selected_year_data = crimes_by_year[['Community Area', selected_year]].copy()
    merged_gdf_year = boundary_gdf.merge(selected_year_data, left_on='area_num_1', right_on='Community Area', how='left')
    
    map_chicago_2 = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

    choropleth_layer_year = folium.Choropleth(
        geo_data=merged_gdf_year.to_json(),
        name='choropleth',
        data=merged_gdf_year,
        columns=['area_num_1', selected_year],
        key_on='feature.properties.area_num_1',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Total Crimes per Community Area ({selected_year})'
    ).add_to(map_chicago_2)

    choropleth_layer_year.geojson.add_child(folium.features.GeoJsonTooltip(['Community Area', selected_year], aliases=['Community Area', 'Total Crimes']))

    folium_static(map_chicago_2)


def create_community_pie_chart(community_df, selected_community):
    # Filter data for the selected community
    community_data = community_df[community_df['COMMUNITY_AREA'] == selected_community]

    # Create pie chart
    fig = px.pie(community_data, names=['Homicides', 'Shootings'], values=['Homicides', 'Shootings'], title=f'Distribution of Shootings and Fatalities in {selected_community}')
    
    st.plotly_chart(fig)
    
def shootings_fatalities():
    st.subheader('Shootings across Chicago')
    
    boundary_gdf = gpd.read_file('data/data_cache/chicago_boundaries.geojson')
    community_df = pd.read_parquet('data/data_cache/4a_shootings_and_deaths.parquet')

    merged_gdf = boundary_gdf.merge(community_df, left_on='community', right_on='COMMUNITY_AREA', how='left')

    #Map
    map_community = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

    choropleth_layer = folium.Choropleth(
        geo_data=merged_gdf.to_json(),
        name='choropleth',
        data=merged_gdf,
        columns=['community', 'Homicides'],  # Change columns accordingly
        key_on='feature.properties.community',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Homicides per Community Area'
    ).add_to(map_community)

    #Map Data
    choropleth_layer.geojson.add_child(folium.features.GeoJsonTooltip(['community', 'Homicides'], aliases=['Community Area', 'Homicides']))

    folium_static(map_community)

    st.write('''
    In the map above, you can clearly see that the same areas tended to be highlighy regardless of the 
    data being visualised. Map shows all homicides, shootings leading in death since 1991, however it should be
    noted that non fatal shooting were not recorded until 2010. 

    Below you can dive deeper into the data looking at Age, Sex and Race of all victims fatal and non fatal
    for each community area.

    ''')


    st.subheader('Explore Community Victim Details')

    csv_data = pd.read_csv('data/data_cache/4_alt_victim_counts_with_overview.csv')

    #User Select
    community_areas = csv_data['COMMUNITY_AREA'].unique()
    selected_area = st.selectbox('Select a Community Area:', community_areas)

    community_filtered_data = csv_data[csv_data['COMMUNITY_AREA'] == selected_area]

    #Community 0
    if not community_filtered_data.empty:
        # Allow the user to select the attribute for further analysis
        selected_attribute = st.selectbox('Select Attribute for Analysis:', ['Age', 'Sex', 'Race'])

        if selected_attribute == 'Age':
            # Create and display a pie chart for Age distribution
            fig_age = px.pie(community_filtered_data, names='AGE', values='Count', title='Distribution of Victims by Age')
            st.plotly_chart(fig_age)

        elif selected_attribute == 'Sex':
            # Create and display a pie chart for Sex distribution
            fig_sex = px.pie(community_filtered_data, names='SEX', values='Count', title='Distribution of Victims by Sex')
            st.plotly_chart(fig_sex)

        elif selected_attribute == 'Race':
            # Create and display a pie chart for Race distribution
            fig_race = px.pie(community_filtered_data, names='RACE', values='Count', title='Distribution of Victims by Race')
            st.plotly_chart(fig_race)

        else:
            st.write('Invalid attribute selected.')

    else:
        st.write('No victim data available for the selected community area.')

def conclusion():
    st.title("Conclusion")

    st.write('''
    In conclusion, our data exploration allowed us to confidently answer the questions we set out to investigate. Although crime rates in Chicago remain overwhelmingly high, certain tourist-heavy neighborhoods are comparatively safer. Unfortunately, due to the structure of the dataset, it is difficult to analyze how crime spills over into surrounding communities—particularly those with a high African American population—limiting our ability to assess broader spatial trends.
    The Chicago Crime dataset itself is extremely unique and, as far as we know, is the only publicly accessible and frequently updated source of this scale. It provides insights into how crime responds to seasons, world events, and demographic factors. For instance, we observed that overall crime fell by around 15 percent during the COVID-19 pandemic—yet some categories like sexual assault rose by 41%. Such findings highlight how global events can drive crime trends, though not uniformly across all categories.
    
    Moreover, according to the data, African Americans comprise a majority of offenders despite representing only about 28 percent of the city’s population (as of 2023). These trends speak to deeper social factors that data alone cannot fully explain.
    
    Data Gaps: Some geospatial analyses are hindered by missing values, which require extra preprocessing.
    Data Size: With over 8 million records, the dataset can be too large for certain visualization libraries or standard computing resources.
    Despite these constraints, the dataset remains both robust and remarkably informative, offering significant potential for further research and even machine-learning applications in crime forecasting.

    ''')

def welcome():
    st.title("Analysis of Crime in Chicago")

    st.write("""
    In this project I will be using the a publicly accessible [DATASET](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data) by the City of Chicago via the 
    [Chicago Data Portal](https://data.cityofchicago.org). The dataset contains over 8 million recorded crimes and is updated a on weekly basis. Due to the share amount of gun crime in Chicago, 
    they maintain a separate and comprehensive [DATASET](https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Victims-of-Homicides-and-Non-Fa/gumc-mgzr/about_data) on shootings across the city, 
    seeing an average of one shooting per two hours. Since 2019 only seven days without a shooting have been recorded. 

    The main question I sought to answer were:

    1. How was crime change over the last 20 years?
    2. Why have narcotic crimes decreased over time despite high drug use?
    3. How is crime distributed across the city?
    4. How did Covid affect crime rates?
    5. Distribution of shootings?

    The majority of the pages on the left are interactive allowing you explore the data yourself.

    """)

def main():
    #User Select
    page_selection = st.sidebar.radio("Navigate to Different Pages:", ("Welcome", "Crime Analysis", "Crime During Covid", "Visual Overview of Crime", "Victims of Shootings", 'Conclusion'))

    if page_selection == "Welcome":
        welcome()
    elif page_selection == "Crime Analysis":
        crime_analysis()
    elif page_selection == "Crime During Covid":
        crime_covid()
    elif page_selection == "Visual Overview of Crime":
        community_crime_overview()
    elif page_selection == "Victims of Shootings":
        shootings_fatalities()
    elif page_selection == "Conclusion":
        conclusion()

if __name__ == '__main__':
    main()
