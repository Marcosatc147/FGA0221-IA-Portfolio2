"""
PROJETO 3: BUSCA COMPLEXA (HILL-CLIMBING) COM VISUALIZAÇÃO GRÁFICA

Esta versão aprimorada destaca em vermelho as rainhas que estão se atacando,
tornando o estado do tabuleiro e os conflitos mais fáceis de visualizar.
"""
import random
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# --- Função de Ataques Modificada ---
def calcular_ataques(estado):
    """
    Função Objetivo: Calcula o número de ataques e retorna os índices das rainhas em conflito.
    
    Returns:
        tuple: (int: número de ataques, set: conjunto com os índices das rainhas atacando)
    """
    n = len(estado)
    ataques = 0
    rainhas_atacando = set() # Usamos um conjunto para evitar adicionar a mesma rainha várias vezes

    for i in range(n):
        for j in range(i + 1, n):
            # Conflito na mesma linha (horizontal)
            if estado[i] == estado[j]:
                ataques += 1
                rainhas_atacando.add(i)
                rainhas_atacando.add(j)
            
            # Conflito na mesma diagonal
            if abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
                rainhas_atacando.add(i)
                rainhas_atacando.add(j)
                
    return ataques, rainhas_atacando

def preparar_tabuleiro_grafico(n, ax):
    """Desenha o tabuleiro de xadrez estático como fundo."""
    tabuleiro = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 1:
                tabuleiro[i, j] = 1
    ax.imshow(tabuleiro, cmap='gray', interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])

# --- Função de Desenho Modificada ---
def desenhar_passo_grafico(ax, estado, ataques_atuais, rainhas_atacando, passo, n, velocidade):
    """
    Desenha um frame da animação, colorindo as rainhas de acordo com seu estado (atacando ou não).
    """
    ax.clear()
    preparar_tabuleiro_grafico(n, ax)
    
    # Desenha cada rainha na sua posição, com a cor apropriada
    for coluna, linha in enumerate(estado):
        # Define a cor: vermelha se a rainha está na lista de atacantes, dourada caso contrário
        cor_rainha = 'red' if coluna in rainhas_atacando else 'gold'
        ax.text(coluna, linha, '♛', ha='center', va='center', fontsize=28, color=cor_rainha)
        
    ax.set_title(f"Algoritmo: Hill-Climbing | Passo: {passo} | Ataques: {ataques_atuais}")
    
    plt.draw()
    plt.pause(velocidade)

# --- Algoritmo Principal Modificado ---
def hill_climbing_visual(n_rainhas=8, velocidade=0.5):
    """
    Executa o Hill-Climbing com visualização gráfica passo a passo.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.manager.set_window_title('Projeto 3: Hill-Climbing para N-Rainhas')
    
    estado_atual = [random.randint(0, n_rainhas - 1) for _ in range(n_rainhas)]
    passo = 0

    while True:
        # Agora a função retorna tanto o número de ataques quanto as rainhas envolvidas
        ataques_atuais, atacantes_atuais = calcular_ataques(estado_atual)
        
        # Passa a lista de rainhas atacando para a função de desenho
        desenhar_passo_grafico(ax, estado_atual, ataques_atuais, atacantes_atuais, passo, n_rainhas, velocidade)
        
        if ataques_atuais == 0:
            ax.set_title(f"SOLUÇÃO ENCONTRADA! (0 Ataques) | Passos: {passo}")
            plt.ioff(); plt.show()
            return estado_atual

        melhor_vizinho = None
        melhores_ataques = ataques_atuais
        
        for coluna in range(n_rainhas):
            posicao_original = estado_atual[coluna]
            for linha in range(n_rainhas):
                if linha == posicao_original:
                    continue
                
                estado_vizinho = list(estado_atual)
                estado_vizinho[coluna] = linha
                # Para os vizinhos, só precisamos do número de ataques para comparar
                ataques_vizinho, _ = calcular_ataques(estado_vizinho)

                if ataques_vizinho < melhores_ataques:
                    melhores_ataques = ataques_vizinho
                    melhor_vizinho = estado_vizinho
        
        if melhores_ataques >= ataques_atuais:
            ax.set_title(f"MÍNIMO LOCAL ALCANÇADO! ({ataques_atuais} Ataques) | Passos: {passo}")
            print("\nO algoritmo ficou preso em um mínimo local.")
            plt.ioff(); plt.show()
            return estado_atual
        else:
            estado_atual = melhor_vizinho
            passo += 1

# Bloco principal de execução
if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("Erro: A biblioteca NumPy não está instalada.")
        print("Por favor, instale-a com o comando: pip install numpy")
        exit()

    NUM_RAINHAS = 8
    VELOCIDADE_ANIMACAO = 0.8 
    
    solucao_final = hill_climbing_visual(NUM_RAINHAS, velocidade=VELOCIDADE_ANIMACAO)
    
    ataques_finais, _ = calcular_ataques(solucao_final)
    
    print(f"\nBusca concluída. Estado final com {ataques_finais} ataques.")
    if ataques_finais == 0:
        print(">>> Sucesso! Uma solução global foi encontrada.")
    else:
        print(">>> Tente rodar novamente para ver se um ponto de partida diferente leva à solução.")