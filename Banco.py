from time import sleep
from cliente import Client
import requests






class Bank():
    def __init__(self,id) -> None:
        self.clientes = {}
        self.id = id
        self.bloqueios = {}
        self.bancos = {}
        self.bancos['1'] = 'http://192.168.1.6:5010/'
        self.bancos['3'] = 'http://192.168.1.6:5030/'
        self.bancos['2'] = 'http://192.168.1.6:5020/'






    def addCliente(self, cpf,senha, cpf2 = None):
        if cpf2:
            self.clientes[cpf+cpf2] = Client(cpf,senha)
            self.clientes[cpf+cpf2].cpf2 =  cpf2
            return
        self.clientes[cpf] = Client(cpf,senha)


    def depositCliente(self, cpf, value):
        self.clientes[cpf].saldo += value


    ## Espera receber um dicionario com seguinte formato {id do banco: [cpf,valor da trasnferencia]}
    def send_message(self,tipo, data):
        for i in data:
            _URL = self.bancos[i] + '/receive_message'
            mensagem = data[i]
            print('Enviando msg para %s',[_URL])

        try:
            response = requests.post(_URL, json={tipo: {self.id :mensagem}}, timeout=2)
            status = response.status_code  # Capturar o código de status da resposta
            response_data = response.json() if status == 200 else {'error': 'Erro no envio'}
            if response.json()['mensage'] == 'ack':
                return 'ack'
        except Exception as e:
            status = 500
            response_data = {'error': str(e)}
        return 'not ack'



    def receive_message(self,data):
        for i in data:
            if i == 'commit':
                for j in data[i]:
                    for y in data[i][j]:
                        self.process_commit_message(j,data[i][j][y],y)
            elif i == 'prepare':
                for j in data[i]:
                    for y in data[i][j]:
                        self.process_prepare_message(j,data[i][j][y],y)

            elif i == 'abort':
                for j in data[i]:
                    for y in data[i][j]:
                        self.process_abort_message(j,data[i][j][y],y)
        return 
    

    def abort_comits(self,comits):
        for j in comits:
            self.send_message('abort',{j:comits[j]})


    
    
    def process_prepare_message(self,banco_id, valor_transferencia,clienteCPF ):
        if valor_transferencia < 0:
            with self.clientes[clienteCPF].lock:
                if self.clientes[clienteCPF].saldo >= -valor_transferencia:
                    return 'ok'
                else:
                    return 'not ok'
        return 'ok'


    def process_commit_message(self,banco_id, valor_transferencia,clienteCPF ):
        with self.clientes[clienteCPF].lock:
            self.clientes[clienteCPF].saldo += valor_transferencia
        return 'ack'  # Confirmação de conclusão

    def process_abort_message(self, clienteCPF, valor_transferencia):
        
        with self.clientes[clienteCPF].lock:
            self.clientes[clienteCPF].saldo -= valor_transferencia


        # Processar mensagem de abort recebida do coordenador
        # Reverter as mudanças feitas durante a fase de preparação
        return 'ack'  # Confirmação de conclusão
    


    def tranferece(self,cliente_destino,banco_destino,transferencias):
        prepare = []
        comit = {}
        valor_transferencia_final = 0


        prepare.append(self.send_message('prepare',{banco_destino : {cliente_destino: valor_transferencia_final}})) ##Perara a conta destino

        for i in transferencias:
            prepare.append(self.send_message('prepare',{i : transferencias[i]}))
        #print(prepare)  #APAGA
        if all(j == 'ack' for j in prepare):
            for y in transferencias:
                for k in transferencias[y]:
                    print('commit', y, transferencias[y], '\n\n')
                    print('commit', {y:{k : transferencias[y][k]}}, '\n\n')
                    aux = self.send_message('commit',{y:{k : transferencias[y][k]}})
                    print(y,transferencias[y][k], 'comit')
                    if aux == 'ack':
                        comit[y] = {transferencias[y][k]}
                        for l in transferencias[y]:
                            valor_transferencia_final += transferencias[y][l]
                    else:
                        self.abort_comits(comit)
                        return 'not ack'
        else:
            return 'not ack'
        
        print(valor_transferencia_final)
        deposito_final = self.send_message('commit',{banco_destino : {cliente_destino: -valor_transferencia_final}})
        if deposito_final != 'ack':
            print(deposito_final)
            self.abort_comits(comit)
            return 'not ack'
        

        #print(f'prepare {prepare}\ncomit {comit}')
        return 'ack'





        
if __name__ == '__main__':



    banco = Bank(1)
    
    banco.addCliente(13,12)
    banco.depositCliente(13,60)
    banco.tranferece('15', 2, {1: {13: -50}})





    

# Exemplo de loop de recebimento de mensagens
'''while True:
    message = receive_message_from_coordinator()
    if message.type == 'prepare':
        response = process_prepare_message()
    elif message.type == 'commit':
        response = process_commit_message()
    elif message.type == 'abort':
        response = process_abort_message()
    send_response_to_coordinator(response)'''





