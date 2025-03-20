import threading
import time
import queue
import random

class Caixa(threading.Thread):
    """
    Classe que representa um caixa do restaurante.
    Cada caixa processa os pagamentos dos clientes quando eles terminam de comer.
    """

    def __init__(self, cashier_id, order_queue):
        super().__init__()
        self.cashier_id = cashier_id  # ID do caixa
        self.order_queue = order_queue  # Fila compartilhada com pedidos

    def run(self):
        """
        Método executado quando a thread do caixa inicia.
        Ele aguarda pedidos na fila e os processa.
        """
        while True:
            try:
                # Aguarda um pedido por um tempo (timeout evita espera infinita)
                order = self.order_queue.get(timeout=3)
                print(f"🧾 Caixa {self.cashier_id} está processando o pagamento do cliente {order}")
                
                # Simulando tempo aleatório de processamento do pagamento
                process_time = random.uniform(1.5, 3.5)
                time.sleep(process_time)
                
                print(f"✅ Caixa {self.cashier_id} finalizou o pagamento do cliente {order} em {process_time:.2f} segundos")
                
                # Marca o pedido como concluído na fila
                self.order_queue.task_done()
            except queue.Empty:
                # Se não há pedidos na fila, o caixa encerra suas atividades
                print(f"❌ Caixa {self.cashier_id} não tem mais clientes para atender e está fechando.")
                break

def main():
    """
    Função principal que simula o funcionamento do restaurante.
    - Clientes terminam a refeição e vão para o caixa pagar.
    - Três caixas processam os pagamentos simultaneamente.
    """

    # Criando uma fila de pedidos (clientes terminando a refeição e indo pagar)
    order_queue = queue.Queue()

    # Criando pedidos de pagamento (simulando clientes finalizando a refeição)
    num_pedidos = 10  # Número total de clientes que irão ao caixa
    for order_id in range(1, num_pedidos + 1):
        order_queue.put(order_id)
    
    print(f"📢 O restaurante tem {num_pedidos} clientes aguardando pagamento.")

    # Criando 3 caixas (threads)
    num_caixas = 3
    cashiers = [Caixa(cashier_id=i, order_queue=order_queue) for i in range(1, num_caixas + 1)]

    # Iniciando as threads dos caixas
    for cashier in cashiers:
        cashier.start()

    # Aguarda até que todos os pedidos sejam processados
    order_queue.join()

    # Aguarda todas as threads finalizarem
    for cashier in cashiers:
        cashier.join()

    print("🏁 Todos os clientes foram atendidos e os caixas fecharam.")

if __name__ == "__main__":
    main()
