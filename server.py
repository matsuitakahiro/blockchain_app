from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


import blockchain
import transaction
import wallet


app = Flask(__name__)


blockchain = blockchain.BlockChain()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/wallet/generate', methods=['POST'])
def generate_wallet():
    my_wallet = wallet.Wallet()
    response = {
        'private_key': my_wallet.private_key,
        'public_key': my_wallet.public_key,
        'blockchain_address': my_wallet.blockchain_address
    }
    return jsonify(response), 200


@app.route('/wallet/calculate', methods=['POST'])
def calculate_total_amount():
    request_json = request.json
    total_amount = blockchain.calculate_amount(request_json['blockchain_address'])
    return jsonify({'total_amount': total_amount}), 200


@app.route('/transaction', methods=['POST', 'GET'])
def handle_transaction():
    request_json = request.json
    if request.method == 'POST':
        sender_blockchain_address = request_json['sender_blockchain_address']
        recipient_blockchain_address = request_json['recipient_blockchain_address']
        value = float(request_json['value'])
        sender_private_key = request_json['sender_private_key']
        sender_public_key = request_json['sender_public_key']

        transaction_to_add = transaction.Transaction(
            sender_blockchain_address,
            recipient_blockchain_address,
            value,
            sender_private_key,
            sender_public_key,
        )
        is_added = blockchain.add_transaction(
            sender_blockchain_address=sender_blockchain_address,
            recipient_blockchain_address=recipient_blockchain_address,
            value=value,
            sender_public_key=sender_public_key,
            signature=transaction_to_add.generate_signature()
        )
        if is_added:
            return jsonify({'message': 'success'}), 200
        return jsonify({'message': 'fail'}), 400

    if request.method == 'GET':
        response = blockchain.transaction_pool
        return jsonify(response), 200


@app.route('/mine')
def mine():
    blockchain.mining()
    return jsonify({'message': 'success'}), 200


@app.route('/chain', methods=['GET'])
def chain():
    response = blockchain.chain
    return jsonify(response), 200


@app.route('/chain/history')
def print_chain():
    None


if __name__ == '__main__':
    app.run(host='localhost', port=8080, threaded=True, debug=True)