"""
PROJETO 4: ALGORITMO GENÉTICO

Este script implementa um Algoritmo Genético para resolver o problema das N-Rainhas.
A visualização mostra o melhor indivíduo de cada geração e um gráfico da evolução do fitness.
"""
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# --- Funções do Problema (Fitness) e do Algoritmo Genético ---

def calcular_fitness(individuo):
    """
    Função Fitness: Avalia a "qualidade" de um indivíduo (solução).
    O objetivo é maximizar o número de pares de rainhas que NÃO se atacam.
    """
    n = len(individuo)
    max_ataques = n * (n - 1) / 2 # Máximo de conflitos possíveis
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            if individuo[i] == individuo[j] or abs(i - j) == abs(individuo[i] - individuo[j]):
                ataques += 1
    return int(max_ataques - ataques)

def selecionar_pais(populacao, fitness_populacao, k=3):
    """Seleciona um pai usando o método de Torneio."""
    # Pega k indivíduos aleatórios da população
    selecao_torneio = random.choices(list(range(len(populacao))), k=k)
    # Encontra o índice do melhor indivíduo entre os selecionados
    indice_melhor = max(selecao_torneio, key=lambda i: fitness_populacao[i])
    return populacao[indice_melhor]

def crossover(pai1, pai2):
    """Realiza o crossover de ponto único para criar um filho."""
    n = len(pai1)
    ponto_corte = random.randint(1, n - 1)
    filho = pai1[:ponto_corte] + pai2[ponto_corte:]
    return filho

def mutacao(individuo, taxa_mutacao=0.1):
    """Aplica uma mutação aleatória em um indivíduo."""
    if random.random() < taxa_mutacao:
        n = len(individuo)
        coluna = random.randint(0, n - 1)
        nova_linha = random.randint(0, n - 1)
        individuo[coluna] = nova_linha
    return individuo

# --- Algoritmo Principal e Visualização ---

def algoritmo_genetico_visual(n_rainhas=8, tam_populacao=100, geracoes=500, taxa_mutacao=0.1):
    """Executa o Algoritmo Genético com visualização gráfica."""
    plt.ion()
    fig = plt.figure(figsize=(12, 6))
    ax_tabuleiro = fig.add_subplot(1, 2, 1)
    ax_grafico = fig.add_subplot(1, 2, 2)
    fig.canvas.manager.set_window_title('Projeto 4: Algoritmo Genético para N-Rainhas')

    # 1. Inicializa a população com indivíduos aleatórios
    populacao = [[random.randint(0, n_rainhas - 1) for _ in range(n_rainhas)] for _ in range(tam_populacao)]
    
    historico_melhor_fitness = []
    max_fitness_possivel = n_rainhas * (n_rainhas - 1) / 2

    for geracao in range(geracoes):
        # 2. Avalia o fitness de toda a população
        fitness_populacao = [calcular_fitness(ind) for ind in populacao]

        # Encontra o melhor indivíduo da geração atual
        melhor_fitness_geracao = max(fitness_populacao)
        indice_melhor = fitness_populacao.index(melhor_fitness_geracao)
        melhor_individuo = populacao[indice_melhor]
        historico_melhor_fitness.append(melhor_fitness_geracao)
        
        # --- Visualização ---
        ax_tabuleiro.clear()
        ax_grafico.clear()
        
        # Desenha o tabuleiro do melhor indivíduo
        tabuleiro_fundo = np.zeros((n_rainhas, n_rainhas))
        for i in range(n_rainhas):
            for j in range(n_rainhas):
                if (i+j)%2 == 1: tabuleiro_fundo[i,j] = 1
        ax_tabuleiro.imshow(tabuleiro_fundo, cmap='gray')
        for col, lin in enumerate(melhor_individuo):
            ax_tabuleiro.text(col, lin, '♛', ha='center', va='center', fontsize=28, color='gold')
        ax_tabuleiro.set_title(f"Melhor Indivíduo | Geração: {geracao}")
        ax_tabuleiro.set_xticks([]); ax_tabuleiro.set_yticks([])

        # Desenha o gráfico de evolução do fitness
        ax_grafico.plot(historico_melhor_fitness, marker='o', linestyle='-')
        ax_grafico.set_title(f"Evolução do Fitness (Max: {max_fitness_possivel})")
        ax_grafico.set_xlabel("Geração"); ax_grafico.set_ylabel("Melhor Fitness")
        ax_grafico.set_xlim(0, geracoes); ax_grafico.set_ylim(0, max_fitness_possivel + 1)
        ax_grafico.grid(True)
        
        plt.tight_layout()
        plt.draw(); plt.pause(0.01)

        # 3. Verifica se encontrou a solução
        if melhor_fitness_geracao == max_fitness_possivel:
            print(f"Solução encontrada na geração {geracao}")
            break

        # 4. Cria a próxima geração
        nova_populacao = []
        # Elitismo: o melhor indivíduo sobrevive para a próxima geração
        nova_populacao.append(melhor_individuo)

        while len(nova_populacao) < tam_populacao:
            # Seleção
            pai1 = selecionar_pais(populacao, fitness_populacao)
            pai2 = selecionar_pais(populacao, fitness_populacao)
            # Crossover
            filho = crossover(pai1, pai2)
            # Mutação
            filho_mutado = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho_mutado)
        
        populacao = nova_populacao

    plt.ioff(); plt.show()
    return melhor_individuo

if __name__ == "__main__":
    solucao = algoritmo_genetico_visual(n_rainhas=8, tam_populacao=100, geracoes=500, taxa_mutacao=0.1)
    ataques_finais = (8*7/2) - calcular_fitness(solucao)
    print(f"\nBusca concluída. Melhor indivíduo com {int(ataques_finais)} ataques.")