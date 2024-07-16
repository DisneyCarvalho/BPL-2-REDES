
from threading import Lock, Thread




class Client:
    def __init__(self,cpf,senha) -> None:
        self.cpf = cpf
        self.cpf2 = None
        self.senha = senha
        self.saldo = 0
        self.lock = Lock()

        
    def get_cpf(self):
        if self.cpf2:
            return self.cpf + self.cpf2 
        return self.cpf


