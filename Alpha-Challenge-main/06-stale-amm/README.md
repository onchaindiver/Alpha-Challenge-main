# stale-amm - Tier 2
It’s May 2021, and while searching for new trading pools, you discovered that someone made [2.8x](https://etherscan.io/tx/0x3f1b5baef6ea7f622834eabe7634bf89e3f473b62a73e357fdd04a1a5cf32ecf) by selling TUSD through one of the old Uniswap v1 pools. Let’s figure out how it happened.


- a) What is the reason for the stale price in this pool?
- b) Provide all necessary simulation data to arbitrage the pool on January 23, 2022.
- c) Could you execute the arbitrage on March 14, 2022? If not, explain why.

# Solution

## Brief Description of the Issue
According to the problem statement, we are interested in the following [transaction](https://etherscan.io/tx/0x3f1b5baef6ea7f622834eabe7634bf89e3f473b62a73e357fdd04a1a5cf32ecf).

There was a stablecoin called TrueUSD (TUSD), which was located at the address [0x8dd5fbCe2F6a956C3022bA3663759011Dd51e73E](https://etherscan.io/address/0x8dd5fbCe2F6a956C3022bA3663759011Dd51e73E). The corresponding Uniswap v1 pool can be found at the address [0x4F30E682D0541eAC91748bd38A648d759261b8f3](https://etherscan.io/address/0x4f30e682d0541eac91748bd38a648d759261b8f3).

At some point, the token (finally) migrated to a new address: [0x0000000000085d4780B73119b644AE5ecd22b376](https://etherscan.io/address/0x0000000000085d4780B73119b644AE5ecd22b376). The corresponding Uniswap v2 pool (paired with WETH) can be found here: [0xb4d0d9df2738abE81b87b66c80851292492D1404](https://etherscan.io/address/0xb4d0d9df2738abe81b87b66c80851292492d1404#readContract).

Thus, at one time, there were multiple entry points for the same TrueUSD (TUSD) token: two contracts under different addresses. The old address [(0x8dd...)](https://etherscan.io/address/0x8dd5fbCe2F6a956C3022bA3663759011Dd51e73E) redirected everything to the new contract [(0x000...)](https://etherscan.io/address/0x0000000000085d4780B73119b644AE5ecd22b376). Whichever contract we interacted with, it would affect the TUSD balance.

### a)
The reason for the stagnant price in the Uniswap v1 pool was that users were making trades with the token at the "new" address [(0x000...)](https://etherscan.io/address/0x0000000000085d4780B73119b644AE5ecd22b376), thus not changing the balance of the Uniswap v1 pool (and therefore the price didn't change). This created an arbitrage opportunity, although this is far from the only problem: a token with such a scheme of multiple entry points poses a danger and the possibility of exploitation.

### b)
Check Task_6.ipynb

### c)
No, as of March 14, 2022, it is not possible to use this arbitrage scheme. Since the scheme with two addresses represented a vulnerability, it caught the attention of Compound, where TUSD transactions could be conducted. They hired OpenZeppelin, and together they forced (almost blackmailed) the TUSD developers to get in touch. Therefore, on February 23, 2022, the vulnerability was urgently fixed. The last [successful transfer](https://etherscan.io/tx/0x37e8d60beefbfe371ec42e7bb02370fe1b463c04b2f17f8808274a367a04375f) was made on February 22, 2022, and all subsequent transactions are reverted.
