import streamlit as st

# Initialize session state variables
if 'users' not in st.session_state:
    st.session_state.users = {}                 # Dictionary to store username and PIN
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None      # To check whether the user is logged in or not
if 'balance' not in st.session_state:
    st.session_state.balance = 1000             # Balance initially = 1000

# Function to register a new user
def register_user(username, pin):
    if username in st.session_state.users:
        st.error("Username already exists. Please choose a different username.")
    else:
        st.session_state.users[username] = pin
        st.success("User registered successfully!")

# Function to authenticate user
def authenticate_user(username, pin):
    if username in st.session_state.users and st.session_state.users[username] == pin:
        st.session_state.logged_in_user = username
        st.success("Login successful!")
    else: 
        st.error("Invalid username or PIN.")

# Function to log out the user
def logout():
    st.session_state.logged_in_user = None      # Reset's the logged in user to none
    st.session_state.balance = 1000             # Reset's the balance to 0
    st.success("Logged out successfully.")      # Display's success message after logout

# Main application title
st.title("ATM Interface")

if st.session_state.logged_in_user is None:     # Check if the user is logged in
    # New User Registration
    st.subheader("Register")
    new_username = st.text_input("New Username")
    new_pin = st.text_input("New PIN", type="password")
    if st.button("Register"):
        register_user(new_username, new_pin)

    # Existing User Login
    st.subheader("Login")
    username = st.text_input("Username")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        authenticate_user(username, pin)
else:                                           
    st.write(f"Welcome, {st.session_state.logged_in_user}!")            # When User is logged in
    st.write(f"Current Balance: ₨ {st.session_state.balance}")

    # Withdrawal functionality
    st.subheader("Withdraw")
    withdraw_amount = st.number_input("Enter the amount to withdraw:", min_value=0, step=1)

    if st.button("Withdraw"):
        if withdraw_amount <= st.session_state.balance:
            st.session_state.balance -= withdraw_amount
            st.success("Withdrawal successful!")
        else:
            st.error("Insufficient balance.")

    # Deposit functionality
    st.subheader("Deposit")
    deposit_amount = st.number_input("Enter the amount to deposit:", min_value=0, step=1)

    if st.button("Deposit"):
        st.session_state.balance += deposit_amount
        st.success("Deposit successful!")

    # Logout button
    if st.button("Logout"):
        st.write(f"Your Closing balance is ₨ {st.session_state.balance}")
        logout()