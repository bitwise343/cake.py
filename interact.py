'''Interact with an already existing blockchain contract'''

import json
from web3 import Web3, HTTPProvider

import cake
YOUR_INFURA_ID = cake.my_keys["INFURA"]
YOUR_SECRET_KEY = cake.my_keys["PRIVATE"]
YOUR_PUBLIC_KEY = cake.my_keys["PUBLIC"]
from cake.myparser import interact_args
from cake.ethereum import ETHInstance

# source = 'TestERC'
# network = 'ropsten'

source, network = interact_args()

ei = ETHInstance(network, YOUR_SECRET_KEY, YOUR_PUBLIC_KEY)
with open('Contracts/'+source+'/contractInfo.json', 'r') as f:
    contract_info = json.load(f)
ei.contract = {
    'abi': contract_info['abi'],
    'contractAddress': contract_info['contractAddress'],
}
call = ei.call
send = ei.send
def show_funcs():
    print('----------------------------------------')
    print('Available functions:')
    print('----------------------------------------')
    for f, fu in enumerate(ei.funcs):
        print( '    ' + fu )
    print('----------------------------------------')
    print('  > call view with call(\'function\', *args, **kwargs)')
    print()
    print('  > call func with send(\'function\', *args, **kwargs) ')
    print('----------------------------------------')
    
# Open a connection to the chosen contract
# contract = w3.eth.contract(
#     address = contract_info['contractAddress'],
#     abi=contract_info['abi']
# )
print('----------------------------------------')
print('Connected to contract: ', source)
show_funcs()


'''

To run a call to a contract, we need to build the transaction first, then sign
and send it. The way to do that is shown by example below:

------------------------------------------------------------------------------
    to call contract.mint(address, amount)):
------------------------------------------------------------------------------

    transaction = ei.build_contract_call('mint', address, amount)
    tx_receipt = ei.send_contract_call(transaction)

------------------------------------------------------------------------------

'''