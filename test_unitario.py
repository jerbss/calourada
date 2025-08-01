import unittest
import datetime
import os
import sys
from io import StringIO
from unittest.mock import patch

# Importa as classes do sistema
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calourada import SistemaCalourada, Calourada, Participante

class TestSistemaCalourada(unittest.TestCase):
    
    def setUp(self):
        # Configura um sistema limpo para cada teste
        self.sistema = SistemaCalourada()
        # Data futura para testes
        self.data_futura = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d/%m/%Y")
    
    def test_criar_calourada(self):
        """Testa a criação de uma calourada"""
        nome = "Calourada de Teste"
        local = "Local de Teste"
        unidade = "CC"
        descricao = "Descrição de teste"
        
        # Testa criação com sucesso
        sucesso, mensagem = self.sistema.criar_calourada(nome, self.data_futura, local, unidade, descricao)
        self.assertTrue(sucesso)
        self.assertIn("criada com sucesso", mensagem)
        
        # Verifica se foi cadastrada corretamente
        calouradas = self.sistema.eventos.in_ordem()
        self.assertEqual(len(calouradas), 1)
        self.assertEqual(calouradas[0].nome, nome)
        self.assertEqual(calouradas[0].local, local)
        self.assertEqual(calouradas[0].unidade_organizadora, unidade)
        self.assertEqual(calouradas[0].descricao, descricao)
    
    def test_buscar_calourada(self):
        """Testa a busca de uma calourada por ID"""
        # Cria uma calourada para teste
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        
        # Testa busca com ID existente
        resultado = self.sistema.buscar_calourada(1)
        self.assertIn("Calourada Teste", resultado)
        
        # Testa busca com ID inexistente
        resultado = self.sistema.buscar_calourada(999)
        self.assertEqual(resultado, "Calourada não encontrada")
    
    def test_demonstrar_interesse(self):
        """Testa o registro de interesse em uma calourada"""
        # Cria uma calourada para teste
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        
        # Testa demonstrar interesse com sucesso
        sucesso, mensagem = self.sistema.demonstrar_interesse(1, "Participante Teste", "Ciência da Computação", "CC", "M", "5")
        self.assertTrue(sucesso)
        self.assertIn("registrado com sucesso", mensagem)
        
        # Verifica se o participante foi registrado
        calourada = self.sistema.eventos.buscar(1)
        self.assertEqual(calourada.participantes.tamanho, 1)
        
        # Testa demonstrar interesse duplicado (mesmo nome)
        sucesso, mensagem = self.sistema.demonstrar_interesse(1, "Participante Teste", "Ciência da Computação", "CC", "M", "5")
        self.assertFalse(sucesso)
        self.assertIn("já demonstrou interesse", mensagem)
    
    def test_cancelar_interesse(self):
        """Testa o cancelamento de interesse em uma calourada"""
        # Cria uma calourada e registra um participante
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        self.sistema.demonstrar_interesse(1, "Participante Teste", "Ciência da Computação", "CC", "M", "5")
        
        # Testa cancelar interesse com sucesso
        sucesso, mensagem = self.sistema.cancelar_interesse(1, "Participante Teste")
        self.assertTrue(sucesso)
        self.assertIn("cancelado com sucesso", mensagem)
        
        # Verifica se o participante foi removido
        calourada = self.sistema.eventos.buscar(1)
        self.assertEqual(calourada.participantes.tamanho, 0)
        
        # Testa cancelar interesse de participante inexistente
        sucesso, mensagem = self.sistema.cancelar_interesse(1, "Inexistente")
        self.assertFalse(sucesso)
        self.assertIn("não encontrado", mensagem)
    
    def test_remover_calourada(self):
        """Testa a remoção de uma calourada"""
        # Cria uma calourada para teste
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        
        # Verifica que foi criada
        self.assertEqual(len(self.sistema.eventos.in_ordem()), 1)
        
        # Testa remover calourada com sucesso
        sucesso, mensagem = self.sistema.remover_calourada(1)
        self.assertTrue(sucesso)
        self.assertIn("removida com sucesso", mensagem)
        
        # Verifica que foi removida
        self.assertEqual(len(self.sistema.eventos.in_ordem()), 0)
        
        # Testa remover calourada inexistente
        sucesso, mensagem = self.sistema.remover_calourada(999)
        self.assertFalse(sucesso)
        self.assertIn("não encontrada", mensagem)
    
    def test_historico_operacoes(self):
        """Testa o registro de operações no histórico"""
        # Realiza várias operações
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        self.sistema.demonstrar_interesse(1, "Participante Teste", "Ciência da Computação", "CC", "M", "5")
        self.sistema.cancelar_interesse(1, "Participante Teste")
        
        # Verifica o tamanho do histórico
        self.assertEqual(self.sistema.historico.tamanho, 3)
        
        # Testa visualizar histórico
        resultado = self.sistema.ver_historico()
        self.assertIn("CRIAR_CALOURADA", resultado)
        self.assertIn("DEMONSTRAR_INTERESSE", resultado)
        self.assertIn("CANCELAR_INTERESSE", resultado)
        
        # Testa buscar no histórico
        resultado = self.sistema.buscar_no_historico("CRIAR", "acao")
        self.assertIn("CRIAR_CALOURADA", resultado)
        self.assertNotIn("CANCELAR_INTERESSE", resultado)
    
    def test_desfazer_ultima_operacao(self):
        """Testa desfazer a última operação"""
        # Cria uma calourada para teste
        self.sistema.criar_calourada("Calourada Teste", self.data_futura, "Local", "CC")
        
        # Desfaz a criação
        sucesso, mensagem = self.sistema.desfazer_ultima_operacao()
        self.assertTrue(sucesso)
        self.assertIn("removida ao desfazer", mensagem)  # Mensagem real retornada pelo método
        
        # Verifica que a calourada foi removida ao desfazer
        self.assertEqual(len(self.sistema.eventos.in_ordem()), 0)
        
        # Verifica que operação de desfazer foi registrada no histórico
        self.assertEqual(self.sistema.historico.tamanho, 1)
        historico = self.sistema.historico.imprimir()[0]
        self.assertEqual(historico['acao'], 'DESFAZER')
    
    def test_normalizar_texto(self):
        """Testa a normalização de texto para buscas flexíveis"""
        texto_original = "Ciência da Computação"
        texto_normalizado = self.sistema.normalizar_texto(texto_original)
        self.assertEqual(texto_normalizado, "ciencia da computacao")
        
        # Teste com acentos e maiúsculas variadas
        texto_original = "EngENHaria de TelecoMUNicaçÕes"
        texto_normalizado = self.sistema.normalizar_texto(texto_original)
        self.assertEqual(texto_normalizado, "engenharia de telecomunicacoes")
    
    def test_busca_flexivel_unidade(self):
        """Testa a busca flexível de unidades acadêmicas"""
        # Teste com sigla exata
        unidade = self.sistema.buscar_unidade_flexivel("CC")
        self.assertEqual(unidade, "CC")
        
        # Teste com nome completo
        unidade = self.sistema.buscar_unidade_flexivel("Centro de Ciências")
        self.assertEqual(unidade, "CC")
        
        # Teste com nome flexível (sem acentos, maiúsculas variadas)
        unidade = self.sistema.buscar_unidade_flexivel("centro de ciencias")
        self.assertEqual(unidade, "CC")
        
        # Teste com unidade inexistente
        unidade = self.sistema.buscar_unidade_flexivel("Inexistente")
        self.assertIsNone(unidade)
    
    def test_busca_flexivel_curso(self):
        """Testa a busca flexível de cursos"""
        # Teste com nome exato
        curso = self.sistema.buscar_curso_flexivel("Ciência da Computação", "CC")
        self.assertEqual(curso, "Ciência da Computação")
        
        # Teste com nome flexível (sem acentos, maiúsculas variadas)
        curso = self.sistema.buscar_curso_flexivel("ciencia da computacao", "CC")
        self.assertEqual(curso, "Ciência da Computação")
        
        # Teste com curso inexistente
        curso = self.sistema.buscar_curso_flexivel("Curso Inexistente", "CC")
        self.assertIsNone(curso)

if __name__ == "__main__":
    print("Iniciando testes unitários do Sistema de Calouradas")
    unittest.main()
