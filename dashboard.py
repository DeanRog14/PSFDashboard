from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import psf_library.cleaning as psf_clean
import psf_library.calcs as psf_calc

# Load and prep data
daily_df = pd.read_csv("data/10Y_Daily_Returns.csv")
split = psf_clean.split_columns_to_dfs(daily_df, "date")

index_options = list(split.keys())
print(index_options)
window_options = [1, 3, 5]

app_ui = ui.page_fluid(
    ui.h2("Index Returns", class_="text-center"),
    
    ui.div(
        ui.layout_columns(
            ui.input_select(
                "window",
                "Window (Years)",
                {str(x): x for x in window_options},
                selected="1"
            ),
            ui.input_select(
                "indexes",
                "Indexes",
                {idx: idx for idx in index_options},
                selected=["SPX Index", "SPW Index"],
                multiple=True
            ),
            col_widths=[6, 6]  # 2 columns, each 50% width
        ),
        class_="mx-auto",
        style="max-width: 800px;"
    ),

    output_widget("cumulative_plot"),
    output_widget("rolling_cumulative_plot"),
    output_widget("rolling_return_plot"),
    output_widget("volatility_plot"),
    output_widget("sharpe_plot"),
)

def create_plot(selected_index, window_years):
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    fig4 = go.Figure()
    fig5 = go.Figure()

    for idx in selected_index:
        df = split[idx]
        rolling_returns = psf_calc.compute_rolling_returns(df, window_years, 0.04)

        # Plot 1: Cumulative Return
        fig1.add_trace(go.Scatter(x=rolling_returns.index, y=rolling_returns['cumulative_return'], mode='lines', name=idx))

        # Plot 2: Rolling Cumulative
        fig2.add_trace(go.Scatter(x=rolling_returns.index, y=rolling_returns['rolling_cumulative_return'], mode='lines', name=idx))

        # Plot 3: Annualized Return
        fig3.add_trace(go.Scatter(x=rolling_returns.index, y=rolling_returns['annualized_return'], mode='lines', name=idx))

        # Plot 4: Volatility
        fig4.add_trace(go.Scatter(x=rolling_returns.index, y=rolling_returns['rolling_volatility'], mode='lines', name=idx))

        # Plot 5: Sharpe
        fig5.add_trace(go.Scatter(x=rolling_returns.index, y=rolling_returns['rolling_sharpe'], mode='lines', name=idx))

    for fig, title, ytitle, format_ in [
        (fig1, "Cumulative Return", "Cumulative Return", ".0%"),
        (fig2, f"{window_years}Y Rolling Cumulative Return", "Cumulative Return", ".0%"),
        (fig3, f"{window_years}Y Rolling Return", "Annualized Return", ".0%"),
        (fig4, f"{window_years}Y Rolling Volatility", "Volatility", ".0%"),
        (fig5, f"{window_years}Y Rolling Sharpe", "Sharpe Ratio", ".2f")
    ]:
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=ytitle,
            hovermode="x unified",
            template="plotly_white",
            yaxis=dict(tickformat=format_)
        )

    return fig1, fig2, fig3, fig4, fig5


def server(input, output, session):
    @render_widget
    def cumulative_plot():
        return create_plot(input.indexes(), int(input.window()))[0]
    output.cumulative_plot = cumulative_plot

    @render_widget
    def rolling_cumulative_plot():
        return create_plot(input.indexes(), int(input.window()))[1]
    output.rolling_cumulative_plot = rolling_cumulative_plot

    @render_widget
    def rolling_return_plot():
        return create_plot(input.indexes(), int(input.window()))[2]
    output.rolling_return_plot = rolling_return_plot

    @render_widget
    def volatility_plot():
        return create_plot(input.indexes(), int(input.window()))[3]
    output.volatility_plot = volatility_plot

    @render_widget
    def sharpe_plot():
        return create_plot(input.indexes(), int(input.window()))[4]
    output.sharpe_plot = sharpe_plot

app = App(app_ui, server)

