# Vault - Tier 1
You are looking through an old version of the OpenZeppelin implementation of ERC-4626 and notice a vulnerability that requires frontrunning an innocent user. You have been granted a large amount of ETH (say e.g. 1k ETH, but you are free to choose the amount :) ) and want to set up a whitehat bot to execute this exploit and return the funds to the user.


- a) Describe the vulnerability and the payoffs for an attacker.
- b)  Produce code that can check if this vulnerability has occurred in the past and determine how much value was lost, if any.
- c)  Write code for the bot that can carry out the exploit (don’t worry about returning user funds).

# Solution
## a)
The vulnerability arises from the way the ERC-4626 tokenized vault standard handles the conversion of assets into shares during the deposit process, specifically in the early stages of a vault's life when the total assets in the vault are minimal. This vulnerability is rooted in the ``` convertToShares ``` function, which calculates the number of shares to mint based on the current total assets in the vault. 

``` sharesAmount = totalShares * assetAmount / asset.balanceOf(address(this)) ```

Attackers can manipulate the denominator so that a victim receives either zero shares of the vault or one share of the vault.

**Payoffs for an Attacker:**

- Rounding to Zero Shares: The victim receives no shares, while the attacker can withdraw nearly all of the deposited assets.
   
  *Attack scenario:*
  
  - Attacker deposits 1 wei into a new ERC-4626 vault, creating 1 share.
  - The attacker front-runs the victim’s deposit of 1,000 ETH, sending 1,000 ETH to the vault, making ```totalAssets() = 1,000 + 1 wei``` and ``` totalSupply() = 1 share ```.
  - The victim's deposit results in 0 shares due to rounding: 

 $$\frac{1 share * 1000 ETH}{1000 ETH + 1 wei} \approx 0 \mbox{ shares}$$

- Rounding to One Share: The victim receives only one share, allowing the attacker to withdraw a significant portion of the pool, leading to a large profit at the expense of the victim.

  *Attack scenario:*
  
   - Attacker deposits 1 wei, creating 1 share.
   - The attacker front-runs the victim’s 1,000 ETH deposit by adding 500 ETH to the pool, making ```totalAssets() = 1 wei + 500 ETH```, ```totalSupply() = 1 share```.
   - The victim's deposit results in 1 share:
     
$$\frac{1 share * 1000 ETH}{500 ETH + 1 wei} \approx 1 \mbox{ share}$$
