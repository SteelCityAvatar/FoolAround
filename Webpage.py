import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import ast
# Read the CSV file
df = pd.read_csv(r'C:\Users\anura\Documents\PyProjects\FoolAround\OutputFiles\20240324_173418_ValueInvestingTestDf.csv')

# Count the frequency of each ticker
df['relevant_tickers'] = df['relevant_tickers'].apply(ast.literal_eval)
flattened_tickers = df['relevant_tickers'].explode()
print(flattened_tickers)
ticker_counts = flattened_tickers.value_counts()

# Create a bar chart
fig = px.bar(ticker_counts, x=ticker_counts.index, y=ticker_counts.values, labels={'x':'Ticker', 'y':'Count'})

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Reddit Ticker Mentions'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# if __name__ == '__main__':
app.run_server(debug=True)