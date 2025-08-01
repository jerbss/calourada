import os
import sys
import subprocess
import time
from datetime import datetime, timedelta

class AutomatedTest:
    def __init__(self):
        self.proc = None
        self.log_file = "test_results.log"
        self.test_calourada_name = f"Teste Automatizado {datetime.now().strftime('%H:%M:%S')}"
        self.test_results = []
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.test_results.append(log_entry)
    
    def write_log(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.test_results))
        self.log(f"Log gravado em {self.log_file}")
    
    def start_process(self):
        self.log("Iniciando processo do sistema de calouradas")
        self.proc = subprocess.Popen(
            ["python", "calourada.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        time.sleep(1)  # Aguarda inicialização
        
    def send_input(self, input_text, delay=0.5):
        self.log(f"Enviando entrada: {input_text}")
        self.proc.stdin.write(input_text + "\n")
        self.proc.stdin.flush()
        time.sleep(delay)
        
    def read_output(self):
        output = ""
        while self.proc.poll() is None:
            # Verifica se há dados disponíveis para leitura
            if self.proc.stdout.readable():
                line = self.proc.stdout.readline()
                if not line:
                    break
                output += line
            else:
                break
        return output
        
    def close(self):
        if self.proc and self.proc.poll() is None:
            self.log("Encerrando processo")
            try:
                self.proc.stdin.write("0\n")  # Tenta sair normalmente
                self.proc.stdin.flush()
                time.sleep(0.5)
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except:
                self.proc.kill()
    
    def test_criar_calourada(self):
        self.log("=== Teste: Criar Calourada ===")
        self.send_input("1")  # Menu: Criar Calourada
        
        # Preenche os dados da calourada
        self.send_input(self.test_calourada_name)  # Nome da calourada
        
        # Data futura (30 dias a partir de hoje)
        future_date = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        self.send_input(future_date)  # Data
        
        self.send_input("Local de Teste")  # Local
        self.send_input("CC")  # Unidade
        self.send_input("Descrição de teste automatizado")  # Descrição
        self.send_input("")  # Continuar
        return True
        
    def test_buscar_calourada(self):
        self.log("=== Teste: Buscar Calourada ===")
        self.send_input("2")  # Menu: Buscar Calourada
        self.send_input("1")  # ID da calourada (assumindo que é a primeira)
        self.send_input("")  # Continuar
        return True
        
    def test_listar_calouradas(self):
        self.log("=== Teste: Listar Calouradas ===")
        self.send_input("3")  # Menu: Listar Calouradas
        self.send_input("")  # Continuar
        return True
        
    def test_demonstrar_interesse(self):
        self.log("=== Teste: Demonstrar Interesse ===")
        self.send_input("5")  # Menu: Demonstrar Interesse
        self.send_input("1")  # ID da calourada (assumindo que é a primeira)
        
        # Dados do participante
        self.send_input("Participante Teste")  # Nome
        self.send_input("CC")  # Unidade
        self.send_input("Ciência da Computação")  # Curso
        self.send_input("M")  # Sexo
        self.send_input("5")  # Período
        self.send_input("")  # Continuar
        return True
        
    def test_listar_participantes(self):
        self.log("=== Teste: Listar Participantes ===")
        self.send_input("7")  # Menu: Listar Participantes
        self.send_input("1")  # ID da calourada (assumindo que é a primeira)
        self.send_input("")  # Continuar
        return True
        
    def test_cancelar_interesse(self):
        self.log("=== Teste: Cancelar Interesse ===")
        self.send_input("6")  # Menu: Cancelar Interesse
        self.send_input("1")  # ID da calourada (assumindo que é a primeira)
        self.send_input("1")  # Número do participante (assumindo que é o primeiro)
        self.send_input("")  # Continuar
        return True
        
    def test_ver_historico(self):
        self.log("=== Teste: Ver Histórico ===")
        self.send_input("8")  # Menu: Ver Histórico
        self.send_input("5")  # Mostrar 5 últimas operações
        self.send_input("")  # Continuar
        return True
        
    def test_pesquisar_historico(self):
        self.log("=== Teste: Pesquisar no Histórico ===")
        self.send_input("9")  # Menu: Pesquisar no Histórico
        self.send_input("1")  # Tipo de busca: ação
        self.send_input("CRIAR")  # Termo de busca
        self.send_input("")  # Continuar
        return True
        
    def test_remover_calourada(self):
        self.log("=== Teste: Remover Calourada ===")
        self.send_input("4")  # Menu: Remover Calourada
        self.send_input("1")  # ID da calourada (assumindo que é a primeira)
        self.send_input("s")  # Confirmar remoção
        self.send_input("")  # Continuar
        return True
        
    def run_all_tests(self):
        try:
            self.start_process()
            
            # Executa os testes em sequência
            tests = [
                self.test_criar_calourada,
                self.test_buscar_calourada,
                self.test_listar_calouradas,
                self.test_demonstrar_interesse,
                self.test_listar_participantes,
                self.test_ver_historico,
                self.test_pesquisar_historico,
                self.test_cancelar_interesse,
                self.test_remover_calourada
            ]
            
            success_count = 0
            for test in tests:
                try:
                    if test():
                        success_count += 1
                except Exception as e:
                    self.log(f"Erro no teste {test.__name__}: {str(e)}")
            
            self.log(f"===== Resumo dos Testes =====")
            self.log(f"Total de testes: {len(tests)}")
            self.log(f"Testes bem-sucedidos: {success_count}")
            self.log(f"Testes com falha: {len(tests) - success_count}")
            
        except Exception as e:
            self.log(f"Erro no teste automatizado: {str(e)}")
        finally:
            self.close()
            self.write_log()

if __name__ == "__main__":
    print("Iniciando testes automatizados do Sistema de Calouradas")
    tester = AutomatedTest()
    tester.run_all_tests()
    print("Testes concluídos. Verifique o arquivo test_results.log para detalhes.")
