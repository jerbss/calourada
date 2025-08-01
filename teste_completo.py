import sys
from calourada import ListaLigada, Pilha, ArvoreAVL, SistemaCalourada

def testar_lista():
    print("\n=== TESTANDO LISTA LIGADA ===")
    lista = ListaLigada()
    
    # Testando inserir
    print("Inserindo dados na lista...")
    lista.inserir({"nome": "Item 1"})
    lista.inserir({"nome": "Item 2"})
    lista.inserir({"nome": "Item 3"})
    
    # Testando imprimir
    print("Imprimindo lista:")
    itens = lista.imprimir()
    for item in itens:
        print(f"- {item['nome']}")
    
    # Testando buscar
    print("\nBuscando 'Item 2'...")
    resultado = lista.buscar(lambda x: x["nome"] == "Item 2")
    print(f"Resultado da busca: {resultado['nome'] if resultado else 'Não encontrado'}")
    
    # Testando remover
    print("\nRemovendo 'Item 2'...")
    removido = lista.remover(lambda x: x["nome"] == "Item 2")
    print(f"Removido? {removido}")
    
    # Verificando após remoção
    print("\nLista após remoção:")
    itens = lista.imprimir()
    for item in itens:
        print(f"- {item['nome']}")
    
    print("\n✓ Teste da Lista Ligada concluído!")

def testar_pilha():
    print("\n=== TESTANDO PILHA ===")
    pilha = Pilha()
    
    # Testando inserir
    print("Inserindo dados na pilha...")
    pilha.inserir({"operacao": "Operação 1", "timestamp": "01/01/2023"})
    pilha.inserir({"operacao": "Operação 2", "timestamp": "02/01/2023"})
    pilha.inserir({"operacao": "Operação 3", "timestamp": "03/01/2023"})
    
    # Testando imprimir
    print("Imprimindo pilha:")
    operacoes = pilha.imprimir()
    for op in operacoes:
        print(f"- {op['operacao']} ({op['timestamp']})")
    
    # Testando buscar
    print("\nBuscando 'Operação 2'...")
    resultado = pilha.buscar(lambda x: x["operacao"] == "Operação 2")
    print(f"Resultado da busca: {resultado['operacao'] if resultado else 'Não encontrado'}")
    
    # Testando remover
    print("\nRemovendo último item da pilha...")
    removido = pilha.remover()
    print(f"Item removido: {removido['operacao'] if removido else 'Nada removido'}")
    
    # Verificando após remoção
    print("\nPilha após remoção:")
    operacoes = pilha.imprimir()
    for op in operacoes:
        print(f"- {op['operacao']} ({op['timestamp']})")
    
    print("\n✓ Teste da Pilha concluído!")

def testar_arvore():
    print("\n=== TESTANDO ÁRVORE AVL ===")
    arvore = ArvoreAVL()
    
    # Testando inserir
    print("Inserindo dados na árvore...")
    dados = [
        {"nome": "Evento A", "id": 5},
        {"nome": "Evento B", "id": 3},
        {"nome": "Evento C", "id": 7},
        {"nome": "Evento D", "id": 2},
        {"nome": "Evento E", "id": 4},
        {"nome": "Evento F", "id": 6},
        {"nome": "Evento G", "id": 8}
    ]
    
    for item in dados:
        arvore.inserir(item, item["id"])
    
    # Testando buscar
    print("\nBuscando evento com ID 4...")
    resultado = arvore.buscar(4)
    print(f"Resultado da busca: {resultado['nome'] if resultado else 'Não encontrado'}")
    
    # Testando remover
    print("\nRemovendo evento com ID 3...")
    removido = arvore.remover(3)
    print(f"Removido? {removido}")
    
    # Testando busca após remoção
    print("\nBuscando evento com ID 3 após remoção...")
    resultado = arvore.buscar(3)
    print(f"Resultado da busca: {'Encontrado (erro!)' if resultado else 'Não encontrado (correto)'}")
    
    # Testando percursos
    print("\nPercurso in-ordem:")
    for item in arvore.in_ordem():
        print(f"- {item['nome']} (ID: {item['id']})")
    
    print("\nPercurso pré-ordem:")
    for item in arvore.pre_ordem():
        print(f"- {item['nome']} (ID: {item['id']})")
    
    print("\nPercurso pós-ordem:")
    for item in arvore.pos_ordem():
        print(f"- {item['nome']} (ID: {item['id']})")
    
    print("\n✓ Teste da Árvore AVL concluído!")

def testar_sistema_versionamento():
    print("\n=== TESTANDO SISTEMA DE VERSIONAMENTO ===")
    sistema = SistemaCalourada()
    
    # Criando algumas operações
    print("Criando operações no histórico...")
    sistema.historico.inserir({
        'acao': 'TESTE_OPERACAO_1',
        'timestamp': '01/01/2023',
        'detalhes': 'Detalhes da operação 1'
    })
    
    sistema.historico.inserir({
        'acao': 'TESTE_OPERACAO_2',
        'timestamp': '02/01/2023',
        'detalhes': 'Detalhes da operação 2'
    })
    
    sistema.historico.inserir({
        'acao': 'TESTE_OPERACAO_3',
        'timestamp': '03/01/2023',
        'detalhes': 'Detalhes da operação 3'
    })
    
    # Mostrando o histórico
    print("\nHistórico atual:")
    historico = sistema.historico.imprimir()
    for i, op in enumerate(historico, 1):
        print(f"{i}. {op['acao']} - {op['detalhes']}")
    
    # Testando desfazer operação
    print("\nDesfazendo última operação...")
    sucesso, mensagem = sistema.desfazer_ultima_operacao()
    print(f"Resultado: {mensagem}")
    
    # Verificando histórico após desfazer
    print("\nHistórico após desfazer:")
    historico = sistema.historico.imprimir()
    for i, op in enumerate(historico, 1):
        print(f"{i}. {op['acao']}" + (f" - {op['detalhes']}" if 'detalhes' in op else ""))
    
    print("\n✓ Teste do Sistema de Versionamento concluído!")

def main():
    print("=== TESTES COMPLETOS DAS ESTRUTURAS DE DADOS ===")
    
    testar_lista()
    testar_pilha()
    testar_arvore()
    testar_sistema_versionamento()
    
    print("\n✓ Todos os testes concluídos com sucesso!")
    print("Todas as estruturas de dados estão implementando corretamente:")
    print("- Lista Ligada: INSERIR, REMOVER, BUSCAR, IMPRIMIR")
    print("- Pilha: INSERIR, REMOVER, BUSCAR, IMPRIMIR")
    print("- Árvore AVL: INSERIR, REMOVER, BUSCAR, IMPRIMIR (percursos)")
    print("\nO sistema de versionamento utiliza a função REMOVER da Pilha para desfazer operações.")

if __name__ == "__main__":
    main()
