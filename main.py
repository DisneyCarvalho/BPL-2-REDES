from flask import Flask, json, jsonify, render_template, request, flash, url_for , redirect, session
from Banco import Bank
import requests


app = Flask(__name__)
app.secret_key = 'afkanjkfakf'

banco = Bank(input('id: '))
banco.addCliente('12','12')
banco.addCliente('11','11')
banco.depositCliente('12',100)
banco.addCliente('13','12')
banco.depositCliente('13',110)


@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')




@app.route('/bank')
def bank():
    return render_template('banco.html', cpf =session['cpf'], saldo = banco.clientes[session['cpf']].saldo , bank = banco.id)

@app.route('/login', methods=['POST'])
def login():
    cpf = request.form['cpf']
    senha = request.form['senha']
    if any(cliente == cpf and banco.clientes[cliente].senha == senha for cliente in banco.clientes):
        session['cpf'] = cpf
        return redirect(url_for('bank'))

    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    cpf = request.form['cpf']
    senha = request.form['senha']
    

    try:
        cpf2 = request.form['cpf2']
        if any(cpf+cpf2 == cliente or cpf2+cpf == cliente for cliente in banco.clientes):
            return 'Já existe'
    except Exception as e:
        print(e)
        if any(cliente == cpf for cliente in banco.clientes):
            return 'Já existe'
        banco.addCliente(cpf,senha)
        return redirect(url_for(('home')))
    if cpf2:
        banco.addCliente(cpf,senha,cpf2)
        return redirect(url_for(('home')))



@app.route('/transferir', methods=['GET'])
def transferir():
    return render_template('trasnferir.html',cpf =session['cpf'], saldo = banco.clientes[session['cpf']].saldo , bank = banco.id)


@app.route('/transferir', methods=['POST'])
def transferir_post():
    try: 
        cpf_transferirf = request.form.get('cpf_transferirf')
        bank = request.form.get('banco')
        valor = request.form.get('valor')
        valores = request.form.get('valores')
        dicta = json.loads(valores)
        print("\n\n",cpf_transferirf,banco,valor, dicta, '\n\n')
        if cpf_transferirf is None or banco is None or valor is None or valores is None:
            raise ValueError('Campos obrigatórios não foram enviados')
        else:
            banco.tranferece(cpf_transferirf,bank,dicta)
        return render_template('trasnferir.html',cpf =session['cpf'], saldo = banco.clientes[session['cpf']].saldo , bank = banco.id)

    except:
        cpf_trasnferir = request.form['cpf_trasnferir']
        bank = request.form['banco']
        valor = request.form['valor']
        j = {banco.id:{session['cpf']:int(valor)}}
        banco.tranferece(cpf_trasnferir,bank,{banco.id:{session['cpf']:-int(valor)}})
        return render_template('trasnferir.html',cpf =session['cpf'], saldo = banco.clientes[session['cpf']].saldo , bank = banco.id)


@app.route('/receive_message', methods=['POST'])
def receive():
    if request.is_json:
        data = request.get_json()
        for i in data:
            if i == 'commit':
                for j in data[i]:
                    for y in data[i][j]:
                        aux = banco.process_commit_message(j,data[i][j][y],y)
                        if aux == 'ack':
                            return jsonify({'mensage':'ack'}), 200
                        else:
                            print('semcomit')
                            return 'not ack'
            elif i == 'prepare':
                for j in data[i]:
                    for y in data[i][j]:
                        aux = banco.process_prepare_message(j,data[i][j][y],y)
                        if aux == 'ok':
                            return jsonify({'mensage':'ack'}), 200
                        else:
                            return 'not ack'
            elif i == 'abort':
                for j in data[i]:
                    for y in data[i][j]:
                        banco.process_abort_message(y,data[i][j][y])
        print("Mensagem recebida:", data)
        return 'ack'
    else:
        return jsonify({"status": "erro", "message": "Apenas JSON é aceito"}), 400
    

@app.route('/transferirvarios', methods=['GET'])
def transferirvarios():
    bancos = banco.bancos
    contas = []

    for i in bancos:
        ul = bancos[i]+'/conta'
        try:
            data = requests.post(ul, json= session['cpf'], timeout=2)
        except Exception as e:
            print(e)
        status = data.status_code  # Capturar o código de status da resposta
        response_data = data.json() if status == 200 else print('erro no envio')
        if response_data:
            if response_data not in contas:
                contas.append(response_data)
    
    return render_template('transferirvarios.html', contas = contas )


@app.route('/conta', methods=['POST'])
def conta():
    cpf = request.get_json()
    cliente = banco.clientes.get(cpf,None)
    if not cliente:
        return {}
    
    contas = []
    for i in banco.clientes:
        if cpf == banco.clientes[i].cpf or cpf == banco.clientes[i].cpf2:
            contas.append({'banco': banco.id , 'cpf': banco.clientes[i].get_cpf(), 'saldo': banco.clientes[i].saldo})

    print(contas)
    return contas


@app.route('/atualizatransferir', methods=['GET'])
def atualiza():
    return render_template('trasnferir.html',cpf =session['cpf'], saldo = banco.clientes[session['cpf']].saldo , bank = banco.id)


@app.route('/atualizatransferirtodas', methods=['GET'])
def atualizatods():
    return redirect(url_for(('transferirvarios')))


    



if __name__ == '__main__':
    app.run(host='192.168.1.6' , port= input('Port: '), debug=True)


