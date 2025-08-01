class Participante:
    """Representa uma pessoa que quer ir a uma calourada."""
    def __init__(self, nome):
        self.nome = nome
    def __str__(self):
        return self.nome

class Calourada:
    """Representa um evento, contendo suas próprias listas e filas."""
    def __init__(self, id_evento, nome):
        self.id = id_evento
        self.nome = nome
        self.participantes = ListaLigada()
        self.fila_entrada = Fila()
    def __str__(self):
        return f"ID:{self.id} - {self.nome}"



class No:
    """Nó genérico para Lista, Fila e Pilha."""
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class NoAVL:
    """Nó para a Árvore AVL, precisa guardar altura."""
    def __init__(self, chave, dados):
        self.chave = chave
        self.dados = dados
        self.altura = 1
        self.esquerda = None
        self.direita = None

class ListaLigada: 
    """Lista para os participantes de cada calourada."""
    def __init__(self):
        self.cabeca = None
    def inserir(self, dados):
        novo_no = No(dados)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def remover(self, valor_dado):
        if not self.cabeca:
            return False
        if self.cabeca.dados.nome.lower() == valor_dado.lower():
            self.cabeca = self.cabeca.proximo
            return True
        
        atual = self.cabeca
        while atual.proximo and atual.proximo.dados.nome.lower() != valor_dado.lower():
            atual = atual.proximo
        
        if atual.proximo:
            atual.proximo = atual.proximo.proximo
            return True
        return False

    def buscar(self, valor_dado):
        atual = self.cabeca
        while atual:
            if atual.dados.nome.lower() == valor_dado.lower():
                return atual.dados
            atual = atual.proximo
        return None

    def imprimir(self):
        itens = []
        atual = self.cabeca
        while atual:
            itens.append(str(atual.dados))
            atual = atual.proximo
        return ", ".join(itens) if itens else "Nenhum participante."

class Fila: # REQUISITO 2: FILA/PILHA (2.0 pontos)
    """Fila para a entrada de cada calourada."""
    def __init__(self):
        self.frente = None
        self.tras = None
    def inserir(self, dados):
        novo_no = No(dados)
        if not self.tras:
            self.frente = self.tras = novo_no
        else:
            self.tras.proximo = novo_no
            self.tras = novo_no

    def remover(self):
        if not self.frente:
            return None
        dados_removidos = self.frente.dados
        self.frente = self.frente.proximo
        if not self.frente:
            self.tras = None
        return dados_removidos

    def buscar(self, valor_dado):
        atual = self.frente
        while atual:
            if atual.dados.nome.lower() == valor_dado.lower():
                return atual.dados
            atual = atual.proximo
        return None

    def imprimir(self):
        itens = []
        atual = self.frente
        while atual:
            itens.append(str(atual.dados))
            atual = atual.proximo
        return "FRENTE -> " + " -> ".join(itens) + " -> FIM" if itens else "Fila vazia."

class Pilha: # REQUISITO 2: FILA/PILHA (2.0 pontos)
    """Pilha para o histórico de operações do sistema."""
    def __init__(self):
        self.topo = None
    def inserir(self, dados):
        novo_no = No(dados)
        novo_no.proximo = self.topo
        self.topo = novo_no

    def remover(self):
        if not self.topo:
            return None
        dados_removidos = self.topo.dados
        self.topo = self.topo.proximo
        return dados_removidos

    def buscar(self, termo_busca):
        atual = self.topo
        while atual:
            if termo_busca.lower() in atual.dados.lower():
                return atual.dados
            atual = atual.proximo
        return None

    def imprimir(self):
        itens = []
        atual = self.topo
        while atual:
            itens.append(str(atual.dados))
            atual = atual.proximo
        
        if not itens:
            return "Histórico vazio."
        else:
            resultado = "--- Histórico de Operações (Topo primeiro) ---\n"
            for item in itens:
                resultado += f"  - {item}\n"
            return resultado.rstrip()

class ArvoreAVL: # REQUISITO 3 e 4: ÁRVORE AVL (2.0 + 2.0 pontos)
    """Árvore AVL que organiza as calouradas por ID."""
    def __init__(self):
        self.raiz = None
    
    def _altura(self, no):
        return no.altura if no else 0

    def _balanceamento(self, no):
        return self._altura(no.esquerda) - self._altura(no.direita) if no else 0
    
    def _rotacao_direita(self, y):
        x = y.esquerda; t2 = x.direita; x.direita = y; y.esquerda = t2
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        return x

    def _rotacao_esquerda(self, x):
        y = x.direita; t2 = y.esquerda; y.esquerda = x; x.direita = t2
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        return y

    def _menor_valor_no(self, no):
        return self._menor_valor_no(no.esquerda) if no.esquerda else no

    def inserir(self, chave, dados):
        self.raiz = self._inserir_recursivo(self.raiz, chave, dados)
        return True
    
    def _inserir_recursivo(self, raiz, chave, dados):
        if not raiz: return NoAVL(chave, dados)
        if chave < raiz.chave: raiz.esquerda = self._inserir_recursivo(raiz.esquerda, chave, dados)
        else: raiz.direita = self._inserir_recursivo(raiz.direita, chave, dados)
        
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        balance = self._balanceamento(raiz)
        
        if balance > 1 and chave < raiz.esquerda.chave: return self._rotacao_direita(raiz)
        if balance < -1 and chave > raiz.direita.chave: return self._rotacao_esquerda(raiz)
        if balance > 1 and chave > raiz.esquerda.chave:
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)
        if balance < -1 and chave < raiz.direita.chave:
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)
        return raiz

    def remover(self, chave):
        self.raiz = self._remover_recursivo(self.raiz, chave)
        return True
    
    def _remover_recursivo(self, raiz, chave):
        if not raiz: return raiz
        
        if chave < raiz.chave: raiz.esquerda = self._remover_recursivo(raiz.esquerda, chave)
        elif chave > raiz.chave: raiz.direita = self._remover_recursivo(raiz.direita, chave)
        else:
            if raiz.esquerda is None: return raiz.direita
            elif raiz.direita is None: return raiz.esquerda
            temp = self._menor_valor_no(raiz.direita)
            raiz.chave, raiz.dados = temp.chave, temp.dados
            raiz.direita = self._remover_recursivo(raiz.direita, temp.chave)
            
        if not raiz: return raiz
        
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        balance = self._balanceamento(raiz)
        
        if balance > 1 and self._balanceamento(raiz.esquerda) >= 0: return self._rotacao_direita(raiz)
        if balance < -1 and self._balanceamento(raiz.direita) <= 0: return self._rotacao_esquerda(raiz)
        if balance > 1 and self._balanceamento(raiz.esquerda) < 0:
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)
        if balance < -1 and self._balanceamento(raiz.direita) > 0:
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)
        return raiz
    
    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, chave)
    
    def _buscar_recursivo(self, raiz, chave):
        if not raiz or raiz.chave == chave:
            return raiz.dados if raiz else None
        if chave < raiz.chave:
            return self._buscar_recursivo(raiz.esquerda, chave)
        return self._buscar_recursivo(raiz.direita, chave)
        
    def pre_ordem(self):
        resultado = []
        self._pre_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _pre_ordem_recursivo(self, raiz, resultado):
        if raiz:
            resultado.append(raiz.dados)
            self._pre_ordem_recursivo(raiz.esquerda, resultado)
            self._pre_ordem_recursivo(raiz.direita, resultado)
    
    def in_ordem(self):
        resultado = []
        self._in_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_ordem_recursivo(self, raiz, resultado):
        if raiz:
            self._in_ordem_recursivo(raiz.esquerda, resultado)
            resultado.append(raiz.dados)
            self._in_ordem_recursivo(raiz.direita, resultado)
    
    def pos_ordem(self):
        resultado = []
        self._pos_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _pos_ordem_recursivo(self, raiz, resultado):
        if raiz:
            self._pos_ordem_recursivo(raiz.esquerda, resultado)
            self._pos_ordem_recursivo(raiz.direita, resultado)
            resultado.append(raiz.dados)

    def imprimir_arvore(self):
        if not self.raiz:
            return "Árvore de eventos está vazia."
        
        resultado = f"--- ESTRUTURA DA ÁRVORE (Altura: {self._altura(self.raiz)}) ---\n"
        linhas = []
        self._visualizar_recursivo(self.raiz, "", True, linhas)
        return resultado + "\n".join(linhas)
    
    def _visualizar_recursivo(self, no, prefixo, eh_ultimo, linhas):
        if no:
            conector = "└── " if eh_ultimo else "├── "
            info_no = f"ID:{no.chave} (b:{self._balanceamento(no):+d}) - {no.dados.nome}"
            linhas.append(prefixo + conector + info_no)
            
            extensao = "    " if eh_ultimo else "│   "
            novo_prefixo = prefixo + extensao
            
            tem_esquerda = no.esquerda is not None
            tem_direita = no.direita is not None
            
            if tem_direita:
                self._visualizar_recursivo(no.direita, novo_prefixo, not tem_esquerda, linhas)
            
            if tem_esquerda:
                self._visualizar_recursivo(no.esquerda, novo_prefixo, True, linhas)


def menu_gerenciar_calourada(calourada, pilha_historico):
    """Sub-menu para interagir com a Lista e a Fila de uma calourada."""
    while True:
        print(f"\n--- Gerenciando: {calourada.nome} ---")
        print("  Participantes (LISTA): " + calourada.participantes.imprimir())
        print("  Fila de Entrada (FILA): " + calourada.fila_entrada.imprimir())
        print("-" * 20)
        print("1. Adicionar Participante (Inserir na Lista)")
        print("2. Remover Participante (Remover da Lista)")
        print("3. Buscar Participante (Buscar na Lista)")
        print("4. Adicionar à Fila de Entrada (Inserir na Fila)")
        print("5. Atender da Fila de Entrada (Remover da Fila)")
        print("0. Voltar ao Menu Principal")
        
        op = input("Opção: ").strip()
        if op == '1':
            nome = input("Nome do participante: ").strip()
            if nome: calourada.participantes.inserir(Participante(nome)); pilha_historico.inserir(f"ADD_PART: {nome} em '{calourada.nome}'")
        elif op == '2':
            nome = input("Nome a remover: ").strip()
            if nome and calourada.participantes.remover(nome): print("Removido com sucesso.")
            else: print("Participante não encontrado.")
        elif op == '3':
            nome = input("Nome a buscar: ").strip()
            resultado = calourada.participantes.buscar(nome)
            print(f"Resultado da busca: {'Encontrado' if resultado else 'Não encontrado'}")
        elif op == '4':
            nome = input("Nome para entrar na fila: ").strip()
            if nome: calourada.fila_entrada.inserir(Participante(nome))
        elif op == '5':
            removido = calourada.fila_entrada.remover()
            if removido: print(f"{removido} foi atendido(a) e entrou na festa.")
            else: print("Fila vazia.")
        elif op == '0': break
        else: print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def main():
    arvore_eventos = ArvoreAVL()
    pilha_historico = Pilha()
    id_contador = 0

    while True:
        print("\n" + "="*50); print("    🎉 SISTEMA DE GERENCIAMENTO DE CALOURADAS 🎉"); print("="*50)
        print("--- GERAL ---")
        print("1. Criar Calourada (Inserir na Árvore)")
        print("2. Listar Calouradas (Percorrer Árvore In-Ordem)")
        print("3. Remover Calourada (Remover da Árvore)")
        print("4. Gerenciar Calourada (Acessar Lista e Fila)")
        print("\n--- VISUALIZAÇÃO/DEPURAÇÃO ---")
        print("5. Ver Percursos da Árvore (Apenas IDs)")
        print("6. Visualizar Estrutura da Árvore AVL")
        print("7. Ver Histórico de Operações (Pilha)")
        print("0. Sair")
        print("="*50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            nome = input("Nome da nova calourada: ").strip()
            if nome:
                id_contador += 1
                nova_calourada = Calourada(id_contador, nome)
                arvore_eventos.inserir(id_contador, nova_calourada)
                pilha_historico.inserir(f"CRIADO: '{nome}' (ID:{id_contador})")
                print(f"'{nome}' criada com ID {id_contador}.")
        
        elif opcao == '2':
            if not arvore_eventos.raiz:
                print("Nenhuma calourada para listar.")
            else:
                print("=== CALOURADAS CADASTRADAS (3 PERCURSOS DA ÁRVORE) ===")
                
                # Pré-Ordem
                print("\n🔸 PRÉ-ORDEM (Raiz → Esquerda → Direita):")
                pre_ordem = arvore_eventos.pre_ordem()
                for i, evento in enumerate(pre_ordem, 1):
                    print(f"  {i}. {evento.nome} (ID: {evento.id})")
                
                # In-Ordem (ordenado)
                print("\n🔸 IN-ORDEM (Esquerda → Raiz → Direita) - ORDENADO:")
                in_ordem = arvore_eventos.in_ordem()
                for i, evento in enumerate(in_ordem, 1):
                    print(f"  {i}. {evento.nome} (ID: {evento.id})")
                
                # Pós-Ordem
                print("\n🔸 PÓS-ORDEM (Esquerda → Direita → Raiz):")
                pos_ordem = arvore_eventos.pos_ordem()
                for i, evento in enumerate(pos_ordem, 1):
                    print(f"  {i}. {evento.nome} (ID: {evento.id})")
                
                print(f"\n📊 Total de calouradas: {len(in_ordem)}")

        elif opcao == '3':
            try:
                id_rem = int(input("ID da calourada a remover: "))
                calourada_rem = arvore_eventos.buscar(id_rem)
                if calourada_rem:
                    arvore_eventos.remover(id_rem)
                    pilha_historico.inserir(f"REMOVIDO: '{calourada_rem.nome}'")
                    print("Removido com sucesso.")
                else: print("Calourada não encontrada.")
            except ValueError: print("ID deve ser um número.")

        elif opcao == '4':
            try:
                id_ger = int(input("ID da calourada para gerenciar: "))
                calourada_ger = arvore_eventos.buscar(id_ger)
                if calourada_ger: menu_gerenciar_calourada(calourada_ger, pilha_historico)
                else: print("Calourada não encontrada.")
            except ValueError: print("ID deve ser um número.")

        elif opcao == '5':
            if not arvore_eventos.raiz:
                print("Árvore vazia.")
            else:
                print("=== PERCURSOS DA ÁRVORE (Visualização Técnica) ===")
                pre_ordem = arvore_eventos.pre_ordem()
                in_ordem = arvore_eventos.in_ordem()
                pos_ordem = arvore_eventos.pos_ordem()
                
                print("\n🔹 Pré-Ordem (IDs): ", end="")
                print(" → ".join([f"ID{c.id}" for c in pre_ordem]))
                print("🔹 In-Ordem (IDs):  ", end="")
                print(" → ".join([f"ID{c.id}" for c in in_ordem]))
                print("🔹 Pós-Ordem (IDs): ", end="")
                print(" → ".join([f"ID{c.id}" for c in pos_ordem]))
                print(f"\n📐 Altura da árvore: {arvore_eventos._altura(arvore_eventos.raiz)}")
                print(f"📊 Total de nós: {len(in_ordem)}")

        elif opcao == '6':
            resultado = arvore_eventos.imprimir_arvore()
            print(resultado)

        elif opcao == '7':
            resultado = pilha_historico.imprimir()
            print(resultado)
            
        elif opcao == '0':
            print("Saindo do sistema de avaliação. Bom trabalho!"); break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()