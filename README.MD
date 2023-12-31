# Market Simulation Process 

This project aims to evaluate phenomena emerging from the actions of individual agents, i.e., buyers and sellers of goods in a simple economy. With [agent-based simulations](https://github.com/willschenk/Guide-to-Agent-Based-Modeling/blob/main/Guide%20to%20Agent-Based%20Modeling.pdf), generalizations keep the computation feasible and allow us to evaluate the cause of emergent phenomena.

## Variables 
- Before starting the simulation, define the number of `Producers (Sellers)` and the number of `Consumers (Buyers)`
- At any point in the simulation, you can update the following: 
  - `Market Price`: Price of one unit on the open market
  - `Production Rate`: How many units of goods producers make per round
  - `Consumption Rate`: How many units of goods consumers use per round
  - `Producer Desired Stock`: How many units producers wish to have in stock
  - `Consumer Desired Stock`: How many units consumers wish to have in their possession
  - `Max Stock (Both)`: Maximum amount of goods any individual producer or consumer can have in possession
  - `Max Trades`: Maximum number of trades that can occur each round
###### **Note**: The `Producer Min Selling Price` and the `Consumer Max Buying Price` are initially randomized

## Generalizations: 
- Many generalizations need to be made to keep this model feasible. Adding more variables leads to an ever-cascading number of new considerations. That is why the number of variables is capped at an amount someone can visualize working in tandem. These are some of the major generalizations that make this model possible: 
  - **Uniform Product**: All goods are considered identical 
  - **Minimal Money Consideration**: The model does not track agents' wealth but focuses solely on goods
  - **Elastic Supply and Demand**: The model assumes constant elasticity, meaning market price adjusts immediately and by exactly 0 or 1 value per round 
  - **No Production Constraints**: Producers can always increase production 
  - **Constant Consumption**: Consumption rates are constant 
  - **No Agent Interaction**: Agents do not communicate outside of trading 
  - **Neglecting Transaction Costs**: The model ignores transaction costs 
  - **Simplified Inventory Management**: Agents do not face storage challenges 
  - **No Learning**: Agents do not change their behavior or strategies 

## Simulation Loop
For each round of the simulation:
  - Conduct trades
  - Adjust market price
  - Update agents' buying and selling prices
  - Modify inventories based on production and consumption

### Conduct Trades
- For each trade from 1 to `Maximum Number of Trades`:
  - Identify producers ready to sell (`Producers with Minimum Selling Price ≤ Market Price` and `Stock > 0`) 
  - Identify consumers ready to buy (`Consumers with Max Buying Price ≥ Market Price` and `Stock < Max Stock`) 
  - If producers and consumers are found:
    - Randomly select 1 producer and 1 consumer to execute the trade 
    - Transfer goods from producer to consumer 
    - Update their respective inventories 
###### **Note**: We do not adjust the money producers and consumers have, a major generalization in this simulation

### Adjust Market Price
- If more producers are willing to sell than consumers willing to buy:
  - Decrease `Market Price` by 1 unit 
- If more consumers are willing to buy than producers are willing to sell:
  - Increase `Market Price` by 1 unit 

### Update *Producer Min Selling Price* and *Consumer Max Buying Price*   
- For each producer:
  - If `Producer's Stock > Producer's Desired Stock`:
    - Decrease this producer's `Min Selling Price` to encourage sales 
    - If reaching stock capacity, decrease significantly (by 10 units)
  - If `Producer's Stock < Producer's Desired Stock`:
    - Increase this producer's `Min Selling Price` due to scarcity 
- For each consumer:
  - If `Consumer's Stock > Consumer's Desired Stock`:
    - Decrease this consumer's `Max Buying Price` 
  - If `Consumer's Stock < Consumer's Desired Stock`:
    - Increase `Max Buying Price` 

### Modify Inventory
- For each producer:
  - Increase stock by `Production Rate`, capped at the `Max Stock (Both)`
- For each consumer: 
  - Decrease stock by `Consumption Rate`, not going below 0 

## End of Simulation
- The simulation runs for 1000 rounds or until the reset button is clicked 
