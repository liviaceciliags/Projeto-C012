import time
from restaurante.core.restaurante import Restaurante
from restaurante.core.chef import Chef
from restaurante.core.garcom import Garcon
from restaurante.core.cliente import Cliente
from restaurante.core.caixa import Caixa
from restaurante.models.configuracao import ConfiguracaoRestaurante
from restaurante.utils.filas import FilaPedidos, FilaPedidosProntos, FilaChamados, FilaCaixa

def main():
    # Configuração
    config = ConfiguracaoRestaurante(
        numeroMesas=5,
        numeroGarcons=5,
        numeroChefs=3,
        numeroCaixas=2,
        tempoPreparoPedido=2,
        tempoComerCliente=0.3,
        tempoProcessamentoPagamento=0.05
    )
    print(f"🏨 Iniciando Restaurante com Configuração: {config}\n")
    
    # Criação das filas compartilhadas
    fila_chamados = FilaChamados()
    fila_pedidos = FilaPedidos()
    fila_prontos = FilaPedidosProntos()
    fila_caixa = FilaCaixa()
    
    # Inicializa o restaurante com capacidade de gerenciar mesas
    restaurante = Restaurante(config)
    
    # Cria funcionários
    chefs = [
        Chef(i, fila_pedidos, fila_prontos, config) 
        for i in range(1, config.numeroChefs + 1)
        ]
    
    garcons = [
        Garcon(i, fila_chamados, fila_pedidos, fila_prontos) 
        for i in range(1, config.numeroGarcons + 1)
        ]
    
    caixa = [
        Caixa(i, fila_caixa, config) 
        for i in range(1, config.numeroCaixas + 1)
        ]
    
    # Criação de clientes
    clientes = [
        Cliente(i, restaurante, fila_chamados, fila_caixa, config) 
        for i in range(1, 51)
        ]
    
    # Inicia threads
    start_time = time.time()
    for c in chefs: c.start()
    for g in garcons: g.start()
    for cx in caixa: cx.start()
    for cl in clientes: cl.start()

    # Monitoramento
    for cl in clientes: cl.join()  # Aguarda término de todos clientes
    
    
    # Encerra threads
    for c in chefs: c.parar()
    for g in garcons: g.parar()
    for cx in caixa: cx.parar()

    # Mostra tempo de execução
    print("\n=== RELATÓRIO FINAL ===")
    print(f"Clientes atendidos: {restaurante.clientes_atendidos}")
    print(f"Tempo total: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
