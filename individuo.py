#!/usr/bin/python3
from __future__ import division
import re
import random


class individuo:


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


	def informacoes_arvore(self, arvore):
		"Retorna as informacoes referentes a arvore"
		return [arvore, self.quantidade_terminais(arvore), \
			self.profundidade(arvore)]


	def subarvores(self, arvore):
		"Retorna todas as subarvores possiveis junto de informacoes"
		# quando está em um nó final retorna as informações
		if "[" not in arvore[1 : len(arvore) - 1]:
			return self.informacoes_arvore(arvore)

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
						self.subarvores(arvore[indice_inicial : indice + 1])
					indice_inicial = -1

		# adiciona a própria árvore na lista
		lista_subarvores += self.informacoes_arvore(arvore)
		return lista_subarvores


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
print(ind.quantidade_terminais("[log[??,sum[??,??]]]"))
print(ind.profundidade("[log[??,sum[??,??]]]"))
print(ind.subarvores("[log[sum[23,??],sum[??,??]]]"))
print(ind.mutacao("[log[sum[23,??],sum[??,44]]]", ['mul', 'exp', 'sin']))