import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.data_prep import prepare_data
from src.segmentation import perform_segmentation

# 1. Page Configuration
st.set_page_config(page_title="IndiSegment Pro | Intelligence Suite", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Dark Neon Theme (Fixed unsafe_allow_html)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border: none; padding: 10px 24px;
        border-radius: 10px; font-weight: bold; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 15px #4facfe; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px;
        border-left: 5px solid #00f2fe;
        margin-bottom: 10px;
    }
    h1 { color: #00f2fe; text-shadow: 0px 0px 10px #00f2fe; }
    h2, h3 { color: #4facfe; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0px 0px; color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background: #4facfe !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Header Section
col_t1, col_t2 = st.columns([1, 5])
with col_t1:
    st.title("🌐")
with col_t2:
    st.title("IndiSegment Pro: Intelligence Suite")
    st.write("---")

# 3. Sidebar Configuration
st.sidebar.markdown("### 🛠 Control Center")
# --- FIX 1: Line 51 completed with 'else' ---
data_file = 'data/mall_customers_india.csv' if os.path.exists('data/mall_customers_india.csv') else 'data/raw_customers.csv'
run_engine = st.sidebar.button('🚀 RUN ANALYTICS ENGINE')

# Executive Overview
st.markdown("""
### 🌐 Executive Overview: IndiSegment Pro
**IndiSegment Pro** is an enterprise-grade Behavioral Intelligence Suite specifically engineered for the **Indian Retail Ecosystem**. It leverages advanced **Unsupervised Machine Learning** to transform raw transactional data into high-value strategic market segments.

---

#### 🚀 Core Objectives
*   **Localized Intelligence:** Processes financial data in **Indian Rupees (₹ Lakhs)**, ensuring regional business relevance.
*   **Behavioral Partitioning:** Utilizes **K-Means Clustering** to identify 5 distinct customer personas based on purchasing power and spending velocity.
*   **Dimensionality Reduction:** Implements **Principal Component Analysis (PCA)** to visualize complex multi-dimensional customer data in a simplified 2D strategic map.
*   **RFM Integration:** Incorporates **Recency, Frequency, and Monetary** logic to track the "Financial Pulse" of the customer base.

#### 📊 Strategic Impact
By identifying high-value **Elite VIPs**, **Impulse Buyers**, and **Budget Guardians**, IndiSegment Pro empowers retail managers to:
1. **Optimize Marketing Spend:** Target the right segment with the right offer.
2. **Increase Retention:** Identify and re-engage "At-Risk" high-income customers.
3. **Maximize ROI:** Drive profitability through data-backed seasonal campaigns.

---
""", unsafe_allow_html=True)
st.write("")

# 4. Main Engine Logic
if run_engine:
    # Check if data exists
    if not os.path.exists(data_file):
        st.error(f"❌ File not found: {data_file}. Please check your 'data' folder.")
    else:
        # --- FIX 2: Using the 'data_file' variable here instead of hardcoded name ---
        processed_path = prepare_data(data_file)
        df, summary = perform_segmentation(processed_path)
        
        st.balloons()
        
        # KPI Metrics
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card">👥 Total Customers<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card" style="border-left-color: #ff9a9e;">💰 Avg Income<br><h2>₹{df["Annual Income (₹ Lakhs)"].mean():.1f}L</h2></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card" style="border-left-color: #a18cd1;">📊 Clusters<br><h2>5</h2></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card" style="border-left-color: #f6d365;">⭐ Avg Score<br><h2>{df["Spending_Score"].mean():.0f}</h2></div>', unsafe_allow_html=True)

        st.write("")

        # Visual Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💎 MARKET CLUSTERS", "🧠 PCA INTELLIGENCE", "📉 ELBOW LAB", "📋 DATA DIRECTORY"])

        with tab1:
            st.subheader("📍 Wealth vs Spending Map")
            fig_m = px.scatter(df, x='Annual Income (₹ Lakhs)', y='Spending_Score', 
                               color='Cluster', size='Monetary', hover_name='CustomerName',
                               template='plotly_dark')
            st.plotly_chart(fig_m, use_container_width=True)

        with tab2:
            st.subheader("🌌 High-Dimensional Neural Projection")
            fig_p = px.scatter(df, x='PCA1', y='PCA2', color='Cluster', 
                               symbol='Cluster', template='plotly_dark')
            st.plotly_chart(fig_p, use_container_width=True)

        with tab3:
            st.subheader("🎯 Identifying the Optimal 'K'")
            if os.path.exists('outputs/elbow_plot.png'):
                st.image('outputs/elbow_plot.png', use_column_width=True)
            else:
                st.warning("Elbow Chart is generating... please refresh.")

        with tab4:
            st.subheader("📝 Segment Profile Summary")
            st.dataframe(summary, use_container_width=True)
            
            st.subheader("🔍 Master Data Explorer")
            st.dataframe(df.drop(columns=['PCA1', 'PCA2']), use_container_width=True)

else:
    st.warning("👈 Please initialize the engine from the Sidebar to visualize the intelligence.")

st.markdown("---")
st.markdown("<center>Developed with ❤️ in India | IndiSegment Pro v1.0</center>", unsafe_allow_html=True)
