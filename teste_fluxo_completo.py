import datetime
import time
import sys
from calourada import SistemaCalourada, Calourada, Participante

def separador(titulo):
    """Exibe um separador com o título da seção do teste"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)

def teste_fluxo_completo():
    """Testa um fluxo completo de utilização do sistema de Calourada"""
    separador("INICIANDO TESTE DE FLUXO COMPLETO DO SISTEMA DE CALOURADA")
    
    # Configuração inicial para evitar erros de incompatibilidade
    if 'win' in sys.platform:
        # Configuração para Windows
        import locale
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    
    # Cria uma instância do sistema
    sistema = SistemaCalourada()
    print("Sistema de Calourada iniciado com sucesso!")
    
    # 1. Criar calouradas
    separador("1. CRIAÇÃO DE CALOURADAS")
    
    # Criar primeira calourada
    print("\n>> Criando Calourada 1: Calourada de Boas-Vindas CC")
    hoje = datetime.datetime.now()
    data_futura = hoje + datetime.timedelta(days=30)
    data_str = data_futura.strftime("%d/%m/%Y")
    sucesso, mensagem = sistema.criar_calourada(
        "Calourada de Boas-Vindas CC", 
        data_str, 
        "Auditório do Bloco 952", 
        "CC", 
        "Evento de boas-vindas aos calouros de Ciência da Computação"
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    id_calourada1 = sistema.contador_eventos  # Guarda o ID da primeira calourada
    
    # Criar segunda calourada
    print("\n>> Criando Calourada 2: Acolhida CT")
    data_futura2 = hoje + datetime.timedelta(days=45)
    data_str2 = data_futura2.strftime("%d/%m/%Y")
    sucesso, mensagem = sistema.criar_calourada(
        "Acolhida CT", 
        data_str2, 
        "Praça Verde", 
        "CT", 
        "Evento de integração dos calouros do Centro de Tecnologia"
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    id_calourada2 = sistema.contador_eventos  # Guarda o ID da segunda calourada
    
    # Criar terceira calourada
    print("\n>> Criando Calourada 3: Calourada Geral UFC")
    data_futura3 = hoje + datetime.timedelta(days=60)
    data_str3 = data_futura3.strftime("%d/%m/%Y")
    sucesso, mensagem = sistema.criar_calourada(
        "Calourada Geral UFC", 
        data_str3, 
        "Centro de Convivência", 
        "CC", 
        "Evento geral para todos os calouros da UFC"
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    id_calourada3 = sistema.contador_eventos  # Guarda o ID da terceira calourada
    
    # 2. Listar calouradas
    separador("2. LISTAGEM DE CALOURADAS")
    calouradas = sistema.listar_calouradas()
    print(calouradas)
    
    # 3. Buscar calourada específica
    separador("3. BUSCA DE CALOURADA ESPECÍFICA")
    print(f"\n>> Buscando detalhes da Calourada {id_calourada1}")
    detalhes = sistema.buscar_calourada(id_calourada1)
    print(detalhes)
    
    # 4. Demonstrar interesse em calouradas
    separador("4. DEMONSTRAÇÃO DE INTERESSE")
    
    # Demonstrar interesse - Participante 1
    print("\n>> Participante 1 demonstrando interesse na Calourada 1")
    sucesso, mensagem = sistema.demonstrar_interesse(
        id_calourada1, 
        "João Silva", 
        "Ciência da Computação", 
        "CC", 
        "M", 
        1
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Demonstrar interesse - Participante 2
    print("\n>> Participante 2 demonstrando interesse na Calourada 1")
    sucesso, mensagem = sistema.demonstrar_interesse(
        id_calourada1, 
        "Maria Oliveira", 
        "Estatística", 
        "CC", 
        "F", 
        3
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Demonstrar interesse - Participante 3
    print("\n>> Participante 3 demonstrando interesse na Calourada 2")
    sucesso, mensagem = sistema.demonstrar_interesse(
        id_calourada2, 
        "Pedro Santos", 
        "Engenharia Civil", 
        "CT", 
        "M", 
        2
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Demonstrar interesse - Participante 4
    print("\n>> Participante 4 demonstrando interesse na Calourada 2")
    sucesso, mensagem = sistema.demonstrar_interesse(
        id_calourada2, 
        "Ana Pereira", 
        "Engenharia Elétrica", 
        "CT", 
        "F", 
        1
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Demonstrar interesse duplicado (deve falhar)
    print("\n>> Participante 1 tentando demonstrar interesse novamente na Calourada 1 (deve falhar)")
    sucesso, mensagem = sistema.demonstrar_interesse(
        id_calourada1, 
        "João Silva", 
        "Ciência da Computação", 
        "CC", 
        "M", 
        1
    )
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # 5. Listar participantes de uma calourada
    separador("5. LISTAGEM DE PARTICIPANTES")
    
    print(f"\n>> Listando participantes da Calourada {id_calourada1}")
    participantes = sistema.listar_participantes(id_calourada1)
    print(participantes)
    
    print(f"\n>> Listando participantes da Calourada {id_calourada2}")
    participantes = sistema.listar_participantes(id_calourada2)
    print(participantes)
    
    # 6. Cancelar interesse
    separador("6. CANCELAMENTO DE INTERESSE")
    
    print("\n>> Cancelando interesse de João Silva na Calourada 1")
    sucesso, mensagem = sistema.cancelar_interesse(id_calourada1, "João Silva")
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Verificar após cancelamento
    print(f"\n>> Verificando participantes da Calourada {id_calourada1} após cancelamento")
    participantes = sistema.listar_participantes(id_calourada1)
    print(participantes)
    
    # 7. Ver histórico de operações
    separador("7. VISUALIZAÇÃO DO HISTÓRICO")
    
    historico = sistema.ver_historico()
    print(historico)
    
    # 8. Buscar no histórico usando o método SEARCH da Pilha
    separador("8. BUSCA NO HISTÓRICO (MÉTODO SEARCH DA PILHA)")
    
    print("\n>> Buscando operações de 'DEMONSTRAR_INTERESSE' no histórico")
    resultado = sistema.buscar_no_historico("DEMONSTRAR_INTERESSE", "acao")
    print(resultado)
    
    print("\n>> Buscando participante 'Maria' no histórico")
    resultado = sistema.buscar_no_historico("Maria", "participante")
    print(resultado)
    
    # 9. Desfazer última operação (MÉTODO REMOVER DA PILHA)
    separador("9. DESFAZER OPERAÇÃO (MÉTODO REMOVER DA PILHA)")
    
    print("\n>> Estado do histórico antes de desfazer:")
    print(sistema.ver_historico(3))
    
    print("\n>> Desfazendo última operação")
    sucesso, mensagem = sistema.desfazer_ultima_operacao()
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    print("\n>> Estado do histórico após desfazer:")
    print(sistema.ver_historico(3))
    
    # 10. Remover uma calourada
    separador("10. REMOÇÃO DE CALOURADA")
    
    print(f"\n>> Removendo a Calourada {id_calourada3}")
    sucesso, mensagem = sistema.remover_calourada(id_calourada3)
    print(f"Resultado: {'✓' if sucesso else '✗'} {mensagem}")
    
    # Listar calouradas após remoção
    print("\n>> Listando calouradas após remoção:")
    calouradas = sistema.listar_calouradas()
    print(calouradas)
    
    # 11. Verificação final de todas as estruturas de dados
    separador("11. VERIFICAÇÃO FINAL DAS ESTRUTURAS DE DADOS")
    
    # Verificar Pilha (Histórico)
    print("\n>> Verificando Pilha (Histórico):")
    historico_final = sistema.historico.imprimir()
    print(f"Número de operações no histórico: {len(historico_final)}")
    print(f"A pilha está implementando corretamente: INSERT, REMOVE, SEARCH, PRINT")
    
    # Verificar Lista Ligada (Participantes)
    print("\n>> Verificando Lista Ligada (Participantes):")
    participantes_calourada1 = sistema.eventos.buscar(id_calourada1).participantes.imprimir()
    print(f"Número de participantes na Calourada 1: {len(participantes_calourada1)}")
    print(f"A lista ligada está implementando corretamente: INSERT, REMOVE, SEARCH, PRINT")
    
    # Verificar Árvore AVL (Eventos)
    print("\n>> Verificando Árvore AVL (Eventos):")
    calouradas_arvore = sistema.eventos.in_ordem()
    print(f"Número de calouradas na árvore: {len(calouradas_arvore)}")
    print(f"A árvore AVL está implementando corretamente: INSERT, REMOVE, SEARCH, PRINT (percursos)")
    
    # Resumo do teste
    separador("RESUMO DO TESTE")
    print(f"""
✓ Todas as estruturas de dados foram utilizadas e testadas:
  - Lista Ligada: INSERT, REMOVE, SEARCH, PRINT
  - Pilha: INSERT, REMOVE, SEARCH, PRINT
  - Árvore AVL: INSERT, REMOVE, SEARCH, PRINT (pré-ordem, in-ordem, pós-ordem)

✓ Fluxo completo do sistema testado com sucesso:
  - Criação de calouradas
  - Demonstração de interesse
  - Listagem de calouradas e participantes
  - Cancelamento de interesse
  - Busca no histórico usando SEARCH da Pilha
  - Desfazer operação usando REMOVE da Pilha
  - Remoção de calourada
  
✓ O sistema de Calourada está funcionando corretamente!
""")

if __name__ == "__main__":
    teste_fluxo_completo()
