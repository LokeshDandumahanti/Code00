import streamlit as st
import webbrowser


# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Product database
products = {
    'Hide & Seek': 30,
    'Maggi': 20,
    'coffee': 10,
}

# Display products
st.title('E-commerce Site')

total_price = 0.0

for product, price in products.items():
    quantity_key = f'quantity_{product.lower().replace(" ", "_")}'
    quantity = st.number_input(f'Quantity of {product}', min_value=0, step=1, key=quantity_key)
    total_key = f'total_{product.lower().replace(" ", "_")}'
    total = quantity * price
    st.session_state.cart[total_key] = total
    total_price += total

# Display cart
st.title('Cart')
for product, price in products.items():
    total_key = f'total_{product.lower().replace(" ", "_")}'
    total = st.session_state.cart.get(total_key, 0)
    if total > 0:
        st.write(f'{product}: {total_price}')

st.write(f'Net Price: {total_price}')

# Transaction section
# Transaction section
st.title('Transaction')

# Function to open Google Pay page with the specified amount


# Function to open Google Pay page with the specified amount and QR code image
def open_google_pay(amount, qr_code_path):
    url = f'https://wallet.google/'
    webbrowser.open(url)

# Transaction section

amount = st.number_input('Enter Amount', int(total_price))
qr_code_path = "C:/Users/vijay/OneDrive/Desktop/jiven.jpg"  # Path to your QR code image
if st.button('Buy'):
    open_google_pay(amount, qr_code_path)
    st.success(f'Opened Google Pay page for ₹{amount:.2f} payment.')
