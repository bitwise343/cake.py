'''Launch a SmartContract on the Ethereum blockchain.'''

import os

import cake
YOUR_INFURA_ID = cake.my_keys["INFURA"]
YOUR_SECRET_KEY = cake.my_keys["PRIVATE"]
YOUR_PUBLIC_KEY = cake.my_keys["PUBLIC"]
from cake.ethereum import ETHInstance
from cake.SmartContract import SmartContract
from cake.myparser import launch_args


if __name__ == '__main__':
    private = YOUR_SECRET_KEY
    public  = YOUR_PUBLIC_KEY
    timeout = 300
    
    (source, network, compile_only) = launch_args()

    '''Test launching a contract'''
    # Create the web3.py contract instance
    TheContract = SmartContract(source + '.sol')
    print('Contract compiled and data saved.')
    
    if not compile_only:
        # Connect to network and initialize the contract into the connection
        eth_instance = ETHInstance(network, private, public)
        eth_instance.smart_contract = TheContract

        # Send the raw transaction to the blockchain and wait for the receipt
        tx_receipt = eth_instance.deploy_contract()

        contract_info = {
                'contractAddress': tx_receipt['contractAddress'],
                'isLive': True,
                'network': eth_instance.network,
                'txHash': eth_instance.tx_hash,
                'owner': eth_instance.address,
                'abi': TheContract.abi,
            }
        
        # Update the database for the smart contract information
        eth_instance.smart_contract.save_json(contract_info, 'contractInfo.json')

        print( '\nThe address of the contract is:' )
        print( contract_info['contractAddress'], '\n' )
