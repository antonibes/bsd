import os
import subprocess

import pandas as pd
import streamlit as st

from src.data_layer.loader import DataLoader
from src.services.categorizer import TransactionCategorizer
from src.services.predictor import ExpensePredictor
from src.ui.charts import (
    render_cashflow_timeline,
    render_category_donut,
    render_prediction_chart,
)
from src.ui.kpi import render_kpi_cards

st.set_page_config(
    page_title="Cashflow Analytics & Forecasting",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            max-width: 1400px;
        }
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-weight: 500;
        }
        /* Muted Metric cards */
        div[data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 600;
            color: #34495e;
        }
        /* Subdued text for descriptions */
        .stMarkdown {
            color: #5d6d7e;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_prepare_data(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
         return pd.DataFrame()

    loader = DataLoader(filepath)
    df = loader.load_and_validate()
    df = TransactionCategorizer.apply_categories(df)
    return df

@st.cache_resource
def get_trained_predictor(df: pd.DataFrame) -> ExpensePredictor:
    predictor = ExpensePredictor()
    predictor.train(df)
    return predictor

def main():
    st.title("Cashflow Analytics")

    with st.sidebar:
        st.header("Data Configuration")
        uploaded_file = st.file_uploader("Upload Bank Export (.csv, .xlsx)", type=['csv', 'xlsx'])
        data_path = 'data/transactions.csv'

        if uploaded_file is not None:
             with open(data_path, 'wb') as f:
                 f.write(uploaded_file.getbuffer())
             st.success("Data source successfully uploaded.")

        if st.button("Generate Synthetic Data", use_container_width=True):
             with st.spinner("Generating synthetic transaction history..."):
                 subprocess.run(["python", "generate_mock_data.py"], check=True)
                 st.rerun()

        st.markdown("---")
        st.markdown("**Core Modules:**")
        st.markdown("- Presentation: `Streamlit`\n- Data Pipeline: `Pandas`, `Pydantic`\n- Forecasting: `Scikit-learn`")
        st.markdown("<small>License: MIT | © Antoni Beśka</small>", unsafe_allow_html=True)

    with st.spinner("Processing data sources..."):
         df = load_and_prepare_data(data_path)

    if df.empty:
        st.warning("No data found. Please initialize data source via sidebar.")
        return

    render_kpi_cards(df)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Overview", "Expenditure Breakdown", "30-Day Forecast"])

    with tab1:
        st.plotly_chart(render_cashflow_timeline(df), key="timeline", on_select="ignore")

        with st.expander("Transaction Ledger"):
            st.dataframe(df.head(250))

    with tab2:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(render_category_donut(df), key="donut", on_select="ignore")
        with col2:
            st.subheader("Aggregate by Category")
            expenses = df[df['amount'] < 0]
            cat_sum = expenses.groupby('category')['amount'].sum().abs().sort_values(ascending=False)
            st.dataframe(cat_sum)

    with tab3:
        st.markdown("### Predictive Expense Model")

        with st.spinner("Training predictive model..."):
            predictor = get_trained_predictor(df)
            last_date = df['date'].max().date()
            future_df = predictor.predict_future(last_date, days_ahead=30)

            st.plotly_chart(render_prediction_chart(df, future_df), key="prediction", on_select="ignore")

            total_predicted = future_df['predicted_expense'].sum()
            st.info(f"**Projected Aggregate Outflow (30 Days):** {total_predicted:,.2f} PLN")

if __name__ == "__main__":
    main()
