# Market Simulation Process

## Initial Setup
- Define `n` buyers and `n` sellers.
- Set initial `production` rate for producers.
- Set initial `consumption` rate for consumers.
- Assign random `min_selling_price` for each producer and `max_buying_price` for each consumer.

## Simulation Loop
For each round of the simulation:
  - Conduct trades.
  - Adjust market price.
  - Update buying and selling prices.
  - Modify inventory based on production and consumption.

### Conduct Trades
- For each trade from 1 to `max_trades`:
    - Identify producers ready to sell (`min_selling_price` ≤ `market_price` and stock > 0).
    - Identify consumers ready to buy (`max_buying_price` ≥ `market_price` and stock < `max_stock`).
    - If eligible producers and consumers are found:
        - Randomly select one producer and one consumer to execute the trade.
        - Transfer goods from producer to consumer.
        - Update their respective inventories.

### Adjust Market Price
- If more producers are willing to sell than consumers willing to buy:
    - Decrease `market_price` by 1 unit.
- If more consumers are willing to buy than producers willing to sell:
    - Increase `market_price` by 1 unit.

### Update Buying and Selling Prices
- For each producer:
    - If stock > `desired_stock`:
        - Decrease `min_selling_price` to encourage sales.
        - If reaching stock capacity, decrease significantly (e.g., by 10 units).
    - If stock < `desired_stock`:
        - Increase `min_selling_price` due to scarcity.
- For each consumer:
    - If stock > `desired_stock`:
        - Decrease `max_buying_price`.
    - If stock < `desired_stock`:
        - Increase `max_buying_price`.

### Modify Inventory
- For each producer:
    - Increase stock by `production` rate, capped at `max_stock`.
- For each consumer:
    - Decrease stock by `consumption` rate, not going below 0.

## End of Simulation
- The simulation can run for a predefined number of rounds or until a certain condition is met.
- Observations and data analysis can be performed at the end.

