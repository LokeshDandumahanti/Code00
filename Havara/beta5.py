import streamlit as st
import pandas as pd
import os
from PIL import Image

# Dictionary to store usernames and passwords
users = {
    'user1': {'password': 'password1', 'room_number': 'R01'},
    'Dibendhu747' : {'password': 'Ghosh1234', 'room_number' : 'R22'},
    'user2': {'password': 'password2', 'room_number': 'T12'},
    'user3': {'password': 'password3', 'room_number': 'S34'}
}

def sign_in():
    # Define the CSS styles for the app
    st.markdown(
        """
        <style>
        body {
            color: white;
            background-color: #f4a261;
            font-family: Arial, sans-serif;
        }
        h1 {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            text-align: center;
            font-size: 36px;
            margin-bottom: 0;
        }
        h3 {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            text-align: center;
            font-size: 20px;
            margin-top: -10px;
        }
        .stTextInput>div>div>input {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def sign_in():
    st.title('Halolo')
    st.subheader('where hunger meets comfort')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    room_letter = st.selectbox('Room Letter', ['R', 'T', 'S', 'F', 'G'])
    room_number_1 = st.number_input('Room Number (1st digit)', min_value=0, max_value=9, step=1)
    room_number_2 = st.number_input('Room Number (2nd digit)', min_value=0, max_value=9, step=1)
    room_number = f'{room_letter.upper()}{room_number_1}{room_number_2}'

    if st.button('Sign In'):
        if username in users and users[username]['password'] == password and users[username]['room_number'] == room_number:
            st.session_state.signed_in = True
            st.session_state.username = username
            st.session_state.room_number = room_number
            st.session_state.total_price = 0  # Initialize total_price
            st.session_state.order_details = {}  # Initialize order_details
            st.success(f'Welcome {username}')
        else:
            st.error('Invalid username, password, or room number.')

def inventory_management(file_path, order_file_path, image_path):
    if 'signed_in' not in st.session_state or not st.session_state.signed_in:
        sign_in()
        return

    df = pd.read_csv(file_path)

    # Prices of Maggis, masala, and ParleG
    Maggi_price = 15
    masala_price = 5
    ParleG_price = 5

    st.title('Savouries and Stationary')

    # Display current inventory for Maggis, masala, and ParleG
    st.header('Quantities remaining in inventory')
    st.write(df)

    # Display total price
    st.header('Place an Order')
    order_Maggi = st.number_input(' Maggi (15rs) :', min_value=0, max_value=df['Maggi'].sum())
    order_masala = st.number_input(' masala (5rs) :', min_value=0, max_value=df['masala'].sum())
    order_ParleG = st.number_input(' ParleG (5rs) :', min_value=0, max_value=df['ParleG'].sum())

    total_price = order_Maggi * Maggi_price + order_masala * masala_price + order_ParleG * ParleG_price 
    st.write(f'Total Price: {total_price}')

    # Load an image from the local filesystem
    image = Image.open(image_path)
    st.image(image, caption='Your Image', width=300)
    order_confirmed = st.checkbox('Have you completed the payment?')
    if order_confirmed and st.button('Order'):
        new_total_Maggi = df.loc[0, 'Maggi'] - order_Maggi
        new_total_masala = df.loc[0, 'masala'] - order_masala
        new_total_ParleG = df.loc[0, 'ParleG'] - order_ParleG
        if new_total_Maggi >= 0 and new_total_masala >= 0 and new_total_ParleG >= 0:
            df.loc[0, 'Maggi'] = new_total_Maggi
            df.loc[0, 'masala'] = new_total_masala
            df.loc[0, 'ParleG'] = new_total_ParleG
            df.to_csv(file_path, index=False)

            # Add order  .csv
            if not os.path.exists(order_file_path):
                order_df = pd.DataFrame(columns=['username', 'room_number', 'Maggi_Noodles', 'Maggi_Masala', 'ParleG', 'Delivery_Charges', 'total'])
                order_df.to_csv(order_file_path, index=False)
            order_df = pd.DataFrame({'username': [st.session_state.username],
                                     'room_number': [st.session_state.room_number],
                                     'Maggi_Noodles': [order_Maggi],
                                     'Maggi_Masala': [order_masala],
                                     'ParleG': [order_ParleG],
                                     'total': [total_price]})
            order_df.to_csv(order_file_path, mode='a', header=not os.path.exists(order_file_path), index=False)
            st.success('It is a pleasure doing buisness with you. Your order will be delivered to your room by 9pm')
            # Reset order confirmation state
        else:
            st.error('Insufficient quantity in stock!')

    # Allow users to view entries with password protection
    st.header('View Orders (Password Protected)')
    password = st.text_input('Enter Password:', type='password')
    if password == 'Dora':
        try:
            order_df = pd.read_csv(order_file_path)
            st.write(order_df[::-1])
        except FileNotFoundError:
            st.info('No orders placed yet.')
    elif password != '':
        st.warning('Incorrect password. Please try again.')

# Example usage
file_path = "Inventory.csv"
order_file_path = "Orders.csv"
image_path = "cutie.jpg"
inventory_management(file_path, order_file_path, image_path)
