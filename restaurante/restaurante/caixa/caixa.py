import threading
import time
import queue

class Caixa(threading.Thread):
    def __init__(self, cashier_id, order_queue):
        threading.Thread.__init__(self)
        self.cashier_id = cashier_id
        self.order_queue = order_queue

    def run(self):
        while True:
            try:
                order = self.order_queue.get(timeout=1)  # Aguardando um pedido
                print(f"Cashier {self.cashier_id} está processando o pedido {order}")
                time.sleep(2)  # Simulando o processamento do pedido
                print(f"Cashier {self.cashier_id} completou a ação {order}")
                self.order_queue.task_done()
            except queue.Empty:
                print(f"Caixa {self.cashier_id} não achou pedidos.")
                break

def main():
    order_queue = queue.Queue()

    # Criando 10 pedidos
    for order_id in range(10):
        order_queue.put(order_id)

    # Criando 3 caixas
    cashiers = [Caixa(cashier_id=i, order_queue=order_queue) for i in range(3)]
    for cashier in cashiers:
        cashier.start()

    # Esperando todos os pedidos serem processados
    order_queue.join()

    # Esperando todos os caixas terminarem
    for cashier in cashiers:
        cashier.join()

    print("All orders have been processed.")

if __name__ == "__main__":
    main()