import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.subplots as sp
from plotly.subplots import make_subplots

# Function to check if the uploaded file is a CSV
def is_csv(file):
    return file.type == 'text/csv'

# Streamlit page content
def insurecheck_collective_main():
    st.title("InsureCheck Collective")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is None:
        pass

    # Check if a file is uploaded
    elif uploaded_file is not None:
        if is_csv(uploaded_file):
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Perform data processing and prediction
            model = joblib.load('model.pkl')
            scaler = joblib.load('scaler.pkl')
            df_test_master = df.copy()
            to_drop = ['policy_annual_premium', 'policy_bind_date', 'policy_state', 'insured_zip', 'incident_location',
                       'incident_date', 'incident_state', 'incident_city', 'insured_hobbies', 'auto_make',
                       'auto_model', 'auto_year']

            df_test_master.drop(to_drop, inplace=True, axis=1)
            df_test_master.drop(columns=['age', 'total_claim_amount'], inplace=True, axis=1)
            df_test_master = pd.get_dummies(df_test_master)

            if 'collision_type_?' in df_test_master.columns:
                df_test_master.drop('collision_type_?', inplace=True, axis=1)

            if 'property_damage_?' in df_test_master.columns:
                df_test_master.drop('property_damage_?', inplace=True, axis=1)

            if 'police_report_available_?' in df_test_master.columns:
                df_test_master.drop('police_report_available_?', inplace=True, axis=1)
            df_test_master = df_test_master[['policy_number', 'months_as_customer'] + list(df_test_master.columns[2:])]


            # Create a copy of df_test
            temp_df_test = df.copy()

            # Add the 'fraud' column to temp_df_test
            temp_df_test['fraud'] = ''

            # Apply scaling to the relevant columns in df_test_master
            scaled_data = scaler.transform(df_test_master.iloc[:, 1:13])

            # Convert the column names to strings
            feature_names = [str(col) for col in df_test_master.columns[1:13]]

            # Create a DataFrame with scaled data and updated feature names
            input_data = pd.DataFrame(scaled_data, columns=feature_names).join(df_test_master.iloc[:, 13:])

            # Make predictions using the model
            predictions = model.predict(input_data)

            # Iterate over each row in df_test_master and add the prediction to temp_df_test
            for i, policy_number in enumerate(df_test_master['policy_number']):
                temp_df_test.loc[temp_df_test['policy_number'] == policy_number, 'fraud'] = predictions[i]

            df_fraud_Y = temp_df_test[temp_df_test['fraud'] == 'Y']
            df_fraud_N = temp_df_test[temp_df_test['fraud'] == 'N']

            # Save the data to CSV files
            df_fraud_Y_csv = df_fraud_Y.to_csv(index=False)
            df_fraud_N_csv = df_fraud_N.to_csv(index=False)


            # Display data predicted as Fraud == Yes
            st.header("Data predicted as Fraud == Yes")
            st.dataframe(df_fraud_Y)
            if st.button("Download Data predicted as Fraud == Yes"):
                st.download_button(
                    label="Download CSV",
                    data=df_fraud_Y_csv,
                    file_name="df_fraud_Y.csv",
                    mime="text/csv"
                )


            # Display data predicted as Fraud == No
            st.header("Data predicted as Fraud == No")
            st.dataframe(df_fraud_N)
            if st.button("Download Data predicted as Fraud == No"):
                st.download_button(
                    label="Download CSV",
                    data=df_fraud_N_csv,
                    file_name="df_fraud_N.csv",
                    mime="text/csv"
                )

            # Group temp_df_test by 'fraud' and count occurrences of each attribute value
            grouped_temp_df = temp_df_test.groupby('fraud').sum().T

            # Create a stacked bar chart using Plotly
            fig = px.bar(grouped_temp_df, title="Attribute Influence for 'fraud' = 'Y' and 'fraud' = 'N'",
                        barmode='stack')
            fig.update_layout(xaxis_tickangle=-90, legend_title='Fraud', legend=dict(x=1, y=1))
            st.plotly_chart(fig)

            # Count the occurrences of 'fraud' = 'Y' and 'fraud' = 'N'
            fraud_counts = temp_df_test['fraud'].value_counts()

            # Create a pie chart using Plotly
            fig = px.pie(values=fraud_counts, names=fraud_counts.index, title='Fraud Distribution in temp_df_test')
            st.plotly_chart(fig)

            categorical_variables = ['insured_education_level', 'insured_occupation', 'incident_type', 'policy_csl']

            # Create subplots with 2 rows and 2 columns
            fig = make_subplots(rows=2, cols=2, subplot_titles=[f'Distribution of {var}' for var in categorical_variables[:4]],
                                vertical_spacing=0.3)

            # Iterate over each categorical variable
            for i, variable in enumerate(categorical_variables[:4]):
                # Count the occurrences of each category for 'fraud' = 'Y'
                fraud_y_counts = temp_df_test[temp_df_test['fraud'] == 'Y'][variable].value_counts()

                # Count the occurrences of each category for 'fraud' = 'N'
                fraud_n_counts = temp_df_test[temp_df_test['fraud'] == 'N'][variable].value_counts()

                # Get the unique categories
                categories = np.union1d(fraud_y_counts.index, fraud_n_counts.index)

                # Create a bar chart for the current categorical variable
                fig.add_trace(go.Bar(x=categories, y=fraud_y_counts.reindex(categories, fill_value=0),
                                    name='Fraud = Y', marker_color='lightblue'), row=(i // 2) + 1, col=(i % 2) + 1)
                fig.add_trace(go.Bar(x=categories, y=fraud_n_counts.reindex(categories, fill_value=0),
                                    name='Fraud = N', marker_color='lightgreen'), row=(i // 2) + 1, col=(i % 2) + 1)

                # Set the axis labels and title
                fig.update_xaxes(title_text='Category', row=(i // 2) + 1, col=(i % 2) + 1)
                fig.update_yaxes(title_text='Count', row=(i // 2) + 1, col=(i % 2) + 1)
                fig.update_layout(title=f'Distribution of {variable}')

            # Update the layout with increased width and gap between rows
            fig.update_layout(width=1500,height=800, showlegend=True, legend=dict(x=0, y=1))

            # Display the figure
            st.plotly_chart(fig)

            # Create subplots with one row and two columns
            fig = sp.make_subplots(rows=1, cols=2)           

            # Scatter plot for 'months_as_customer' and 'total_claim_amount'
            scatter1 = go.Scatter(
                x=temp_df_test['months_as_customer'],
                y=temp_df_test['total_claim_amount'],
                mode='markers',
                marker=dict(
                    size=8,
                    color='blue',
                    opacity=0.7
                ),
                name='Months as Customer vs Total Claim Amount'
            )

            # Scatter plot for 'age' and 'policy_annual_premium'
            scatter2 = go.Scatter(
                x=temp_df_test['age'],
                y=temp_df_test['policy_annual_premium'],
                mode='markers',
                marker=dict(
                    size=8,
                    color='green',
                    opacity=0.7
                ),
                name='Age vs Policy Annual Premium'
            )

            # Create the layout
            layout = go.Layout(
                title='Scatter Plots',
                xaxis=dict(title='Months as Customer / Age'),
                yaxis=dict(title='Total Claim Amount / Policy Annual Premium'),
                showlegend=True,
                legend=dict(x=0, y=1)
            )

            # Create the figure and add the scatter plots
            fig = go.Figure(data=[scatter1, scatter2], layout=layout)

            # Display the figure
            st.plotly_chart(fig)


            # Scatter plot for 'incident_hour_of_the_day' and 'vehicle_claim'
            scatter1 = go.Scatter(
                x=temp_df_test['incident_hour_of_the_day'],
                y=temp_df_test['vehicle_claim'],
                mode='markers',
                marker=dict(
                    size=8,
                    color='blue',
                    opacity=0.7
                ),
                name='Incident Hour of the Day vs Vehicle Claim Amount'
            )

            # Scatter plot for 'age' and 'months_as_customer'
            scatter2 = go.Scatter(
                x=temp_df_test['age'],
                y=temp_df_test['months_as_customer'],
                mode='markers',
                marker=dict(
                    size=8,
                    color='green',
                    opacity=0.7
                ),
                name='Age vs Months as Customer'
            )

            # Create the layout
            layout = go.Layout(
                title='Scatter Plots',
                xaxis=dict(title='Incident Hour of the Day / Age'),
                yaxis=dict(title='Vehicle Claim Amount / Months as Customer'),
                showlegend=True,
                legend=dict(x=0, y=1)
            )
           
            # Create the figure and add the scatter plots
            fig = go.Figure(data=[scatter1, scatter2], layout=layout)

            # Display the figure
            st.plotly_chart(fig)
          
            

    else:
        st.error("Invalid file format. Please upload a CSV file.")


