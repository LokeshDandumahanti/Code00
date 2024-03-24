import streamlit as st
import pandas as pd
import os

# Dictionary to store usernames and passwords
users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

import streamlit as st

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

    # Display the styled title
    st.title('Halolo')
    st.subheader('where hunger meets comfort')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Sign In'):
        if username in users and users[username] == password:
            st.session_state.signed_in = True
            st.session_state.username = username
            st.session_state.total_price = 0  # Initialize total_price
            st.success(f'Welcome {username}')
        else:
            st.error('Invalid username or password.')


def inventory_management(file_path, order_file_path):
    if 'signed_in' not in st.session_state or not st.session_state.signed_in:
        sign_in()
        return

    df = pd.read_csv(file_path)

    # Prices of chocolates and pasta
    chocolate_price = 30
    pasta_price = 60

    st.title('Inventory Management')

    # Display current inventory for chocolates and pasta
    st.header('Savouries and Stationary')
    st.write(df)

    # Display total price
   

    # Allow users to place an order for chocolates and pasta
    st.header('Place an Order')
    order_chocolate = st.number_input('Enter the quantity of chocolate to order:', min_value=0, max_value=df['chocolate'].sum())
    order_pasta = st.number_input('Enter the quantity of pasta to order:', min_value=0, max_value=df['pasta'].sum())

    total_price = order_chocolate * chocolate_price + order_pasta * pasta_price
    st.write(f'Total Price: {total_price}')

    if st.button('Order'):
        new_total_chocolate = df.loc[0, 'chocolate'] - order_chocolate
        new_total_pasta = df.loc[0, 'pasta'] - order_pasta
        if new_total_chocolate >= 0 and new_total_pasta >= 0:
            df.loc[0, 'chocolate'] = new_total_chocolate
            df.loc[0, 'pasta'] = new_total_pasta
            df.to_csv(file_path, index=False)

            # Calculate total price


            # Add order to order.csv
            if not os.path.exists(order_file_path):
                order_df = pd.DataFrame(columns=['chocolate', 'pasta', 'total'])
                order_df.to_csv(order_file_path, index=False)
            order_df = pd.DataFrame({'chocolate': [order_chocolate], 'pasta': [order_pasta], 'total': [total_price]})
            order_df.to_csv(order_file_path, mode='a', header=not os.path.exists(order_file_path), index=False)
            st.success('Order placed successfully!')
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
file_path = "chocolate.csv"
order_file_path = "Order.csv"
inventory_management(file_path, order_file_path)
