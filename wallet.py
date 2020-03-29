import base58
import codecs
import hashlib


from ecdsa import SigningKey
from ecdsa import NIST256p


import transaction
import blockchain

class Wallet(object):

    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()
        
    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemed160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex'
        )

        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        checksum = sha256_hex[:8]

        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')

        blockchain_address = base58.b58encode(address_hex).decode('utf-8')

        return blockchain_address


if __name__ == '__main__':
    wallet_A = Wallet()
    wallet_B = Wallet()
    value = 100
    print(f'wallet_A\'s blockchain_address : {wallet_A.blockchain_address}')
    print(f'wallet_B\'s blockchain_address : {wallet_B.blockchain_address}')
    print(f'value : {value}')
    t = transaction.Transaction(
            wallet_A.blockchain_address,
            wallet_B.blockchain_address,
            100,
            wallet_A.private_key,
            wallet_A.public_key
        )
    blockchain = blockchain.BlockChain()
    blockchain.add_transaction(
        sender_blockchain_address=wallet_A.blockchain_address,
        recipient_blockchain_address=wallet_B.blockchain_address,
        value=value,
        sender_public_key=wallet_A.public_key,
        signature=t.generate_signature()
    )
    blockchain.mining()
    print(blockchain.print_chain())
