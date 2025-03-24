import threading
import time
import random

class Cliente(threading.Thread):
    def __init__(self, id, estado, pedidoAtual, mesaAlocada):
        super().__init__()
        self.id = id
        self.estado = estado
        self.pedidoAtual = pedidoAtual
        self.mesaAlocada = mesaAlocada

    def run(self):
        self.chamarGarcom()
        self.fazerPedido()
        self.receberPedido()
        self.pagarConta()

    def chamarGarcom(self):
        self.mesaAlocada = True
        self.estado = '🛎️ Esperando o Graçom'
        print(f'🛎️ Cliente {self.id} na mesa chamou o Garçom')
        time.sleep(1)

    def fazerPedido(self):
        #pratos = random.choice(['Lasanha', 'Macarrão', 'Pizza', 'Salada', 'Hambúrguer', 'Sushi'])
        #self.pedidoAtual = pratos
        print(f'📝 Cliente {self.id} fez um pedido: {self.pedidoAtual}')
        self.estado = 'Esperando o pedido'

    def receberPedido(self):
        print(f'🍽️ Cliente {self.id} recebeu o pedido do garçom: {self.pedidoAtual}')
        self.estado = 'Comendo'
        time.sleep(random.uniform(2,5))

    def pagarConta(self):
        self.estado = 'Finalizado'
        print(f'✅ Cliente {self.id} pagou a conta e deixou o restaurante')
        self.mesaAlocada = False