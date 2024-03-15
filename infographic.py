import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
#######################
# Page configuration
st.set_page_config(
    page_title="Accident Analysis Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.title("Accident Analysis Dashboard")

injuries=pd.read_csv('road_accident_data_by_severity_of_injuries_2012.csv',nrows=25).drop(columns='Total')
vehicles=pd.read_csv('road_accident_data_by_vehicle_type_2012.csv',nrows=25).drop(columns='Total')
records_2012=injuries.merge(vehicles,on='Location',how='inner')
records_2012['Year']=2012

injuries=pd.read_csv('road_accident_data_by_severity_of_injuries_2011.csv',nrows=25).drop(columns='Total')
vehicles=pd.read_csv('road_accident_data_by_vehicle_type_2011.csv',nrows=25).drop(columns='Total')
records_2011=injuries.merge(vehicles,on='Location',how='inner')
records_2011['Year']=2011

injuries=pd.read_csv('roadaccidentdatabyseverityofinjuries2010.csv',nrows=25).drop(columns='Total')
injuries.rename(columns={'Districts': 'Location'}, inplace=True)
vehicles=pd.read_csv('road_accident_data_by_vehicle_type_2010.csv',nrows=25).drop(columns='Total')
records_2010=injuries.merge(vehicles,on='Location',how='inner')
records_2010['Year']=2010

all_records = pd.concat([records_2010, records_2011, records_2012])
all_records.Location=all_records.Location.str.strip()
all_records=all_records.sort_values(by='Location')
all_records=all_records.reset_index(drop=True).set_index('Location')
all_columns=all_records.columns

col0,col2 = st.columns((2))

year_options = ['All', 2010, 2011, 2012]
selected_year = st.sidebar.multiselect("Enter Year", year_options)
if 'All' in selected_year:
    all_records_year = all_records
else:
    all_records_year = all_records[all_records['Year'].isin(selected_year)]

location_options = ['All'] + list(all_records.index.unique())
selected_location = st.sidebar.multiselect("Select Locations", location_options, default=['All'])
if 'All' in selected_location:
    all_records_location = all_records_year
else:
    all_records_location = all_records_year.loc[selected_location]



vehicle_options = ['All'] + list(all_records.columns[6:-1])
selected_vehicle = st.sidebar.multiselect("Select Vehicle", vehicle_options, default=['All'])
if 'All' in selected_vehicle:
    all_records_vehicle = all_records_location[list(all_records.columns[6:-1])]
else:
    all_records_vehicle = all_records_location[selected_vehicle]

vehicles=all_records_vehicle.sum(axis=1)
vehicles = pd.concat([vehicles,all_records_location['Year']],axis=1).reset_index()
vehicles.rename(columns={0: 'Vehicle Accident'}, inplace=True)


sri_lanka_mapping = {
    "Western": ["Colombo", "Gampaha", "Kalutara"],
    "Central": ["Kandy", "Matale", "Nuwara Eliya"],
    "Southern": ["Galle", "Matara", "Hambantota","Tangalle"],
    "Northern": ["Jaffna", "Kilinochchi", "Mannar", "Mullativ", "Vavuniya"],
    "Eastern": ["Trincomalee", "Batticaloa", "Ampara"],
    "North Western": ["Kurunegala", "Puttalam","Chilaw"],
    "North Central": ["Anuradhapura", "Polonnaruwa"],
    "Uva": ["Badulla", "Monaragala"],
    "Sabaragamuwa": ["Kegalle", "Ratnapura"]
}
def map_location_to_state(location):
    for state, districts in sri_lanka_mapping.items():
        if location in districts:
            return state

vehicles['State'] = vehicles['Location'].apply(map_location_to_state)
statewise_accidents = vehicles.groupby('State')['Vehicle Accident'].sum().reset_index()
# st.write(vehicles)
# st.write(statewise_accidents)


with col0:
    # # # Create the clustered bar chart
    fig = px.bar(vehicles, x=vehicles['Location'], y='Vehicle Accident', color='Year', barmode='group')


    # # Update layout
    fig.update_layout(
        title='Location Vs Vehicle Type',
        xaxis_title='Location',
        yaxis_title='Count'
    )
    st.metric(label='Total Vehicles Count', value=vehicles['Vehicle Accident'].sum(axis=0))

    # Show the plot
    st.plotly_chart(fig)


    # st.write('vehicles',all_records_vehicle.sum(axis=0))
    fig = px.pie(all_records_vehicle.sum(axis=0), values=0, names=all_records_vehicle.sum(axis=0).index, title='Vehicle Accident Distribution')
    st.plotly_chart(fig)

with col0:
    st.markdown("State Wise Vehicle Accident")

    st.dataframe(statewise_accidents,
                    column_order=("State", 'Vehicle Accident'),
                    hide_index=True,
                    width=None,
                    column_config={
                    "State": st.column_config.TextColumn(
                        "State",
                    ),
                    'Vehicle Accident': st.column_config.ProgressColumn(
                        "Vehicle Accident",
                        format="%f",
                        min_value=0,
                        max_value=max(vehicles['Vehicle Accident']),
                        )}
                    )

injury_options = ['All'] + list(all_records.columns[:6])
selected_injury = st.sidebar.multiselect("Select Injury", injury_options, default=['All'])
if 'All' in selected_injury:
    all_records_injury = all_records_location[list(all_records.columns[:6])]
else:
    all_records_injury = all_records_location[selected_injury]

injuries=all_records_injury.sum(axis=1)
injuries = pd.concat([injuries,all_records_location['Year']],axis=1).reset_index()
injuries.rename(columns={0: 'Injuries Occured'}, inplace=True)

injuries['State'] = injuries['Location'].apply(map_location_to_state)
statewise_injuries = injuries.groupby('State')['Injuries Occured'].sum().reset_index()
# st.write(vehicles)
# st.write(statewise_accidents)



with col2:

    # # # Create the clustered bar chart
    fig = px.bar(injuries, x=injuries['Location'], y='Injuries Occured', color='Year', barmode='group')


    # # Update layout
    fig.update_layout(
        title='Location Vs Injury Type',
        xaxis_title='Location',
        yaxis_title='Count'
    )

    st.metric(label='Total Injuries Count', value=injuries['Injuries Occured'].sum(axis=0))

    # Show the plot
    st.plotly_chart(fig)
    
    fig = px.pie(all_records_injury.sum(axis=0), values=0, names=all_records_injury.sum(axis=0).index, title='Injury Accident Distribution')
    st.plotly_chart(fig)

with col2:

    st.markdown("State Wise Injuries")
    st.dataframe(statewise_injuries,
                column_order=("State", 'Injuries Occured'),
                hide_index=True,
                width=None,
                column_config={
                "State": st.column_config.TextColumn(
                    "State",
                ),
                'Injuries Occured': st.column_config.ProgressColumn(
                    "Injuries Occured",
                    format="%f",
                    min_value=0,
                    max_value=max(injuries['Injuries Occured']),
                    )}
                )

    

