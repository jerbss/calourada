import sys
sys.path.append('.')
from calourada import Pilha

# Criar uma pilha
pilha = Pilha()
print("Pilha vazia criada")

# Inserir elementos
pilha.inserir('Item 1')
pilha.inserir('Item 2')
pilha.inserir('Item 3')
print("Pilha após inserções:", pilha.imprimir())
print("Tamanho da pilha:", pilha.tamanho)

# Testar a busca
item = pilha.buscar(lambda x: x == 'Item 2')
print("Resultado da busca por 'Item 2':", item)

# Testar a remoção
removido = pilha.remover()
print("Item removido do topo:", removido)
print("Pilha após remoção:", pilha.imprimir())
print("Novo tamanho da pilha:", pilha.tamanho)

# Testar remoção até esvaziar
print("\nRemovendo todos os itens da pilha:")
while pilha.tamanho > 0:
    removido = pilha.remover()
    print(f"Removido: {removido}, Itens restantes: {pilha.tamanho}")

# Tentar remover de uma pilha vazia
removido = pilha.remover()
print("\nTentativa de remover de uma pilha vazia:", "Sucesso" if removido is None else "Falha")
