from eth_keys import keys
from web3 import Web3


def create_key_pair():
    private_key = keys.PrivateKey(os.urandom(32))
    public_key = private_key.public_key.to_canonical_address().hex()
    public_key = Web3.toChecksumAddress(public_key)
    return private_key, public_key
