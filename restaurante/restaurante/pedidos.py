import queue

# Filas compartilhadas para pedidos
fila_pedidos = queue.Queue()  # Clientes fazem pedidos aqui
fila_cozinha = queue.Queue()  # Garçons levam pedidos para a cozinha
fila_prontos = queue.Queue()  # Chefes colocam pratos prontos aqui


# Escolha o modo: "FCFS" ou "SJF"
#MODO_ESCALONAMENTO = "SJF"  # ou "FCFS"

# Filas compartilhadas para pedidos
#fila_pedidos = queue.Queue()  # Clientes fazem pedidos aqui

#if MODO_ESCALONAMENTO == "SJF":
#    fila_cozinha = queue.PriorityQueue()  # Menor tempo de preparo primeiro
#else:
#    fila_cozinha = queue.Queue()  # Ordem de chegada (FCFS)

#fila_prontos = queue.Queue()  # Cozinheiros colocam pratos prontos aqui


# PARA GARÇOM 

#if MODO_ESCALONAMENTO == "SJF":
  #  fila_cozinha.put((pedido.tempo_preparo, pedido))
#else:
  #  fila_cozinha.put(pedido)


# PARA CHEF 

#  if MODO_ESCALONAMENTO == "SJF":
 #   _, pedido = fila_cozinha.get()
#else:
 #   pedido = fila_cozinha.get()