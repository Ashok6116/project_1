import streamlit as st
import sqlite3
import pandas as pd
# Function to fetch data from the SQLite database
def fetch_data():
    conn = sqlite3.connect('bus_data.db')
    query = "SELECT * FROM bus_data"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fetch the data
data = fetch_data()



# Streamlit app
st.set_page_config(page_title="Available Bus", page_icon="🚌", layout="wide")

# Header
st.markdown("<div class='header'><h1>Available Buses 🚌</h1></div>", unsafe_allow_html=True)

# Route Filter
routes = st.sidebar.selectbox(
    'Select Routes',
    options=['All'] + list(data['bus_route_name'].unique()))
busname = st.sidebar.selectbox(
    'Select Bus Name',
    options=['All'] + list(data['bus_name'].unique())
)
# Bus Type Filter (Dropdown)
bustype = st.sidebar.selectbox(
    'Select Bus Type',
    options=['All'] + list(data['bus_type'].unique())
)

fares=data['fare'].apply(pd.to_numeric, errors='ignore')
rates=data['rating'].apply(pd.to_numeric, errors='ignore')
price_range = st.sidebar.slider(
    'Select Price Range',
    min_value=fares.min(),
    max_value=fares.max(),
    value=(fares.min(),fares.max())
)

star_rating = st.sidebar.slider(
    'Select Rating Range',
    min_value=int(rates.min()),
    max_value=int(rates.max()),
    value=(int(rates.min()),int(rates.max())),step=1
)


filtered_data = data.copy()

# Apply Filters
if routes != 'All':
    filtered_data = data[data['bus_route_name'] == routes]
if busname != 'All':
    filtered_data = data[data['bus_name'] == busname]
if bustype != 'All':
    filtered_data = data[data['bus_type'] == bustype]

# Apply Filters
filtered_data = filtered_data[
    (fares >= price_range[0]) &
    (fares <= price_range[1]) &
    (rates >= star_rating[0]) &
    (rates <= star_rating[1])
    ]

# Display total row count
st.write(f"Total rows in the filtered data: {filtered_data.shape[0]}")

# Display the filtered data
st.dataframe(filtered_data, height=1000, width=1000)
