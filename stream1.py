import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from streamlit_extras.buy_me_a_coffee import button
from pandasql import sqldf

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
def display_data(df_session):
    st.write("Cleaned Data:")
    st.dataframe(df_session)


# App Title
st.title("CsvCleaner App")

st.write('''Is your data tangled in a web of disorder and inconsistencies? Meet CSV Cleaner,
          the ultimate no code and SQL solution tailored for those seeking to breathe life into messy datasets.
            Built with a passion for precision, our app specializes in the fine art of data cleaning and meticulous ordering.''')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file is not None:
    session_state = st.session_state
    if 'df' not in session_state:
        session_state['df'] = pd.read_csv(uploaded_file)

    st.write("Dataframe View:")
    st.button("Refresh Dataframe", type="primary")
    st.dataframe(session_state['df'])

    # Rename Columns Button
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
            session_state['df'] = handle_missing_values(session_state['df'])

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
    col1, col2, col3 = st.columns(3)
    with col1:
        if session_state['df'] is not None:
            st.download_button(label="Download Cleaned Data", data=session_state['df'].to_csv(
                index=False), file_name="cleaned_data.csv")
    with col2:
        if st.button("Reload page"):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    st.markdown("""---""")

    if 'df' in session_state:
        df = session_state['df']

    with st.expander("🗃️ Type in your SQL queries for advanced cleaning"):
        sql_query = st.text_area(
            "Enter your SQL query:" + "   " + "(table name will be 'df' by default)")

        if st.button("Execute Query"):
            if sql_query:

                # Execute the SQL query
                try:
                    result_df = sqldf(sql_query)
                    st.write("Query Result:")
                    st.dataframe(result_df)
                except Exception as e:
                    st.error(f"Error executing SQL query: {e}")

        # Download Cleaned Data Button
                col1, col2, col3 = st.columns(3)
                with col1:
                    if session_state['df'] is not None:
                        df = result_df
                        st.download_button(label="Download Cleaned Data", data=df.to_csv(
                            index=False), file_name="cleaned_data_sql.csv")

    st.write('\n')
    st.write('\n')

    button(username="joganutl", floating=False, width=220)
