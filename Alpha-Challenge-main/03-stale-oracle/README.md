# Stale-Oracle - Tier 1
While digging around, you learn about the manual process involved in updating oracle prices for [Compound v1](https://etherscan.io/address/0x3fda67f7583380e67ef93072294a7fac882fd7e7). According to the official blog post, the protocol was deprecated on June 3, 2019. However, according to the contract, it was never paused, and there are no functions for freezing markets. Given this, perhaps it’s possible to use stale prices and borrow all assets cheaply?


- a) Are the prices stale according to the view of Compound v1?
- b) Were markets paused in some way? Provide all necessary data to simulate the borrowing of any asset on June 5, 2019 to prove your point.

# Solution

## a) Are the Prices Stale According to Compound v1?

Yes, the prices in the oracle are indeed stale. For instance, Ether is considered very cheap based on the prices that were last updated in the oracle. However, from the perspective of the Compound v1 protocol, the code does not recognize the staleness of prices. It accepts the outdated prices as valid. Therefore, according to the protocol, the prices are considered "okay".

## b)

While the protocol was not explicitly paused, the ability to borrow assets was effectively disabled. This was achieved by updating the implementation of the `InterestRateModel` for all markets. Here are the transactions that confirm this change:
- [Transaction 1](https://etherscan.io/tx/0x9f63b8aa822fd6df5e1f3a031fa14471813e25640a34aa6fa5a6d53adb16d087)
- [Transaction 2](https://etherscan.io/tx/0x90354d104a130e682c3996d24c6807050ba6af18a696123239ccb6d240a7349d)
- [Transaction 3](https://etherscan.io/tx/0x78e95b393dac244f22d73c826450ff72f9eef352ecf25d86f0b4ed52ff1e5987)
- [Transaction 4](https://etherscan.io/tx/0x1bbdeaa35df1aeab4fdf902cec2968c97011e61262ef5f1ddbfb5f796164ac5c)
- [Transaction 5](https://etherscan.io/tx/0xf743521c0dbda437cedf5db123d35c519e582b6e71d3e9dc7edd66c61c275116)

For any interaction with the Compound protocol (deposit, withdrawal, borrowing, or repayment), the `InterestRateModel` calls the `getBorrowRate()` function. The updated implementation introduced a `require()` statement in this function, which fails if a borrow action is attempted:

```solidity
function isAllowed(address asset, uint newCash, uint newBorrows) internal returns(bool) {
    return ( allowLiquidation || !isLiquidate(asset, newCash) ) && !isBorrow(asset, newCash, newBorrows);
}
```

As a result, any attempt to borrow assets would fail. An example of such a failed attempt can be seen in the transaction from June 5, 2019: [Failed Borrow Attempt](https://etherscan.io/tx/0x82855e1f0f9ad1aacd39302a978aa2e86f45075ceb60c0470af89d66f3c4f245) [(Tenderly Dashboard)](https://dashboard.tenderly.co/tx/mainnet/0x82855e1f0f9ad1aacd39302a978aa2e86f45075ceb60c0470af89d66f3c4f245?trace=0.29)
The transaction reverted on the ```require(isAllowed(asset, cash, borrows))``` check.
