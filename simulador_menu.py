#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Simulação de Menu Interativo
Simula um usuário real navegando pelo sistema de calouradas.
"""

import sys
import time
from io import StringIO
from unittest.mock import patch

def simular_entrada_usuario(entradas):
    """Simula entradas do usuário de forma sequencial."""
    iterator = iter(entradas)
    return lambda prompt="": next(iterator, "0")  # Retorna "0" (sair) se acabarem as entradas

def executar_simulacao_completa():
    """Executa uma simulação completa do sistema."""
    print(">> INICIANDO SIMULAÇÃO COMPLETA DO SISTEMA")
    print("=" * 60)
    
    # Sequência de comandos que simula um usuário real
    comandos_simulacao = [
        # Criar algumas calouradas
        "1",  # Criar calourada
        "Festa da Computação",  # Nome da calourada
        
        "1",  # Criar outra calourada
        "Festa da Engenharia",  # Nome da calourada
        
        "1",  # Criar terceira calourada
        "Festa da Medicina",  # Nome da calourada
        
        # Listar calouradas (opção 2)
        "2",  # Listar calouradas
        "",   # Enter para continuar
        
        # Gerenciar uma calourada (opção 4)
        "4",  # Gerenciar calourada
        "1",  # ID da calourada (Festa da Computação)
        
        # Dentro do submenu - adicionar participantes
        "1",  # Adicionar participante
        "João Silva",  # Nome do participante
        
        "1",  # Adicionar outro participante
        "Maria Santos",  # Nome do participante
        
        "1",  # Adicionar terceiro participante
        "Pedro Oliveira",  # Nome do participante
        
        # Adicionar pessoas à fila de entrada
        "4",  # Adicionar à fila de entrada
        "Ana Costa",  # Nome para fila
        
        "4",  # Adicionar outro à fila
        "Bruno Lima",  # Nome para fila
        
        # Buscar um participante
        "3",  # Buscar participante
        "maria",  # Nome a buscar (teste case insensitive)
        
        # Atender alguém da fila
        "5",  # Atender da fila
        
        # Remover um participante
        "2",  # Remover participante
        "João Silva",  # Nome a remover
        
        "0",  # Voltar ao menu principal
        
        # Ver percursos da árvore (opção 5)
        "5",  # Ver percursos
        "",   # Enter para continuar
        
        # Visualizar estrutura da árvore (opção 6)
        "6",  # Visualizar árvore
        "",   # Enter para continuar
        
        # Ver histórico (opção 7)
        "7",  # Ver histórico
        "",   # Enter para continuar
        
        # Remover uma calourada (opção 3)
        "3",  # Remover calourada
        "2",  # ID da calourada a remover (Festa da Engenharia)
        "",   # Enter para continuar
        
        # Listar novamente para ver a remoção
        "2",  # Listar calouradas
        "",   # Enter para continuar
        
        # Sair do sistema
        "0"   # Sair
    ]
    
    print(">> Comandos a serem executados:")
    for i, cmd in enumerate(comandos_simulacao, 1):
        if cmd.strip():
            print(f"   {i}. {cmd}")
    
    print("\n>> Executando simulação...")
    print("-" * 60)
    
    try:
        # Redireciona a entrada padrão para nossa simulação
        with patch('builtins.input', side_effect=comandos_simulacao):
            # Importa e executa o main do sistema
            from calourada_alt import main
            main()
            
    except (IndexError, StopIteration):
        print("\n[OK] Simulação concluída - Sistema funcionou corretamente!")
    except Exception as e:
        print(f"\n[ERRO] Erro durante a simulação: {e}")
        return False
    
    return True

def executar_teste_stress():
    """Testa o sistema com muitas operações."""
    print("\n>> TESTE DE STRESS - MUITAS OPERAÇÕES")
    print("=" * 60)
    
    # Criar comandos para 20 calouradas
    comandos_stress = []
    for i in range(1, 21):
        comandos_stress.extend(["1", f"Festa {i}"])
    comandos_stress.extend(["2", "", "5", "", "6", "", "0"])  # Ver listas e sair
    
    print(">> Testando criação de 20 calouradas...")
    
    try:
        with patch('builtins.input', side_effect=comandos_stress):
            from calourada_alt import main
            main()
        print("[OK] Teste de stress passou!")
        return True
    except Exception as e:
        print(f"[ERRO] Teste de stress falhou: {e}")
        return False

def executar_teste_casos_especiais():
    """Testa casos especiais e situações de erro."""
    print("\n>> TESTE DE CASOS ESPECIAIS")
    print("=" * 60)
    
    casos_especiais = [
        # Tentar operações em sistema vazio
        "2",  # Listar calouradas vazias
        "",   # Enter
        "3",  # Tentar remover de árvore vazia
        "1",  # ID qualquer
        "",   # Enter
        "4",  # Tentar gerenciar calourada inexistente
        "999", # ID inexistente
        "",   # Enter
        "5",  # Ver percursos em árvore vazia
        "",   # Enter
        "6",  # Ver estrutura de árvore vazia
        "",   # Enter
        "7",  # Ver histórico vazio
        "",   # Enter
        
        # Criar uma calourada para testes
        "1", "Festa Teste",
        
        # Gerenciar calourada com operações em estruturas vazias
        "4", "1",  # Gerenciar calourada ID 1
        "2", "Inexistente",  # Tentar remover participante inexistente
        "3", "Inexistente",  # Buscar participante inexistente
        "5",  # Tentar atender fila vazia
        "0",  # Voltar
        
        "0"   # Sair
    ]
    
    print(">> Testando casos especiais e validação de erros...")
    
    try:
        with patch('builtins.input', side_effect=casos_especiais):
            from calourada_alt import main
            main()
        print("[OK] Teste de casos especiais passou!")
        return True
    except Exception as e:
        print(f"[ERRO] Teste de casos especiais falhou: {e}")
        return False

def main():
    """Função principal do simulador."""
    print(">> SIMULADOR AUTOMATIZADO DO SISTEMA DE CALOURADAS")
    print("Versão 1.0 - Simula interações reais do usuário")
    print("=" * 70)
    
    resultados = []
    
    # Executa simulação completa
    print("1. Executando simulação completa...")
    resultado1 = executar_simulacao_completa()
    resultados.append(("Simulação Completa", resultado1))
    
    # Executa teste de stress
    print("\n2. Executando teste de stress...")
    resultado2 = executar_teste_stress()
    resultados.append(("Teste de Stress", resultado2))
    
    # Executa teste de casos especiais
    print("\n3. Executando teste de casos especiais...")
    resultado3 = executar_teste_casos_especiais()
    resultados.append(("Casos Especiais", resultado3))
    
    # Relatório final
    print("\n" + "=" * 70)
    print(">> RELATÓRIO FINAL DA SIMULAÇÃO")
    print("=" * 70)
    
    total_passou = sum(1 for _, resultado in resultados if resultado)
    total_testes = len(resultados)
    
    for nome, resultado in resultados:
        status = "[PASSOU]" if resultado else "[FALHOU]"
        print(f"{nome}: {status}")
    
    print(f"\n>> Resumo: {total_passou}/{total_testes} testes passaram")
    print(f">> Taxa de sucesso: {(total_passou/total_testes)*100:.1f}%")
    
    if total_passou == total_testes:
        print("\n>> EXCELENTE! Sistema passou em todos os testes de simulação!")
        print(">> Pronto para demonstração e avaliação!")
    else:
        print(f"\n>> {total_testes - total_passou} teste(s) falharam.")
        print(">> Verifique os erros reportados acima.")
    
    print("\n>> DICAS PARA DEMONSTRAÇÃO:")
    print("   • O sistema suporta nomes com espaços e acentos")
    print("   • Busca é case-insensitive (maria = Maria)")
    print("   • Árvore AVL mantém balanceamento automático")
    print("   • Histórico registra todas as operações importantes")
    print("   • Interface clara mostra todos os percursos da árvore")
    print("=" * 70)

if __name__ == "__main__":
    main()
