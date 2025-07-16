import dash
from dash import dcc, html, Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np
import psf_library.cleaning as psf_clean
import psf_library.calcs as psf_calc

# Load and prep data
daily_df = pd.read_csv('data/10Y_Daily_Returns.csv')

split = psf_clean.split_columns_to_dfs(daily_df, 'date')

# Dash app
app = dash.Dash(__name__)
app.title = "Rolling Return Dashboard"

app.layout = html.Div([
    html.H2("Index Returns", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='window-select',
        options=[
            {'label': '1 Year', 'value': 1},
            {'label': '3 Years', 'value': 3},
            {'label': '5 Years', 'value': 5}
        ],
        value=1,
        clearable=False,
        style={'width': '200px', 'margin': 'auto'}
    ),

    dcc.Dropdown(
        id='index-select',
        options=[{'label': idx, 'value': idx} for idx in split.keys()],
        value=['SPX Index', 'SPW Index'],
        multi=True,
        clearable=False,
        style={'width': '200px', 'margin': 'auto'}
    ),

    dcc.Graph(id='cumulative-plot'),
    dcc.Graph(id='rolling-cumulative-plot'),
    dcc.Graph(id='rolling-return-plot'),
    dcc.Graph(id='volatility-plot'),
    dcc.Graph(id='sharpe-plot'),

])

@app.callback(
    Output('cumulative-plot', 'figure'),
    Output('rolling-cumulative-plot', 'figure'),
    Output('rolling-return-plot', 'figure'),
    Output('volatility-plot', 'figure'),
    Output('sharpe-plot', 'figure'),
    Input('index-select', 'value'),
    Input('window-select', 'value')
)

def update_rolling_plot(selected_index, window_years):
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    fig4 = go.Figure()
    fig5 = go.Figure()
    for idx in selected_index:
        df = split[idx]
        rolling_returns = psf_calc.compute_rolling_returns(df, window_years, 0.04)

        # Cumulative Return
        fig1.add_trace(go.Scatter(
            x=rolling_returns.index,
            y=rolling_returns['cumulative_return'],
            mode='lines',
            name=f'{idx} Cumulative Return'
        ))

        fig1.update_layout(
            title='Cumulative Return',
            xaxis_title='Date',
            yaxis_title='Cumulative Return',
            yaxis=dict(
                tickformat=".0%"),
            template='plotly_white'
        )

        fig2.add_trace(go.Scatter(
            x=rolling_returns.index,
            y=rolling_returns['rolling_cumulative_return'],
            mode='lines',
            name=f'{idx} Rolling Cumulative Return'
        ))

        fig2.update_layout(
            title=f'{window_years}Y Rolling Cumulative Return',
            xaxis_title='Date',
            yaxis_title='Cumulative Return',
            yaxis=dict(
                tickformat=".0%"),
            template='plotly_white'
        )

        # Rolling Return
        fig3.add_trace(go.Scatter(
            x=rolling_returns.index,
            y=rolling_returns['annualized_return'],
            mode='lines',
            name=f'{idx} Rolling Return'
        ))

        fig3.update_layout(
            title=f'{window_years}Y Rolling Return',
            xaxis_title='Date',
            yaxis_title='Annualized Return',
            yaxis=dict(
                tickformat=".0%"),
            template='plotly_white'
        )

        # Rolling Volatility
        fig4.add_trace(go.Scatter(
            x=rolling_returns.index,
            y=rolling_returns['rolling_volatility'],
            mode='lines',
            name=f'{idx} Rolling Volatility'
        ))

        fig4.update_layout(
            title=f'{window_years}Y Rolling Volatility',
            xaxis_title='Date',
            yaxis_title='Volatility',
            yaxis=dict(
                tickformat=".0%"),
            template='plotly_white'
        )

        # Rolling Sharpe
        fig5.add_trace(go.Scatter(
            x=rolling_returns.index,
            y=rolling_returns['rolling_sharpe'],
            mode='lines',
            name=f'{idx} Rolling Sharpe'
        ))

        fig5.update_layout(
            title=f'{window_years}Y Rolling Sharpe',
            xaxis_title='Date',
            yaxis_title='Sharpe Ratio',
            template='plotly_white'
        )

    return fig1, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    app.run(debug=True)

