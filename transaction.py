import utils
import hashlib

from ecdsa import SigningKey
from ecdsa import NIST256p


class Transaction(object):

    def __init__(self, sender_blockchain_address, recipient_blockchain_address,
                 value, sender_private_key, sender_public_key):
        self.sender_blockchain_address = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key

    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = {
            'sender_blockchain_address': self.sender_blockchain_address,
            'recipient_blockchain_address': self.recipient_blockchain_address,
            'value': self.value
        }
        sha256.update(str(utils.sorted_dict_by_key(transaction)).encode('utf-8'))
        message = sha256.digest()
        # String -> SigningKey object
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p
        )
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature
