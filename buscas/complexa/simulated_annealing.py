"""
PROJETO 3 (VARIAÇÃO): BUSCA COMPLEXA - SIMULATED ANNEALING

Este script implementa o algoritmo Simulated Annealing para o problema das N-Rainhas,
demonstrando uma técnica para escapar de mínimos locais.
(Versão com parâmetros otimizados para maior taxa de sucesso)
"""
import random
import math
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def calcular_ataques(estado):
    """Função Objetivo: Calcula o número total de pares de rainhas se atacando."""
    n = len(estado)
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            if estado[i] == estado[j] or abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
    return ataques

def preparar_tabuleiro_grafico(n, ax):
    """Desenha o tabuleiro de xadrez estático como fundo."""
    tabuleiro = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 1: tabuleiro[i, j] = 1
    ax.imshow(tabuleiro, cmap='gray', interpolation='nearest')
    ax.set_xticks([]); ax.set_yticks([])

def desenhar_passo_sa(ax, estado, ataques, temperatura, n):
    """Desenha um frame da animação para o Simulated Annealing."""
    ax.clear()
    preparar_tabuleiro_grafico(n, ax)
    
    rainhas_atacando, _ = calcular_ataques_detalhado(estado)
    
    for coluna, linha in enumerate(estado):
        cor_rainha = 'red' if coluna in rainhas_atacando else 'gold'
        ax.text(coluna, linha, '♛', ha='center', va='center', fontsize=28, color=cor_rainha)
        
    ax.set_title(f"Simulated Annealing | Ataques: {ataques} | Temperatura: {temperatura:.2f}")
    
    plt.draw()
    plt.pause(0.01)

def calcular_ataques_detalhado(estado):
    """Função auxiliar para a visualização, retorna os índices das rainhas em conflito."""
    n = len(estado)
    rainhas_atacando = set()
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            if estado[i] == estado[j] or abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
                rainhas_atacando.add(i)
                rainhas_atacando.add(j)
    return rainhas_atacando, ataques
    
# --- Algoritmo Principal: Simulated Annealing ---

def simulated_annealing_visual(n_rainhas=8, temperatura_inicial=1000.0, taxa_resfriamento=0.999):
    """Executa o Simulated Annealing com visualização gráfica."""
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.manager.set_window_title('Projeto 3: Simulated Annealing para N-Rainhas')
    
    estado_atual = [random.randint(0, n_rainhas - 1) for _ in range(n_rainhas)]
    temperatura = temperatura_inicial

    # O loop principal agora depende da temperatura e se a solução foi encontrada
    while temperatura > 0.1:
        ataques_atuais = calcular_ataques(estado_atual)
        if ataques_atuais == 0:
            break # Encontrou a solução, pode parar antes da temperatura acabar
            
        desenhar_passo_sa(ax, estado_atual, ataques_atuais, temperatura, n_rainhas)

        # 1. Escolhe um vizinho aleatório
        coluna = random.randint(0, n_rainhas - 1)
        nova_linha = random.randint(0, n_rainhas - 1)
        
        estado_vizinho = list(estado_atual)
        estado_vizinho[coluna] = nova_linha
        ataques_vizinho = calcular_ataques(estado_vizinho)

        # 2. Calcula a diferença de "energia" (custo)
        delta_energia = ataques_vizinho - ataques_atuais

        # 3. Decide se aceita o novo estado
        if delta_energia < 0 or (temperatura > 0 and random.random() < math.exp(-delta_energia / temperatura)):
            estado_atual = estado_vizinho
        
        # 4. "Esfria" a temperatura
        temperatura *= taxa_resfriamento
    
    # Desenha o estado final
    ataques_finais = calcular_ataques(estado_atual)
    desenhar_passo_sa(ax, estado_atual, ataques_finais, temperatura, n_rainhas)

    if ataques_finais == 0:
        ax.set_title(f"SOLUÇÃO ENCONTRADA! (0 Ataques)")
    else:
        ax.set_title(f"Busca finalizada com {ataques_finais} ataques.")
    plt.ioff(); plt.show()
    return estado_atual

if __name__ == "__main__":
    try: import numpy as np
    except ImportError: print("Instale a biblioteca NumPy: pip install numpy"); exit()

    NUM_RAINHAS = 8
    
    ### ALTERAÇÃO 2: Define os parâmetros otimizados aqui para fácil ajuste ###
    params_otimizados = {
        'temperatura_inicial': 1000.0,
        'taxa_resfriamento': 0.999
    }
    
    # Chama a função visual passando os parâmetros otimizados
    solucao = simulated_annealing_visual(
        n_rainhas=NUM_RAINHAS,
        **params_otimizados
    )
    
    ataques_finais = calcular_ataques(solucao)
    print(f"\nBusca concluída. Estado final com {ataques_finais} ataques.")