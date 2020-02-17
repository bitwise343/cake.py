# Interact with the Ethereum blockchain
- Send transactions on the Ethereum blockchain
- Compile and deploy Solidity smart contracts
- Call smart contract functions

## Requirements
- [Solidity compiler (solc)](https://solidity.readthedocs.io/en/v0.4.21/installing-solidity.html)
- [web3.py](https://web3py.readthedocs.io/en/stable/quickstart.html#installation)
- [An Infura ID](https://infura.io/)

## Installation using a virtual environment
All python dependencies are accounted for in the requirements.txt file. Here's how I installed everything during a test installation:

	git clone https://github.com/jmb-42/cake.py
	python3 -m venv cake-env
	source cake-env/bin/activate
	cd cake.py
	pip install -r requirements.txt

## Using Infura
Create "`infura.json`"" in `/cake.py/cake/config/`, populate it with your own Infura ID:

```
{
    "INFURA": "your_infura_id"
}
```

If you want to contribute to the project, by default the repository ignores  all json files in `/cake.py/cake/config/`, so you should be fine to fork it without sharing your keys/infuraID. That being said, **never** use any private/public keys that you have *real* Ethers on. Only use wallets that are exclusively for testnets. Currently only supports infura nodes, but in the future I will implement different methods of connecting to Ethereum nodes, via IPC or websockets.

## Getting test Ether
Here is a faucet for getting Ether on the Ropsten testnet.
https://faucet.metamask.io/

## Launching Smart Contracts
- Create a directory for `YourContractName`
  - `/cake.py/Contracts/YourContractName/`
- Write the Solidity code
  - `/Contracts/YourContractName/YourContractName.sol`

Notice the matching names above. Your contract directories must follow that convention.

After creating the source code, you can compile and launch your contract using `launch.py` with `YourContractName` and your intended `network` as options.

	source cake-env/bin/activate
	cd cake.py
	python -i launch.py --source YourContractName --network ropsten

Upon launching the contract, various `.json` files will populate  `/Contracts/YourContractName/`. These contain the compiled information about the contract. As of right now, launching the same contract twice overwrites the previous contract, and redeploys it to the blockchain. That will be fixed later.

## Interacting with existing Smart Contracts

After launching the contract, you can begin an interactive instance with the contract using the following code:

	source cake-env/bin/activate
	cd cake.py
	python -i interact.py --source YourContractName --network ropsten

The script will begin by showing you all of the possible functions of the  contract, and give two examples of how to call a function. The way that these functions are called depends on whether they return `constant` (`view`) or  actually do calculations on Ethereum.

## `call('func', *args, **kwargs)`

Use for functions that simply return a `constant` (also called a `view` in Solidity). Does not consume any gas. Does not require keys. Does require a connection to an ethereum node.

## `send('func', *args, **kwargs)`

Use for functions that alter the state of the blockchain, e.g. transfers, setter functions, approvals, minting, etc. Consumes gas, requires a funded account key-pair. Calculates the gas automatically. Returns the transaction receipt.

## Examples:

First running the script:

	(cake-env) user@hostname: ~/cake.py$ python -i interact.py -s Greeter -n ropsten
	----------------------------------------
	Connected to contract:  Greeter
	----------------------------------------
	Available functions:
	----------------------------------------
		setGreeting
		greet
		greeting
	----------------------------------------
	> call view with call('function', *args, **kwargs)

	> call func with send('function', *args, **kwargs) 
	----------------------------------------
	>>> _

Now it's expecting input (>>> in last line). Let's call `greet`.

	>>>call('greet')
	'Hello, world!'

Let's change the greeting stored in the blockchain using `setGreeting`.

	>>>tx_receipt = send('setGreeting', 'He was number 0ne!')
	0x42ca822fb8c6129947276d68dac612a6bb83e2a9604e0f46478b5329632669de
	Waiting for tx to be mined. Timeout = 300s
	_

It shows the tx hash of the sent transaction. Note that this consumed gas to send to the blockchain. The script waits 5 minutes for a response before returning control to the user. If it doesn't respond in time, the transaction was still broadcast to the blockchain so just wait a few and it should go through. After it's done, control will return to the user:

	>>>tx_receipt = send('setGreeting', 'He was number 0ne!')
	0x42ca822fb8c6129947276d68dac612a6bb83e2a9604e0f46478b5329632669de
	Waiting for tx to be mined. Timeout = 300s
	>>> _

Note: I fully intend to implement threading that will allow the transaction to be mined in the background without witholding control from the user. Anyway, now we can see that the greeting changed by calling `greet` again.

	>>>call('greet')
	'He was number 0ne!'

## What functions are available to the given contract?

If ever you want to see the possible functions of the smart contract, call:

	>>>show_funcs()
	----------------------------------------
	Available functions:
	----------------------------------------
		setGreeting
		greet
		greeting
	----------------------------------------
	> call view with call('function', *args, **kwargs)

	> call func with send('function', *args, **kwargs)
	----------------------------------------
	>>> _
	
# Disclaimer
All transactions are signed locally, helping to preserve the privacy of the user's sensitive wallet information, but users of this code must exercise utmost caution when using their keys to interact with the blockchain. I explicitly recommend **NOT** using this code to launch projects onto mainnet Ethereum. I basically wrote this code as a personal project to practice deploying Solidity smart contracts exclusively on testnets. There are no encryption techniques in this code to secure your keys. If you download this code, a random private/public key pair will be created for you to use on Ethereum the first time you run it. You don't ever have to connect your own wallet. You shouldn't. I also recommend against ever sending real Ether or other ERC tokens to the address generated by this code.

By downloading and using this code you agree to take on all responsibility for the results of using it, including any damages incurred or assets lost as a result of using the code.
