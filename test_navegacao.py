import subprocess
import time
import os

def test_interface_navegacao():
    """
    Testa a navegação básica pelos menus da interface
    """
    print("Iniciando teste de navegação pela interface...")
    
    # Inicia o programa
    proc = subprocess.Popen(
        ["python", "calourada.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    # Lista de opções a testar em sequência
    opcoes = ["3", "2", "0"]  # Listar calouradas, Buscar calourada, Sair
    
    # Navega pelas opções
    for opcao in opcoes:
        print(f"Enviando opção: {opcao}")
        proc.stdin.write(opcao + "\n")
        proc.stdin.flush()
        
        # Se não for a opção de sair, dá Enter para continuar
        if opcao != "0":
            time.sleep(1)
            proc.stdin.write("\n")
            proc.stdin.flush()
            time.sleep(1)
    
    # Aguarda o término do processo
    try:
        proc.wait(timeout=5)
        print("Programa encerrado corretamente.")
        return True
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Erro: Programa não encerrou corretamente")
        return False

if __name__ == "__main__":
    print("=== Teste de Navegação da Interface ===")
    
    success = test_interface_navegacao()
    
    if success:
        print("\n✅ Teste de navegação concluído com sucesso!")
    else:
        print("\n❌ Teste de navegação falhou.")
        
    print("\nObs: Este teste verifica apenas a navegação básica pelos menus.")
    print("Para testes mais detalhados, utilize os testes unitários em test_unitario.py")
