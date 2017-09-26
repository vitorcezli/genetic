#!/usr/bin/python3
from __future__ import division
import re
import random


class individuo:


	def geracao_individuos(self, funcoes):
		"Gera um novo individuo a partir das funcoes"
		pass


	def calcula(self, arvore, dados):
		"Realiza o calculo da funcao especificada pela arvore com os dados"
		arvore_valores = self.substituicao_argumentos_valores(arvore, dados)
		self.calcula_aux(arvore_valores)


	def calcula_aux(self, arvore):
		"Funcao auxiliar a calcula"
		# retorna uma lista com os números caso chegue ao final da árvore
		if re.search("[a-zA-Z]+", arvore) == None:
			lista_numeros = []
			padrao = re.compile("[\d\.]+")
			iterador = padrao.finditer(arvore)

			# pega cada número encontrado
			for ocorrencia in iterador:
				regiao = ocorrencia.span()
				numero = arvore[regiao[0] : regiao[1]]
				lista_numeros.append(float(numero))
			return lista_numeros


	def substitui_substring(self, string, regiao, substituicao):
		"Substitui a substring na regiao especificada"
		return string[: regiao[0]] + substituicao + string[regiao[1] :]


	def substituicao_argumentos_valores(self, arvore, valores):
		"Substitui os argumentos da arvore pelos valores a serem calculados"
		padrao = re.compile("\?\?")
		iterador = padrao.finditer(arvore)

		# substitui cada argumento pelo seu valor
		indice = 0
		for ocorrencia in iterador:
			regiao = ocorrencia.span()
			arvore = self.substitui_substring(arvore, regiao, str(valores[indice]))
			indice += 1

		return arvore


	def quantidade_terminais(self, arvore):
		"Retorna a quantidade de terminais da arvore"
		return arvore.count("??")


	def profundidade(self, arvore):
		"Retorna a profundidade maxima da arvore"
		profundidade_maxima = 0
		profundidade = 0

		for letra in arvore:
			if letra == '[':
				profundidade += 1
				if profundidade > profundidade_maxima:
					profundidade_maxima = profundidade
			elif letra == ']':
				profundidade -= 1
		return profundidade_maxima


	def informacoes_arvore(self, arvore, interior, indice_primeiro):
		"Retorna as informacoes referentes a arvore"
		return [[arvore, interior, self.profundidade(arvore), \
			self.quantidade_terminais(arvore), indice_primeiro]]


	def subarvores(self, arvore, interior, indice_primeiro):
		"Retorna todas as subarvores possiveis junto de informacoes"
		# quando está em um nó final retorna as informações
		if "[" not in arvore[1 : len(arvore) - 1]:
			return self.informacoes_arvore(arvore, interior, indice_primeiro)

		# armazena as informações das sub-árvores
		lista_subarvores = []

		# variáveis a serem utilizadas para pegar as sub-árvores
		profundidade = 0
		indice_inicial = -1

		# adiciona subarvores na lista
		for indice in range(1, len(arvore) - 1):
			if arvore[indice] == "[":
				profundidade += 1
				# nova sub-árvore foi encontrada
				if indice_inicial == -1:
					indice_inicial = indice
			elif arvore[indice] == "]":
				profundidade -= 1
				# fim da sub-árvore encontrada
				if profundidade == 0:
					lista_subarvores += \
						self.subarvores(arvore[indice_inicial : indice + 1], \
							interior + 1, indice_primeiro + indice_inicial)
					indice_inicial = -1

		# adiciona a própria árvore na lista
		lista_subarvores += \
			self.informacoes_arvore(arvore, interior, indice_primeiro)
		return lista_subarvores


	def cruzamento(self, maximo, arvore1, arvore2):
		"Realiza a cruzamento entre dois individuos, retornando dois filhos"
		# genótipos dos dois indivíduos
		possibilidades1 = self.subarvores(arvore1, 1, 0)
		possibilidades2 = self.subarvores(arvore2, 1, 0)

		# armazena os genótipos que podem ser trocados
		lista_troca = []
		for lista1 in possibilidades1:
			for lista2 in possibilidades2:
				if lista1[3] == lista2[3] and lista1[1] + lista2[2] <= maximo:
					lista_troca.append([[lista1[0], lista1[4]], [lista2[0], lista2[4]]])

		# seleciona os genótipos que serão trocados
		troca = lista_troca[random.randint(0, len(lista_troca) - 1)]

		# realiza a troca de informação genética
		filho1 = arvore1[0 : troca[0][1]] + troca[1][0] + \
			arvore1[troca[0][1] + len(troca[0][0]) :]
		filho2 = arvore2[0 : troca[1][1]] + troca[0][0] + \
			arvore2[troca[1][1] + len(troca[1][0]) :]

		# retorna os indivíduos
		return [filho1, filho2]


	def mutacao_funcao(self, arvore, substitutos):
		"Realiza o processo de mutacao em uma funcao do individuo"
		padrao = re.compile("[a-zA-Z]+")
		iterador = padrao.finditer(arvore)

		# armazena cada índice de ocorrência
		indices = []
		for ocorrencia in iterador:
			indices.append(ocorrencia.span())
		
		# seleciona o lugar que será substituído e o que será colocado no lugar
		substituicao = indices[random.randint(0, len(indices) - 1)]
		substituto = substitutos[random.randint(0, len(substitutos) - 1)]

		# realiza a substituição
		nova = arvore[0 : substituicao[0]] + substituto + \
			arvore[substituicao[1] :]
		return nova


	def mutacao_numero(self, arvore):
		"Realiza o processo de mutaao em um valor do individuo"
		padrao = re.compile("\d+")
		iterador = padrao.finditer(arvore)

		# armazena cada índice de ocorrência
		indices = []
		for ocorrencia in iterador:
			indices.append(ocorrencia.span())
		
		# seleciona o lugar que será substituído e o que será colocado no lugar
		substituicao = indices[random.randint(0, len(indices) - 1)]

		# realiza a substituição
		nova = arvore[0 : substituicao[0]] + str(2 * random.random() - 1) + \
			arvore[substituicao[1] :]
		return nova


	def mutacao(self, arvore, substitutos):
		"Realiza mutacao no individuo"
		# a probabilidade de substituir um número ou uma função é proporcional
		# à sua quantidade
		padrao_valor = re.compile("\d+")
		padrao_funcao = re.compile("\w+")
		quantidade_valor = len(padrao_valor.findall(arvore))
		quantidade_funcao = len(padrao_funcao.findall(arvore))

		# tenta substituir um número
		if random.random() < quantidade_valor / \
			(quantidade_valor + quantidade_funcao):
			return self.mutacao_numero(arvore)
		# caso contrário substitui uma função
		else:
			return self.mutacao_funcao(arvore, substitutos)



ind = individuo()
#print(ind.quantidade_terminais("[log[??,sum[??,??]]]"))
#print(ind.profundidade("[log[??,sum[??,??]]]"))
#print(ind.subarvores("[log[sum[23,??],sum[??,??]]]", 1))
#print(ind.mutacao("[log[sum[23,??],sum[??,44]]]", ['mul', 'exp', 'sin']))
print(ind.cruzamento(6, "[exp[mul[0.35,??],sum[??,44]]]", "[log[sum[23,??],sum[??,44]]]"))
print(ind.substituicao_argumentos_valores("[exp[mul[0.35,??],sum[??,44]]]", [13, 43]))
print(ind.calcula_aux("[1.234,44]"))