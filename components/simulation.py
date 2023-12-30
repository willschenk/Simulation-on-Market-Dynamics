import numpy as np

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
    Initialize the simulation data 
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

def update_simulation_parameters(sim_data, production, consumption, max_stock, 
                                 producer_desired_stock, consumer_desired_stock, max_trades, market_price):
    sim_data['production'] = production
    sim_data['consumption'] = consumption
    sim_data['max_stock'] = max_stock
    sim_data['producer_desired_stock'] = producer_desired_stock 
    sim_data['consumer_desired_stock'] = consumer_desired_stock

    sim_data['max_trades'] = max_trades
    sim_data['market_price'] = market_price 

def run_simulation(sim_data): 
    max_stock = sim_data['max_stock']
    producer_desired_stock = sim_data['producer_desired_stock'] 
    consumer_desired_stock = sim_data['consumer_desired_stock']

    max_trades = sim_data['max_trades']

    sim_data['iteration'] += 1 

    # Convert lists to numpy arrays for element-wise operations 
    min_selling_prices = np.array(sim_data['min_selling_prices']) 
    max_buying_prices = np.array(sim_data['max_buying_prices']) 
    goods_sellers = np.array(sim_data['goods_sellers'])
    goods_buyers = np.array(sim_data['goods_buyers'])

    # Execute trades 
    for _ in range(max_trades):
        ind_willing_to_sell = np.where((sim_data['market_price'] >= min_selling_prices) & (goods_sellers > 0))[0]
        ind_willing_to_buy = np.where((sim_data['market_price'] <= max_buying_prices) & (goods_buyers < max_stock))[0]

        if len(ind_willing_to_sell) == 0 or len(ind_willing_to_buy) == 0:
            break

        seller = np.random.choice(ind_willing_to_sell)
        buyer = np.random.choice(ind_willing_to_buy)

        goods_sellers[seller] -= 1
        goods_buyers[buyer] += 1 

    # Adjust market price after attempting trades 
    sim_data['market_price'] = max(sim_data['market_price'] + np.sign(len(ind_willing_to_buy) - len(ind_willing_to_sell)), 1)


    ## Adjust Prices: We only adjust prices + or - 1 at a time. 
    # Adjust individual selling prices: 
    for i in range(len(goods_sellers)):  # For each seller 
        # If desired_stock is higher, the adjustment is -1 
        # If desired_stock is lower, the adjustment is +1 
        adjustment = np.sign(goods_sellers[i] - producer_desired_stock) 
        # If the number of goods we have is at the stock limit, we need to make a huge negative adjustment in price 
        adjustment *= 10 if goods_sellers[i] >= max_stock else 1 
        # If the adjustment is negative, this means our stock is lower than desired -> Raise the price -> Adjustment is negative -> Raise price 
        min_selling_prices[i] = max(min_selling_prices[i] - adjustment, 1)

    # Adjust individual buying prices: 
    for i in range(len(goods_buyers)):  # For each buyer 
        adjustment = np.sign(consumer_desired_stock - goods_buyers[i]) 
        # Less goods than desired -> Positive adjustment in max buying price 
        # More goods than desired -> Negative adjustment in max buying price 
        max_buying_prices[i] = max(max_buying_prices[i] + adjustment, 0) 

    # Production and consumption logic 
    goods_sellers = np.minimum(goods_sellers + sim_data['production'], max_stock)
    goods_buyers = np.maximum(goods_buyers - sim_data['consumption'], 0)

    # Convert arrays back to lists before updating sim_data 
    sim_data['min_selling_prices'] = min_selling_prices.tolist()
    sim_data['max_buying_prices'] = max_buying_prices.tolist()
    sim_data['goods_sellers'] = goods_sellers.tolist()
    sim_data['goods_buyers'] = goods_buyers.tolist()

    return sim_data
