import streamlit as st
import pandas as pd
import pydeck as pdk
import geopandas as gpd



data = pd.read_csv('e:\\Data\\2017-18-crdc-data\\2017-18 Public-Use Files\\Data\\LEA\\CRDC\\CSV\\LEA Characteristics.csv', encoding='cp1252')
data['LEAID'] = data['LEAID'].astype(str)
data['LEAID'] = data['LEAID'].apply(lambda x: str(x)[2:].lstrip('0'))
data2 = pd.read_excel('e:\\Data\\ussd17.xls', skiprows=2)
data2.rename(columns={data2.columns[-1]: "Children in Poverty", 'District ID': 'LEAID', 'State Postal Code': 'LEA_STATE'}, inplace=True)
data2['LEAID'] = data2['LEAID'].astype(str)
gdf = gpd.read_file('e:\Data\EDGE_GEOCODE_PUBLICLEA_1718\EDGE_GEOCODE_PUBLICLEA_1718\EDGE_GEOCODE_PUBLICLEA_1718.shp')
gdf['LEAID'] = gdf['LEAID'].apply(lambda x: str(x)[2:].lstrip('0'))
gdf.rename(columns={'STATE': 'LEA_STATE', 'ZIP': 'LEA_ZIP'}, inplace=True)
merged_data = pd.merge(data[['LEAID', 'LEA_STATE', 'LEA_ZIP', 'LEA_ENR']], data2[['LEAID', 'LEA_STATE','Children in Poverty']], on=['LEAID', 'LEA_STATE'])
merged_data = pd.merge(merged_data, gdf[['LEAID', 'LEA_STATE', 'LEA_ZIP', 'LAT', 'LON']], on=['LEAID', 'LEA_STATE', 'LEA_ZIP'])


st.write("""
# My first app
Hello *world*
""")

st.dataframe(data2)


chart_data = merged_data

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=98,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[LON, LAT]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[LON, LAT]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))