#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Automatizado para o Sistema de Calouradas
Testa todas as funcionalidades das estruturas de dados implementadas.
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

# Importa as classes do sistema
from calourada_alt import (
    Participante, Calourada, ListaLigada, Fila, Pilha, ArvoreAVL,
    menu_gerenciar_calourada
)

class TesteSistemaCalouradas:
    """Classe para automatizar testes do sistema de calouradas."""
    
    def __init__(self):
        self.resultados = []
        self.teste_numero = 0
        
    def log_resultado(self, nome_teste, sucesso, detalhes=""):
        """Registra o resultado de um teste."""
        self.teste_numero += 1
        status = "[PASSOU]" if sucesso else "[FALHOU]"
        self.resultados.append(f"Teste {self.teste_numero}: {nome_teste} - {status}")
        if detalhes:
            self.resultados.append(f"   Detalhes: {detalhes}")
        print(f"Teste {self.teste_numero}: {nome_teste} - {status}")
        if detalhes:
            print(f"   Detalhes: {detalhes}")
    
    def teste_lista_ligada(self):
        """Testa todas as operações da Lista Ligada."""
        print("\n>> TESTANDO LISTA LIGADA...")
        lista = ListaLigada()
        
        # Teste 1: Inserção
        lista.inserir(Participante("João"))
        lista.inserir(Participante("Maria"))
        lista.inserir(Participante("Pedro"))
        resultado = lista.imprimir()
        sucesso = "Pedro" in resultado and "Maria" in resultado and "João" in resultado
        self.log_resultado("Lista - Inserção", sucesso, f"Resultado: {resultado}")
        
        # Teste 2: Busca existente
        encontrado = lista.buscar("maria")
        sucesso = encontrado is not None and encontrado.nome == "Maria"
        self.log_resultado("Lista - Busca (existente)", sucesso, f"Encontrado: {encontrado}")
        
        # Teste 3: Busca não existente
        nao_encontrado = lista.buscar("Carlos")
        sucesso = nao_encontrado is None
        self.log_resultado("Lista - Busca (não existente)", sucesso, f"Resultado: {nao_encontrado}")
        
        # Teste 4: Remoção existente
        removido = lista.remover("Maria")
        sucesso = removido and "Maria" not in lista.imprimir()
        self.log_resultado("Lista - Remoção (existente)", sucesso, f"Removido: {removido}")
        
        # Teste 5: Remoção não existente
        nao_removido = lista.remover("Carlos")
        sucesso = not nao_removido
        self.log_resultado("Lista - Remoção (não existente)", sucesso, f"Resultado: {nao_removido}")
    
    def teste_fila(self):
        """Testa todas as operações da Fila."""
        print("\n>> TESTANDO FILA...")
        fila = Fila()
        
        # Teste 1: Inserção
        fila.inserir(Participante("Ana"))
        fila.inserir(Participante("Bruno"))
        fila.inserir(Participante("Carlos"))
        resultado = fila.imprimir()
        sucesso = "Ana" in resultado and "Bruno" in resultado and "Carlos" in resultado
        self.log_resultado("Fila - Inserção", sucesso, f"Estado: {resultado}")
        
        # Teste 2: Remoção FIFO
        primeiro = fila.remover()
        sucesso = primeiro is not None and primeiro.nome == "Ana"
        self.log_resultado("Fila - Remoção FIFO", sucesso, f"Primeiro removido: {primeiro}")
        
        # Teste 3: Busca
        encontrado = fila.buscar("bruno")
        sucesso = encontrado is not None and encontrado.nome == "Bruno"
        self.log_resultado("Fila - Busca", sucesso, f"Encontrado: {encontrado}")
        
        # Teste 4: Fila vazia
        fila.remover()  # Remove Bruno
        fila.remover()  # Remove Carlos
        vazio = fila.remover()  # Tenta remover de fila vazia
        sucesso = vazio is None
        self.log_resultado("Fila - Remoção em fila vazia", sucesso, f"Resultado: {vazio}")
    
    def teste_pilha(self):
        """Testa todas as operações da Pilha."""
        print("\n>> TESTANDO PILHA...")
        pilha = Pilha()
        
        # Teste 1: Inserção
        pilha.inserir("Operação 1")
        pilha.inserir("Operação 2")
        pilha.inserir("Operação 3")
        resultado = pilha.imprimir()
        sucesso = "Operação 1" in resultado and "Operação 2" in resultado and "Operação 3" in resultado
        self.log_resultado("Pilha - Inserção", sucesso, "Múltiplas operações inseridas")
        
        # Teste 2: Remoção LIFO
        ultimo = pilha.remover()
        sucesso = ultimo == "Operação 3"
        self.log_resultado("Pilha - Remoção LIFO", sucesso, f"Último removido: {ultimo}")
        
        # Teste 3: Busca
        encontrado = pilha.buscar("operação 2")
        sucesso = encontrado is not None and "Operação 2" in encontrado
        self.log_resultado("Pilha - Busca", sucesso, f"Encontrado: {encontrado}")
        
        # Teste 4: Pilha vazia
        pilha.remover()  # Remove Operação 2
        pilha.remover()  # Remove Operação 1
        vazio = pilha.remover()  # Tenta remover de pilha vazia
        sucesso = vazio is None
        self.log_resultado("Pilha - Remoção em pilha vazia", sucesso, f"Resultado: {vazio}")
    
    def teste_arvore_avl(self):
        """Testa todas as operações da Árvore AVL."""
        print("\n>> TESTANDO ÁRVORE AVL...")
        arvore = ArvoreAVL()
        
        # Teste 1: Inserção
        calourada1 = Calourada(10, "Festa da Computação")
        calourada2 = Calourada(5, "Festa da Engenharia")
        calourada3 = Calourada(15, "Festa da Medicina")
        calourada4 = Calourada(3, "Festa da Física")
        calourada5 = Calourada(7, "Festa da Química")
        
        arvore.inserir(10, calourada1)
        arvore.inserir(5, calourada2)
        arvore.inserir(15, calourada3)
        arvore.inserir(3, calourada4)
        arvore.inserir(7, calourada5)
        
        sucesso = arvore.raiz is not None
        self.log_resultado("Árvore - Inserção", sucesso, f"Raiz: ID {arvore.raiz.chave}")
        
        # Teste 2: Busca existente
        encontrado = arvore.buscar(7)
        sucesso = encontrado is not None and encontrado.nome == "Festa da Química"
        self.log_resultado("Árvore - Busca (existente)", sucesso, f"Encontrado: {encontrado}")
        
        # Teste 3: Busca não existente
        nao_encontrado = arvore.buscar(99)
        sucesso = nao_encontrado is None
        self.log_resultado("Árvore - Busca (não existente)", sucesso, f"Resultado: {nao_encontrado}")
        
        # Teste 4: Percursos
        in_ordem = arvore.in_ordem()
        ids_in_ordem = [c.id for c in in_ordem]
        sucesso = ids_in_ordem == sorted(ids_in_ordem)  # Deve estar ordenado
        self.log_resultado("Árvore - Percurso In-Ordem", sucesso, f"IDs: {ids_in_ordem}")
        
        pre_ordem = arvore.pre_ordem()
        sucesso = len(pre_ordem) == 5
        self.log_resultado("Árvore - Percurso Pré-Ordem", sucesso, f"Quantidade: {len(pre_ordem)}")
        
        pos_ordem = arvore.pos_ordem()
        sucesso = len(pos_ordem) == 5
        self.log_resultado("Árvore - Percurso Pós-Ordem", sucesso, f"Quantidade: {len(pos_ordem)}")
        
        # Teste 5: Balanceamento AVL
        altura = arvore._altura(arvore.raiz)
        sucesso = altura <= 4  # Para 5 nós, altura máxima deve ser baixa
        self.log_resultado("Árvore - Balanceamento AVL", sucesso, f"Altura: {altura}")
        
        # Teste 6: Remoção
        arvore.remover(5)
        encontrado_apos_remocao = arvore.buscar(5)
        sucesso = encontrado_apos_remocao is None
        self.log_resultado("Árvore - Remoção", sucesso, f"Busca após remoção: {encontrado_apos_remocao}")
    
    def teste_integracao_calourada(self):
        """Testa a integração entre as estruturas em uma Calourada."""
        print("\n>> TESTANDO INTEGRAÇÃO CALOURADA...")
        
        calourada = Calourada(1, "Festa de Integração")
        
        # Teste 1: Adicionar participantes à lista
        calourada.participantes.inserir(Participante("Alice"))
        calourada.participantes.inserir(Participante("Bob"))
        lista_resultado = calourada.participantes.imprimir()
        sucesso = "Alice" in lista_resultado and "Bob" in lista_resultado
        self.log_resultado("Integração - Lista de Participantes", sucesso, lista_resultado)
        
        # Teste 2: Adicionar à fila de entrada
        calourada.fila_entrada.inserir(Participante("Carlos"))
        calourada.fila_entrada.inserir(Participante("Diana"))
        fila_resultado = calourada.fila_entrada.imprimir()
        sucesso = "Carlos" in fila_resultado and "Diana" in fila_resultado
        self.log_resultado("Integração - Fila de Entrada", sucesso, fila_resultado)
        
        # Teste 3: Processamento da fila (Carlos deve sair primeiro)
        primeiro_atendido = calourada.fila_entrada.remover()
        sucesso = primeiro_atendido is not None and primeiro_atendido.nome == "Carlos"
        self.log_resultado("Integração - Processamento FIFO", sucesso, f"Primeiro atendido: {primeiro_atendido}")
    
    def teste_casos_extremos(self):
        """Testa casos extremos e situações de erro."""
        print("\n>> TESTANDO CASOS EXTREMOS...")
        
        # Teste 1: Operações em estruturas vazias
        lista_vazia = ListaLigada()
        resultado = lista_vazia.imprimir()
        sucesso = "Nenhum participante" in resultado
        self.log_resultado("Extremo - Lista vazia", sucesso, resultado)
        
        fila_vazia = Fila()
        resultado = fila_vazia.imprimir()
        sucesso = "vazia" in resultado
        self.log_resultado("Extremo - Fila vazia", sucesso, resultado)
        
        pilha_vazia = Pilha()
        resultado = pilha_vazia.imprimir()
        sucesso = "vazio" in resultado
        self.log_resultado("Extremo - Pilha vazia", sucesso, resultado)
        
        arvore_vazia = ArvoreAVL()
        resultado = arvore_vazia.imprimir_arvore()
        sucesso = "vazia" in resultado
        self.log_resultado("Extremo - Árvore vazia", sucesso, resultado)
        
        # Teste 2: Inserção de muitos elementos (teste de performance)
        arvore_grande = ArvoreAVL()
        for i in range(1, 16):  # 15 elementos
            arvore_grande.inserir(i, Calourada(i, f"Festa {i}"))
        
        altura_final = arvore_grande._altura(arvore_grande.raiz)
        sucesso = altura_final <= 5  # Altura máxima para 15 nós balanceados
        self.log_resultado("Extremo - Árvore com 15 nós", sucesso, f"Altura: {altura_final}")
    
    def simular_menu_principal(self):
        """Simula operações do menu principal."""
        print("\n>> SIMULANDO MENU PRINCIPAL...")
        
        # Simula o sistema completo
        from calourada_alt import ArvoreAVL, Pilha
        
        arvore_eventos = ArvoreAVL()
        pilha_historico = Pilha()
        
        # Simula criação de calouradas
        calouradas_teste = [
            (1, "Festa da Computação"),
            (2, "Festa da Engenharia"),
            (3, "Festa da Medicina")
        ]
        
        for id_evento, nome in calouradas_teste:
            nova_calourada = Calourada(id_evento, nome)
            arvore_eventos.inserir(id_evento, nova_calourada)
            pilha_historico.inserir(f"CRIADO: '{nome}' (ID:{id_evento})")
        
        # Verifica se todas foram inseridas
        in_ordem = arvore_eventos.in_ordem()
        sucesso = len(in_ordem) == 3
        self.log_resultado("Menu - Criação de múltiplas calouradas", sucesso, f"Total criadas: {len(in_ordem)}")
        
        # Simula busca
        calourada_encontrada = arvore_eventos.buscar(2)
        sucesso = calourada_encontrada is not None and calourada_encontrada.nome == "Festa da Engenharia"
        self.log_resultado("Menu - Busca de calourada", sucesso, f"Encontrada: {calourada_encontrada}")
        
        # Simula remoção
        arvore_eventos.remover(2)
        calourada_removida = arvore_eventos.buscar(2)
        sucesso = calourada_removida is None
        self.log_resultado("Menu - Remoção de calourada", sucesso, f"Busca após remoção: {calourada_removida}")
        
        # Verifica histórico
        historico = pilha_historico.imprimir()
        sucesso = "CRIADO" in historico
        self.log_resultado("Menu - Histórico de operações", sucesso, "Histórico registrando operações")
    
    def executar_todos_os_testes(self):
        """Executa todos os testes e gera relatório final."""
        print(">> INICIANDO TESTES AUTOMATIZADOS DO SISTEMA DE CALOURADAS")
        print("=" * 70)
        
        self.teste_lista_ligada()
        self.teste_fila()
        self.teste_pilha()
        self.teste_arvore_avl()
        self.teste_integracao_calourada()
        self.teste_casos_extremos()
        self.simular_menu_principal()
        
        print("\n" + "=" * 70)
        print(">> RELATÓRIO FINAL DOS TESTES")
        print("=" * 70)
        
        total_testes = self.teste_numero
        testes_passou = sum(1 for resultado in self.resultados if "[PASSOU]" in resultado)
        testes_falhou = total_testes - testes_passou
        
        print(f">> Total de testes: {total_testes}")
        print(f">> Testes que passaram: {testes_passou}")
        print(f">> Testes que falharam: {testes_falhou}")
        print(f">> Taxa de sucesso: {(testes_passou/total_testes)*100:.1f}%")
        
        print("\n>> DETALHES DOS TESTES:")
        for resultado in self.resultados:
            print(resultado)
        
        if testes_falhou == 0:
            print("\n>> PARABÉNS! Todos os testes passaram!")
            print(">> O sistema está funcionando perfeitamente!")
        else:
            print(f"\n>> {testes_falhou} teste(s) falharam. Verifique os detalhes acima.")
        
        return testes_passou == total_testes


def main():
    """Função principal para executar os testes."""
    print("Sistema de Teste Automatizado para Calouradas")
    print("Versão 1.0 - Testa todas as estruturas de dados implementadas")
    print()
    
    tester = TesteSistemaCalouradas()
    sucesso_total = tester.executar_todos_os_testes()
    
    print("\n" + "=" * 70)
    if sucesso_total:
        print(">> RESULTADO: SISTEMA APROVADO - Todos os requisitos funcionando!")
        print(">> Estruturas testadas:")
        print("   [OK] Lista Ligada (INSERT, REMOVE, SEARCH, PRINT)")
        print("   [OK] Fila (INSERT, REMOVE, SEARCH, PRINT)")
        print("   [OK] Pilha (INSERT, REMOVE, SEARCH, PRINT)")
        print("   [OK] Árvore AVL (INSERT, REMOVE, PRÉ/IN/PÓS-ORDEM)")
        print("   [OK] Balanceamento AVL funcionando")
        print("   [OK] Integração entre estruturas")
        print("\n>> Pronto para avaliação acadêmica!")
    else:
        print(">> RESULTADO: SISTEMA COM PROBLEMAS - Verifique os erros acima.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
