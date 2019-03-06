import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import plotly.graph_objs as go
from plotly import tools

API_KEY = "3QQPGBCI54Z8BFMZ"

# print(pd)
class StockDataHandler(object):
    def __init__(self):
        self.company = 'MSFT'
        self.current_df = {}
        self.current_graph = {}
    
    def getStockData(self, company):
        dataurl = f"https://www.alphavantage.co/query?"
        dataurl += f"function=TIME_SERIES_DAILY&symbol={company}&apikey={API_KEY}&datatype=csv"
        print(dataurl)
        try:
            df = pd.read_csv(dataurl)
            if df is not None and "timestamp" in df:
                self.company = company
                self.current_df = df
                return df
        except Exception as e:
            print(e)
            return None

            
# new an object for keeping data
stock_data_handler = StockDataHandler()

# initialize Dash app
app = dash.Dash(__name__)

# set up an layout
app.layout = html.Div(children=[
    # H1 title on the page
    html.H1(children='Input box + Line Chart'),

    html.H2(children='Please enter a stock name that you want to find about'),
    html.H3(children='ex: AAPL, MSFT, AMZN, and etc'),

    # a div to put a short description
    html.Label(children='Enter a stock name:'),

    dcc.Input(id='symbol', value='MSFT', type='text'),
    html.Button(id='submit', type='submit', children='submit'),
    

    # append the visualization to the page
    dcc.Graph(
        id='linechart'
    )
])
@app.callback(
    Output(component_id='linechart', component_property='figure'),
    [Input(component_id='symbol', component_property='n_submit'), 
     Input(component_id='symbol', component_property='n_blur'),
     Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='symbol', component_property='value')]
)

def get_data(n_submit, n_blur, n_clicks, company):
    company = company.strip()
    if company == '':
        return stock_data_handler.current_graph

   # fig = tools.make_subplots(rows=len(4), cols=1, shared_xaxes=True)

    df = stock_data_handler.getStockData(company)
    if df is not None and "timestamp" in df:
        stock_data_handler.current_graph = {
            # configure the data
            'data': [
                # We use line chart to represent our data.
                go.Scatter(
                    x=df["timestamp"],
                    y=df["high"],
                    mode='lines+markers',
                    name="high"
                ),
                go.Scatter(
                    x=df["timestamp"],
                    y=df["close"],
                    mode='lines+markers',
                    name="close"
                )
                ,
                go.Scatter(
                    x=df["timestamp"],
                    y=df["low"],
                    mode='lines+markers',
                    name="low"
                ),
                go.Scatter(
                    x=df["timestamp"],
                    y=df["open"],
                    mode='lines+markers',
                    name="open"
                )

            ],
            # configure the layout of the visualization
            'layout': {
                # Highest Stock Price Tend of "Company" '"'
                'title': 'Highest Stock Price Trend of "' + company + '"'
            }



        }
        
    return stock_data_handler.current_graph
    


# start the app
if __name__ == '__main__':
    app.run_server()

