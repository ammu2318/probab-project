import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Data Analyzer"),
    dcc.Input(id="stock-name", type="text", placeholder="Enter Stock Name"),
    dcc.Dropdown(
        id="timeframe",
        options=[
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Months', 'value': '3mo'},
            {'label': '6 Months', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '2 Years', 'value': '2y'},
            {'label': '5 Years', 'value': '5y'},
            {'label': '10 Years', 'value': '10y'},
            {'label': 'Max', 'value': 'max'}
        ],
        value='1y'
    ),
    html.Button("Plot Stock Data", id="plot-button"),
    dcc.Graph(id="stock-graph")
])

@app.callback(
    Output('stock-graph', 'figure'),
    Input('plot-button', 'n_clicks'),
    Input('stock-name', 'value'),
    Input('timeframe', 'value')
)
def plot_stock_graph(n_clicks, stock_name, selected_timeframe):
    if n_clicks is None:
        return go.Figure()

    stock = yf.Ticker(stock_name)
    stock_history = stock.history(period=selected_timeframe)
    stock_history.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_history['Date'], y=stock_history['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=stock_history['Date'], y=stock_history['Open'], name='Open Price'))

    fig.update_layout(
        title=f'{stock_name} Opening & Closing Prices Over Time ({selected_timeframe})',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
