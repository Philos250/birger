# Uploading the file
# ==================
import os
import pandas as pd
import streamlit as st

# Uploading the file
# ==================
fl = st.file_uploader(
    ":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"])
)

if fl is not None:
    filename = fl.name
    st.write(filename)
    dfd = pd.read_excel(fl)
else:
    # Get the directory of the currently running script
    script_dir = (
        os.path.dirname(os.path.abspath(__file__))
        if "__file__" in locals()
        else None
    )

    if script_dir:
        # If the script is run from a file, use its directory as the base
        data_file_path = os.path.join(
            script_dir, "BITS-Reports Practicum Dummy Data.xlsx"
        )
    else:
        # Fallback to a specific directory if the script is run interactively
        data_file_path = "C:\\Users\\Savage\\Desktop\\BIRGER\\BITS-Reports Practicum Dummy Data.xlsx"

    dfd = pd.read_excel(data_file_path)

# End of upload tab

# Data Pre-processing
# Interpolate missing values using forward fill ('pad')
dfd.interpolate(method='pad', inplace=True)

# Making 2 columns
col1, col2 = st.columns((2))
dfd["Created On"] = pd.to_datetime(dfd["Created On"])

# Getting the min and max date
# Convert 'Start Date' and 'Start Time' to datetime
# Ensure 'Start Date' and 'Start Time' are strings
dfd["Start Date"] = dfd["Start Date"].astype(str)
dfd["Start Time"] = dfd["Start Time"].astype(str)

# Combine 'Start Date' and 'Start Time' into 'Start DateTime'
dfd["Start DateTime"] = pd.to_datetime(dfd["Start Date"] + ' ' + dfd["Start Time"], format="%d/%m/%Y %H:%M", errors='coerce')

# Ensure 'End Date' and 'End Time' are strings
dfd["End Date"] = dfd["End Date"].astype(str)
dfd["End Time"] = dfd["End Time"].astype(str)

# Combine 'End Date' and 'End Time' into 'End DateTime'
dfd["End DateTime"] = pd.to_datetime(dfd["End Date"] + ' ' + dfd["End Time"], format="%d/%m/%Y %H:%M", errors='coerce')

# Drop the original date and time columns if needed
dfd.drop(["Start Date", "Start Time", "End Date", "End Time"], axis=1, inplace=True)

# Check for rows with invalid datetime values (NaT)
invalid_rows = dfd[(dfd['Start DateTime'].isna()) | (dfd['End DateTime'].isna())]

# You can handle or remove the invalid rows as needed
dfd = dfd.dropna(subset=['Start DateTime', 'End DateTime'])

# Check the data types of the 'Incident Id' column
st.write("Data types of 'Incident Id' column:", dfd['Incident Id'].dtype)

# If the 'Incident Id' column is not already of string type, convert it
if dfd['Incident Id'].dtype != 'object':
    dfd['Incident Id'] = dfd['Incident Id'].astype(str)

# Strip whitespaces from 'Incident Id' values
dfd['Incident Id'] = dfd['Incident Id'].str.strip()

# Display unique values in 'Incident Id'
st.write("Unique values in 'Incident Id':", dfd['Incident Id'].unique())

# Calculate the total number of unique incidents
total_incidents = dfd['Incident Id'].nunique()

# Streamlit app
# st.title("Unique Incidents Counter")
# st.write("This app calculates and displays the total number of unique incidents.")
with st.expander("View Dataset"):
    st.dataframe(dfd)  # Display your incident data

st.write("**Total number of unique incidents:**", total_incidents)
