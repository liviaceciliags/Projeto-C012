import threading
import time
import queue

class Garcom(threading.Thread):
    def __init__(self, garcom_id, fila_pedidos, fila_cozinha, fila_prontos):
        super().__init__()
        self.garcom_id = garcom_id
        self.fila_pedidos = fila_pedidos  # Clientes colocam pedidos aqui
        self.fila_cozinha = fila_cozinha  # Garçom leva os pedidos para a cozinha
        self.fila_prontos = fila_prontos  # Chefes colocam pedidos prontos aqui

    def atenderCliente(self):
        """Recebe pedidos dos clientes e os leva para a cozinha."""
        try:
            pedido = self.fila_pedidos.get(timeout=2)  # Aguarda um pedido na fila
            print(f"Garçom {self.garcom_id} pegou o pedido {pedido['id']} do Cliente {pedido['cliente'].id}")
            self.fila_cozinha.put(pedido)  # Envia para a cozinha
            self.fila_pedidos.task_done()
        except queue.Empty:
            pass  # Nenhum pedido pendente no momento

    def entregarPedido(self):
        """Entrega pedidos prontos para os clientes."""
        try:
            pedido = self.fila_prontos.get(timeout=2)  # Aguarda um pedido pronto
            cliente = pedido["cliente"]
            print(f"Garçom {self.garcom_id} entregou o pedido {pedido['id']} para Cliente {cliente.id}")
            cliente.receberPedido(pedido)  # Cliente recebe o pedido
            self.fila_prontos.task_done()
        except queue.Empty:
            pass  # Nenhum pedido pronto no momento

    def run(self):
        """Executa o fluxo do garçom continuamente."""
        while True:
            self.atenderCliente()
            self.entregarPedido()
            time.sleep(1)  # Simula tempo de atendimento
