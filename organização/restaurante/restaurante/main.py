from clientes.cliente import Cliente
from garcons.garcom import Garcom
from chefes.chefe import Chefe
from garcons.servico import Servico
from caixa.caixa import Caixa

# Criando clientes
clientes = [Cliente(f"Cliente {i}") for i in range(5)]

# Criando garçons e chefes
garcons = [Garcom() for _ in range(2)]
chefes = [Chefe() for _ in range(2)]
servico = Servico()

# Iniciando threads
for cliente in clientes:
    cliente.start()

for garcom in garcons:
    garcom.start()

for chefe in chefes:
    chefe.start()

servico.start()

# Esperando todos os clientes terminarem
for cliente in clientes:
    cliente.join()

print("🏁 O restaurante encerrou as operações.")
