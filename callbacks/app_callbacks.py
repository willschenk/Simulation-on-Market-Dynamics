from dash import Input, Output, State, callback_context, callback, html 
import numpy as np 
import dash 

from components.simulation import run_simulation, update_simulation_parameters
from components.figures import create_price_figure, create_stock_figure
from layouts.main_layout import initialize_simulation_data
from layouts.main_layout import initial_values

def register_callbacks(app):
    @callback(
        [Output('price-graph', 'figure'),
        Output('stock-graph', 'figure'),
        Output('simulation-data', 'data'),
        Output('interval-component', 'disabled')],
        [Input('start-button', 'n_clicks'),
        Input('reset-button', 'n_clicks'), 
        Input('interval-component', 'n_intervals'), 
        Input('sellers-slider', 'value'),
        Input('buyers-slider', 'value'),
        Input('production-slider', 'value'),
        Input('consumption-slider', 'value'),
        Input('max-stock-slider', 'value'), 
        Input('producer-desired-stock-slider', 'value'),
        Input('consumer-desired-stock-slider', 'value'),
        Input('max-trades-slider', 'value'),
        Input('market-price-slider', 'value')],
        [State('simulation-data', 'data')]
    )
    def update_simulation(start, reset, n_intervals, sellers, buyers, production, consumption, max_stock, producer_desired_stock, consumer_desired_stock, max_trades, slider_market_price, sim_data):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] 
        
        # Check which input triggered the callback 
        if triggered_id == 'market-price-slider':
            sim_data['market_price'] = slider_market_price
        elif triggered_id in ['sellers-slider', 'buyers-slider']:
            sim_data = initialize_simulation_data(sellers, buyers)
        
        if triggered_id == 'start-button': 
            sim_data['running'] = True 
        elif triggered_id == 'reset-button': 
            sim_data = initialize_simulation_data(sellers, buyers) 
            sim_data['running'] = False 
            
        # Update simulation parameters 
        update_simulation_parameters(sim_data, production, consumption, max_stock, producer_desired_stock, consumer_desired_stock, max_trades, sim_data['market_price']) 

        # Run simulation  
        if sim_data['running']: 
            sim_data = run_simulation(sim_data)
            disabled_interval = False
        else:
            disabled_interval = True

        # Create figures
        price_fig = create_price_figure(sim_data, sellers, buyers, sim_data['market_price'])
        stock_fig = create_stock_figure(sim_data, sellers, buyers, max_stock, producer_desired_stock, consumer_desired_stock)

        return price_fig, stock_fig, sim_data, disabled_interval 

    @callback(
        [Output('sellers-slider', 'disabled'),
        Output('buyers-slider', 'disabled')],
        [Input('start-button', 'n_clicks'),
        Input('reset-button', 'n_clicks')],
        [State('simulation-data', 'data')]
    )
    def toggle_sliders(start_clicks, reset_clicks, sim_data):
        # Check if the start button is clicked and the simulation is not running
        if start_clicks and not sim_data.get('running', False):
            return True, True  
        elif reset_clicks:
            return False, False 

        return sim_data.get('running', False), sim_data.get('running', False) 

    @callback(
        Output('start-button', 'disabled'),
        Input('start-button', 'n_clicks'),
        Input('reset-button', 'n_clicks'),
        State('simulation-data', 'data')
    )
    def disable_start_button(start_clicks, reset_clicks, sim_data): 
        if reset_clicks > 0: 
            # The reset button was clicked 
            return False 
        elif start_clicks is None: 
            # Not yet clicked  
            return False 
        elif sim_data['running']: 
            # Already running 
            return True 
        else: 
            # It is reset 
            return False 


    @callback(
        [Output('market-price-slider', 'value'),
        Output('sellers-slider', 'value'),
        Output('buyers-slider', 'value'),
        Output('production-slider', 'value'),
        Output('consumption-slider', 'value'),
        Output('producer-desired-stock-slider', 'value'),
        Output('consumer-desired-stock-slider', 'value'),
        Output('max-stock-slider', 'value'),
        Output('max-trades-slider', 'value')],
        [Input('reset-button', 'n_clicks')],
        [State('simulation-data', 'data')]
    )
    def reset_sliders(reset_clicks, sim_data):
        if reset_clicks:
            # Reset sliders to their initial values
            return (initial_values['market_price'], 
                    initial_values['sellers'],
                    initial_values['buyers'],
                    initial_values['production'],
                    initial_values['consumption'],
                    initial_values['producer_desired_stock'],
                    initial_values['consumer_desired_stock'],
                    initial_values['max_stock'],
                    initial_values['max_trades'])
        # Returning dash.no_update prevents the callback from firing if the reset button hasn't been clicked
        return dash.no_update