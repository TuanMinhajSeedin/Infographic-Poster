import geopandas as gpd
import plotly.express as px
import streamlit as st
import json
import pandas as pd

# Load Sri Lankan GeoJSON data
with open("geoBoundaries-LKA-ADM0_simplified.geojson", "r") as f:
    geojson_data = json.load(f)

# Sample DataFrame
districts = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya', 'Galle', 'Matara', 'Hambantota',
    'Jaffna', 'Kilinochchi', 'Mannar', 'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla', 'Monaragala', 'Ratnapura', 'Kegalle'
]

population = [100000, 150000, 80000, 120000, 90000, 80000, 110000, 95000, 85000, 75000, 60000, 50000, 45000,
              40000, 85000, 90000, 75000, 130000, 75000, 140000, 65000, 100000, 90000, 110000, 120000]

input_df = pd.DataFrame({'District': districts, 'Population': population})

# Column containing district names
input_id = 'District'

# Column containing the data to be visualized
input_column = 'Population'

# Color theme for the choropleth map
input_color_theme = 'darkmint'

# Create choropleth map
choropleth = px.choropleth_mapbox(
    input_df,
    geojson=geojson_data,
    locations=input_id,
    featureidkey="properties.shapeID",  # Adjust based on your GeoJSON structure
    color=input_column,
    mapbox_style="carto-positron",
    zoom=7,
    center={"lat": 7.87, "lon": 80.77},  # Centered on Sri Lanka
    opacity=0.5,
    color_continuous_scale=input_color_theme,
    labels={'population': 'Population'}
)

# Display the choropleth map
st.plotly_chart(choropleth)
