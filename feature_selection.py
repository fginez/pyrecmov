import numpy as np
from skfeature.function.similarity_based import fisher_score

def seleciona_caracteristicas(vetor_caracteristicas, classes):
	caracteristicas_selecionadas  = []
	limiar_consideracao = 0

	score = fisher_score.fisher_score(vetor_caracteristicas, classes)
	rank = fisher_score.feature_ranking(score)
	features_consideradas = conta_features_limiar(score, limiar_consideracao)
	if features_consideradas > 1:
		rank_considerado = rank[0:features_consideradas:1]
		caracteristicas_selecionadas = vetor_caracteristicas[:, rank_considerado]

	return caracteristicas_selecionadas, rank_considerado

def conta_features_limiar(score, limiar):
	contagem = 0
	for i in range(0, len(score)):
		if score[i] >= limiar:
			contagem += 1
	return contagem