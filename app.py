import streamlit as st
import pandas as pd
import os

# 1. Title of your web page
st.title("💰 Smart AI Expense Tracker")
st.write("Welcome! Type your transactions below to track your budget.")

# 2. Input fields on the screen
category = st.selectbox("Choose Category", ["Food", "Rent", "Entertainment", "Utilities", "Other"])
amount = st.number_input("Amount ($)", min_value=0.0, step=1.0)
description = st.text_input("What did you buy? (e.g., Coffee, Netflix)")

# 3. What happens when you click the button
if st.button("Save Expense"):
    if amount > 0: # Ensure they actually entered an amount
        # Group the input into a table row
        new_row = pd.DataFrame([[category, amount, description]], columns=["Category", "Amount", "Description"])
        
        # Save it to a spreadsheet file named expenses.csv
        if not os.path.isfile("expenses.csv"):
            new_row.to_csv("expenses.csv", index=False)
        else:
            new_row.to_csv("expenses.csv", mode='a', header=False, index=False)
        
        st.success("Successfully saved!")
        st.rerun() # Forces the charts and tables to refresh instantly
    else:
        st.warning("Please enter an amount greater than 0.")

# 4. Show the table and chart if data exists
if os.path.isfile("expenses.csv"):
    try:
        df = pd.read_csv("expenses.csv")
        
        if not df.empty:
            st.markdown("---") # Visual separator
            
            st.subheader("📊 Your Transaction History")
            st.dataframe(df, use_container_width=True) # Makes the table look nicer
            
            st.subheader("📈 Spending Breakdown")
            chart_data = df.groupby("Category")["Amount"].sum()
            st.bar_chart(chart_data) 
    except Exception as e:
        # Catches edge cases like an empty/corrupted CSV file
        st.info("Start adding expenses to see your history!")