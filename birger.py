import streamlit as st
import pandas as pd
# IMPORTS
import plotly.express as px
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
# from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
import upload_db
import warnings
warnings.filterwarnings('ignore') 
import pickle
from pathlib import Path
import streamlit_authenticator as stauth # pip install streamlit-authenticator
import pdfkit  # Import the pdfkit library
# new version
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# URL TITLE
# =========
st.set_page_config(page_title="⚛ BIRGER Dashboard", page_icon="bar_chart:", layout="wide")

# Define the custom color palette
custom_theme = {
    "primaryColor": "#30AEE4",
    "backgroundColor": "#F8F7F8",
    "textColor": "#171A2A",
    "secondaryBackgroundColor": "#2FB9E4",
}

with open('style.css') as f:
    	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# LOGIN FIRST
# ===========

# st.title("Dashboard")
# Sidebar Logo
st.sidebar.image("Images/birger-retina.png")

with st.sidebar:
    selected = option_menu(
        menu_title="Birger",
        options=["Home", "BITS Team"],
        icons=["speedometer2","person-gear"],
        menu_icon="cast"
    )
# Condition
# =========
# if selected == "Upload DB":
#     upload_db

if selected == "Home":
    # -------------------- LOGON TO BASHBOARD ---------------------------
    # ------------------- USER AUTHENTICATION ---------------------------
    names =  ["Birger", "Adeline Musonera", "Bievenu Murenzi", "HABIMANA Jean de Dieu"]
    usernames = ["birger", "amusonera", "mbievenu", "jd"]

    # Load hashed passwords
    #=======================
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

        # In line dashboard title
        # -----------------------
        # st.title(" :var_cart: ⚛ BIRGER DASHBOARD")
        st.title("⚛ BIRGER ANALYTICS DASHBOARD")
        # st.markdown('<style>div.block-container{padding-top:1em;}</style>', hide_st_style, unsafe_allow_html=True)

        # MAIN CONTENT FOR THE DASHBOARD
        # ******************************

        def metrics():
            # 
            # from streamlit_extras.metric_cards import style_metric_card
            col1, col2, col3 = st.columns(3)
            col1.metric("Total")
        # LEVEL I
        # @@@@@@@

        # # Uploading the file
        # # ------------------
        # fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))
        # if fl is not None:
        #     filename = fl.name
        #     st.write(filename)
        #     df = pd.read_excel(filename)
        # else:
        #     os.chdir(r"C:\Users\Savage\Desktop\BIRGER")
        #     df = pd.read_excel("SST-Report-Practicum Dummy Data.xlsx")
        # # End of upload tab

        # Uploading the file
        # ==================
        fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

        if fl is not None:
            filename = fl.name
            st.write(filename)
            df = pd.read_excel(fl)
        else:
            # Get the directory of the currently running script
            script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else None

            if script_dir:
                # If the script is run from a file, use its directory as the base
                data_file_path = os.path.join(script_dir, "SST-Report-Practicum Dummy Data.xlsx")
            else:
                # Fallback to a specific directory if the script is run interactively
                data_file_path = "C:\\Users\\Savage\\Desktop\\BIRGER\\SST-Report-Practicum Dummy Data.xlsx"

            df = pd.read_excel(data_file_path)

        # End of upload tab


        # DATA PRE-PROCESSING
        # @@@@@@@@@@@@@@@@@@@
        # Interpolate missing values using forward fill ('pad')
        df.interpolate(method='pad', inplace=True)

        # Making 2 columns
        col1, col2 = st.columns((2))
        df["Created On"] = pd.to_datetime(df["Created On"])

        # Getting the min and max date
        # Combine date and time columns for 'Start' and 'End'
        df['Start DateTime'] = pd.to_datetime(df['Start Date'] + ' ' + df['Start Time'], format='%d/%m/%Y %H:%M', errors='coerce')
        df['End DateTime'] = pd.to_datetime(df['End Date'] + ' ' + df['End Time'], format='%d/%m/%Y %H:%M', errors='coerce')
        # Drop the original date and time columns if needed
        df.drop(['Start Date', 'Start Time', 'End Date', 'End Time'], axis=1, inplace=True)

        # Check for rows with invalid datetime values (NaT)
        invalid_rows = df[(df['Start DateTime'].isna()) | (df['End DateTime'].isna())]

        # You can handle or remove the invalid rows as needed
        df = df.dropna(subset=['Start DateTime', 'End DateTime'])
        # End of data processing

        # Retrieving the data for KPIs
        # ============================
        # Calculate the total number of unique incidents
        incident_counts = df['Incident Id'].value_counts()
        total_incidents = len(incident_counts)

        # Streamlit app
        # st.title("Unique Incidents Counter")
        # st.write("This app calculates and displays the total number of unique incidents.")
        with st.expander("View Dataset"):
            st.dataframe(df)  # Display your incident data

        st.write("**Total number of unique incidents:**", total_incidents)

        # Key Performance Indicator (KPI)
        # ===============================

        # Retreivign the data
        # For InProgress
        total_incidents_inprogress = len(df[df['Task Status'] == "InProgress"]['Incident Id'].unique())
        print("Total number of unique incidents: InProgress")
        print("Total number of incidents received:", total_incidents_inprogress)

        # Closed
        total_incidents_closed = len(df[df['Task Status'] == "Closed"]['Incident Id'].unique())
        print("Total number of unique incidents: Closed")
        print("Total number of incidents received:", total_incidents_closed)

        st.subheader('Dataset Metrics', divider='rainbow',)
        from streamlit_extras.metric_cards import style_metric_cards
        a1, a2, a3 = st.columns(3)
        a1.metric(label="All Incidents ", value=total_incidents, delta="Number of Unique Incidences")
        a2.metric(label="No. of In Progress Incidences:", value= total_incidents_inprogress, delta=total_incidents_inprogress)
        a3.metric(label="No. of Closed Incidences:", value= total_incidents_closed, delta=total_incidents_closed)
        style_metric_cards(background_color="#ffffff",border_left_color="#30aee4",border_color="#30aee4",box_shadow="#F71938")

        # Retreivign the data
        # ===================
        # For Assigned
        total_incidents_assigned = len(df[df['Task Status'] == "Assigned"]['Incident Id'].unique())
        print("Total number of unique incidents: Assigned")
        print("Total number of incidents received:", total_incidents_assigned)

        # For Technician
        unique_technicians = df['Technician'].nunique()
        print("Total number of unique technicians:", unique_technicians)

        # Resolution Accepted
        total_incidents_resol_accepted = len(df[df['Task Status'] == "Resolution Accepted"]['Incident Id'].unique())
        print("Total number of unique incidents: Resolution Accepted")
        print("Total number of incidents received:", total_incidents_resol_accepted)

        # Resolution Rejected
        total_incidents_resol_rejected = len(df[df['Task Status'] == "Resolution Rejected"]['Incident Id'].unique())
        print("Total number of unique incidents: Resolution Rejected")
        print("Total number of incidents received:", total_incidents_resol_rejected)

        # Resolution - Notified
        total_incidents_resol_notified = len(df[df['Task Status'] == "Resolution - Notified"]['Incident Id'].unique())
        print("Total number of unique incidents: Resolution - Notified")
        print("Total number of incidents received:", total_incidents_resol_notified)

        e1, e2, e3, e4 = st.columns(4)
        e1.metric(label="All Engineers ", value=unique_technicians, delta="Number of all Engineers")
        e2.metric(label="No. of Resolution Accepted:", value= total_incidents_resol_accepted, delta=total_incidents_resol_accepted)
        e3.metric(label="No. of Resolution Rejected:", value= total_incidents_resol_rejected, delta=total_incidents_resol_rejected)
        e4.metric(label="No. of Resolution - Notified:", value= total_incidents_resol_notified, delta=total_incidents_resol_notified)
        style_metric_cards(background_color="#ffffff",border_left_color="#30aee4",border_color="#30aee4",box_shadow="#F71938")
        # End of KPI

        # LEVEL II
        # @@@@@@@@

        # CALENDAR
        # ========
        # I decide to go with a Function called Main()

        def main(st):
            import pandas as pd
            import plotly.express as px
            from datetime import datetime
            import pdfkit  # Import the pdfkit library
            import plotly.io as pio
            from io import BytesIO
            import base64  # Import base64 for encoding
            from fpdf import FPDF
            import base64
            from tempfile import NamedTemporaryFile
            # st.write("## Count of ATM Interventions and ATM Servicing by Month and Geo")  # Big title above both charts
            # st.sidebar.header("Choose your Filter:")
            # Calendar Filter
            startDate = df['Start DateTime'].min()
            endDate = df['End DateTime'].max()

            # st.write("# Data Visualization")  # Set the main title

            # Making 2 columns for Date
            d1, d2 = st.columns(2)
            with d1:
                dateOne = st.date_input("Start Date", startDate)
            with d2:
                dateTwo = st.date_input("End Date", endDate)

            dateOne = datetime(dateOne.year, dateOne.month, dateOne.day)
            dateTwo = datetime(dateTwo.year, dateTwo.month, dateTwo.day)

            if dateOne <= dateTwo:
                filtered_df = df[(df["Start DateTime"] >= dateOne) & (df["End DateTime"] <= dateTwo)].copy()
            else:
                st.error("End Date should be greater than or equal to Start Date.")
                filtered_df = df  # No filtering if dates are not selected correctly

            # Sidebar Logo
            # st.sidebar.image("Images/birger-retina.png")
            # Sidebar filters
            st.sidebar.header("Choose your Filter:")
            geo = st.sidebar.multiselect("Pick your Geographical Location", df["Geo"].unique())

            # Filter the data based on the selected Geo
            if geo:
                filtered_df = filtered_df[filtered_df["Geo"].isin(geo)]

            # Get unique locations based on selected Geo
            unique_locations = filtered_df["Location"].unique()

            location = st.sidebar.multiselect("Pick your Location", unique_locations)

            # Filter the data based on the selected Location
            if location:
                filtered_df = filtered_df[filtered_df["Location"].isin(location)]

            # Creating two columns for Interventions, Servicing and Geo Location
            # ------------------------------------------------------------------

            # Making 2 columns for charts
            c1, c2 = st.columns((2))

            with c1:
                # Main content
                # st.title('Data Visualization')

                # Create a column 'Month' from 'Created On'
                filtered_df['Month'] = pd.to_datetime(filtered_df['Created On']).dt.strftime('%b')

                # Define the custom order of months
                custom_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

                # Pivot the data for 'ATM Interventions' and 'ATM Servicing'
                pivot_df = filtered_df[filtered_df['Intervention Type'].isin(['ATM Interventions', 'ATM Servicing'])].pivot_table(
                    index='Month', columns='Intervention Type', values='Incident Id', aggfunc='count', fill_value=0
                )

                # Reorder the DataFrame by custom month order
                pivot_df = pivot_df.reindex(custom_month_order)

                # Create a grouped bar chart
                fig = px.bar(pivot_df, barmode='group')

                # st.subheader('Count of ATM Interventions and ATM Servicing by Month')

                # Customize the layout
                fig.update_layout(
                    title='Count of ATM Interventions and ATM Servicing by Month',
                    xaxis_title='Month',
                    yaxis_title='Count',
                    xaxis=dict(tickangle=-45),
                )

                # Show the chart
                st.plotly_chart(fig, use_container_width=True)

                # Download the bar chart as PDF
                # Declare the download button for the chart in c1
                st.button("Download Chart as PDF", key="bar_chart_pdf")

            with c2:
                # st.title('Data Visualization')
                # Group the data by 'Geo' and count the number of incidents
                geo_counts = filtered_df['Geo'].value_counts()

                # Streamlit app
                # st.subheader('Interventions by Geo')

                # Create a pie chart using Plotly Express with a hole in the center
                fig = px.pie(values=geo_counts, names=geo_counts.index, hole=0.4)
                fig.update_traces(textinfo='percent+label')

                # Set the title for the pie chart
                fig.update_layout(
                    title='Count of ATM Interventions and ATM Servicing by Geo',
                    # title_x=0.1  # Center the title
                )

                st.plotly_chart(fig, use_container_width=True)


            # NEXT LEVEL
            # ----------
            # LEVEL III
            # @@@@@@@@@

            # Filter the dataset for 'Closed' incidents per Technician
            closed_incidents = filtered_df[filtered_df['Status'] == 'Closed']

            # Group the data by Technician and count unique Incidents
            technician_interventions = closed_incidents.groupby('Technician')['Incident Id'].nunique()

            # Sort the results in descending order
            technician_interventions = technician_interventions.sort_values(ascending=False)

            #-----------------------------------------------------------------------------------------

            columns_to_select = ['Created On', 'Technician', 'Status']

            st.title("View Data")

            # Filter the DataFrame to include only 'Closed' status incidents
            selected_df_closed = filtered_df[filtered_df['Status'] == 'Closed'][columns_to_select]

            # Extract the month from the 'Created On' column
            selected_df_closed['Month'] = pd.to_datetime(selected_df_closed['Created On']).dt.strftime('%b')

            # Pivot the DataFrame to get the counts of each status per technician and month
            pivot_table = selected_df_closed.pivot_table(index=['Technician', 'Status'], columns='Month', aggfunc='size', fill_value=0)

            # Calculate the 'Grand Total' by summing the counts across all months for each technician
            pivot_table['Grand Total'] = pivot_table.sum(axis=1)

            # Calculate the 'Final Total' by summing the counts across all technicians for each month
            final_total = pivot_table.sum().rename('Final Total')

            # Concatenate the final_total as a new row to the pivot_table
            pivot_table = pd.concat([pivot_table, final_total.to_frame().T])

            # Reorder the columns to match the desired format
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Grand Total']

            # Extract unique months without the year
            df['Month'] = df['Created On'].dt.strftime('%b')
            unique_months = df['Month'].unique()

            # Sort the unique months based on the custom order
            unique_months_sorted = sorted(unique_months, key=lambda x: month_order.index(x))


            # TWO COLUMNS
            # -----------
            cl1, cl2 = st.columns(2)
            with cl1:
                with st.expander("Total_Technician_Interventions_ViewData"):
                    # Convert the Series to a DataFrame
                    technician_df = technician_interventions.reset_index()
                    st.dataframe(technician_df.style.background_gradient(cmap="Blues"))

                    # Export the DataFrame as CSV
                    csv = technician_df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Data", data=csv, file_name="Technician_Interventions.csv", 
                                    key="download_csv")
                
            with cl2:
                with st.expander("Technician_Interventions_by_Month_ViewData"):
                    # Display the pivot table in Streamlit
                    st.write(pivot_table.style.background_gradient(cmap="Oranges"))

                    # Export the DataFrame as CSV
                    csv = pivot_table.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Data", data=csv, file_name="Technician_Interventions_by_Month.csv", 
                                    mime="text/csv", help='Click Here to download the data as a CSV File')
                    
            # NEXT LEVEL
            # ----------
            # LEVEL IV
            # @@@@@@@@
            selected_df = filtered_df.copy()
            columns_to_select = ['Created On', 'Technician', 'Status']

            # st.title("Technician Interventions by Month")

            # Extract the month from the 'Created On' column
            selected_df['Month'] = pd.to_datetime(selected_df['Created On']).dt.strftime('%b')

            # Pivot the DataFrame to get the counts of each status per technician and month
            pivot_table = selected_df.pivot_table(index=['Technician', 'Status'], columns='Month', aggfunc='size', fill_value=0)

            # Calculate the 'Grand Total' by summing the counts across all months
            pivot_table['Grand Total'] = pivot_table.sum(axis=1)

            # Reorder the columns to match the desired format
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Grand Total']

            # Extract unique months without the year
            df['Month'] = df['Created On'].dt.strftime('%b')
            unique_months = df['Month'].unique()

            # Sort the unique months based on the custom order
            unique_months_sorted = sorted(unique_months, key=lambda x: month_order.index(x))

            # Display the pivot table in Streamlit
            # st.write(pivot_table.style.background_gradient(cmap="Oranges"))

            # ----------------------------------------------------------------------------------

            # Filter the DataFrame for 'Closed' status incidents
            selected_df_cl = df[columns_to_select]

            # Extract the month from the 'Created On' column
            selected_df_cl['Month'] = pd.to_datetime(selected_df_cl['Created On']).dt.strftime('%b')

            # Pivot the DataFrame to get the counts of each status per month
            No_interventions_status_month = selected_df_cl.pivot_table(index='Status', columns='Month', aggfunc='size', fill_value=0)

            # Calculate the 'Grand Total' by summing the counts across all months
            No_interventions_status_month['Grand Total'] = No_interventions_status_month.sum(axis=1)

            # Reorder the columns to match the desired format
            # month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Grand Total']
            No_interventions_status_month = No_interventions_status_month[unique_months_sorted]

            # Define a function to apply cell color based on status
            def color_cells(val):
                if val == 'Assigned':
                    color = 'background-color: blue'
                elif val == 'Closed':
                    color = 'background-color: green'
                elif val == 'InProgress':
                    color = 'background-color: orange'
                else:
                    color = ''
                return f'background-color: {color}'

            # Apply cell color based on status
            styled_table = No_interventions_status_month.style.applymap(color_cells, subset=pd.IndexSlice[:, No_interventions_status_month.columns[:-1]])

            # TWO COLUMNS
            # -----------
            cl11, cl22 = st.columns(2)
            with cl11:
                with st.expander("Status of Incidents per Technician ViewData"):
                    # Convert the Series to a DataFrame
                    pivot_table = pivot_table.reset_index()
                    st.dataframe(pivot_table.style.background_gradient(cmap="Greens"))

                    # Export the DataFrame as CSV
                    csv = pivot_table.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Data", data=csv, file_name="Status of Incidents per Technician.csv", 
                                    mime="text/csv", help='Click Here to download the data as a CSV File')
            with cl22:
                with st.expander("Total number of Interventions status per month ViewData"):
                    # Convert the Series to a DataFrame
                    No_interventions_status_month = No_interventions_status_month.reset_index()
                    # st.dataframe(styled_table)
                    st.write(styled_table)

                    # Export the DataFrame as CSV
                    csv = No_interventions_status_month.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Data", data=csv, file_name="Total_number_of_Interventions_status_per_month.csv", mime="text/csv",
                                    help='Click Here to download the data as a CSV File')

            import plotly.io as pio
            import kaleido as kaleido
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            import plotly.express as px
            from io import BytesIO

            # FUNCTION FOR GENERATING PDF
            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
            
            st.title("Time Series Analysis")

            selected_df['Month'] = pd.to_datetime(selected_df['Created On']).dt.strftime('%b')

            # Define the custom order of months
            # custom_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Grand Total']

            # Extract unique months without the year
            df['Month'] = df['Created On'].dt.strftime('%b')
            unique_months = df['Month'].unique()
            # Pivot the data for 'ATM Interventions' and 'ATM Servicing'
            pivot_df = filtered_df[filtered_df['Intervention Type'].isin(['ATM Interventions', 'ATM Servicing'])].pivot_table(
                index='Month', columns='Intervention Type', values='Incident Id', aggfunc='count', fill_value=0
            )

            # Reorder the DataFrame by custom month order
            pivot_df = pivot_df.reindex(custom_month_order)

            # Create a line chart
            fig = px.line(pivot_df, markers=True, line_shape='linear')

            # Customize the layout
            fig.update_layout(
                title='Count of ATM Interventions and ATM Servicing by Month on Line chart',
                xaxis_title='Month',
                yaxis_title='Count',
                xaxis=dict(tickangle=-45),
            )

            st.plotly_chart(fig, use_container_width=True)

            # Download the Time Series chart as PDF
            # st.download_button("Download PDF", data=filtered_df, file_name="line_chart_pdf.pdf", key="line_chart_pdf", mime="application/pdf")
            # st.button("Export Report")

            if st.button("Export Report", key="lamba"):
                pdf = FPDF()
                pdf.add_page()
                with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                    fig.write_image(tmpfile.name, format="png")
                    pdf.image(tmpfile.name, x=10, y=10, w=200, h=100)
                pdf_file = BytesIO()
                pdf.output(pdf_file)
                pdf_file = pdf_file.getvalue()

                # Provide a download link for the PDF
                href = f'<a href="data:application/pdf;base64,{base64.b64encode(pdf_file).decode()}" download="testfile.pdf">Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)


            # Download the Time Series Data
            with st.expander("View Data of Time Series"):
                st.write(pivot_df.T.style.background_gradient(cmap="Blues"))
                csv = pivot_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data = csv, file_name= "Time Series.csv", mime = 'text/csv')

            # Top 10 Incidents by FE
            # ======================
            # Title of the Streamlit app
            st.title('Customized Incidents by Subject')

            # Group the data by 'Subject' and count the number of incidents
            subject_counts = selected_df['Subject'].value_counts().reset_index()
            subject_counts.columns = ['Subject', 'Count']

            # Create an interactive pie chart with Plotly Express
            fig = px.pie(
                subject_counts,
                names='Subject',
                values='Count',
                title='Incidents by Subject',
                hole=0.4,  # Adjust the hole size for space inside
            )

            # Customize the pie chart size
            fig.update_layout(
                width=800,  # Set the width
                height=600,  # Set the height
            )

            # Display the chart with hover details
            st.plotly_chart(fig)

            # Download the chart as an image or CSV
            if st.button('Download Chart as Image'):
                st.markdown("### Downloading Chart as Image...")
                fig.write_image("incidents_pie_chart.png")

            # if st.button('Download Data as CSV'):
            #     st.markdown("### Downloading Data as CSV...")
            #     df.to_csv("incidents_data.csv", index=False)

            csv = subject_counts.to_csv(index=False)
            st.download_button("Download Data as CSV", data=csv, file_name="incidents_pie_chart.csv", 
                                mime="text/csv", help='Click Here to download the data as a CSV File')

            # Display chart details on hover
            st.write("Hover over the chart portions to see subject details.")

            with st.expander("View Dataset"):
                st.dataframe(selected_df)  # Display your incident data

            # Scatter Plot of Number of Incidents by Month and Geo with their Customer
            # ========================================================================
            import streamlit as st
            import pandas as pd
            import matplotlib.pyplot as plt

            # Title of the Streamlit app
            st.title('Incidents by Month and Geo with its Customers')

            # Convert 'Created On' to 'Month' and format it to show only the month abbreviation
            selected_df['Month'] = pd.to_datetime(selected_df['Created On']).dt.strftime('%b')

            # Define the custom order of months
            # custom_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            custom_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            # Extract unique months without the year
            df['Month'] = df['Created On'].dt.strftime('%b')
            unique_months = df['Month'].unique()

            # Set the 'Month' column data type and order
            selected_df['Month'] = pd.Categorical(selected_df['Month'], categories=unique_months, ordered=True)

            # Group the data by 'Month' and 'Geo' and count the number of incidents
            geo_month_counts = selected_df.groupby(['Month', 'Geo']).size().unstack().fillna(0)

            # Create a color map for the different Geo values
            # colors = {'Mauritius': 'red', 'Seychelles': 'blue', 'Rodrigues': 'green'}
            colors = {'Mauritius': 'red', 'Seychelles': 'blue', 'Rodrigues': 'green'}

            # Scatter plot for each Geo
            fig, ax = plt.subplots(figsize=(12, 8))  # Set the figure size

            for geo in colors:
                if geo in geo_month_counts.columns:  # Check if the geo location exists in the DataFrame
                    color = colors[geo]
                    ax.scatter(geo_month_counts.index, geo_month_counts[geo], label=geo, c=color, alpha=0.6, s=50)

                    # Add 'Customer' annotations on top of the dots (only for available data points)
                    for i, txt in enumerate(df[df['Geo'] == geo]['Customer']):
                        if i < len(geo_month_counts):
                            ax.annotate(txt, (geo_month_counts.index[i], geo_month_counts[geo].iloc[i]), ha='center', rotation=45)

            # Set labels and title
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Incidents')
            ax.set_title('Number of Incidents by Month and Geo')
            plt.xticks(rotation=90)  # Rotate month labels by 90 degrees
            ax.legend(title='Geo', loc='upper right')

            # Display the scatter plot in Streamlit
            st.pyplot(fig)

            # Optionally display the raw DataFrame
            # st.write("Raw Data", df)

            # Download the chart as an image or CSV
            if st.button('Download Chart as Image', key='download_scatter_image'):
                st.markdown("### Downloading Chart as Image...")
                fig.savefig("incidents_scatter_plot.png")

            # if st.button('Download Data as CSV', key='download_scatter_csv'):
            #     st.markdown("### Downloading Data as CSV...")
            csv = geo_month_counts.to_csv(index=False)
            st.download_button("Download Data as CSV", data=csv, file_name="incidents_data_geo_customer.csv", 
                                mime="text/csv", help='Click Here to download the data as a CSV File')
            

            # DOWNLOAD BUTTON
            #================
            import streamlit as st
            import pandas as pd
            import matplotlib.pyplot as plt
            import pdfkit  # Import the pdfkit library

            # ... (the rest of your code)

            # Add a button to generate the PDF report
            if st.button('Generate PDF Report'):
                # Define a PDF output path
                pdf_filename = "birger_dashboard_report.pdf"

                # Save your Streamlit app as an HTML file
                html_filename = "birger_dashboard_report.html"
                with open(html_filename, 'w') as f:
                    # You can include any Streamlit elements you want to save in the PDF here
                    # For example, you can use st.write, st.table, and st.pyplot
                    st.title("BIRGER ANALYTICS DASHBOARD")
                    # Add your Streamlit app elements here
                    st.write("Total number of unique incidents:", total_incidents)
                    # ...

                # Convert the HTML file to a PDF
                pdfkit.from_file(html_filename, pdf_filename)

                # Provide a download link to the generated PDF
                st.markdown(f'[Download PDF Report]({pdf_filename})', unsafe_allow_html=True)
        
        
        # Function calling
        if __name__ == '__main__':
            main(st)


elif selected == "BITS Team":
    upload_db


import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Create a download button to download data as a PDF
def download_pdf():
    pdf_buffer = BytesIO()
    # Set the page size explicitly to landscape mode
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

    # Create a table from the DataFrame
    table_data = [df.columns] + df.values.tolist()
    table = Table(table_data, colWidths=[1.5 * inch for i in range(len(df.columns))])

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements = [table]

    # Add a label indicating landscape orientation
    landscape_text = "<font size='3'>Page Size: Landscape</font>"
    landscape_paragraph = Paragraph(landscape_text, getSampleStyleSheet()["Normal"])
    elements.append(landscape_paragraph)

    # Build the PDF
    doc.build(elements)

    # Download the dataset as PDF
    st.title('Download the dataset as PDF')

    st.write('You can generate a PDF report of the dataset above.')

    # Offer the PDF file for download
    pdf_buffer.seek(0)
    st.download_button("Download PDF", data=pdf_buffer, file_name="sample_dataset.pdf", key="download_pdf", mime="application/pdf")

# Display data
# st.table(df)

# Create the download button
download_pdf()
