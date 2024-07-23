import streamlit as st
import sqlite3
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

# Connect to the SQLite database (or any other database)
conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

# Fetch data from the database
query = "SELECT * FROM bus_data"
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the data in Streamlit
st.title("Database Bus Details ")


dynamic_filters = DynamicFilters(data, filters=['bus_route_name', 'bus_type','departure_time', 'rating'])

dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')
dynamic_filters.display_df()


#st.dataframe(data)

# Optionally, you can display the data in other formats
#st.table(data)
