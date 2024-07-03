
from threading import Lock, Thread




class Client:
    def __init__(self,cpf,senha) -> None:
        self.cpf = cpf
        self.senha = senha
        self.saldo = 0
        self.lock = Lock()

        pass


