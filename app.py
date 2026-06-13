import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Set a wide, ultra-modern page layout
st.set_page_config(page_title="Expense Tracker", layout="wide")

# --- CUSTOM CSS THEME (Color Palette from c06f809dd75e18fe334692df91c84392.jpg) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&family=Playfair+Display:wght@600&family=Poppins:wght@400;600&display=swap');
    
    /* Main App Canvas Setup with Creme Background */
    .stApp {
        background-color: #D2CDC3 !important; /* Creme Outside Background */
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #3E2B24; /* Brownie Body Text */
    }
    
    /* Header Accent Banner in Deep Ruby */
    .header-banner {
        background-color: #3E1F20; /* Ruby */
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Main Title Styling inside the banner (Creme color for optimal reading contrast) */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 46px;
        font-weight: 600;
        color: #D2CDC3 !important; /* Creme Title Text */
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    /* Original Section Headings Styling in Ruby for Main Content */
    h3, .section-header {
        color: #3E1F20 !important; /* Ruby */
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        margin-top: 15px;
    }
    
    /* SAFELY ISOLATED: Force ONLY Sidebar Headings to Creme Color */
    section[data-testid="stSidebar"] h3 {
        color: #D2CDC3 !important;
    }
    
    /* Force Sidebar Input Labels (Set Total Amount / Set Max Spending Limit) to Creme Color */
    section[data-testid="stSidebar"] label {
        color: #D2CDC3 !important;
    }
    
    /* Metric Card Customization */
    div[data-testid="stMetricLabel"] > div {
        color: #3E1F20 !important; /* Ruby Labels */
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #3E2B24 !important; /* Brownie Values */
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* Style Form Inputs for crisp visibility against Creme */
    .stSelectbox, .stNumberInput, .stTextInput {
        color: #3E2B24 !important;
    }
    
    label {
        color: #3E1F20 !important; /* Form Labels in Ruby for Main Page */
        font-weight: 500;
    }
    
    /* Style the Form Button to match the Ruby layout */
    .stButton>button {
        background-color: #3E1F20 !important; /* Ruby */
        color: #D2CDC3 !important; /* Creme text */
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #552B2C !important; /* Lighter Ruby */
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1 class="main-title">Expense Tracker</h1>
        <p style='color: #D2CDC3; margin-top: 8px; font-family: "Plus Jakarta Sans"; font-size: 16px; font-style: italic; letter-spacing: 0.5px; opacity: 0.95;'>
            — spend smarter, live richer, track easier —
        </p>
    </div>
""", unsafe_allow_html=True)

# --- DATA PROCESSING SETUP ---
if os.path.isfile("expenses.csv"):
    try:
        df = pd.read_csv("expenses.csv")
        total_used = float(df["Amount"].sum())
    except Exception:
        df = pd.DataFrame(columns=["Category", "Amount", "Description"])
        total_used = 0.0
else:
    df = pd.DataFrame(columns=["Category", "Amount", "Description"])
    total_used = 0.0

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    total_savings = st.number_input("Set Total Amount ($)", min_value=1.0, value=30000.0, step=500.0)
    
    st.markdown("---")
    st.markdown("### ⚠️ Spend Guard")
    warning_limit = st.number_input("Set Max Spending Limit ($)", min_value=0.0, value=5000.0, step=100.0)
    st.caption("Triggers visual dashboard warnings if expenditures break this marker.")

# --- FINANCIAL METRICS DASHBOARD ---
st.markdown("### 🏷️ Expenditure Tracking")
remaining_savings = total_savings - total_used
spent_percentage = min(100, int((total_used / total_savings) * 100)) if total_savings > 0 else 100
remaining_percentage = max(0, 100 - spent_percentage)

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Savings", value=f"${total_savings:,.2f}")
col2.metric(label="Amount Used", value=f"${total_used:,.2f}", delta=f"-${total_used:,.2f}", delta_color="inverse")
col3.metric(label="Remaining Balance", value=f"${remaining_savings:,.2f}")

# Dynamic Budget Progress Bar
st.progress(remaining_percentage / 100)

# Threshold Notification Triggers
if total_used >= warning_limit:
    st.error(f"⚠️ **LIMIT EXCEEDED:** Total expenditure has overridden your custom ${warning_limit:,.2f} safeguard ceiling!")
elif total_used >= (warning_limit * 0.8):
    st.warning(f"⏳ **BUDGET WARNING:** Your spending has consumed over 80% of your allowed threshold!")

st.markdown("---")

# --- USER INPUT & DATA VISUALIZATION ---
col_left, col_right = st.columns([2, 3])

with col_left:
    st.markdown("### 🖋️ Transaction Details")
    
    category = st.selectbox("Choose Category", [
        "🍟 Food & Cafes", 
        "🛒 Shopping & Fits", 
        "📱 Subscriptions", 
        "🛫 Travel & Transit", 
        "🧴 Self-Care & Beauty", 
        "💳 Savings & Investments", 
        "🏷️ Other"
    ])
    
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=1.0)
    description = st.text_input("Transaction Note", placeholder="e.g., Starbucks, Zara, Netflix, Gas")

    if st.button("Commit Transaction", width="stretch"):
        if amount > 0: 
            new_row = pd.DataFrame([[category, amount, description]], columns=["Category", "Amount", "Description"])
            if not os.path.isfile("expenses.csv"):
                new_row.to_csv("expenses.csv", index=False)
            else:
                new_row.to_csv("expenses.csv", mode='a', header=False, index=False)
            st.success("Entry securely logged!")
            st.rerun()
        else:
            st.warning("Please specify an amount greater than 0.")

with col_right:
    st.markdown("### 💰 Total Available Balance")
    
    # Process Pie Chart Slices
    if not df.empty:
        spending_by_cat = df.groupby("Category")["Amount"].sum().reset_index()
    else:
        spending_by_cat = pd.DataFrame(columns=["Category", "Amount"])
    
    if remaining_savings > 0:
        remaining_row = pd.DataFrame([["Remaining Balance", remaining_savings]], columns=["Category", "Amount"])
        pie_data = pd.concat([spending_by_cat, remaining_row], ignore_index=True)
    else:
        pie_data = spending_by_cat

    # Draw the Pie Chart matching the color choices
    if not pie_data.empty and pie_data["Amount"].sum() > 0:
        organic_pie_palette = ['#3E1F20', '#3E2B24', '#AA9F95', '#6E5D53', '#543C3E', '#8C7A6B', '#4A3B32', '#D2CDC3']
        
        fig = px.pie(
            pie_data, 
            values='Amount', 
            names='Category', 
            hole=0.45,
            color_discrete_sequence=organic_pie_palette
        )
        fig.update_traces(textinfo='percent+label', textfont_size=12, textfont_family="Plus Jakarta Sans")
        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#3E2B24', family="Plus Jakarta Sans")
        )
        # FIXED: Reverted back to container width to eliminate the yellow box warning completely
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Log your initial expense rows to populate your asset distribution visualization matrix.")

# --- TRANSACTION HISTORY LOG ---
if not df.empty:
    st.markdown("---")
    st.markdown("### 📜 Ledger Transaction History")
    st.dataframe(df, width="stretch", height=220)