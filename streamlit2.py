import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import pydeck as pdk
import geopandas as gpd
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html



data = pd.read_csv('/Volumes/Untitled/Data-20231026T061813Z-001/Data/2017-18-crdc-data/2017-18 Public-Use Files/Data/LEA/CRDC/CSV/LEA Characteristics.csv', encoding='cp1252')

data['LEAID'] = data['LEAID'].astype(str)
data['LEAID'] = data['LEAID'].apply(lambda x: str(x)[2:].lstrip('0'))
data2 = pd.read_excel('/Volumes/Untitled/Data-20231026T061813Z-001/Data/ussd17.xls', skiprows=2)
data2.rename(columns={data2.columns[-1]: "Children in Poverty", 'District ID': 'LEAID', 'State Postal Code': 'LEA_STATE'}, inplace=True)
data2['LEAID'] = data2['LEAID'].astype(str)
gdf = gpd.read_file('/Volumes/Untitled/Data-20231026T061813Z-001/Data/EDGE_GEOCODE_PUBLICLEA_1718/EDGE_GEOCODE_PUBLICLEA_1718/EDGE_GEOCODE_PUBLICLEA_1718.shp')
gdf['LEAID'] = gdf['LEAID'].apply(lambda x: str(x)[2:].lstrip('0'))
gdf.rename(columns={'STATE': 'LEA_STATE', 'ZIP': 'LEA_ZIP'}, inplace=True)
merged_data = pd.merge(data[['LEAID', 'LEA_STATE', 'LEA_ZIP', 'LEA_ENR']], data2[['LEAID', 'LEA_STATE','Children in Poverty']], on=['LEAID', 'LEA_STATE'])
df = pd.merge(merged_data, gdf[['LEAID', 'LEA_STATE', 'LEA_ZIP', 'LAT', 'LON']], on=['LEAID', 'LEA_STATE', 'LEA_ZIP'])
df['Percentage Children In Pov'] = df['Children in Poverty'] / df['LEA_ENR']


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    #menu_items={
    #    'Get Help': 'https://www.extremelycoolapp.com/help',
    #    'Report a bug': "https://www.extremelycoolapp.com/bug",
    #    'About': "# This is a header. This is an *extremely* cool app!"
    #}
)

st.write("""
# Rowdy Datathon 2023

## Interactive: Children in Poverty


""")

st.write("---")


# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "I'll walk you through each of the data points we found to stand out.",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    add_intro = st.write("""
        *Introduction*
        
        This is a collection of data and visuals that help demonstrate the differences in rates of children living in poverty.
        """)
    add_intro = st.write("""
        *Table View*
        
        This is the data that we ended up using from a number of datasets.  
        """)
    add_intro = st.write("""
        *Map View*
        
        Set Coordinate System to Geographic.
        Drag lon and lat to their input spaces. 
        Drag Perc Children In Poverty to "Size" and "Color"



        On the first tab of the map view you can see the percentage of children living in poverty per school district.

        The second tab of the map view drills down to those same data points but with a focus on Texas school districts.

        We decided to apply aadditional filtering based on a pre determined school size label, large being 2000-10000 students, medium being 500-1999, and small being less than 500.

        When we focus on large school districts we are able to visualize the highest rates of child poverty in the largest districts, many of which are southern border cities with high rates of minorities.


        """)
                         






st.dataframe(data2)

st.write("---")

# Initialize pygwalker communication
init_streamlit_comm()

# When using `use_kernel_calc=True`, you should cache your pygwalker html, if you don't want your memory to explode
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    # If you want to use feature of saving chart config, set `debug=True`
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True, debug=False)
    return html

#@st.cache_data
#def get_df() -> pd.DataFrame:
#    return pd.read_csv("/bike_sharing_dc.csv")

#df = get_df()

components.html(get_pyg_html(df), width=1300, height=1000, scrolling=True)