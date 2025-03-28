# Chicago Crime Analysis

A Streamlit-based data analysis project using publicly available Chicago crime datasets. This application enables interactive visualization and exploration of crime trends, including hour-by-hour breakdowns, distribution across community areas, shootings and fatalities, and the impact of COVID-19 on crime rates.

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Data Sources](#data-sources)  
4. [Installation](#installation)  
5. [Project Structure](#project-structure)  
6. [Usage](#usage)  
7. [License](#license)

---

## Overview
Chicago has one of the most detailed and frequently updated public crime datasets in the world. This project downloads and preprocesses that dataset, then uses **Streamlit** to generate interactive charts and maps. Topics covered include:
- Hourly crime trends  
- Overall crime distribution by type  
- Geospatial analysis of crime across community areas  
- Effects of COVID-19 on crime rates  
- Detailed breakdown of shootings and fatalities  

---

## Features
- **Interactive Bar Charts & Line Graphs**  
  Explore crime rates by type and year.
- **Choropleth Maps**  
  View city-wide crime distribution and hot spots using Folium maps.
- **Community Area Drilldowns**  
  Check out which neighborhoods have the highest or lowest rates of reported offenses.
- **COVID-19 Impact**  
  Understand how global events (in this case, the COVID-19 pandemic) affected crime trends.

---

## Data Sources
1. [Crimes — 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)  
2. [Victims of Homicides and Non-Fatal Shootings](https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Victims-of-Homicides-and-Non-Fa/gumc-mgzr)  
3. [Chicago Community Boundaries (GeoJSON)](https://data.cityofchicago.org/d/bb7r-5n3h)

**Note:**  
- Datasets are quite large (~8M+ rows). Certain visualizations or analyses may require efficient data handling.  
- Some code references local paths in a `data/data_cache/` folder. You must either replicate that structure or adjust file paths accordingly.

---

## Installation
1. **Clone the Repository**  
   ```bash
   git clone git@github.com:<YOUR_USERNAME>/Chicago_crime_analysis.git
   cd Chicago_crime_analysis
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
---

## Project Structure

Example folder layout:
```
Chicago_crime_analysis/
│
├─ data/
│   └─ data_cache/
│       ├─ 1_top_10_crimes_per_year.parquet
│       ├─ 1b_crime_count_total_amount.csv
│       ├─ 1a_average_crimes_per_hour.parquet
│       ├─ 2_crimes_by_community_area.parquet
│       ├─ 2b_crime_counts_every_year_community.parquet
│       ├─ 3_crime_counts_covid_19.csv
│       ├─ 4a_shootings_and_deaths.parquet
│       ├─ 4_alt_victim_counts_with_overview.csv
│       └─ chicago_boundaries.geojson
│
├─ chicago_crime.py        # Main Python script with Streamlit app
├─ requirements.txt        # Python dependencies
└─ README.md               # Project readme
```

---

## Usage
1. **Run the Streamlit App**  
   ```bash
   streamlit run chicago_crime.py
   ```
2. **Navigate to the Web Interface**  
   - By default, Streamlit launches on `http://localhost:8501`.  
   - Use the left-hand sidebar to navigate between different pages:  
     - **Welcome**  
     - **Crime Analysis**  
     - **Crime During Covid**  
     - **Visual Overview of Crime**  
     - **Victims of Shootings**  
     - **Conclusion**  

3. **Explore the Data**  
   - Interact with multi-select widgets, sliders, and drop-downs to filter crimes by type, year, and community area.  
   - Hover over charts or map markers for additional data.  

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to adapt or extend it for your own needs, but please note that the Chicago Crime dataset may have its own usage terms. Always check the source for any additional restrictions.
