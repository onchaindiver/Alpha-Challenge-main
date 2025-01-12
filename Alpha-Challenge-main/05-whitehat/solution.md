# Vulnerability Assessment for Polygon Forks

## a) Potentially Vulnerable Polygon Forks

1. Mumbai Testnet
2. Metis Andromeda

## b) Code to Check Blockchain Safety

```solidity
pragma solidity ^0.8.0;

interface IMRC20 {
    function transferWithSig(bytes memory sig, uint256 amount, bytes32 data, uint256 expiration, address to) external returns (address from);
}

contract VulnerabilityChecker {
    function checkVulnerability(address mrc20Contract, uint256 amount) external returns (bool) {
      
        bytes memory code = address(mrc20Contract).code;
        
        if(code.length == 0) {
            return false;
        }
        
        bytes memory invalidSig = new bytes(64);
        
        try IMRC20(mrc20Contract).transferWithSig(invalidSig, amount, bytes32(0), block.timestamp + 1 hours, address(this)) returns (address from) {
            return from == address(0);
        } catch {
            return false;
        }
    }
}
```

To use this checker:
1. Call `checkVulnerability` with the address of the MRC20 contract and a large amount
2. If it returns true, the contract is vulnerable

## c) Estimating the Potential Maximum Loss

Given the information from the summary, we can make a more accurate estimate:

1. **Mumbai Testnet**: As a testnet, the potential loss remains minimal, close to $0.
2. **Metis Andromeda**: The potential loss would be the total supply of the native token. 


Potential maximum loss calculation:
- For Mumbai Testnet: Negligible
- For Metis Andromeda: Potentially millions of dollars
