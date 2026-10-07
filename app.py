import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Mobile Phone Sales Data Analysis",
    page_icon="📱",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #1f77b4;
        font-weight: bold;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        color: #555555;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Title Header
st.markdown('<div class="main-title">📱 Mobile Phone Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">An interactive dashboard highlighting key insights from the mobile sales dataset.</div>', unsafe_allow_html=True)

# Load Dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv('Sales.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ `Sales.csv` file not found! Please ensure it is in the same directory as `app.py`.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to:", ["Overview & Summary", "Brand Analysis", "Pricing & Discounts", "Raw Data Explorer"])

# 1. Overview & Summary
if options == "Overview & Summary":
    st.header("📊 Dataset Overview & Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{df.shape[0]:,}")
    with col2:
        st.metric("Total Features", df.shape[1])
    with col3:
        st.metric("Unique Brands", df['Brands'].nunique())
    with col4:
        st.metric("Unique Models", df['Models'].nunique())

    st.markdown("---")
    
    st.subheader("Statistical Summary of Numerical Columns")
    st.dataframe(df.describe().style.format("{:.2f}"))

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

# 2. Brand Analysis
elif options == "Brand Analysis":
    st.header("🏢 Brand Distribution & Market Presence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Number of Models per Brand")
        brand_counts = df['Brands'].value_counts()
        st.bar_chart(brand_counts)
        
    with col2:
        st.subheader("Brand Share (Pie Chart)")
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(brand_counts, labels=brand_counts.index, autopct='%1.1f%%', startangle=140, 
               colors=sns.color_palette("pastel"))
        ax.axis('equal')
        st.pyplot(fig)

# 3. Pricing & Discounts
elif options == "Pricing & Discounts":
    st.header("💰 Pricing & Discount Analysis")
    
    st.subheader("Average Selling Price by Brand")
    avg_prices = df.groupby('Brands')['Selling Price'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    avg_prices.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Average Selling Price per Brand[cite: 1]")
    ax.set_xlabel("Brands")
    ax.set_ylabel("Average Selling Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Average Discount Percentage by Brand")
    avg_discount = df.groupby('Brands')['discount percentage'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    avg_discount.plot(kind='bar', color='salmon', ax=ax)
    ax.set_title("Average Discount Percentage (%)[cite: 1]")
    ax.set_xlabel("Brands")
    ax.set_ylabel("Discount Percentage")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 4. Raw Data Explorer
elif options == "Raw Data Explorer":
    st.header("🔍 Explore Raw Data")
    
    # Filters
    selected_brand = st.selectbox("Filter by Brand", ['All'] + sorted(df['Brands'].unique().tolist()))
    
    if selected_brand != 'All':
        filtered_df = df[df['Brands'] == selected_brand]
    else:
        filtered_df = df
        
    st.write(f"Showing **{len(filtered_df)}** records:")
    st.dataframe(filtered_df)