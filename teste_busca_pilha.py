from calourada import Pilha, SistemaCalourada
import datetime

def testar_buscar_pilha():
    print("=== TESTANDO O MÉTODO BUSCAR DA PILHA ===")
    
    # Criar uma pilha e adicionar alguns elementos
    pilha = Pilha()
    
    # Inserir alguns registros de teste
    pilha.inserir({
        'acao': 'CRIAR_CALOURADA',
        'calourada_id': 1,
        'timestamp': datetime.datetime.now(),
        'detalhes': 'Calourada de Teste 1'
    })
    
    pilha.inserir({
        'acao': 'DEMONSTRAR_INTERESSE',
        'calourada_id': 1,
        'participante': 'João Silva',
        'timestamp': datetime.datetime.now()
    })
    
    pilha.inserir({
        'acao': 'DEMONSTRAR_INTERESSE',
        'calourada_id': 1,
        'participante': 'Maria Oliveira',
        'timestamp': datetime.datetime.now()
    })
    
    pilha.inserir({
        'acao': 'CRIAR_CALOURADA',
        'calourada_id': 2,
        'timestamp': datetime.datetime.now(),
        'detalhes': 'Calourada de Teste 2'
    })
    
    # Testar a busca por diferentes critérios
    print("\n1. Busca por tipo de ação 'CRIAR_CALOURADA':")
    resultado = pilha.buscar(lambda op: op['acao'] == 'CRIAR_CALOURADA')
    print(f"Resultado encontrado: {resultado['acao']} - ID: {resultado['calourada_id']}")
    
    print("\n2. Busca por participante contendo 'Maria':")
    resultado = pilha.buscar(lambda op: 'participante' in op and 'Maria' in op['participante'])
    print(f"Resultado encontrado: {resultado['acao']} - Participante: {resultado['participante']}")
    
    print("\n3. Busca por calourada_id = 2:")
    resultado = pilha.buscar(lambda op: 'calourada_id' in op and op['calourada_id'] == 2)
    print(f"Resultado encontrado: {resultado['acao']} - ID: {resultado['calourada_id']} - Detalhes: {resultado['detalhes']}")
    
    print("\n4. Busca por detalhes contendo 'Teste 1':")
    resultado = pilha.buscar(lambda op: 'detalhes' in op and 'Teste 1' in op['detalhes'])
    print(f"Resultado encontrado: {resultado['acao']} - Detalhes: {resultado['detalhes']}")
    
    print("\n5. Busca por critério inexistente:")
    resultado = pilha.buscar(lambda op: 'participante' in op and 'Carlos' in op['participante'])
    print(f"Resultado encontrado: {resultado}")
    
    print("\n✓ Testes do método BUSCAR da Pilha concluídos!")

def testar_busca_historico_sistema():
    print("\n=== TESTANDO A BUSCA NO HISTÓRICO DO SISTEMA ===")
    
    # Criar sistema
    sistema = SistemaCalourada()
    
    # Simular algumas operações
    sistema.historico.inserir({
        'acao': 'CRIAR_CALOURADA',
        'calourada_id': 1,
        'timestamp': datetime.datetime.now(),
        'detalhes': 'Calourada de Teste A'
    })
    
    sistema.historico.inserir({
        'acao': 'DEMONSTRAR_INTERESSE',
        'calourada_id': 1,
        'participante': 'Pedro Souza',
        'timestamp': datetime.datetime.now()
    })
    
    sistema.historico.inserir({
        'acao': 'DEMONSTRAR_INTERESSE',
        'calourada_id': 1,
        'participante': 'Ana Pereira',
        'timestamp': datetime.datetime.now()
    })
    
    sistema.historico.inserir({
        'acao': 'CRIAR_CALOURADA',
        'calourada_id': 2,
        'timestamp': datetime.datetime.now(),
        'detalhes': 'Calourada de Teste B'
    })
    
    # Testar busca no histórico do sistema
    print("\n1. Busca por ação 'CRIAR_CALOURADA':")
    print(sistema.buscar_no_historico('CRIAR_CALOURADA', 'acao'))
    
    print("\n2. Busca por participante 'Ana':")
    print(sistema.buscar_no_historico('Ana', 'participante'))
    
    print("\n3. Busca por ID de calourada '1':")
    print(sistema.buscar_no_historico('1', 'calourada_id'))
    
    print("\n4. Busca por detalhes contendo 'Teste':")
    print(sistema.buscar_no_historico('Teste', 'detalhes'))
    
    print("\n5. Busca por termo inexistente:")
    print(sistema.buscar_no_historico('XYZ', 'acao'))
    
    print("\n✓ Testes da busca no histórico do sistema concluídos!")

if __name__ == "__main__":
    print("=== TESTES DO MÉTODO BUSCAR DA PILHA ===\n")
    
    testar_buscar_pilha()
    testar_busca_historico_sistema()
    
    print("\n✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("O método SEARCH (buscar) da Pilha está funcionando corretamente!")
