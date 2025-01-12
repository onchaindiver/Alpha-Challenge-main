# Liquidations - Tier 3
It’s DeFi Summer, and you run one of the most successful liquidators on Compound v2. On August 20, 2020, you realize that you are losing market share to [this address](https://etherscan.io/tx/0xec4f2ab36afa4fac4ba79b1ca67165c61c62c3bb6a18271c18f42a6bdfdb533d). This is odd because you updated the trading setup after [this proposal](https://compound.finance/governance/proposals/19), and have consistently won almost all liquidations since then.


- a) What’s the edge of this liquidator that allows them to win more liquidations?
- b) When you figure out the source of the edge, you notice that their calldata is extremely obfuscated. Can you explain on how the calldata works?
- c) Write code for the bot in Solidity, and provide all necessary information to simulate this liquidation on a mainnet fork.

## Source of the edge
### Usage of Gas Tokens
Gas Token Mechanism: Gas tokens (like GST2) allow users to store gas during periods of low prices by occupying storage slots. Later, during transactions with higher gas prices, the tokens can be "released" to receive gas refunds, helping reduce overall transaction costs. In the provided example we can see that out of about 1 million gas being used, around 500k was rebated.

### Coinbase Oracle Usage
You mention using a Coinbase price oracle. Reading their docs, it seems that it is a permissionless oracle where signed price data from Coinbase can be submitted on-chain. Instead of waiting for price updates directly on-chain, liquidators could proactively monitor Coinbase prices off-chain and use that real-time data bundled with their liquidation transaction.


## Solidity ABI Encoding and Transaction Obfuscation
Calldata Encoding: Although the ABI is not known, it seems that the calldata adheres to Solidity’s ABI encoding conventions. By examining the calldata, we noticed that it contains three fixed-length parameters (uint256), two variable-length parameters (an empty list), and a long string of 0x744 bytes.
The first param is slightly odd, because it has some non-zero bytes in the lower bytes and in the higher. Likely it is parsed in the code using some bitwise operations.
Second param is zero, and a third looks like an address, 20 bytes, but this address is not existing.
The long string in the calldata likely contains a set of instructions for an interpreter inside the main contract. This complex data structure can serve as an anti-front-running mechanism, making it difficult for bots or other parties to copy and modify the transaction. This complexity prevents front-runners from simply replacing addresses or analyzing the transaction in real-time. It can also be used to minimize costs of storing the calldata, in case of some optimized multicall-like contracts (which is a general purpose tool, so it is pretty inefficient), but I think in this case, most of the code inside the contract could have been done much simpler, so obfuscation seems to be a main reason.

References:
- [1] https://dashboard.tenderly.co/tx/mainnet/0xec4f2ab36afa4fac4ba79b1ca67165c61c62c3bb6a18271c18f42a6bdfdb533d?trace=0.1
- [2] https://www.4byte.directory/signatures/?bytes4_signature=389eee82
