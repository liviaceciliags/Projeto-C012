import threading
import time
import random

# ========================
# Classe Cliente (Thread)
# ========================
class Cliente(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def fazer_pedido(self):
        pratos = ["Pizza", "Hambúrguer", "Salada", "Macarrão", "Sushi"]
        pedido = random.choice(pratos)
        print(f"{self.nome} fez um pedido: {pedido}")
        return pedido

    def run(self):
        time.sleep(random.randint(1, 3))  # Tempo para decidir o pedido
        pedido = self.fazer_pedido()
        pedidos.append((self.nome, pedido))

# ========================
# Classe Garçom (Thread)
# ========================
class Garcom(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def entregar_pedido(self, pedido):
        print(f"{self.nome} está entregando o pedido de {pedido[0]}: {pedido[1]}")
        time.sleep(random.randint(2, 4))  # Tempo para entregar o pedido
        print(f"{self.nome} entregou o pedido de {pedido[0]}")

    def run(self):
        while pedidos:
            pedido = pedidos.pop(0)
            self.entregar_pedido(pedido)

# ========================
# Classe Chefe de Cozinha (Thread)
# ========================
class Chefe(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def preparar_pedido(self, pedido):
        print(f"{self.nome} está preparando o pedido de {pedido[0]}: {pedido[1]}")
        time.sleep(random.randint(3, 6))  # Tempo de preparo
        print(f"{self.nome} terminou o pedido de {pedido[0]}")

    def run(self):
        while pedidos:
            pedido = pedidos.pop(0)
            self.preparar_pedido(pedido)
            pedidos_prontos.append(pedido)

# ========================
# Execução do Programa
# ========================
if __name__ == "__main__":
    pedidos = []  # Lista de pedidos em espera
    pedidos_prontos = []  # Lista de pedidos prontos
    
    # Criando clientes
    clientes = [Cliente(f"Cliente {i+1}") for i in range(3)]
    
    # Criando chefes de cozinha
    chefe = Chefe("Chef Gordon")
    
    # Criando garçons
    garcom = Garcom("Garçom João")
    chefe.start()
    garcom.start()
    # Iniciando threads
    for cliente in clientes:
        cliente.start()
    
    #time.sleep(5)  # Espera inicial para garantir que pedidos sejam feitos
    
    chefe.join()  # Espera chef terminar

    garcom.join() # Espera garçom terminar
    
    print("Restaurante fechou! Todos foram servidos.")
