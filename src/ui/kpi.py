import pandas as pd
import streamlit as st


def render_kpi_cards(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available for KPIs.")
        return

    current_balance = df.iloc[0]['balance'] if 'balance' in df.columns else 0.0

    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expense = df[df['amount'] < 0]['amount'].abs().sum()
    cashflow = total_income - total_expense

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Available Liquidity",
            value=f"{current_balance:,.2f} PLN",
            delta="Latest",
            delta_color="off"
        )

    with col2:
        st.metric(
            label="Gross Inflow",
            value=f"{total_income:,.2f} PLN",
            delta="+",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="Aggregate Outflow",
            value=f"{total_expense:,.2f} PLN",
            delta="-",
            delta_color="inverse"
        )

    with col4:
        delta_sign = "+" if cashflow >= 0 else ""
        st.metric(
            label="Net Variance",
            value=f"{cashflow:,.2f} PLN",
            delta=f"{delta_sign}{cashflow:,.2f}",
            delta_color="normal"
        )
