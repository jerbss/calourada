import datetime
import unicodedata

class NoLista:
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class ListaLigada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def inserir(self, dados):
        novo_no = NoLista(dados)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1
        return True
    
    def remover(self, criterio_busca):
        if not self.cabeca:
            return False
        
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
        atual = self.cabeca
        while atual:
            if criterio_busca(atual.dados):
                return atual.dados
            atual = atual.proximo
        return None
    
    def imprimir(self):
        elementos = []
        atual = self.cabeca
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class NoPilha:
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None

class Pilha:
    def __init__(self):
        self.topo = None
        self.tamanho = 0
    
    def inserir(self, dados):
        novo_no = NoPilha(dados)
        novo_no.proximo = self.topo
        self.topo = novo_no
        self.tamanho += 1
        return True
    
    def buscar(self, criterio_busca):
        atual = self.topo
        while atual:
            if criterio_busca(atual.dados):
                return atual.dados
            atual = atual.proximo
        return None
    
    def remover(self):
        if not self.topo:
            return None
            
        dados = self.topo.dados
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return dados
    
    def imprimir(self):
        elementos = []
        atual = self.topo
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class NoAVL:
    def __init__(self, dados, chave):
        self.dados = dados
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None
    
    def _altura(self, no):
        if not no:
            return 0
        return no.altura
    
    def _balanceamento(self, no):
        if not no:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)
    
    def _rotacao_direita(self, y):
        x = y.esquerda
        t2 = x.direita
        
        x.direita = y
        y.esquerda = t2
        
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        
        return x
    
    def _rotacao_esquerda(self, x):
        y = x.direita
        t2 = y.esquerda
        
        y.esquerda = x
        x.direita = t2
        
        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        
        return y
    
    def inserir(self, dados, chave):
        self.raiz = self._inserir_recursivo(self.raiz, dados, chave)
        return True
    
    def _inserir_recursivo(self, raiz, dados, chave):
        if not raiz:
            return NoAVL(dados, chave)
        
        if chave < raiz.chave:
            raiz.esquerda = self._inserir_recursivo(raiz.esquerda, dados, chave)
        elif chave > raiz.chave:
            raiz.direita = self._inserir_recursivo(raiz.direita, dados, chave)
        else:
            raiz.dados = dados
            return raiz
        
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        
        balance = self._balanceamento(raiz)
        
        if balance > 1 and chave < raiz.esquerda.chave:
            return self._rotacao_direita(raiz)
        
        if balance < -1 and chave > raiz.direita.chave:
            return self._rotacao_esquerda(raiz)
        
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
        if not raiz:
            return raiz
        
        if chave < raiz.chave:
            raiz.esquerda = self._remover_recursivo(raiz.esquerda, chave)
        elif chave > raiz.chave:
            raiz.direita = self._remover_recursivo(raiz.direita, chave)
        else:
            if not raiz.esquerda or not raiz.direita:
                temp = raiz.esquerda if raiz.esquerda else raiz.direita
                if not temp:
                    temp = raiz
                    raiz = None
                else:
                    raiz = temp
            else:
                temp = self._menor_valor(raiz.direita)
                raiz.chave = temp.chave
                raiz.dados = temp.dados
                raiz.direita = self._remover_recursivo(raiz.direita, temp.chave)
        
        if not raiz:
            return raiz
        
        raiz.altura = 1 + max(self._altura(raiz.esquerda), self._altura(raiz.direita))
        balance = self._balanceamento(raiz)
        
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
        if not raiz.esquerda:
            return raiz
        return self._menor_valor(raiz.esquerda)
    
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
    
    def visualizar_arvore(self):
        if not self.raiz:
            return "Árvore vazia"
        
        linhas = []
        self._desenhar_arvore(self.raiz, "", True, linhas)
        return "\n".join(linhas)
    
    def _desenhar_arvore(self, no, prefixo, eh_ultimo, linhas):
        if no is not None:
            conector = "└── " if eh_ultimo else "├── "
            balance = self._balanceamento(no)
            info_no = f"ID:{no.chave} (h:{no.altura}, b:{balance:+d})"
            linhas.append(prefixo + conector + info_no)
            
            extensao = "    " if eh_ultimo else "│   "
            novo_prefixo = prefixo + extensao
            
            tem_esquerda = no.esquerda is not None
            tem_direita = no.direita is not None
            
            if tem_direita:
                self._desenhar_arvore(no.direita, novo_prefixo, not tem_esquerda, linhas)
            
            if tem_esquerda:
                self._desenhar_arvore(no.esquerda, novo_prefixo, True, linhas)
    
    def nivel_arvore(self):
        return self._altura(self.raiz)
    
    def contar_nos(self):
        return self._contar_nos_recursivo(self.raiz)
    
    def _contar_nos_recursivo(self, no):
        if not no:
            return 0
        return 1 + self._contar_nos_recursivo(no.esquerda) + self._contar_nos_recursivo(no.direita)

class Participante:
    def __init__(self, nome, curso, unidade, sexo, periodo):
        self.nome = nome
        self.curso = curso
        self.unidade = unidade
        self.sexo = sexo
        self.periodo = periodo
        self.data_interesse = datetime.datetime.now()
    
    def __str__(self):
        return f"{self.nome} - {self.curso}/{self.unidade} ({self.periodo}º período)"

class Calourada:
    def __init__(self, id_sequencial, nome, data, local, unidade_organizadora, descricao=""):
        self.id = id_sequencial
        self.nome = nome
        self.data = data
        self.local = local
        self.unidade_organizadora = unidade_organizadora
        self.descricao = descricao
        self.participantes = ListaLigada()
        self.data_criacao = datetime.datetime.now()
    
    def __str__(self):
        return f"{self.nome} - {self.data} ({self.unidade_organizadora})"

class SistemaCalourada:
    def __init__(self):
        self.eventos = ArvoreAVL()
        self.historico = Pilha()
        self.contador_eventos = 0
        
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
        texto_normalizado = unicodedata.normalize('NFD', texto.lower())
        texto_normalizado = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
        texto_normalizado = ''.join(c if c.isalnum() else ' ' for c in texto_normalizado)
        return ' '.join(texto_normalizado.split())
    
    def buscar_curso_flexivel(self, curso_digitado, unidade):
        curso_normalizado = self.normalizar_texto(curso_digitado)
        
        for curso_oficial in self.unidades.get(unidade, {}).get('cursos', []):
            if self.normalizar_texto(curso_oficial) == curso_normalizado:
                return curso_oficial
        return None
    
    def buscar_unidade_flexivel(self, unidade_digitada):
        unidade_upper = unidade_digitada.upper()
        
        if unidade_upper in self.unidades:
            return unidade_upper
        
        unidade_normalizada = self.normalizar_texto(unidade_digitada)
        for sigla, info in self.unidades.items():
            if self.normalizar_texto(info['nome']) == unidade_normalizada:
                return sigla
        
        return None
    
    def criar_calourada(self, nome, data_str, local, unidade, descricao=""):
        try:
            data = datetime.datetime.strptime(data_str, "%d/%m/%Y")
            
            hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if data < hoje:
                return False, f"A data {data_str} é no passado. Escolha uma data futura."
            
            if unidade not in self.unidades:
                return False, "Unidade acadêmica não encontrada"
            
            self.contador_eventos += 1
            
            calourada = Calourada(self.contador_eventos, nome, data, local, unidade, descricao)
            self.eventos.inserir(calourada, calourada.id)
            
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
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        unidade = self.buscar_unidade_flexivel(unidade_digitada)
        if not unidade:
            return False, f"Unidade '{unidade_digitada}' não encontrada. Use uma das siglas: {', '.join(self.unidades.keys())}"
        
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
        
        ja_inscrito = calourada.participantes.buscar(lambda p: p.nome.lower() == nome.lower())
        
        if ja_inscrito:
            return False, "Participante já demonstrou interesse nesta calourada"
        
        calourada.participantes.inserir(participante)
        
        self.historico.inserir({
            'acao': 'DEMONSTRAR_INTERESSE',
            'calourada_id': calourada_id,
            'participante': nome,
            'timestamp': datetime.datetime.now()
        })
        
        return True, f"Interesse de {nome} registrado com sucesso!"
    
    def cancelar_interesse(self, calourada_id, nome):
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        removido = calourada.participantes.remover(lambda p: p.nome.lower() == nome.lower())
        
        if removido:
            self.historico.inserir({
                'acao': 'CANCELAR_INTERESSE',
                'calourada_id': calourada_id,
                'participante': nome,
                'timestamp': datetime.datetime.now()
            })
            
            return True, "Interesse cancelado com sucesso"
        
        return False, "Participante não encontrado"
    
    def listar_calouradas(self):
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
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return "Calourada não encontrada"
        
        resultado = f"=== PARTICIPANTES - {calourada.nome} ===\n"
        
        participantes = calourada.participantes.imprimir()
        if participantes:
            resultado += f"INTERESSADOS ({len(participantes)}):\n"
            for i, p in enumerate(participantes, 1):
                resultado += f"{i}. {p}\n"
        else:
            resultado += "Nenhum participante interessado ainda.\n"
        
        return resultado
    
    def buscar_calourada(self, calourada_id):
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



    def listar_unidades(self):
        resultado = "=== UNIDADES ACADÊMICAS - UFC CAMPUS PICI ===\n"
        
        for sigla, info in self.unidades.items():
            resultado += f"\n{sigla} - {info['nome']}\n"
            resultado += f"Cursos ({len(info['cursos'])}):\n"
            for curso in info['cursos']:
                resultado += f"  • {curso}\n"
        
        return resultado
    
    def estatisticas(self):
        calouradas = self.eventos.in_ordem()
        
        if not calouradas:
            return "Nenhuma calourada cadastrada para gerar estatísticas"
        
        total_calouradas = len(calouradas)
        total_participantes = sum(c.participantes.tamanho for c in calouradas)
        
        stats_sexo = {'M': 0, 'F': 0, 'O': 0}
        stats_periodo = {}
        stats_unidade = {}
        stats_curso = {}
        
        for calourada in calouradas:
            participantes = calourada.participantes.imprimir()
            
            for p in participantes:
                stats_sexo[p.sexo] += 1
                
                if p.periodo not in stats_periodo:
                    stats_periodo[p.periodo] = 0
                stats_periodo[p.periodo] += 1
                
                if p.unidade not in stats_unidade:
                    stats_unidade[p.unidade] = 0
                stats_unidade[p.unidade] += 1
                
                if p.curso not in stats_curso:
                    stats_curso[p.curso] = 0
                stats_curso[p.curso] += 1
        
        stats_por_calourada = {}
        for calourada in calouradas:
            unidade = calourada.unidade_organizadora
            if unidade not in stats_por_calourada:
                stats_por_calourada[unidade] = {'calouradas': 0, 'participantes': 0}
            stats_por_calourada[unidade]['calouradas'] += 1
            stats_por_calourada[unidade]['participantes'] += calourada.participantes.tamanho
        
        resultado = "=== ESTATÍSTICAS DO SISTEMA ===\n"
        resultado += f"Total de calouradas: {total_calouradas}\n"
        resultado += f"Total de participantes interessados: {total_participantes}\n"
        resultado += f"Operações no histórico: {self.historico.tamanho}\n\n"
        
        if total_participantes > 0:
            resultado += "DISTRIBUIÇÃO POR SEXO:\n"
            for sexo, count in stats_sexo.items():
                nome_sexo = {'M': 'Masculino', 'F': 'Feminino', 'O': 'Outro'}[sexo]
                percentual = (count / total_participantes) * 100
                resultado += f"  - {nome_sexo}: {count} ({percentual:.1f}%)\n"
            resultado += "\n"
            
            periodos_ordenados = sorted(stats_periodo.items(), key=lambda x: x[1], reverse=True)[:5]
            if periodos_ordenados:
                resultado += "TOP 5 PERÍODOS:\n"
                for periodo, count in periodos_ordenados:
                    percentual = (count / total_participantes) * 100
                    resultado += f"  - {periodo}º período: {count} ({percentual:.1f}%)\n"
                resultado += "\n"
            
            cursos_ordenados = sorted(stats_curso.items(), key=lambda x: x[1], reverse=True)[:5]
            if cursos_ordenados:
                resultado += "TOP 5 CURSOS MAIS PARTICIPATIVOS:\n"
                for curso, count in cursos_ordenados:
                    percentual = (count / total_participantes) * 100
                    resultado += f"  - {curso}: {count} ({percentual:.1f}%)\n"
                resultado += "\n"
        
        resultado += "POR UNIDADE ACADÊMICA:\n"
        for sigla, stats in stats_por_calourada.items():
            nome_unidade = self.unidades[sigla]['nome']
            participantes_unidade = stats_unidade.get(sigla, 0)
            resultado += f"{sigla} ({nome_unidade}):\n"
            resultado += f"  - Calouradas organizadas: {stats['calouradas']}\n"
            resultado += f"  - Participantes da própria unidade: {participantes_unidade}\n"
        
        return resultado

    def remover_calourada(self, calourada_id):
        calourada = self.eventos.buscar(calourada_id)
        if not calourada:
            return False, "Calourada não encontrada"
        
        nome_calourada = calourada.nome
        
        removido = self.eventos.remover(calourada_id)
        
        if removido:
            self.historico.inserir({
                'acao': 'REMOVER_CALOURADA',
                'calourada_id': calourada_id,
                'timestamp': datetime.datetime.now(),
                'detalhes': f"Calourada '{nome_calourada}' (ID: {calourada_id}) foi removida"
            })
            return True, f"Calourada '{nome_calourada}' removida com sucesso"
        
        return False, "Falha ao remover a calourada"

    def ver_historico(self, limite=10):
        historico_completo = self.historico.imprimir()
        
        if not historico_completo:
            return "Nenhuma operação no histórico"
        
        resultado = f"=== HISTÓRICO DE OPERAÇÕES (últimas {min(limite, len(historico_completo))}) ===\n"
        
        for i, operacao in enumerate(historico_completo[:limite], 1):
            timestamp = operacao['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
            resultado += f"{i}. [{timestamp}] {operacao['acao']}\n"
            
            if 'detalhes' in operacao:
                resultado += f"   Detalhes: {operacao['detalhes']}\n"
            elif 'calourada_id' in operacao:
                resultado += f"   ID da Calourada: {operacao['calourada_id']}\n"
            
            if 'participante' in operacao:
                resultado += f"   Participante: {operacao['participante']}\n"
        
        return resultado
        
    def desfazer_ultima_operacao(self):
        if self.historico.tamanho == 0:
            return False, "Não há operações no histórico para desfazer"
        
        ultima_operacao = self.historico.remover()
        
        if not ultima_operacao:
            return False, "Falha ao recuperar a última operação"
        
        acao = ultima_operacao['acao']
        mensagem = f"Operação '{acao}' desfeita com sucesso"
        
        # Dependendo do tipo de ação desfeita, podemos precisar reverter outras mudanças no sistema
        if acao == 'CRIAR_CALOURADA' and 'calourada_id' in ultima_operacao:
            self.eventos.remover(ultima_operacao['calourada_id'])
            mensagem = f"Calourada de ID {ultima_operacao['calourada_id']} removida ao desfazer criação"
            
        elif acao == 'DEMONSTRAR_INTERESSE' and 'calourada_id' in ultima_operacao and 'participante' in ultima_operacao:
            calourada = self.eventos.buscar(ultima_operacao['calourada_id'])
            if calourada:
                calourada.participantes.remover(lambda p: p.nome == ultima_operacao['participante'])
                mensagem = f"Interesse de {ultima_operacao['participante']} cancelado ao desfazer"
                
        elif acao == 'CANCELAR_INTERESSE':
            mensagem = "Operação de cancelamento de interesse desfeita, mas o participante precisa demonstrar interesse novamente"
            
        elif acao == 'REMOVER_CALOURADA':
            mensagem = "Operação de remoção de calourada desfeita, mas a calourada precisa ser criada novamente"
        
        # Registramos a operação de desfazer no histórico
        self.historico.inserir({
            'acao': 'DESFAZER',
            'timestamp': datetime.datetime.now(),
            'detalhes': f"Desfeita operação: {acao}"
        })
        
        return True, mensagem
        
    def buscar_no_historico(self, termo_busca, tipo_busca="acao"):
        """
        Busca operações específicas no histórico usando o método buscar da Pilha
        
        Parâmetros:
        - termo_busca: Termo a ser pesquisado
        - tipo_busca: Tipo de busca (acao, participante, calourada_id)
        
        Retorna:
        - Uma string formatada com os resultados da busca
        """
        if self.historico.tamanho == 0:
            return "Histórico vazio. Nenhuma operação para pesquisar."
            
        termo_busca_lower = str(termo_busca).lower()
        
        # Função que implementa o critério de busca para o método buscar da Pilha
        def criterio_busca(operacao):
            if tipo_busca == "acao":
                return termo_busca_lower in operacao.get('acao', '').lower()
            elif tipo_busca == "participante" and 'participante' in operacao:
                return termo_busca_lower in operacao.get('participante', '').lower()
            elif tipo_busca == "calourada_id" and 'calourada_id' in operacao:
                return str(operacao.get('calourada_id', '')) == termo_busca_lower
            elif tipo_busca == "detalhes" and 'detalhes' in operacao:
                return termo_busca_lower in operacao.get('detalhes', '').lower()
            return False
        
        # Usamos o método buscar da Pilha para encontrar a primeira ocorrência
        resultado = self.historico.buscar(criterio_busca)
        
        if not resultado:
            return f"Nenhuma operação encontrada com o termo '{termo_busca}' no campo '{tipo_busca}'."
        
        # Para encontrar todas as ocorrências, precisamos percorrer todo o histórico
        todas_ocorrencias = []
        historico_completo = self.historico.imprimir()
        
        for operacao in historico_completo:
            if criterio_busca(operacao):
                todas_ocorrencias.append(operacao)
        
        # Formatamos o resultado
        resultado_txt = f"=== RESULTADOS DA PESQUISA NO HISTÓRICO ===\n"
        resultado_txt += f"Termo pesquisado: '{termo_busca}' no campo '{tipo_busca}'\n"
        resultado_txt += f"Ocorrências encontradas: {len(todas_ocorrencias)}\n\n"
        
        for i, operacao in enumerate(todas_ocorrencias, 1):
            timestamp = operacao['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
            resultado_txt += f"{i}. [{timestamp}] {operacao['acao']}\n"
            
            if 'detalhes' in operacao:
                resultado_txt += f"   Detalhes: {operacao['detalhes']}\n"
            elif 'calourada_id' in operacao:
                resultado_txt += f"   ID da Calourada: {operacao['calourada_id']}\n"
            
            if 'participante' in operacao:
                resultado_txt += f"   Participante: {operacao['participante']}\n"
                
        return resultado_txt

def menu_principal():
    print("\n" + "="*60)
    print("    🎉 SISTEMA DE GERENCIAMENTO DE CALOURADAS 🎉")
    print("                UFC - CAMPUS PICI")
    print("="*60)
    print("=== GERENCIAMENTO DE CALOURADAS ===")
    print("1.  🎉 Criar Calourada")
    print("2.  � Buscar Calourada")
    print("3.  📋 Listar Calouradas")
    print("4.  🗑️  Remover Calourada")
    print("\n=== GERENCIAMENTO DE PARTICIPANTES ===")
    print("5.  👋 Demonstrar Interesse")
    print("6.  ❌ Cancelar Interesse")
    print("7.  👥 Listar Participantes de Calourada")
    print("\n=== HISTÓRICO E OPERAÇÕES ===")
    print("8.  � Ver Histórico")
    print("9.  � Pesquisar no Histórico")
    print("10. ↩️  Desfazer Última Operação")
    print("\n0.  🚪 Sair")
    print("-"*60)





def main():
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
            
            elif opcao == "2":  # Buscar Calourada
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    print("\n" + sistema.buscar_calourada(calourada_id))
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    print("✗ Não há calouradas disponíveis para demonstrar interesse.")
                    continue
                
                try:
                    calourada_id_input = input("ID da calourada: ").strip()
                    if not calourada_id_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    calourada_id = int(calourada_id_input)
                    
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
                    
                    curso_escolhido = None
                    try:
                        indice = int(curso_input)
                        if 1 <= indice <= len(cursos_unidade):
                            curso_escolhido = cursos_unidade[indice - 1]
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(cursos_unidade)}")
                            continue
                    except ValueError:
                        curso_escolhido = sistema.buscar_curso_flexivel(curso_input, unidade_validada)
                        if not curso_escolhido:
                            print(f"✗ Curso '{curso_input}' não encontrado!")
                            continue
                    
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
            
            elif opcao == "3":  # Listar Calouradas
                print("\n" + sistema.listar_calouradas())
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    print("✗ Não há calouradas disponíveis.")
                    continue
                
                try:
                    calourada_id_input = input("ID da calourada: ").strip()
                    if not calourada_id_input:
                        print("↩️  Voltando ao menu principal...")
                        continue
                    
                    calourada_id = int(calourada_id_input)
                    
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
                    
                    nome_participante = None
                    try:
                        indice = int(participante_input)
                        if 1 <= indice <= len(participantes):
                            nome_participante = participantes[indice - 1].nome
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(participantes)}")
                            continue
                    except ValueError:
                        nome_participante = participante_input
                    
                    sucesso, mensagem = sistema.cancelar_interesse(calourada_id, nome_participante)
                    print(f"\n{'✓ ' if sucesso else '✗ '} {mensagem}")
                    
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "4":  # Remover Calourada
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    
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
            
            elif opcao == "5":  # Demonstrar Interesse
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
                    
                    curso_escolhido = None
                    try:
                        indice = int(curso_input)
                        if 1 <= indice <= len(cursos_unidade):
                            curso_escolhido = cursos_unidade[indice - 1]
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(cursos_unidade)}")
                            continue
                    except ValueError:
                        curso_escolhido = sistema.buscar_curso_flexivel(curso_input, unidade_validada)
                        if not curso_escolhido:
                            print(f"✗ Curso '{curso_input}' não encontrado!")
                            continue
                    
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
            
            elif opcao == "6":  # Cancelar Interesse
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
                    
                    nome_participante = None
                    try:
                        indice = int(participante_input)
                        if 1 <= indice <= len(participantes):
                            nome_participante = participantes[indice - 1].nome
                        else:
                            print(f"✗ Número inválido! Digite um número entre 1 e {len(participantes)}")
                            continue
                    except ValueError:
                        nome_participante = participante_input
                    
                    sucesso, mensagem = sistema.cancelar_interesse(calourada_id, nome_participante)
                    print(f"\n{'✓ ' if sucesso else '✗ '} {mensagem}")
                    
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "7":  # Listar Participantes de Calourada
                calouradas_disponiveis = sistema.listar_calouradas()
                print(calouradas_disponiveis)
                
                if "Nenhuma calourada cadastrada" in calouradas_disponiveis:
                    continue
                
                try:
                    calourada_id = int(input("ID da calourada: "))
                    print("\n" + sistema.listar_participantes(calourada_id))
                except ValueError:
                    print("\n✗ ID da calourada deve ser um número")
            
            elif opcao == "8":  # Ver Histórico
                try:
                    limite = input("Quantas operações mostrar? (padrão 10): ")
                    limite = int(limite) if limite else 10
                    print("\n" + sistema.ver_historico(limite))
                except ValueError:
                    print("\n" + sistema.ver_historico())
                    
            elif opcao == "9":  # Pesquisar no Histórico
                print("\n=== PESQUISAR NO HISTÓRICO ===")
                print("💡 Esta funcionalidade permite buscar operações específicas no histórico")
                
                print("\nTipo de busca:")
                print("1. Buscar por tipo de ação (CRIAR_CALOURADA, DEMONSTRAR_INTERESSE, etc.)")
                print("2. Buscar por nome de participante")
                print("3. Buscar por ID de calourada")
                print("4. Buscar nos detalhes")
                
                tipo_busca_opcao = input("Escolha uma opção (1-4): ").strip()
                
                tipo_busca = None
                if tipo_busca_opcao == "1":
                    tipo_busca = "acao"
                    print("\nTipos de ação disponíveis:")
                    print("- CRIAR_CALOURADA")
                    print("- DEMONSTRAR_INTERESSE")
                    print("- CANCELAR_INTERESSE")
                    print("- REMOVER_CALOURADA")
                    print("- DESFAZER")
                elif tipo_busca_opcao == "2":
                    tipo_busca = "participante"
                elif tipo_busca_opcao == "3":
                    tipo_busca = "calourada_id"
                elif tipo_busca_opcao == "4":
                    tipo_busca = "detalhes"
                else:
                    print("✗ Opção inválida!")
                    continue
                
                termo_busca = input(f"\nDigite o termo para buscar por {tipo_busca}: ").strip()
                if not termo_busca:
                    print("✗ Termo de busca não pode ser vazio!")
                    continue
                
                resultado_busca = sistema.buscar_no_historico(termo_busca, tipo_busca)
                print("\n" + resultado_busca)
                    
            elif opcao == "10":  # Desfazer Última Operação
                print("\n=== DESFAZER ÚLTIMA OPERAÇÃO ===")
                print("⚠️  Esta operação irá desfazer a última ação registrada no histórico.")
                
                historico = sistema.ver_historico(1)
                print("\nÚltima operação:")
                print(historico)
                
                confirmacao = input("\n❓ Tem certeza que deseja desfazer esta operação? (s/N): ").lower()
                
                if confirmacao == 's':
                    sucesso, mensagem = sistema.desfazer_ultima_operacao()
                    print(f"\n{'✓ ' if sucesso else '✗ '} {mensagem}")
                else:
                    print("\n✓ Operação cancelada")
                
                print("\nTipo de busca:")
                print("1. Buscar por tipo de ação (CRIAR_CALOURADA, DEMONSTRAR_INTERESSE, etc.)")
                print("2. Buscar por nome de participante")
                print("3. Buscar por ID de calourada")
                print("4. Buscar nos detalhes")
                
                tipo_busca_opcao = input("Escolha uma opção (1-4): ").strip()
                
                tipo_busca = None
                if tipo_busca_opcao == "1":
                    tipo_busca = "acao"
                    print("\nTipos de ação disponíveis:")
                    print("- CRIAR_CALOURADA")
                    print("- DEMONSTRAR_INTERESSE")
                    print("- CANCELAR_INTERESSE")
                    print("- REMOVER_CALOURADA")
                    print("- DESFAZER")
                elif tipo_busca_opcao == "2":
                    tipo_busca = "participante"
                elif tipo_busca_opcao == "3":
                    tipo_busca = "calourada_id"
                elif tipo_busca_opcao == "4":
                    tipo_busca = "detalhes"
                else:
                    print("✗ Opção inválida!")
                    continue
                
                termo_busca = input(f"\nDigite o termo para buscar por {tipo_busca}: ").strip()
                if not termo_busca:
                    print("✗ Termo de busca não pode ser vazio!")
                    continue
                
                resultado_busca = sistema.buscar_no_historico(termo_busca, tipo_busca)
                print("\n" + resultado_busca)
            
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