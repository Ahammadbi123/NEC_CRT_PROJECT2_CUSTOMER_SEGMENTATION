import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_prep import prepare_data
from src.segmentation import perform_segmentation

st.title("🌐 IndiSegment Pro: Analytics Dashboard")

if st.button('🚀 Run Analysis'):
    
    processed_path = prepare_data('data/raw_customers.csv')
    df, summary = perform_segmentation(processed_path)
    
    st.success("Analysis Complete!")
    
    
    fig = px.scatter(df, x='Annual Income (₹ Lakhs)', y='Spending_Score', color='Cluster')
    st.plotly_chart(fig)
    
    st.write("### Customer Summary", summary)