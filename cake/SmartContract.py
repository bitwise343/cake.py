'''
This will be the module that compiles contracts written in *.sol files in the
directory.
'''

import os
import json
from solc import compile_standard


class SmartContract:
    '''SmartContract takes a solidity filename (Source.sol) and compiles it. The
    bytecode and abi can be accessed easily. Future work will include possible
    alterations of the compilation process, depending on what is available to
    the solc module.
    '''
    # More robust file structure / automatic naming or something in the future?
    HOME = os.path.realpath(os.curdir)
    CONTRACTS = HOME+'/Contracts/'

    DATA = {
        # Compiling Solidity
        'language': 'Solidity',
        
        # These are the smart contracts to compile. Only do one at a time (?)
        'sources': {},
        
        # This never changes, hence putting DATA as a class attribute.
        'settings': {
            
            'outputSelection' : {
                '*': {'*':['metadata','evm.bytecode','evm.bytecode.sourceMap']}
            }

        } 
    }

    def __init__(self, source):
        '''Compile the contract with the given source file name.'''
        # Save the file name of the contract
        self.source = source
        # Isolate the name of the contract
        self.name = source.rstrip('.sol')

        # Load the text from the *.sol file
        self.contract_text = self.load_text()

        # Add the text data into the compiler dictionary
        self.DATA['sources'][source] = {'content': self.contract_text}     
        
        # Populate the SmartContract with all of its attributes
        self.compile_contract()

    def compile_contract(self):
        '''Compiles the contract and saves the output into *.json files in the 
        appropriate Contract directory. Sets the abi and bytecode attributes of
        the SmartContract instance.'''
        # Pass the contract into the solidity compiler
        compiled = self.compile_standard()

        # Load compiler data that might be needed at runtime
        self._metadata = json.loads( compiled['metadata'] )
        self._abi      = self.metadata['output']['abi']
        self._bytecode = compiled['evm']['bytecode']['object']
        
        # Save all of the metadata from the compilation into a json file
        self.save_json(self.metadata, 'metadata.json')
        self.save_json(self.abi, 'abi.json')
        self.save_json({'bytecode':self.bytecode}, 'bytecode.json')
        
        try:
            contract_info = self.load_json('contractInfo.json')
            if not contract_info['isLive']:
                # if the contract is live, then use its info (address/abi/etc.)
                raise ValueError 
        except:
            # if the contract hasn't been compiled yet or isn't live yet, then
            # populate a contractInfo.json file with the following defaults
            contract_info = {
                'contractAddress': None,
                'isLive': False,
                'network': None,
                'txHash': None,
                'owner': None,
                'abi': self.abi, # exception: this is the actual contract abi
            }
            self.save_json(contract_info, 'contractInfo.json')
        
        # Either take the default values or the real values
        self._contract_address = contract_info['contractAddress']
        self._owner = contract_info['owner']
        self._contract_info = contract_info

    def load_json(self, fname):
        return json.load(self.CONTRACTS+self.name+'/'+fname)

    def save_json(self, JSON, fname):
        with open(self.CONTRACTS+self.name+'/'+fname, 'w+') as f:
            json.dump(JSON, f, indent=4)
        return

    def load_text(self):
        '''Pull the Solidity smart contract from the file. Returns text.'''
        with open(self.CONTRACTS + self.name + '/' + self.source, 'r') as f:
            contract_text = f.read()
        return contract_text

    def compile_standard(self):
        '''Might update this later. Only returns the parts we care about.'''
        return compile_standard(self.DATA)['contracts'][self.source][self.name]

    
    '''Write these properties so that we can't edit them without compiling a
    contract again.'''
    @property
    def metadata(self):
        return self._metadata
    @metadata.setter
    def metadata(self, waste):
        print('metadata is set by self.compile_contract')
        return
    
    @property
    def abi(self):
        return self._abi
    @abi.setter
    def abi(self, waste):
        print('abi is set by self.compile_contract')
        return
    
    @property
    def bytecode(self):
        return self._bytecode
    @bytecode.setter
    def bytecode(self, waste):
        print('bytecode is set by self.compile_contract')
        return 

    @property
    def contract_info(self):
        return self._contract_info
    @contract_info.setter
    def contract_info(self, waste):
        print('Only set through the SmartContract constructor')
        return

    @property
    def owner(self):
        return self._owner
    @owner.setter
    def owner(self, waste):
        print('Only set through the SmartContract constructor')
        return

    @property
    def contract_address(self):
        return self._contract_address
    @contract_address.setter
    def contract_address(self, waste):
        print('Only set through the SmartContract constructor')
        return
    
if __name__ == '__main__':
    Greeter = SmartContract('Greeter.sol')
    