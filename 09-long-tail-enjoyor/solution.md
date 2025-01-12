# ETH Wrappr (SIP-112) Key Points

## ETH Wrappr Introduction

The SIP introduces a new "ETH Wrappr" contract, which is central to both solutions.

> "This SIP proposes to add an ETH Wrappr, allowing users to mint sETH with ETH as collateral"

## No Slippage Minting/Burning

The Wrappr allows 1:1 conversion between ETH and sETH without slippage, which is crucial for the arbitrage in Solution 1.

> "Users can mint sETH by depositing ETH, and burn sETH to withdraw ETH, at a 1:1 ratio"

## Maximum ETH Cap

The SIP specifies a maximum amount of ETH that can be wrapped, which is used in the simulations.

> "The debt pool's exposure to ETH price risk should be limited by only allowing a maximum of maxETH to be wrapped"

## Integration with Synthetix System

The sETH minted can be used within the Synthetix ecosystem, which is leveraged in Solution 2.

> "sETH minted from the wrappr can be used like any other synth in the Synthetix protocol"

## Application in Solutions

### Solution 1:
- Uses the no-slippage minting/burning feature to arbitrage between Wrappr and market prices.
- Utilizes the maxETH amount in the simulation.

### Solution 2:
- Leverages the ability to mint sETH using the Wrappr.
- Uses the minted sETH as collateral within the Synthetix system to create a leveraged position.

Both solutions take advantage of the new ETH Wrappr's core functionality as described in SIP-112, particularly the ability to easily convert between ETH and sETH at a 1:1 ratio. This feature creates new arbitrage and leveraging opportunities that didn't exist before the implementation of this SIP.

## Solution 1: Arbitrage Strategy

### a) Theoretical Approach

1. Wait for the ETH Wrappr contract deployment.
2. Monitor ETH/sETH price on DEXs like Curve.
3. When sETH trades at a premium to ETH:
   - Deposit maximum allowed ETH into Wrappr to mint sETH
   - Sell minted sETH on DEXs for profit
4. When sETH price returns closer to peg:
   - Buy back sETH at lower price
   - Burn it in Wrappr to withdraw ETH
5. Repeat as opportunities arise

This arbitrage exploits no-slippage minting/burning in Wrappr vs. market prices.

### b) Simulation Data (Hypothetical)

- maxETH: 5000 ETH
- ETH price: $4000
- sETH premium: 2%

Process:
1. Deposit 5000 ETH ($20,000,000) to mint 5000 sETH
2. Sell 5000 sETH at $4080 each = $20,400,000
3. Profit: $400,000 minus gas fees

When premium disappears:
1. Buy back 5000 sETH at $4000 each = $20,000,000
2. Burn for 5000 ETH
3. Net profit: ~$400,000 minus gas fees

## Solution 2: Leveraged Long ETH Strategy

### a) Theoretical Approach

1. Borrow ETH from lending protocol (e.g., Aave)
2. Use borrowed ETH to mint sETH via Wrappr
3. Use sETH as collateral in Synthetix to mint sUSD
4. Use sUSD to buy more ETH
5. Repeat steps 2-4 to leverage long ETH exposure
6. Unwind position if/when ETH price increases

This strategy amplifies ETH long exposure using Wrappr in a leveraged position.

### b) Simulation Data (Hypothetical)

- Starting capital: 1000 ETH ($4,000,000)
- Borrow 4000 ETH from Aave
- Total 5000 ETH to deposit in Wrappr

Process:
1. Mint 5000 sETH
2. Use as collateral to mint 2,000,000 sUSD (400% c-ratio)
3. Buy 500 ETH with sUSD
4. Repeat once more:
   - Mint 500 sETH
   - Mint 200,000 sUSD
   - Buy 50 ETH

Final position:
- 5550 ETH equivalent exposure
- 2,200,000 sUSD debt
- 4000 ETH debt to Aave

If ETH price increases 10%:
- Position value: $24,420,000
- Repay debts: $19,200,000
- Profit: $1,220,000 (30.5% return) minus fees