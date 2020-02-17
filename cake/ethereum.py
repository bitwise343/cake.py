'''
Developing a module that enables interaction with the Ethereum blockchain using
only Python code.
'''
# external modules
from web3 import Web3
from web3 import HTTPProvider
from eth_account import Account

# user generated modules
# config contains keys and access IDs
import cake
YOUR_INFURA_ID  = cake.my_keys["INFURA"]
YOUR_SECRET_KEY = cake.my_keys["PRIVATE"]
YOUR_PUBLIC_KEY = cake.my_keys["PUBLIC"]
# contracts contain the compiled Contract objects
from .SmartContract import SmartContract

class ETHInstance(Web3):
    ''' There are multiple ways of connecting to the blockchain.'''
    
    # Infura access code to connect to the various eth networks
    INFURA_ID = YOUR_INFURA_ID

    CHAIN_IDS = {'ropsten': 3, 'rinkeby': 4, 'kovan': 42}
    # CHAIN_IDS = {'ethereum': 1, 'mainnet': 1, 'ropsten': 3, 'rinkeby': 4,
    #    'kovan': 42}

    def __init__(self, network, private=None, public=None):

        assert network in self.CHAIN_IDS.keys(), ( 'Chosen network not valid.'
            ' Possible networks include:\n{}'.format(self.CHAIN_IDS.keys()) )
        self.chainId = (network, 'mainnet')[int(network=='ethereum')]
        httpprovider = 'https://{}.infura.io/v3/{}'.format(network,
            self.INFURA_ID)
        super().__init__(HTTPProvider(httpprovider))
        self._network = network

        if private is not None:
            # Create an account object from the private key
            self.acct  = self.init_account(private, public)
            self.eth.defaultAccount = self.address
        else:
            self._nonce   = None
            self._address = None

    def verify_connected(self):
        '''Throws AssertionError if not connected to an Ethereum node'''
        assert self.isConnected(), 'Not currently connected to any networks.'
        return

    '''Account methods begin here'''
    def init_account(self, private, public):
        '''Create the Account object with the given private key.'''
        acct = Account.from_key(private)
        public = self.toChecksumAddress(public)
        assert public == acct.address, 'Address does not match the private key.'
        self._address = acct.address
        self._nonce   = self.eth.getTransactionCount(self.address)
        return acct

    '''Transaction methods begin here'''
    def create_transaction(self, to_address, amount_in_wei, gas=2000000,
            gasPrice=1):
        '''Create transaction data to be signed with the account/private key.
        The amount being sent MUST be in denominations of wei. The web3.py
        base API has a function: Web3.toWei(amount, currency) that you can use
        to convert from a given denomination of Ether into wei.
        '''
        assert Web3.isChecksumAddress(to_address), 'Address not Checksum format'
        transaction = {
            'to'       : to_address,
            'value'    : amount_in_wei,
            'gas'      : gas,
            'gasPrice' : gasPrice,
            'nonce'    : self.nonce,
            'chainId'  : self.chainId,
        }
        return transaction

    def sign_transaction(self, transaction, key=None):
        if key is not None:
            signed_transaction = Account.sign_transaction(transaction, key)
        else:
            signed_transaction = self.acct.sign_transaction(transaction)
        return signed_transaction

    def send_raw_transaction(self, signed_transaction):
        '''Actually send the signed transaction to the network.'''
        return self.eth.sendRawTransaction(signed_transaction.rawTransaction)

    '''Building and deploying contracts begin here'''
    def build_contract_transaction(self):
        transaction = {
            'value': 0,
            'chainId': self.chainId,
            'from' : self.address,
            'data' : self.bytecode,
            'nonce' : self.nonce,
        }
        transaction['gas'] = self.eth.estimateGas(transaction)
        transaction['gasPrice'] = self.eth.gasPrice
        return transaction

    def deploy_contract(self):
        signed = self.sign_transaction(self.build_contract_transaction())
        tx_hash = self.send_raw_transaction(signed)

        self._tx_hash = self.toHex(tx_hash)
        print( 'tx_hash:' )
        print( self.tx_hash, '\n' )
        contract_info = {
                'contractAddress': None,
                'isLive': True,
                'network': self.network,
                'txHash': self.tx_hash,
                'owner': self.address,
                'abi': self.abi,
        }
        self.smart_contract.save_json(contract_info, 'contractInfo.json')
        print('Waiting for tx to be mined. Timeout = 300s')
        tx_receipt = self.eth.waitForTransactionReceipt(tx_hash, timeout=300)
        print(tx_receipt)
        return tx_receipt

    '''Calling contract functions begins here'''
    def build_contract_call(self, func, *args, **kwargs):
        transaction = self.funcs[func](*args, **kwargs).buildTransaction({'nonce': self.nonce})
        return transaction

    def send_contract_call(self, transaction):
        raw = self.sign_transaction(transaction)
        tx_hash = self.send_raw_transaction(raw)
        print( self.toHex(tx_hash) )
        print('Waiting for tx to be mined. Timeout = 300s')
        tx_receipt = self.eth.waitForTransactionReceipt(tx_hash, timeout=300)
        return tx_receipt

    def call(self, function, *args, **kwargs):
        return self.contract.functions[function](*args, **kwargs).call()

    def send(self, func, *args, **kwargs):
        t = self.build_contract_call(func, *args, **kwargs)
        return self.send_contract_call(t)

    '''Class Properties begin here'''
    @property
    def network(self):
        return self._network
    @network.setter
    def network(self, waste):
        print('network is set when the instance connects to a node.')
        return
    @property
    def nonce(self):
        '''Getter for the nonce of the given account. Nonce == # of transactions
        '''
        self.verify_connected()
        return self.eth.getTransactionCount(self.address)
    @nonce.setter
    def nonce(self, n):
        print('The current nonce is gathered from address transaction count.')
        return

    @property
    def chainId(self):
        '''Getter for the chainId of the currently connected network'''
        try:
            return self._chainId
        except:
            print('Not connected. Try ETHInstance.connect(network)')
            return
    @chainId.setter
    def chainId(self, network):
        '''Check that the given network is valid'''
        assert network in self.CHAIN_IDS.keys(), ( 'Chosen network not valid.'
            +' Possible networks:\n{}'.format(self.CHAIN_IDS.keys()) )
        self._chainId = self.CHAIN_IDS[network]

    @property
    def address(self):
        '''Getter for our address property'''
        try:
            return self._address
        except:
            print('No address: Run init_account to connect an account')
            return
    @address.setter
    def address(self, value):
        '''Prevent the user from setting the address manually'''
        print('Address must be derived from private key.')
        print('To change the address, call init_account method with new keys.')
        return

    @property
    def tx_hash(self):
        return self._tx_hash
    @tx_hash.setter
    def tx_hash(self, waste):
        print('tx_hash is set during contract deployment.')
        return

    @property
    def funcs(self):
        return self._funcs
    @funcs.setter
    def funcs(self, waste):
        print('functions dictionary set during initialization of eth.Contract')
        return

    @property
    def contract(self):
        return self._contract
    @contract.setter
    def contract(self, data):
        self._abi = data['abi']
        self._contract = self.eth.contract(
            address=data['contractAddress'],
            abi=self.abi
        )
        self._funcs = self.contract.functions
        return

    @property
    def smart_contract(self):
        return self._smart_contract
    @smart_contract.setter
    def smart_contract(self, Contract):
        self._smart_contract = Contract
        self._abi = Contract.abi
        self._bytecode = Contract.bytecode
        return

    @property
    def bytecode(self):
        return self._bytecode
    @bytecode.setter
    def bytecode(self, waste):
        print("bytecode is set during contract creation")
        return
    @property
    def abi(self):
        return self._abi
    @abi.setter
    def abi(self):
        print("abi is set during contract creation")
        return


if __name__ == '__main__':
    import json
    private = YOUR_SECRET_KEY
    public  = YOUR_PUBLIC_KEY

    # You can choose a different testnet if you'd like
    network = 'ropsten' 
    print('Connecting to network: ', network)

    # Connect to given network with your account
    ei = ETHInstance(network, private, public)

    # Check that it's connected ( assert only, doesn't output anything )
    ei.verify_connected()
    print('If you made it this far, you are connected!')

    # Compare keys generated by private key and given by user
    print('Public key hashed from private key: ', ei.address )
    print('Given public key: ', YOUR_PUBLIC_KEY )