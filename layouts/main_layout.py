from dash import html, dcc
import plotly.graph_objs as go
import numpy as np 
from components.figures import create_price_figure, create_stock_figure

# Define initial values for the simulation 
initial_values = {
    'sellers': 15,
    'buyers': 15,
    'production': 1,
    'consumption': 1,
    'max_stock': 100,
    'producer_desired_stock': 50, 
    'consumer_desired_stock': 50, 
    'max_trades': 30,
    'market_price': 50
} 

def initialize_simulation_data(sellers, buyers):
    """
    Initialize the simulation data with given number of sellers and buyers.
    """
    sellers = int(sellers) 
    buyers = int(buyers) 

    return {
        'running': False,
        'iteration': 0,
        'market_price': initial_values['market_price'],
        'min_selling_prices': np.random.randint(1, initial_values['market_price'] * 2, sellers).tolist(),
        'max_buying_prices': np.random.randint(1, initial_values['market_price'] * 2, buyers).tolist(),
        'goods_sellers': [initial_values['producer_desired_stock']] * sellers,
        'goods_buyers': [initial_values['consumer_desired_stock']] * buyers, 
        'production': initial_values['production'],
        'consumption': initial_values['consumption']
    }

# Read markdown 
def read_markdown_file(markdown_file):
    with open(markdown_file, 'r') as file:
        return file.read() 

def main_layout(): 
    markDown = read_markdown_file("markDown.md")

    layout = html.Div([ 
        dcc.Location(id='url', refresh=False), 

        # Container 
        html.Div([
            dcc.Graph(id='price-graph'),
            dcc.Graph(id='stock-graph') 
        ], style={'position': 'top'}),  
        # Market Price Slider 
        html.Div([
            html.Label('Market Price:', style={'fontSize': '12px', 'marginRight': '10px'}),
            dcc.Slider(
                id='market-price-slider',
                min=0,
                max=100,
                value=initial_values['market_price'],
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
                marks={0: '0', 100: '100', initial_values['market_price']: str(initial_values['market_price'])}
            )
        ], style={'marginBottom': '0px', 'marginTop': '10px', 'width': '100%'}),

        # Producers Consumers Rates sliders
        html.Div([
            # Producers (Sellers) Sliders
            html.Div([
                html.Label('Producers (Sellers):', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='sellers-slider',
                    min=1,
                    max=40,
                    value=initial_values['sellers'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={1: '1', 40: '40', initial_values['sellers']: str(initial_values['sellers'])}
                ),
                html.Label('Production Rate:', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='production-slider',
                    min=0,
                    max=10,
                    value=initial_values['production'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={0: '0', 10: '10', initial_values['production']: str(initial_values['production'])}
                ),
                html.Label('Producer Desired Stock:', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='producer-desired-stock-slider',
                    min=0,
                    max=100,
                    value=initial_values['producer_desired_stock'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={0: '0', 100: '100', initial_values['producer_desired_stock']: str(initial_values['producer_desired_stock'])}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            # Consumers 
            html.Div([
                html.Label('Consumers (Buyers):', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='buyers-slider',
                    min=1,
                    max=40,
                    value=initial_values['buyers'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={1: '1', 40: '40', initial_values['buyers']: str(initial_values['buyers'])}
                ),
                html.Label('Consumption Rate:', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='consumption-slider',
                    min=0,
                    max=10,
                    value=initial_values['consumption'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={0: '0', 10: '10', initial_values['consumption']: str(initial_values['consumption'])}
                ),
                html.Label('Consumer Desired Stock:', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='consumer-desired-stock-slider',
                    min=1,
                    max=100,
                    value=initial_values['consumer_desired_stock'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={0: '0', 100: '100', initial_values['consumer_desired_stock']: str(initial_values['consumer_desired_stock'])}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),

        # Max Stock and Max Trades Sliders 
        html.Div([
            html.Div([
                html.Label('Max Stock (Both):', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='max-stock-slider',
                    min=10,
                    max=150,
                    value=initial_values['max_stock'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={10: '10', 150: '150', initial_values['max_stock']: str(initial_values['max_stock'])}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                html.Label('Max Trades:', style={'fontSize': '12px', 'marginRight': '10px'}),
                dcc.Slider(
                    id='max-trades-slider',
                    min=1,
                    max=80,
                    value=initial_values['max_trades'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks={1: '1', 80: '80', initial_values['max_trades']: str(initial_values['max_trades'])}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),

        # Control Buttons: Reset, Start 
        html.Div([
            html.Button('Reset', id='reset-button', n_clicks=0,
                        style={'fontSize': '16px', 'padding': '10px 20px'}),
            html.Button('Start', id='start-button', n_clicks=0,
                        style={'fontSize': '16px', 'padding': '10px 20px', 'backgroundColor': 'green', 'color': 'white'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'padding': '20px'}), 
        
        # Markdown Text Box 
        html.Div(
            dcc.Markdown(markDown),
            style={
                'border': '1px solid #ddd', # Box border
                'padding': '20px', 
                'margin': '20px 0', 
                'width': '80%',  
                'margin-left': 'auto', 
                'margin-right': 'auto', 
                'background-color': '#f9f9f9' 
            }
        ), 

        # Interval Component 
        dcc.Interval(
            id='interval-component',
            interval=900, # Milliseconds 
            n_intervals=0,
            disabled=False
        ), 

        # Data Storage
        dcc.Store(id='simulation-data', data=initialize_simulation_data(initial_values['sellers'], initial_values['buyers'])) 
    ], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '900px', 'position': 'relative', 'margin': 'auto'}) 
   
   
    return layout 