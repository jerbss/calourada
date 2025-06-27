"""
Sistema de Gerenciamento de Calouradas - UFC Campus Pici
Implementa Lista Ligada, Fila, Pilha e Árvore AVL para gerenciar eventos universitários
"""

import datetime
from typing import Optional, List as ListType, Dict, Any

# =====================================================
# ESTRUTURAS DE DADOS
# =====================================================

class NoLista:
    """Nó para Lista Ligada"""
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class ListaLigada:
    """Lista Ligada para gerenciar participantes"""
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def inserir(self, dados):
        """Insere um novo elemento na lista"""
        novo_no = NoLista(dados)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1
        return True
    
    def remover(self, criterio_busca):
        """Remove elemento baseado em critério de busca"""
        if not self.cabeca:
            return False
        
        # Se o primeiro elemento deve ser removido
        if criterio_busca(self.cabeca.dados):
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return True
        
        atual = self.cabeca
        while atual.proximo:
            if criterio_busca(atual.proximo.dados):
                atual.proximo = atual.proximo.proximo
                self.tamanho -= 1
                return True
            atual = atual.proximo
        return False
    
    def buscar(self, criterio_busca):
        """Busca elemento na lista"""
        atual = self.cabeca
        while atual:
            if criterio_busca(atual.dados):
                return atual.dados
            atual = atual.proximo
        return None
    
    def imprimir(self):
        """Imprime todos os elementos da lista"""
        elementos = []
        atual = self.cabeca
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class NoFila:
    """Nó para Fila"""
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class Fila:
    """Fila para controle de entrada nos eventos"""
    def __init__(self):
        self.frente = None
        self.tras = None
        self.tamanho = 0
    
    def inserir(self, dados):
        """Insere elemento no final da fila"""
        novo_no = NoFila(dados)
        if not self.tras:
            self.frente = self.tras = novo_no
        else:
            self.tras.proximo = novo_no
            self.tras = novo_no
        self.tamanho += 1
        return True
    
    def remover(self):
        """Remove elemento da frente da fila"""
        if not self.frente:
            return None
        
        dados = self.frente.dados
        self.frente = self.frente.proximo
        if not self.frente:
            self.tras = None
        self.tamanho -= 1
        return dados
    
    def buscar(self, criterio_busca):
        """Busca elemento na fila"""
        atual = self.frente
        while atual:
            if criterio_busca(atual.dados):
                return atual.dados
            atual = atual.proximo
        return None
    
    def imprimir(self):
        """Imprime todos os elementos da fila"""
        elementos = []
        atual = self.frente
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class NoPilha:
    """Nó para Pilha"""
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class Pilha:
    """Pilha para histórico de operações"""
    def __init__(self):
        self.topo = None
        self.tamanho = 0
    
    def inserir(self, dados):
        """Insere elemento no topo da pilha"""
        novo_no = NoPilha(dados)
        novo_no.proximo = self.topo
        self.topo = novo_no
        self.tamanho += 1
        return True
    
    def remover(self):
        """Remove elemento do topo da pilha"""
        if not self.topo:
            return None
        
        dados = self.topo.dados
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return dados
    
    def buscar(self, criterio_busca):
        """Busca elemento na pilha"""
        atual = self.topo
        while atual:
            if criterio_busca(atual.dados):
                return atual.dados
            atual = atual.proximo
        return None
    
    def imprimir(self):
        """Imprime todos os elementos da pilha"""
        elementos = []
        atual = self.topo
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class NoAVL:
    """Nó para Árvore AVL"""
    def __init__(self, dados, chave):
        self.dados = dados
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    """Árvore AVL para busca eficiente de eventos"""
    def __init__(self):
        self.raiz = None
    
    def _altura(self, no):
        """Retorna altura do nó"""
        if not no:
            return 0
        return no.altura
    
    def _balanceamento(self, no):
        """Calcula fator de balanceamento"""
        if not no:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)
    
    def _rotacao_direita(self, y):
        """Rotação simples à direita"""
        x = y.esquerda
        t2 = x.direita
        
        x.direita = y
        y.esquerda = t2
        
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        
        return x
    
    def _rotacao_esquerda(self, x):
        """Rotação simples à esquerda"""
        y = x.direita
        t2 = y.esquerda
        
        y.esquerda = x
        x.direita = t2
        
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        
        return y
    
    def inserir(self, dados, chave):
        """Insere elemento na árvore AVL"""
        self.raiz = self._inserir_recursivo(self.raiz, dados, chave)
        return True
    
    def _inserir_recursivo(self, raiz, dados, chave):
        """Inserção recursiva com balanceamento"""
        # Inserção normal da BST
        if not raiz:
            return NoAVL(dados, chave)
        
        if chave < raiz.chave:
            raiz.esquerda = self._inserir_recursivo(raiz.esquerda, dados, chave)
        elif chave > raiz.chave:
            raiz.direita = self._inserir_recursivo(raiz.direita, dados, chave)
        else:
            # Chave duplicada, atualiza dados
            raiz.dados = dados
            return raiz
        
        # Atualiza altura
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        
        # Obtém fator de balanceamento
        balance = self._balanceamento(raiz)
        
        # Rotações para balanceamento
        # Caso Esquerda-Esquerda
        if balance > 1 and chave < raiz.esquerda.chave:
            return self._rotacao_direita(raiz)
        
        # Caso Direita-Direita
        if balance < -1 and chave > raiz.direita.chave:
            return self._rotacao_esquerda(raiz)
        
        # Caso Esquerda-Direita
        if balance > 1 and chave > raiz.esquerda.chave:
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)
        
        # Caso Direita-Esquerda
        if balance < -1 and chave < raiz.direita.chave:
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)
        
        return raiz
    
    def remover(self, chave):
        """Remove elemento da árvore"""
        self.raiz = self._remover_recursivo(self.raiz, chave)
        return True
    
    def _remover_recursivo(self, raiz, chave):
        """Remoção recursiva com balanceamento"""
        if not raiz:
            return raiz
        
        if chave < raiz.chave:
            raiz.esquerda = self._remover_recursivo(raiz.esquerda, chave)
        elif chave > raiz.chave:
            raiz.direita = self._remover_recursivo(raiz.direita, chave)
        else:
            # Nó a ser removido encontrado
            if not raiz.esquerda or not raiz.direita:
                temp = raiz.esquerda if raiz.esquerda else raiz.direita
                if not temp:
                    temp = raiz
                    raiz = None
                else:
                    raiz = temp
            else:
                # Nó com dois filhos
                temp = self._menor_valor(raiz.direita)
                raiz.chave = temp.chave
                raiz.dados = temp.dados
                raiz.direita = self._remover_recursivo(raiz.direita, temp.chave)
        
        if not raiz:
            return raiz
        
        # Atualiza altura e rebalanceia
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        balance = self._balanceamento(raiz)
        
        # Rotações
        if balance > 1 and self._balanceamento(raiz.esquerda) >= 0:
            return self._rotacao_direita(raiz)
        
        if balance < -1 and self._balanceamento(raiz.direita) <= 0:
            return self._rotacao_esquerda(raiz)
        
        if balance > 1 and self._balanceamento(raiz.esquerda) < 0:
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)
        
        if balance < -1 and self._balanceamento(raiz.direita) > 0:
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)
        
        return raiz
    
    def _menor_valor(self, raiz):
        """Encontra o menor valor na árvore"""
        if not raiz.esquerda:
            return raiz
        return self._menor_valor(raiz.esquerda)
    
    def buscar(self, chave):
        """Busca elemento na árvore"""
        return self._buscar_recursivo(self.raiz, chave)
    
    def _buscar_recursivo(self, raiz, chave):
        """Busca recursiva"""
        if not raiz or raiz.chave == chave:
            return raiz.dados if raiz else None
        
        if chave < raiz.chave:
            return self._buscar_recursivo(raiz.esquerda, chave)
        return self._buscar_recursivo(raiz.direita, chave)
    
    def pre_ordem(self):
        """Percurso pré-ordem"""
        resultado = []
        self._pre_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _pre_ordem_recursivo(self, raiz, resultado):
        if raiz:
            resultado.append(raiz.dados)
            self._pre_ordem_recursivo(raiz.esquerda, resultado)
            self._pre_ordem_recursivo(raiz.direita, resultado)
    
    def in_ordem(self):
        """Percurso in-ordem"""
        resultado = []
        self._in_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_ordem_recursivo(self, raiz, resultado):
        if raiz:
            self._in_ordem_recursivo(raiz.esquerda, resultado)
            resultado.append(raiz.dados)
            self._in_ordem_recursivo(raiz.direita, resultado)
    
    def pos_ordem(self):
        """Percurso pós-ordem"""
        resultado = []
        self._pos_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _pos_ordem_recursivo(self, raiz, resultado):
        if raiz:
            self._pos_ordem_recursivo(raiz.esquerda, resultado)
            self._pos_ordem_recursivo(raiz.direita, resultado)
            resultado.append(raiz.dados)

# =====================================================
# CLASSES DO SISTEMA
# =====================================================

class Participante:
    """Classe para representar um participante"""
    def __init__(self, nome, curso, unidade, sexo, periodo):
        self.nome = nome
        self.curso = curso
        self.unidade = unidade
        self.sexo = sexo  # M, F, O (Masculino, Feminino, Outro)
        self.periodo = periodo  # Período do curso (1, 2, 3, etc.)
        self.data_interesse = datetime.datetime.now()
    
    def __str__(self):
        return f"{self.nome} - {self.curso}/{self.unidade} ({self.periodo}º período)"

class Calourada:
    """Classe para representar uma calourada universitária"""
    def __init__(self, id_sequencial, nome, data, local, unidade_organizadora, descricao=""):
        self.id = id_sequencial  # ID simples e sequencial
        self.nome = nome
        self.data = data
        self.local = local
        self.unidade_organizadora = unidade_organizadora
        self.descricao = descricao
        self.participantes = ListaLigada()
        self.interessados = Fila()  # Lista de interessados
        self.data_criacao = datetime.datetime.now()
    
    def __str__(self):
        return f"{self.nome} - {self.data} ({self.unidade_organizadora})"

class SistemaCalourada:
    """Sistema principal de gerenciamento de calouradas"""
    def __init__(self):
        # Estruturas de dados principais
        self.eventos = ArvoreAVL()  # Calouradas organizadas por ID
        self.historico = Pilha()    # Histórico de operações
        self.contador_eventos = 0   # Contador para IDs sequenciais
        
        # Dados das unidades acadêmicas do Campus Pici
        self.unidades = {
            "CCA": {
                "nome": "Centro de Ciências Agrárias",
                "cursos": [
                    "Agronomia", "Economia Doméstica", "Economia Ecológica",
                    "Engenharia de Alimentos", "Engenharia de Pesca", 
                    "Gestão de Políticas Públicas", "Zootecnia"
                ]
            },
            "CC": {
                "nome": "Centro de Ciências",
                "cursos": [
                    "Biotecnologia", "Ciência da Computação", "Ciência de Dados",
                    "Ciências Biológicas", "Estatística", "Física", "Geografia",
                    "Geologia", "Matemática", "Química"
                ]
            },
            "CT": {
                "nome": "Centro de Tecnologia",
                "cursos": [
                    "Engenharia Ambiental e Sanitária", "Engenharia Civil",
                    "Engenharia Elétrica", "Engenharia Mecânica", "Engenharia Metalúrgica",
                    "Engenharia Química", "Engenharia de Computação", "Engenharia de Energias Renováveis",
                    "Engenharia de Petróleo", "Engenharia de Produção", "Engenharia de Telecomunicações"
                ]
            },
            "ICA": {
                "nome": "Instituto de Cultura e Arte",
                "cursos": [
                    "Cinema e Audiovisual", "Comunicação Social - Publicidade e Propaganda",
                    "Design - Moda", "Filosofia", "Gastronomia", "Música", "Teatro"
                ]
            },
            "IEFES": {
                "nome": "Instituto de Educação Física e Esportes",
                "cursos": ["Educação Física"]
            },
            "IUV": {
                "nome": "Instituto Universidade Virtual",
                "cursos": ["Sistemas e Mídias Digitais"]
            }
        }
    
    def normalizar_texto(self, texto):
        """Normaliza texto removendo acentos e convertendo para minúsculas"""
        import unicodedata
        # Remove acentos e converte para minúsculas
        texto_normalizado = unicodedata.normalize('NFD', texto.lower())
        texto_normalizado = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
        # Remove caracteres especiais como hífen, espaços extras
        texto_normalizado = ''.join(c if c.isalnum() else ' ' for c in texto_normalizado)
        # Remove espaços extras
        return ' '.join(texto_normalizado.split())
    
    def buscar_curso_flexivel(self, curso_digitado, unidade):
        """Busca curso de forma flexível (case insensitive e sem acentos)"""
        curso_normalizado = self.normalizar_texto(curso_digitado)
        
        for curso_oficial in self.unidades.get(unidade, {}).get('cursos', []):
            if self.normalizar_texto(curso_oficial) == curso_normalizado:
                return curso_oficial
        return None
    
    def buscar_unidade_flexivel(self, unidade_digitada):
        """Busca unidade de forma flexível"""
        unidade_upper = unidade_digitada.upper()
        
        # Primeiro tenta pela sigla
        if unidade_upper in self.unidades:
            return unidade_upper
        
        # Depois tenta pelo nome
        unidade_normalizada = self.normalizar_texto(unidade_digitada)
        for sigla, info in self.unidades.items():
            if self.normalizar_texto(info['nome']) == unidade_normalizada:
                return sigla
        
        return None
    
    def criar_calourada(self, nome, data_str, local, unidade, descricao=""):
        """Cria uma nova calourada universitária"""
        try:
            data = datetime.datetime.strptime(data_str, "%d/%m/%Y")
            
            # Verifica se a data não é no passado
            hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if data < hoje:
                return False, f"A data {data_str} é no passado. Escolha uma data futura."
            
            if unidade not in self.unidades:
                return False, "Unidade acadêmica não encontrada"
            
            # Incrementa contador para ID sequencial
            self.contador_eventos += 1
            
            calourada = Calourada(self.contador_eventos, nome, data, local, unidade, descricao)
            self.eventos.inserir(calourada, calourada.id)
            
            # Registra no histórico
            self.historico.inserir({
                'acao': 'CRIAR_CALOURADA',
                'calourada_id': calourada.id,
                'timestamp': datetime.datetime.now(),
                'detalhes': f"Calourada '{nome}' criada para {unidade}"
            })
            
            return True, f"Calourada '{nome}' criada com sucesso! ID: {calourada.id}"
        
        except ValueError:
            return False, "Data inválida. Use o formato DD/MM/AAAA"
        except Exception as e:
            return False, f"Erro ao criar calourada: {str(e)}"
    
    def demonstrar_interesse(self, calourada_id, nome, curso_digitado, unidade_digitada, sexo, periodo):
        """Registra interesse de um participante em uma calourada"""
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        # Busca unidade de forma flexível
        unidade = self.buscar_unidade_flexivel(unidade_digitada)
        if not unidade:
            return False, f"Unidade '{unidade_digitada}' não encontrada. Use uma das siglas: {', '.join(self.unidades.keys())}"
        
        # Busca curso de forma flexível
        curso = self.buscar_curso_flexivel(curso_digitado, unidade)
        if not curso:
            cursos_disponiveis = ', '.join(self.unidades[unidade]['cursos'])
            return False, f"Curso '{curso_digitado}' não encontrado na unidade {unidade}. Cursos disponíveis: {cursos_disponiveis}"
        
        if sexo not in ['M', 'F', 'O']:
            return False, "Sexo deve ser M (Masculino), F (Feminino) ou O (Outro)"
        
        try:
            periodo = int(periodo)
            if periodo < 1 or periodo > 12:
                return False, "Período deve ser entre 1 e 12"
        except ValueError:
            return False, "Período deve ser um número"
        
        participante = Participante(nome, curso, unidade, sexo, periodo)
        
        # Verifica se já demonstrou interesse (pelo nome - mais prático)
        ja_inscrito = calourada.participantes.buscar(lambda p: p.nome.lower() == nome.lower())
        ja_interessado = calourada.interessados.buscar(lambda p: p.nome.lower() == nome.lower())
        
        if ja_inscrito or ja_interessado:
            return False, "Participante já demonstrou interesse nesta calourada"
        
        # Adiciona à lista de participantes confirmados
        calourada.participantes.inserir(participante)
        
        # Registra no histórico
        self.historico.inserir({
            'acao': 'DEMONSTRAR_INTERESSE',
            'calourada_id': calourada_id,
            'participante': nome,
            'timestamp': datetime.datetime.now()
        })
        
        return True, f"Interesse de {nome} registrado com sucesso!"
    
    def cancelar_interesse(self, calourada_id, nome):
        """Cancela interesse de um participante"""
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        # Remove da lista principal
        removido = calourada.participantes.remover(lambda p: p.nome.lower() == nome.lower())
        
        if removido:
            self.historico.inserir({
                'acao': 'CANCELAR_INTERESSE',
                'calourada_id': calourada_id,
                'participante': nome,
                'timestamp': datetime.datetime.now()
            })
            
            return True, "Interesse cancelado com sucesso"
        
        # Remove da lista de interessados
        removido_interessados = False
        participantes_interessados = []
        
        # Reconstrói lista sem o participante
        while calourada.interessados.tamanho > 0:
            p = calourada.interessados.remover()
            if p.nome.lower() != nome.lower():
                participantes_interessados.append(p)
            else:
                removido_interessados = True
        
        # Reinsere participantes na lista
        for p in participantes_interessados:
            calourada.interessados.inserir(p)
        
        if removido_interessados:
            return True, "Interesse cancelado da lista de interessados"
        
        return False, "Participante não encontrado"
    
    def listar_calouradas(self):
        """Lista todas as calouradas em ordem"""
        calouradas = self.eventos.in_ordem()
        if not calouradas:
            return "Nenhuma calourada cadastrada"
        
        resultado = "=== CALOURADAS CADASTRADAS ===\n"
        for calourada in calouradas:
            resultado += f"ID: {calourada.id}\n"
            resultado += f"Nome: {calourada.nome}\n"
            resultado += f"Data: {calourada.data.strftime('%d/%m/%Y')}\n"
            resultado += f"Local: {calourada.local}\n"
            resultado += f"Unidade: {self.unidades[calourada.unidade_organizadora]['nome']}\n"
            resultado += f"Participantes interessados: {calourada.participantes.tamanho}\n"
            if calourada.descricao:
                resultado += f"Descrição: {calourada.descricao}\n"
            resultado += "-" * 40 + "\n"
        
        return resultado
    
    def listar_participantes(self, calourada_id):
        """Lista participantes de uma calourada específica"""
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return "Calourada não encontrada"
        
        resultado = f"=== PARTICIPANTES - {calourada.nome} ===\n"
        
        # Participantes que demonstraram interesse
        participantes = calourada.participantes.imprimir()
        if participantes:
            resultado += f"INTERESSADOS ({len(participantes)}):\n"
            for i, p in enumerate(participantes, 1):
                resultado += f"{i}. {p}\n"
        else:
            resultado += "Nenhum participante interessado ainda.\n"
        
        # Lista de interessados (pode ser usada para outros fins)
        interessados = calourada.interessados.imprimir()
        if interessados:
            resultado += f"\nLISTA DE CONTATOS ({len(interessados)}):\n"
            for i, p in enumerate(interessados, 1):
                resultado += f"{i}. {p}\n"
        
        return resultado
    
    def buscar_calourada(self, calourada_id):
        """Busca uma calourada específica"""
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return "Calourada não encontrada"
        
        resultado = f"=== DETALHES DA CALOURADA ===\n"
        resultado += f"ID: {calourada.id}\n"
        resultado += f"Nome: {calourada.nome}\n"
        resultado += f"Data: {calourada.data.strftime('%d/%m/%Y')}\n"
        resultado += f"Local: {calourada.local}\n"
        resultado += f"Unidade: {self.unidades[calourada.unidade_organizadora]['nome']}\n"
        resultado += f"Participantes interessados: {calourada.participantes.tamanho}\n"
        if calourada.descricao:
            resultado += f"Descrição: {calourada.descricao}\n"
        resultado += f"Criada em: {calourada.data_criacao.strftime('%d/%m/%Y %H:%M')}\n"
        
        return resultado
    
    def remover_calourada(self, calourada_id):
        """Remove uma calourada do sistema"""
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        self.eventos.remover(calourada_id)
        
        # Registra no histórico
        self.historico.inserir({
            'acao': 'REMOVER_CALOURADA',
            'calourada_id': calourada_id,
            'nome': calourada.nome,
            'timestamp': datetime.datetime.now()
        })
        
        return True, f"Calourada '{calourada.nome}' removida com sucesso"
    
    def ver_historico(self, limite=10):
        """Mostra histórico de operações"""
        if self.historico.tamanho == 0:
            return "Nenhuma operação registrada"
        
        resultado = f"=== HISTÓRICO DE OPERAÇÕES (últimas {limite}) ===\n"
        operacoes = self.historico.imprimir()[:limite]
        
        for op in operacoes:
            resultado += f"{op['timestamp'].strftime('%d/%m/%Y %H:%M')} - "
            resultado += f"{op['acao']}"
            
            if 'evento_id' in op:
                resultado += f" (ID: {op['evento_id']})"
            if 'calourada_id' in op:
                resultado += f" (ID: {op['calourada_id']})"
            if 'participante' in op:
                resultado += f" - {op['participante']}"
            if 'detalhes' in op:
                resultado += f" - {op['detalhes']}"
            
            resultado += "\n"
        
        return resultado
    
    def listar_unidades(self):
        """Lista todas as unidades acadêmicas e seus cursos"""
        resultado = "=== UNIDADES ACADÊMICAS - UFC CAMPUS PICI ===\n"
        
        for sigla, info in self.unidades.items():
            resultado += f"\n{sigla} - {info['nome']}\n"
            resultado += f"Cursos ({len(info['cursos'])}):\n"
            for curso in info['cursos']:
                resultado += f"  • {curso}\n"
        
        return resultado
    
    def estatisticas(self):
        """Gera estatísticas detalhadas do sistema"""
        calouradas = self.eventos.in_ordem()
        
        if not calouradas:
            return "Nenhuma calourada cadastrada para gerar estatísticas"
        
        total_calouradas = len(calouradas)
        total_participantes = sum(c.participantes.tamanho for c in calouradas)
        
        # Estatísticas gerais
        stats_sexo = {'M': 0, 'F': 0, 'O': 0}
        stats_periodo = {}
        stats_unidade = {}
        stats_curso = {}
        
        # Coleta dados de todos os participantes
        for calourada in calouradas:
            participantes = calourada.participantes.imprimir()
            
            for p in participantes:
                # Contagem por sexo
                stats_sexo[p.sexo] += 1
                
                # Contagem por período
                if p.periodo not in stats_periodo:
                    stats_periodo[p.periodo] = 0
                stats_periodo[p.periodo] += 1
                
                # Contagem por unidade
                if p.unidade not in stats_unidade:
                    stats_unidade[p.unidade] = 0
                stats_unidade[p.unidade] += 1
                
                # Contagem por curso
                if p.curso not in stats_curso:
                    stats_curso[p.curso] = 0
                stats_curso[p.curso] += 1
        
        # Estatísticas por calourada
        stats_por_calourada = {}
        for calourada in calouradas:
            unidade = calourada.unidade_organizadora
            if unidade not in stats_por_calourada:
                stats_por_calourada[unidade] = {'calouradas': 0, 'participantes': 0}
            stats_por_calourada[unidade]['calouradas'] += 1
            stats_por_calourada[unidade]['participantes'] += calourada.participantes.tamanho
        
        # Monta resultado
        resultado = "=== ESTATÍSTICAS DO SISTEMA ===\n"
        resultado += f"Total de calouradas: {total_calouradas}\n"
        resultado += f"Total de participantes interessados: {total_participantes}\n"
        resultado += f"Operações no histórico: {self.historico.tamanho}\n\n"
        
        # Distribuição por sexo
        if total_participantes > 0:
            resultado += "DISTRIBUIÇÃO POR SEXO:\n"
            for sexo, count in stats_sexo.items():
                nome_sexo = {'M': 'Masculino', 'F': 'Feminino', 'O': 'Outro'}[sexo]
                percentual = (count / total_participantes) * 100
                resultado += f"  - {nome_sexo}: {count} ({percentual:.1f}%)\n"
            resultado += "\n"
            
            # Top 5 períodos
            periodos_ordenados = sorted(stats_periodo.items(), key=lambda x: x[1], reverse=True)[:5]
            if periodos_ordenados:
                resultado += "TOP 5 PERÍODOS:\n"
                for periodo, count in periodos_ordenados:
                    percentual = (count / total_participantes) * 100
                    resultado += f"  - {periodo}º período: {count} ({percentual:.1f}%)\n"
                resultado += "\n"
            
            # Top 5 cursos
            cursos_ordenados = sorted(stats_curso.items(), key=lambda x: x[1], reverse=True)[:5]
            if cursos_ordenados:
                resultado += "TOP 5 CURSOS MAIS PARTICIPATIVOS:\n"
                for curso, count in cursos_ordenados:
                    percentual = (count / total_participantes) * 100
                    resultado += f"  - {curso}: {count} ({percentual:.1f}%)\n"
                resultado += "\n"
        
        # Por unidade acadêmica
        resultado += "POR UNIDADE ACADÊMICA:\n"
        for sigla, stats in stats_por_calourada.items():
            nome_unidade = self.unidades[sigla]['nome']
            participantes_unidade = stats_unidade.get(sigla, 0)
            resultado += f"{sigla} ({nome_unidade}):\n"
            resultado += f"  - Calouradas organizadas: {stats['calouradas']}\n"
            resultado += f"  - Participantes da própria unidade: {participantes_unidade}\n"
        
        return resultado

# =====================================================
# INTERFACE DO SISTEMA
# =====================================================

def menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*60)
    print("    🎉 SISTEMA DE GERENCIAMENTO DE CALOURADAS 🎉")
    print("                UFC - CAMPUS PICI")
    print("="*60)
    print("1.  🎉 Criar Calourada")
    print("2.  👋 Demonstrar Interesse")
    print("3.  ❌ Cancelar Interesse")
    print("4.  📋 Listar Calouradas")
    print("5.  👥 Listar Participantes de Calourada")
    print("6.  🔍 Buscar Calourada")
    print("7.  🗑️  Remover Calourada")
    print("8.  📜 Ver Histórico")
    print("9.  🏫 Listar Unidades e Cursos")
    print("10. 📊 Estatísticas")
    print("11. 🔧 Demonstrar Estruturas de Dados")
    print("0.  🚪 Sair")
    print("-"*60)

def demonstrar_estruturas(sistema):
    """Demonstra o funcionamento das estruturas de dados de forma interativa"""
    print("\n=== DEMONSTRAÇÃO INTERATIVA DAS ESTRUTURAS DE DADOS ===")
    print("Esta demonstração mostra como cada estrutura funciona no sistema real.")
    
    # Dados atuais do sistema
    calouradas = sistema.eventos.in_ordem()
    total_participantes = sum(c.participantes.tamanho for c in calouradas)
    
    print(f"\n📊 ESTADO ATUAL DO SISTEMA:")
    print(f"   • Calouradas cadastradas: {len(calouradas)}")
    print(f"   • Participantes interessados: {total_participantes}")
    print(f"   • Operações no histórico: {sistema.historico.tamanho}")
    
    # 1. ÁRVORE AVL - Demonstração mais detalhada
    print(f"\n🌳 1. ÁRVORE AVL (Organização eficiente de calouradas por ID)")
    print(f"   📋 Função: Busca rápida O(log n), inserção e remoção balanceadas")
    
    if len(calouradas) > 0:
        print(f"   📊 Estrutura atual:")
        for calourada in calouradas:
            participantes_str = f"({calourada.participantes.tamanho} participantes)" if calourada.participantes.tamanho > 0 else "(sem participantes)"
            print(f"     • ID {calourada.id}: {calourada.nome} {participantes_str}")
        
        print(f"   🔍 Percursos da árvore:")
        in_ordem = [f"ID {c.id}" for c in sistema.eventos.in_ordem()]
        pre_ordem = [f"ID {c.id}" for c in sistema.eventos.pre_ordem()]
        pos_ordem = [f"ID {c.id}" for c in sistema.eventos.pos_ordem()]
        
        print(f"     • In-ordem (crescente): {' → '.join(in_ordem)}")
        print(f"     • Pré-ordem (raiz primeiro): {' → '.join(pre_ordem)}")
        print(f"     • Pós-ordem (filhos primeiro): {' → '.join(pos_ordem)}")
        
        # Demonstração de busca
        print(f"   ⚡ Teste de busca eficiente:")
        if calouradas:
            teste_id = calouradas[0].id
            resultado = sistema.eventos.buscar(teste_id)
            print(f"     • Buscar ID {teste_id}: {'✓ Encontrado' if resultado else '✗ Não encontrado'} - {resultado.nome if resultado else 'N/A'}")
    else:
        print("     ⚠️  Nenhuma calourada cadastrada para demonstração")
    
    # 2. LISTA LIGADA - Participantes de cada calourada
    print(f"\n🔗 2. LISTA LIGADA (Participantes interessados em cada calourada)")
    print(f"   📋 Função: Inserção O(1), percurso sequencial, remoção por critério")
    
    if calouradas:
        for calourada in calouradas:
            participantes = calourada.participantes.imprimir()
            print(f"   📝 Calourada '{calourada.nome}' (ID {calourada.id}):")
            print(f"     • Tamanho da lista: {calourada.participantes.tamanho}")
            if participantes:
                print(f"     • Participantes (mais recente primeiro):")
                for i, p in enumerate(participantes[:3], 1):  # Mostra apenas os 3 primeiros
                    print(f"       {i}. {p.nome} - {p.curso} ({p.periodo}º período)")
                if len(participantes) > 3:
                    print(f"       ... e mais {len(participantes) - 3} participantes")
            else:
                print(f"     • Lista vazia")
    else:
        print("     ⚠️  Nenhuma calourada para demonstrar listas")
    
    # 3. PILHA - Histórico de operações
    print(f"\n📚 3. PILHA (Histórico de operações - LIFO)")
    print(f"   📋 Função: Última operação primeiro, controle de histórico")
    print(f"   📊 Tamanho atual: {sistema.historico.tamanho}")
    
    if sistema.historico.tamanho > 0:
        operacoes = sistema.historico.imprimir()[:5]
        print(f"   ⏰ Últimas 5 operações (mais recente no topo):")
        for i, op in enumerate(operacoes, 1):
            acao_emoji = {
                'CRIAR_CALOURADA': '🎉',
                'DEMONSTRAR_INTERESSE': '👋',
                'CANCELAR_INTERESSE': '❌',
                'REMOVER_CALOURADA': '🗑️'
            }.get(op['acao'], '📝')
            
            detalhes = ""
            if 'detalhes' in op:
                detalhes = f" - {op['detalhes']}"
            elif 'participante' in op:
                detalhes = f" - {op['participante']}"
            
            print(f"     {i}. {acao_emoji} {op['acao']} {detalhes}")
            print(f"        ⏱️  {op['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}")
        
        print(f"   🔄 Demonstração de remoção (pop):")
        print(f"     • Próxima operação a ser removida: {operacoes[0]['acao']}")
    else:
        print("     ⚠️  Histórico vazio")
    
    # 4. FILA - Demonstração conceitual
    print(f"\n🚶 4. FILA (Lista de contatos para comunicação - FIFO)")
    print(f"   📋 Função: Primeiro a entrar, primeiro a sair - controle de notificações")
    
    # Conta filas de todas as calouradas
    total_filas = sum(c.interessados.tamanho for c in calouradas)
    print(f"   📊 Total de contatos em todas as filas: {total_filas}")
    
    if calouradas:
        for calourada in calouradas:
            if calourada.interessados.tamanho > 0:
                interessados = calourada.interessados.imprimir()
                print(f"   📧 Fila de notificações '{calourada.nome}':")
                print(f"     • Tamanho: {calourada.interessados.tamanho}")
                for i, p in enumerate(interessados[:2], 1):
                    print(f"       {i}. {p.nome} - {p.curso}")
                if len(interessados) > 2:
                    print(f"       ... e mais {len(interessados) - 2} na fila")
    
    # Demonstração prática se houver dados
    if total_participantes > 0:
        print(f"\n💡 DEMONSTRAÇÃO PRÁTICA:")
        print(f"   🔍 Busca rápida por ID na Árvore AVL: O(log n)")
        print(f"   ➕ Inserção de novo participante na Lista: O(1)")
        print(f"   📝 Registro de operação na Pilha: O(1)")
        print(f"   📧 Enfileiramento para notificação: O(1)")
        print(f"   ⚡ Total de operações realizadas: {sistema.historico.tamanho}")
    
    print(f"\n🎯 VANTAGENS DE CADA ESTRUTURA NO SISTEMA:")
    print(f"   🌳 Árvore AVL: Busca eficiente de calouradas mesmo com muitos eventos")
    print(f"   🔗 Lista Ligada: Flexibilidade para adicionar/remover participantes")
    print(f"   📚 Pilha: Rastreamento cronológico de ações para auditoria")
    print(f"   🚶 Fila: Ordem justa para notificações e comunicações")

def main():
    """Função principal do sistema"""
    sistema = SistemaCalourada()
    
    print("Bem-vindo ao Sistema de Gerenciamento de Calouradas!")
    print("UFC - Campus Pici")
    print("💡 Dica: Para cancelar qualquer operação, deixe o campo vazio e pressione Enter")
    
    while True:
        try:
            menu_principal()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "0":
                print("\nObrigado por usar o Sistema de Calouradas!")
                print("Até logo! 🎉")
                break
            
            elif opcao == "1":  # Criar Calourada
                print("\n=== CRIAR NOVA CALOURADA ===")
                print("💡 Pressione Enter em qualquer campo para voltar ao menu")
                
                nome = input("🎉 Nome da calourada: ").strip()
                if not nome:
                    print("↩️  Voltando ao menu principal...")
                    continue
                    
                data = input("📅 Data (DD/MM/AAAA): ").strip()
                if not data:
                    print("↩️  Voltando ao menu principal...")
                    continue
                    
                local = input("📍 Local: ").strip()
                if not local:
                    print("↩️  Voltando ao menu principal...")
                    continue
                
                print("\n🏫 UNIDADES ACADÊMICAS:")
                for sigla, info in sistema.unidades.items():
                    print(f"  {sigla} - {info['nome']}")
                
                unidade_input = input("\n🏫 Sigla da unidade organizadora: ").strip()
                if not unidade_input:
                    print("↩️  Voltando ao menu principal...")
                    continue
                
                unidade = sistema.buscar_unidade_flexivel(unidade_input)
                if not unidade:
                    print(f"✗ Unidade '{unidade_input}' não encontrada!")
                    continue
                
                descricao = input("📝 Descrição (opcional): ").strip()
                
                sucesso, mensagem = sistema.criar_calourada(nome, data, local, unidade, descricao)
                print(f"\n{'🎉 ' if sucesso else '✗ '} {mensagem}")
            
            elif opcao == "2":  # Demonstrar Interesse
                print("\n=== DEMONSTRAR INTERESSE ===")
                print("💡 Pressione Enter em qualquer campo para voltar ao menu")
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    print("✗ Não há calouradas disponíveis para demonstrar interesse.")
                    continue
                
                try:
                    calourada_id_input = input("ID da calourada: ").strip()
                    if not calourada_id_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    calourada_id = int(calourada_id_input)
                    
                    # Busca a calourada para mostrar informações
                    calourada = sistema.eventos.buscar(calourada_id)
                    if not calourada:
                        print("✗ Calourada não encontrada!")
                        continue
                    
                    print(f"\n🎉 Demonstrando interesse na: {calourada.nome}")
                    print(f"📅 Data: {calourada.data.strftime('%d/%m/%Y')}")
                    print(f"📍 Local: {calourada.local}")
                    print(f"🏛️  Organizada por: {sistema.unidades[calourada.unidade_organizadora]['nome']}")
                    
                    print("\n--- SEUS DADOS ---")
                    nome = input("👤 Seu nome: ").strip()
                    if not nome:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    print("\n🏫 UNIDADES ACADÊMICAS (digite a sigla ou nome completo):")
                    for sigla, info in sistema.unidades.items():
                        print(f"  {sigla} - {info['nome']}")
                    
                    unidade_input = input("\n🏫 Sua unidade: ").strip()
                    if not unidade_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    # Valida unidade primeiro para mostrar cursos específicos
                    unidade_validada = sistema.buscar_unidade_flexivel(unidade_input)
                    if not unidade_validada:
                        print(f"✗ Unidade '{unidade_input}' não encontrada!")
                        continue
                    
                    print(f"\n📚 CURSOS DO {unidade_validada} (digite o número ou nome do curso):")
                    cursos_unidade = sistema.unidades[unidade_validada]['cursos']
                    for i, curso in enumerate(cursos_unidade, 1):
                        print(f"  {i}. {curso}")
                    
                    curso_input = input("\n📚 Seu curso (número ou nome): ").strip()
                    if not curso_input:
                        print("✗ Curso é obrigatório!")
                        continue
                    
                    # Verifica se o input é um número (seleção por índice)
                    curso_escolhido = None
                    try:
                        indice = int(curso_input)
                        if 1 <= indice <= len(cursos_unidade):
                            curso_escolhido = cursos_unidade[indice - 1]
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(cursos_unidade)}")
                            continue
                    except ValueError:
                        # Se não for número, busca por nome usando a função flexível
                        curso_escolhido = sistema.buscar_curso_flexivel(curso_input, unidade_validada)
                        if not curso_escolhido:
                            print(f"✗ Curso '{curso_input}' não encontrado!")
                            continue
                    
                    # Atualiza curso_input com o nome oficial do curso
                    curso_input = curso_escolhido
                    
                    print("\n👥 Sexo:")
                    print("  M - Masculino")
                    print("  F - Feminino") 
                    print("  O - Outro")
                    sexo = input("👥 Selecione (M/F/O): ").strip().upper()
                    
                    if sexo not in ['M', 'F', 'O']:
                        print("✗ Sexo deve ser M, F ou O!")
                        continue
                    
                    periodo = input("📖 Período do curso (1-12): ").strip()
                    
                    sucesso, mensagem = sistema.demonstrar_interesse(calourada_id, nome, curso_input, unidade_input, sexo, periodo)
                    print(f"\n{'🎉 ' if sucesso else '✗ '} {mensagem}")
                    
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "3":  # Cancelar Interesse
                print("\n=== CANCELAR INTERESSE ===")
                print("💡 Pressione Enter em qualquer campo para voltar ao menu")
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    print("✗ Não há calouradas disponíveis.")
                    continue
                
                try:
                    calourada_id_input = input("ID da calourada: ").strip()
                    if not calourada_id_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    calourada_id = int(calourada_id_input)
                    
                    # Busca a calourada para mostrar participantes
                    calourada = sistema.eventos.buscar(calourada_id)
                    if not calourada:
                        print("✗ Calourada não encontrada!")
                        continue
                    
                    print(f"\n🎉 Calourada: {calourada.nome}")
                    participantes = calourada.participantes.imprimir()
                    
                    if not participantes:
                        print("✗ Nenhum participante nesta calourada ainda.")
                        continue
                    
                    print("\n👥 PARTICIPANTES INTERESSADOS:")
                    for i, p in enumerate(participantes, 1):
                        print(f"  {i}. {p.nome}")
                    
                    participante_input = input("\n👤 Participante para cancelar (número ou nome): ").strip()
                    if not participante_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    # Verifica se o input é um número (seleção por índice)
                    nome_participante = None
                    try:
                        indice = int(participante_input)
                        if 1 <= indice <= len(participantes):
                            nome_participante = participantes[indice - 1].nome
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(participantes)}")
                            continue
                    except ValueError:
                        # Se não for número, usa o nome digitado
                        nome_participante = participante_input
                    
                    sucesso, mensagem = sistema.cancelar_interesse(calourada_id, nome_participante)
                    print(f"\n{'✓ ' if sucesso else '✗ '} {mensagem}")
                    
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "4":  # Listar Calouradas
                print("\n" + sistema.listar_calouradas())
            
            elif opcao == "5":  # Listar Participantes
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    print("\n" + sistema.listar_participantes(calourada_id))
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "6":  # Buscar Calourada
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    print("\n" + sistema.buscar_calourada(calourada_id))
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "7":  # Remover Calourada
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    
                    # Mostra detalhes antes de remover
                    calourada = sistema.eventos.buscar(calourada_id)
                    if not calourada:
                        print("✗ Calourada não encontrada!")
                        continue
                    
                    print(f"\n⚠️  Você está prestes a remover:")
                    print(f"🎉 {calourada.nome}")
                    print(f"📅 {calourada.data.strftime('%d/%m/%Y')}")
                    print(f"👥 {calourada.participantes.tamanho} participantes interessados")
                    
                    confirmacao = input("\n❓ Tem certeza? (s/N): ").lower()
                    
                    if confirmacao == 's':
                        sucesso, mensagem = sistema.remover_calourada(calourada_id)
                        print(f"\n{'✓ ' if sucesso else '✗ '} {mensagem}")
                    else:
                        print("\n✓ Operação cancelada")
                        
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "8":  # Ver Histórico
                try:
                    limite = input("Quantas operações mostrar? (padrão 10): ")
                    limite = int(limite) if limite else 10
                    print("\n" + sistema.ver_historico(limite))
                except ValueError:
                    print("\n" + sistema.ver_historico())
            
            elif opcao == "9":  # Listar Unidades
                print("\n" + sistema.listar_unidades())
            
            elif opcao == "10":  # Estatísticas
                print("\n" + sistema.estatisticas())
            
            elif opcao == "11":  # Demonstrar Estruturas
                demonstrar_estruturas(sistema)
            
            else:
                print("\n✗ Opção inválida! Tente novamente.")
            
            if opcao != "0":
                input("\nPressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            break
        except Exception as e:
            print(f"\n✗ Erro inesperado: {str(e)}")
            print("Tente novamente ou contacte o suporte.")

if __name__ == "__main__":
    main()