import plotly.graph_objs as go
import numpy as np


def create_price_figure(sim_data, sellers, buyers, market_price):
    sellers = int(sellers) 
    buyers = int(buyers) 

    seller_colors = ['green' if price < market_price else 'red' for price in sim_data['min_selling_prices']]
    buyer_colors = ['green' if price > market_price else 'red' for price in sim_data['max_buying_prices']]

    seller_bar = go.Bar(x=np.arange(-sellers, 0), y=sim_data['min_selling_prices'][:sellers], name='Producer Min Selling Price', marker_color=seller_colors[:sellers])
    buyer_bar = go.Bar(x=np.arange(1, buyers + 1), y=sim_data['max_buying_prices'][:buyers], name='Consumers Max Buying Price', marker_color=buyer_colors[:buyers])

    price_fig = go.Figure(data=[seller_bar, buyer_bar])

    max_price = max(sim_data['min_selling_prices'] + sim_data['max_buying_prices'] + [market_price])
    y_axis_limit = max(max_price * 1.1, 100)  

    price_fig.update_layout(
        title='Prices',
        yaxis_title='Price',
        xaxis={'visible': True, 'tickvals': [-sellers/2, buyers/2], 'ticktext': ['Producer Min Selling Price', 'Consumer Max Buying Price'], 'tickfont': {'size': 16, 
'color': 'black'}},
        showlegend=False,
        plot_bgcolor='white',
        yaxis=dict(showgrid=False, range=[0, y_axis_limit], title_font=dict(size=16)), 
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=16), 
        title_x=0.5, 
        height = 350 
    )

    price_fig.add_hline(
        y=market_price, line_dash="dot",
        annotation_text=f"Market Price: {market_price}",
        annotation_position="bottom right",
        annotation_bgcolor='white',
        annotation_font_size=12 
    )
    return price_fig

def create_stock_figure(sim_data, sellers, buyers, max_stock, producer_desired_stock, consumer_desired_stock):
    sellers = int(sellers)  
    buyers = int(buyers)   

    producer_supply_colors = ['green' if stock < producer_desired_stock else 'red' for stock in sim_data['goods_sellers']]
    consumer_supply_colors = ['green' if stock < consumer_desired_stock else 'red' for stock in sim_data['goods_buyers']]

    producer_bar = go.Bar(x=np.arange(-sellers, 0), y=sim_data['goods_sellers'][:sellers], name='Producer Supply', marker_color=producer_supply_colors[:sellers])
    consumer_bar = go.Bar(x=np.arange(1, buyers + 1), y=sim_data['goods_buyers'][:buyers], name='Consumer Supply', marker_color=consumer_supply_colors[:buyers])

    stock_fig = go.Figure(data=[producer_bar, consumer_bar])

    max_goods = max(sim_data['goods_sellers'] + sim_data['goods_buyers'] + [max_stock, producer_desired_stock])
    y_axis_limit = max(max_goods * 1.1, 100)  


    stock_fig.update_layout(
        title='Number of Goods',
        yaxis_title='Number of Goods',
        xaxis={'visible': True, 'tickvals': [-sellers/2, buyers/2], 'ticktext': ['Producer Supply', 'Consumer Supply'], 'tickfont': {'size': 16, 'color': 'black'}},
        showlegend=False,
        plot_bgcolor='white',
        yaxis=dict(showgrid=False, range=[0, y_axis_limit], title_font=dict(size=16)), 
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=16),  
        title_x=0.5, 
        height = 350 
    ) 

    stock_fig.add_hline(
        y=max_stock, line_dash="dot",
        annotation_text=f"Max Stock: {max_stock}",
        annotation_position="bottom right",
        annotation_bgcolor='white',
        annotation_font_size=12  
    )

    stock_fig.add_hline(
        y=consumer_desired_stock, line_dash="dot",
        annotation_text=f"Consumers' Desired Stock: {consumer_desired_stock}",
        annotation_position="bottom right",
        annotation_bgcolor='white',
        annotation_font_size=12  
    ) 

    stock_fig.add_hline(
        y=producer_desired_stock, line_dash="dot",
        annotation_text=f"Producers' Desired Stock: {producer_desired_stock}",
        annotation_position="bottom left",
        annotation_bgcolor='white',
        annotation_font_size=12  
    ) 

    return stock_fig 
