import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from streamlit_extras.buy_me_a_coffee import button
from pandasql import sqldf

st.set_page_config(layout="wide")

st.markdown(
    """
<style>
.css-cio0dv.ea3mdgi1
{
    display: none;
}
.css-czk5ss.e16jpq800
{
    display: none;
}
.stActionButton
{
    display:none;
}
</style>
""", unsafe_allow_html=True)


def handle_missing_values(df_session):
    try:
        cleaned_df = df_session.dropna()
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error handling missing values: {e}")
        return df_session


# Function to rename columns
def rename_columns(df_session, column_mapping):
    try:
        cleaned_df = df_session.rename(columns=column_mapping)
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error renaming columns: {e}")
        return df_session


# Function to remove duplicate rows
def remove_duplicates(df_session):
    try:
        cleaned_df = df_session.drop_duplicates()
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error removing duplicates: {e}")
        return df_session


# Function to convert data type of a specific column
def convert_data_type(df_session, column_name, target_dtype):
    try:
        cleaned_df = df_session.astype({column_name: target_dtype})
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error converting data type: {e}")
        return df_session


# Function to drop specified columns
def drop_columns(df_session, columns_to_drop):
    try:
        cleaned_df = df_session.drop(columns=columns_to_drop, errors='ignore')
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error dropping columns: {e}")
        return df_session


# Function to fill missing values in a specific column with a specified value
def fill_na_column_specific(df_session, column_name, fill_value):
    try:
        cleaned_df = df_session.fillna({column_name: fill_value})
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error filling missing values: {e}")
        return df_session


def order_by_column(df_session, column_name, ascending=True):
    try:
        cleaned_df = df_session.sort_values(
            by=column_name, ascending=ascending)
        st.success("Task completed")
        return cleaned_df
    except Exception as e:
        st.error(f"Error ordering by column: {e}")
        return df_session


# Function to display data
def delete_session(df_session):
    del df_session


# App Title

button(username="joganutl", floating=False, width=220, bg_color='#00B3FF', )
st.title("CsvCleaner")

lay1, lay2 = st.columns([3, 2])

with lay1:
    st.caption('''CSV Cleaner App is a web application for cleaning and manipulating CSV data. It provides various options for data cleaning operations, including handling missing values, renaming columns, removing duplicates, converting data types, dropping columns, filling missing values, and sorting data.''')

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        session_state = st.session_state
        if 'df' not in session_state:
            session_state['df'] = pd.read_csv(uploaded_file)

        st.write("Dataframe View:")
        st.button("Refresh Dataframe", type="primary")
        st.dataframe(session_state['df'], width=1000, height=600)

        with lay2:
            if st.button("Clear Current Session", type="secondary"):
                streamlit_js_eval(
                    js_expressions="parent.window.location.reload()")
            st.write('\n')
            st.write('\n')
            st.write('\n')

            with st.expander("HOW TO USE"):
                st.caption(
                    '1. Click on the "Upload CSV file" button to upload your CSV data.')
                st.caption(
                    "2. Once the CSV file is uploaded, you'll see a view of the dataframe. Use the 'Refresh button' to see changes.")
                st.caption(
                    '3. Expand the section titled "🔄 Rename your columns as you please". Enter new names for the columns as desired and click "Apply Column Renaming".')
                st.caption('4. Expand the section titled "🔀 Convert datatypes of your columns". Select a column to convert its data type, choose the target data type, and click "Convert Data Type".')
                st.caption(
                    '5. Expand the section titled \"🔽 Drop columns you don\'t need\". Select the columns to drop and click \"Drop Columns\".')
                st.caption('6. Expand the section titled "🔍 Fill missing data from your columns". Select a column and enter a value to fill missing entries. Click "Fill Missing Values".')
                st.caption(
                    '7. Expand the section titled "⬆️⬇️ Sort your data in ascending or descending". Select a column and choose the sorting order. Click "Order by Column".')
                st.caption(
                    '8. Use "Clear Current Session" button to clear the current session and upload another CSV file')

            with st.expander("🔄 Rename your columns as you please"):
                st.write("Rename Columns:")
                column_mapping = {}
                for col in session_state['df'].columns:
                    new_name = st.text_input(f"New Name for '{col}'", key=col)
                    if new_name:
                        column_mapping[col] = new_name

                if st.button("Apply Column Renaming") and column_mapping:
                    session_state['df'] = rename_columns(
                        session_state['df'], column_mapping)

            if 'df' in session_state:
                session_state['df'] = session_state['df']

            # Handle Missing Values Button
            with st.expander("🗑️ Drop null values from your data"):

                if st.button("Handle Missing Values"):
                    session_state['df'] = handle_missing_values(
                        session_state['df'])

            if 'df' in session_state:
                session_state['df'] = session_state['df']

            # Convert Data Type Button (Column Specific)
            with st.expander("🔀 Convert datatypes of your columns"):
                convert_column = st.selectbox(
                    "Select Column to Convert Data Type", session_state['df'].columns)
                target_dtype = st.selectbox("Select Target Data Type", [
                    'int', 'float', 'str'])

                if st.button("Convert Data Type"):
                    target_dtype = int if target_dtype == 'int' else float if target_dtype == 'float' else str
                    session_state['df'] = convert_data_type(
                        session_state['df'], convert_column, target_dtype)

            if 'df' in session_state:
                session_state['df'] = session_state['df']

            # Drop Columns Button
            with st.expander("🔽 Drop columns you dont need"):
                columns_to_drop = st.multiselect(
                    "Select Columns to Drop", session_state['df'].columns)
                if st.button("Drop Columns"):
                    session_state['df'] = drop_columns(
                        session_state['df'], columns_to_drop)

            if 'df' in session_state:
                session_state['df'] = session_state['df']

            # Fill Missing Values Button (Column Specific)
            with st.expander("🔍 Fill missing data from your columns"):
                fill_column = st.selectbox(
                    "Select Column to Fill", session_state['df'].columns)
                fill_value = st.text_input(
                    f"Fill missing values in '{fill_column}' with:")
                if st.button("Fill Missing Values") and fill_value:
                    session_state['df'] = fill_na_column_specific(
                        session_state['df'], fill_column, fill_value)

            if 'df' in session_state:
                session_state['df'] = session_state['df']

            with st.expander("⬆️⬇️ Sort your data in ascending or descending"):
                order_column = st.selectbox(
                    "Select Column to Order By", session_state['df'].columns)
                order_direction = st.radio(
                    "Order Direction", ["Ascending", "Descending"])

                ascending_order = True if order_direction == "Ascending" else False

                if st.button("Order by Column"):
                    session_state['df'] = order_by_column(
                        session_state['df'], order_column, ascending_order)

            # Download Cleaned Data Button
            col1, col2 = st.columns([2, 3])
            with col1:
                if session_state['df'] is not None:
                    st.download_button(label="Download Cleaned Data", data=session_state['df'].to_csv(
                        index=False), file_name="cleaned_data.csv")


# else:
#     st.write("Dataframe View:")
#     st.dataframe(pd.DataFrame(), width=1000)
