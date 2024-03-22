import streamlit as st
import pandas as pd

file_path = "chocolate.csv"
df = pd.read_csv(file_path)

st.title('Entries')

# Allow users to add new entries
st.header('Add New Entry')
with st.form("add_entry_form"):
    name = st.text_input('Name')
    age = st.number_input('Age', min_value=0, max_value=150)
    email = st.text_input('Email')
    submit_button = st.form_submit_button('Submit')

if submit_button:
    new_entry = pd.DataFrame({'Name': [name],
                              'Age': [age], 
                              'Email': [email]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(file_path, index=False)
    st.success('Entry added successfully!')

# Allow users to view entries with password protection
st.header('View Entries (Password Protected)')
password = st.text_input('Enter Password:', type='password')
if password == 'Dora':
    st.write(df[::-1])
elif password != '':
    st.warning('Incorrect password. Please try again.')
