from threading import Lock, Thread
from flask import Flask, request, jsonify
import requests

'''
app = Flask(__name__)


@app.route('/send_message', methods=['GET'])
def send_message():
    TARGET_URL = 'http://192.168.1.3:5000/receive_message'
    response = requests.post(TARGET_URL, json={'mesage': 'ok'})

    # Aqui você pode adicionar a lógica para processar a mensagem, como enviá-la para outro serviço, armazená-la, etc.
    print(f"Received message: {'essage'}")
    
    return jsonify({"status": "success"},response.json())

if __name__ == '__main__':
    app.run(debug=True)



b = ['1','1','1']

if all(c == '1' for c in b):
    print(True)



trasnferencia = {1:['cpf','valortranferencia'], 2 : '141'}

comit = {'comit': 'mensagem'}




class Conta:
    def __init__(self, id, saldo):
        self.id = id
        self.saldo = saldo
        self.lock = Lock()  # Bloqueio específico para a conta

contas = [
    Conta(id=0, saldo=1000),
    Conta(id=1, saldo=2000),
    Conta(id=2, saldo=3000)
]'''

import os
from datetime import datetime




a ={ 'p': {1:2}}


print(list(a['p'].keys()))





