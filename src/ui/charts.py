import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLORS = {
    'income': '#2E7D32',
    'expense': '#C62828',
    'balance': '#1565C0',
    'prediction': '#F9A825',
    'background': 'rgba(0,0,0,0)',
    'text': '#333333',
    'donut': px.colors.qualitative.Pastel
}

def update_layout_style(fig):
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', zeroline=False),
        hovermode="x unified"
    )
    return fig

def render_cashflow_timeline(df: pd.DataFrame) -> go.Figure:
    df_chart = df.copy()
    df_chart['month'] = df_chart['date'].dt.to_period('M').dt.to_timestamp()

    monthly = df_chart.groupby('month').agg(
        income=('amount', lambda x: x[x > 0].sum()),
        expense=('amount', lambda x: x[x < 0].sum())
    ).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=monthly['month'],
        y=monthly['income'],
        name='Inflow',
        marker_color=COLORS['income']
    ))

    fig.add_trace(go.Bar(
        x=monthly['month'],
        y=monthly['expense'],
        name='Outflow',
        marker_color=COLORS['expense']
    ))

    fig.update_layout(
        title="Aggregate Monthly Liquidity",
        barmode='relative',
        xaxis_title="Financial Period",
        yaxis_title="Volume (PLN)"
    )

    return update_layout_style(fig)

def render_category_donut(df: pd.DataFrame) -> go.Figure:
    expenses = df[df['amount'] < 0].copy()
    expenses = expenses[expenses['category'] != 'Inflow / Revenue']
    expenses['amount'] = expenses['amount'].abs()

    cat_totals = expenses.groupby('category')['amount'].sum().reset_index()

    fig = px.pie(
        cat_totals,
        names='category',
        values='amount',
        hole=0.6,
        color_discrete_sequence=COLORS['donut'],
        title="Outflow Distribution"
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return update_layout_style(fig)

def render_prediction_chart(historical_df: pd.DataFrame, future_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    hist_expenses = historical_df[historical_df['amount'] < 0].copy()
    daily_actual = hist_expenses.groupby('date')['amount'].sum().abs().reset_index()
    last_30_actual = daily_actual.tail(30)

    fig.add_trace(go.Scatter(
        x=last_30_actual['date'],
        y=last_30_actual['amount'],
        mode='lines+markers',
        name='Actual Outflow',
        line=dict(color=COLORS['expense'], width=2)
    ))

    fig.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['predicted_expense'],
        mode='lines',
        name='Predicted Trend',
        line=dict(color=COLORS['prediction'], width=3, dash='dash')
    ))

    fig.update_layout(
        title="Algorithmic Liquidity Forecast (30-Day Forward)",
        xaxis_title="Valuation Date",
        yaxis_title="Projected Volume (PLN)"
    )

    return update_layout_style(fig)
