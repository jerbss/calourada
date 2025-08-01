import sys
import datetime
from calourada import SistemaCalourada

def print_separador(titulo):
    """Exibe um separador com o título"""
    print("\n" + "="*60)
    print(f"    {titulo}")
    print("="*60)

def menu_demo():
    """Menu de demonstração do sistema"""
    print_separador("🎉 DEMONSTRAÇÃO DO SISTEMA DE CALOURADA 🎉")
    
    sistema = SistemaCalourada()
    
    # Pré-carregando algumas calouradas e participantes para demonstração
    print("\n>> Pré-carregando dados de demonstração...")
    
    # Datas para calouradas (próximos 2 meses)
    hoje = datetime.datetime.now()
    datas = [
        (hoje + datetime.timedelta(days=15)).strftime("%d/%m/%Y"),
        (hoje + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
        (hoje + datetime.timedelta(days=45)).strftime("%d/%m/%Y")
    ]
    
    # Calouradas
    calouradas = [
        {
            "nome": "Acolhida de Ciência da Computação",
            "local": "Bloco 952 - CC",
            "unidade": "CC",
            "descricao": "Evento de boas-vindas para os novos alunos de CC"
        },
        {
            "nome": "Integração de Engenharias",
            "local": "Praça Verde",
            "unidade": "CT",
            "descricao": "Integração entre os cursos de engenharia"
        },
        {
            "nome": "Calourada Geral UFC",
            "local": "Centro de Convivência",
            "unidade": "CCA",
            "descricao": "Evento para todos os novos alunos da UFC"
        }
    ]
    
    # Criar calouradas
    for i, (calourada, data) in enumerate(zip(calouradas, datas)):
        sucesso, _ = sistema.criar_calourada(
            calourada["nome"],
            data,
            calourada["local"],
            calourada["unidade"],
            calourada["descricao"]
        )
        print(f"  ✓ Calourada criada: {calourada['nome']} ({i+1})")
    
    # Participantes
    participantes = [
        {"nome": "João Silva", "curso_digitado": "Ciência da Computação", "unidade_digitada": "CC", "sexo": "M", "periodo": 1},
        {"nome": "Maria Oliveira", "curso_digitado": "Estatística", "unidade_digitada": "CC", "sexo": "F", "periodo": 2},
        {"nome": "Pedro Santos", "curso_digitado": "Engenharia Civil", "unidade_digitada": "CT", "sexo": "M", "periodo": 3},
        {"nome": "Ana Costa", "curso_digitado": "Engenharia Elétrica", "unidade_digitada": "CT", "sexo": "F", "periodo": 1}
    ]
    
    # Registrar interesse dos participantes
    sistema.demonstrar_interesse(1, participantes[0]["nome"], participantes[0]["curso_digitado"], 
                                 participantes[0]["unidade_digitada"], participantes[0]["sexo"], participantes[0]["periodo"])
    sistema.demonstrar_interesse(1, participantes[1]["nome"], participantes[1]["curso_digitado"], 
                                 participantes[1]["unidade_digitada"], participantes[1]["sexo"], participantes[1]["periodo"])
    sistema.demonstrar_interesse(2, participantes[2]["nome"], participantes[2]["curso_digitado"], 
                                 participantes[2]["unidade_digitada"], participantes[2]["sexo"], participantes[2]["periodo"])
    sistema.demonstrar_interesse(2, participantes[3]["nome"], participantes[3]["curso_digitado"], 
                                 participantes[3]["unidade_digitada"], participantes[3]["sexo"], participantes[3]["periodo"])
    print("  ✓ Participantes registrados")
    
    print("\n✓ Sistema pronto para demonstração!")
    
    # Loop principal do menu
    while True:
        print_separador("MENU DE DEMONSTRAÇÃO")
        print("1. Ver Todas as Calouradas")
        print("2. Ver Detalhes de uma Calourada")
        print("3. Ver Participantes de uma Calourada")
        print("4. Demonstrar Interesse")
        print("5. Cancelar Interesse")
        print("6. Ver Histórico de Operações")
        print("7. Buscar no Histórico")
        print("8. Desfazer Última Operação")
        print("0. Sair da Demonstração")
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "0":
                print("\nFinalizando demonstração. Obrigado!")
                break
                
            elif opcao == "1":
                print("\n" + sistema.listar_calouradas())
                
            elif opcao == "2":
                print("\n=== VER DETALHES DE CALOURADA ===")
                try:
                    calourada_id = int(input("Digite o ID da calourada: ").strip())
                    detalhes = sistema.buscar_calourada(calourada_id)
                    print("\n" + detalhes)
                except ValueError:
                    print("✗ ID inválido! Digite um número.")
                    
            elif opcao == "3":
                print("\n=== VER PARTICIPANTES DE CALOURADA ===")
                try:
                    calourada_id = int(input("Digite o ID da calourada: ").strip())
                    participantes = sistema.listar_participantes(calourada_id)
                    print("\n" + participantes)
                except ValueError:
                    print("✗ ID inválido! Digite um número.")
                    
            elif opcao == "4":
                print("\n=== DEMONSTRAR INTERESSE ===")
                
                # Listar calouradas disponíveis
                print("\nCalouradas disponíveis:")
                print(sistema.listar_calouradas())
                
                try:
                    calourada_id = int(input("Digite o ID da calourada: ").strip())
                    
                    # Verificar se a calourada existe
                    calourada = sistema.eventos.buscar(calourada_id)
                    if not calourada:
                        print("✗ Calourada não encontrada!")
                        continue
                    
                    # Dados do participante
                    nome = input("\nNome: ").strip()
                    
                    print("\nUnidades acadêmicas:")
                    for sigla, info in sistema.unidades.items():
                        print(f"  {sigla} - {info['nome']}")
                    unidade = input("Unidade (sigla): ").strip().upper()
                    
                    if unidade in sistema.unidades:
                        print("\nCursos disponíveis:")
                        for i, curso in enumerate(sistema.unidades[unidade]["cursos"], 1):
                            print(f"  {i}. {curso}")
                        
                        curso_input = input("Curso (nome ou número): ").strip()
                        try:
                            idx = int(curso_input) - 1
                            if 0 <= idx < len(sistema.unidades[unidade]["cursos"]):
                                curso = sistema.unidades[unidade]["cursos"][idx]
                            else:
                                curso = curso_input
                        except ValueError:
                            curso = curso_input
                            
                        sexo = input("Sexo (M/F/O): ").strip().upper()
                        
                        try:
                            periodo = int(input("Período (1-12): ").strip())
                            
                            # Registrar interesse
                            sucesso, mensagem = sistema.demonstrar_interesse(
                                calourada_id, nome, curso, unidade, sexo, periodo
                            )
                            print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
                            
                        except ValueError:
                            print("✗ Período deve ser um número!")
                    else:
                        print(f"✗ Unidade {unidade} não encontrada!")
                        
                except ValueError:
                    print("✗ ID inválido! Digite um número.")
                    
            elif opcao == "5":
                print("\n=== CANCELAR INTERESSE ===")
                
                # Listar calouradas disponíveis
                print("\nCalouradas disponíveis:")
                print(sistema.listar_calouradas())
                
                try:
                    calourada_id = int(input("Digite o ID da calourada: ").strip())
                    
                    # Verificar se a calourada existe
                    calourada = sistema.eventos.buscar(calourada_id)
                    if not calourada:
                        print("✗ Calourada não encontrada!")
                        continue
                    
                    # Listar participantes
                    print("\n" + sistema.listar_participantes(calourada_id))
                    
                    # Se não houver participantes, voltar ao menu
                    if calourada.participantes.tamanho == 0:
                        continue
                    
                    nome = input("\nDigite o nome do participante: ").strip()
                    
                    # Cancelar interesse
                    sucesso, mensagem = sistema.cancelar_interesse(calourada_id, nome)
                    print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
                    
                except ValueError:
                    print("✗ ID inválido! Digite um número.")
                    
            elif opcao == "6":
                print("\n=== HISTÓRICO DE OPERAÇÕES ===")
                
                try:
                    limite = input("Quantas operações mostrar? (padrão 10): ").strip()
                    limite = int(limite) if limite else 10
                    print("\n" + sistema.ver_historico(limite))
                except ValueError:
                    print("\n" + sistema.ver_historico())
                    
            elif opcao == "7":
                print("\n=== BUSCAR NO HISTÓRICO ===")
                print("Tipos de busca:")
                print("1. Por tipo de ação (CRIAR_CALOURADA, DEMONSTRAR_INTERESSE, etc.)")
                print("2. Por nome de participante")
                print("3. Por ID de calourada")
                print("4. Por detalhes")
                
                tipo_opcao = input("\nEscolha o tipo de busca (1-4): ").strip()
                
                tipo_busca = None
                if tipo_opcao == "1":
                    tipo_busca = "acao"
                    print("\nAções disponíveis:")
                    print("- CRIAR_CALOURADA")
                    print("- DEMONSTRAR_INTERESSE")
                    print("- CANCELAR_INTERESSE")
                    print("- DESFAZER")
                elif tipo_opcao == "2":
                    tipo_busca = "participante"
                elif tipo_opcao == "3":
                    tipo_busca = "calourada_id"
                elif tipo_opcao == "4":
                    tipo_busca = "detalhes"
                else:
                    print("✗ Opção inválida!")
                    continue
                
                termo = input(f"\nDigite o termo para buscar por {tipo_busca}: ").strip()
                if termo:
                    resultado = sistema.buscar_no_historico(termo, tipo_busca)
                    print("\n" + resultado)
                else:
                    print("✗ Termo de busca não pode ser vazio!")
                    
            elif opcao == "8":
                print("\n=== DESFAZER ÚLTIMA OPERAÇÃO ===")
                
                # Mostrar última operação
                print("\nÚltima operação:")
                print(sistema.ver_historico(1))
                
                confirmacao = input("\nDeseja desfazer esta operação? (s/N): ").strip().lower()
                if confirmacao == "s":
                    sucesso, mensagem = sistema.desfazer_ultima_operacao()
                    print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
                else:
                    print("\n✓ Operação cancelada")
                    
            else:
                print("\n✗ Opção inválida! Tente novamente.")
                
            # Pausa para o usuário ler o resultado
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nDemonstração encerrada.")
            break
        except Exception as e:
            print(f"\n✗ Erro inesperado: {str(e)}")
            print("Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    if 'win' in sys.platform:
        # Configuração para Windows
        import locale
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    
    print("\nBem-vindo ao sistema de demonstração da Calourada!")
    print("Este programa permite testar todas as funcionalidades do sistema.")
    menu_demo()
