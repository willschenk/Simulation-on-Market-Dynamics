from dash import Dash
import dash_bootstrap_components as dbc

# Import modules 
from layouts.main_layout import main_layout
from callbacks.app_callbacks import register_callbacks

# Stylesheets 
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'assets/custom.css' 
]

# Initialize application 
app = Dash(__name__, external_stylesheets=external_stylesheets, update_title=None) 
app.title = 'Market Simulation ABM' 

# Server instance 
server = app.server

# Define layout 
app.layout = main_layout

# Define callbacks 
register_callbacks(app)

# Run 
if __name__ == '__main__':
    app.run_server(debug=True)

