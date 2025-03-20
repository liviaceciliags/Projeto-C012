import queue

# Filas compartilhadas para pedidos
fila_pedidos = queue.Queue()  # Clientes fazem pedidos aqui
fila_cozinha = queue.Queue()  # Garçons levam pedidos para a cozinha
fila_prontos = queue.Queue()  # Chefes colocam pratos prontos aqui
