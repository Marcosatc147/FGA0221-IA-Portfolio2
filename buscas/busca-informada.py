# -*- coding: utf-8 -*-

"""
PROJETO 2 (FINAL): LABORATÓRIO DE BUSCA INFORMADA - ANÁLISE DO PENSAMENTO

Esta versão final adiciona textos sobre as células para mostrar os valores de
g(n), h(n) e f(n), revelando o "processo de pensamento" do algoritmo A*.
"""

import os
import time
from collections import deque
import heapq

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ... (funções auxiliares como encontrar_posicao, obter_vizinhos, etc. permanecem as mesmas) ...
def encontrar_posicao(labirinto, simbolo):
    for i, linha in enumerate(labirinto):
        for j, char in enumerate(linha):
            if char == simbolo:
                return (i, j)
    return None

def obter_vizinhos(labirinto, posicao):
    linha, coluna = posicao
    vizinhos = []
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dr, dc in movimentos:
        nova_linha, nova_coluna = linha + dr, coluna + dc
        if 0 <= nova_linha < len(labirinto) and 0 <= nova_coluna < len(labirinto[0]):
            if labirinto[nova_linha][nova_coluna] != '#':
                vizinhos.append((nova_linha, nova_coluna))
    return vizinhos

def heuristica_manhattan(posicao_a, posicao_b):
    (x1, y1) = posicao_a
    (x2, y2) = posicao_b
    return abs(x1 - x2) + abs(y1 - y2)

def preparar_visualizacao_grafica(labirinto, nome_algoritmo):
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8)) # Aumentei um pouco a figura
    cores = ['black', 'white', 'green', 'red', 'orange', 'lightgray', 'lightblue']
    cmap = mcolors.ListedColormap(cores)
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    return fig, ax, cmap, norm

# --- FUNÇÃO DE VISUALIZAÇÃO APRIMORADA ---
def visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo, fim):
    """Desenha o estado da busca, incluindo os textos com os custos g, h, f."""
    mapa_numerico = []
    for i, linha_str in enumerate(labirinto):
        linha_num = []
        for j, char in enumerate(linha_str):
            if char == '#': linha_num.append(0)
            elif char == 'S': linha_num.append(2)
            elif char == 'E': linha_num.append(3)
            else: linha_num.append(1)
        mapa_numerico.append(linha_num)
    
    for pos in visitados:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 5 # Visitado
    for pos in fronteira_coords:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 4 # Fronteira
    for pos in caminho_atual:
        if mapa_numerico[pos[0]][pos[1]] in (4,5): mapa_numerico[pos[0]][pos[1]] = 6 # Caminho

    ax.clear()
    ax.imshow(mapa_numerico, cmap=cmap, norm=norm)
    ax.set_xticks([])
    ax.set_yticks([])

    # --- NOVO: Adiciona texto com os custos em cada célula visitada ---
    for pos, g_cost in visitados.items():
        h_cost = heuristica_manhattan(pos, fim)
        f_cost = g_cost + h_cost
        texto_display = ""
        if algoritmo == 'ucs':
            texto_display = f"g={g_cost}"
        elif algoritmo == 'greedy':
            texto_display = f"h={h_cost}"
        elif algoritmo == 'a_star':
            texto_display = f"{f_cost}\n g={g_cost} h={h_cost}"
        
        ax.text(pos[1], pos[0], texto_display, ha='center', va='center', fontsize=6, color='black')

    # --- NOVO: Adiciona um título dinâmico (placar) ---
    pos_atual = caminho_atual[-1]
    g_atual = visitados.get(pos_atual, 0)
    h_atual = heuristica_manhattan(pos_atual, fim)
    f_atual = g_atual + h_atual
    ax.set_title(f"Algoritmo: {algoritmo.upper()} | Expandindo: {pos_atual} | g={g_atual}, h={h_atual}, f={f_atual}")

    plt.draw()
    plt.pause(velocidade)

def buscar_no_labirinto_informado(labirinto, algoritmo='a_star', velocidade=0.05):
    inicio = encontrar_posicao(labirinto, 'S')
    fim = encontrar_posicao(labirinto, 'E')
    if not inicio or not fim: return None

    prioridade_inicial = 0
    fronteira = [(prioridade_inicial, [inicio])]
    visitados = {inicio: 0}
    
    fig, ax, cmap, norm = preparar_visualizacao_grafica(labirinto, algoritmo.upper())

    while fronteira:
        _, caminho_atual = heapq.heappop(fronteira)
        posicao_atual = caminho_atual[-1]
        
        # Otimização: se já encontramos um caminho melhor para este nó, ignoramos.
        if visitados[posicao_atual] < len(caminho_atual) - 1:
            continue

        fronteira_coords = [caminho[-1] for _, caminho in fronteira]
        visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo, fim)

        if posicao_atual == fim:
            print("\nSolução encontrada! Feche a janela gráfica para terminar.")
            plt.ioff(); plt.show()
            return caminho_atual

        for vizinho in obter_vizinhos(labirinto, posicao_atual):
            novo_g_cost = visitados[posicao_atual] + 1
            
            if vizinho not in visitados or novo_g_cost < visitados[vizinho]:
                visitados[vizinho] = novo_g_cost
                
                prioridade = 0
                if algoritmo == 'ucs':
                    prioridade = novo_g_cost
                elif algoritmo == 'greedy':
                    prioridade = heuristica_manhattan(vizinho, fim)
                elif algoritmo == 'a_star':
                    h_cost = heuristica_manhattan(vizinho, fim)
                    prioridade = novo_g_cost + h_cost

                novo_caminho = list(caminho_atual)
                novo_caminho.append(vizinho)
                heapq.heappush(fronteira, (prioridade, novo_caminho))

    print("\nSolução não encontrada.")
    plt.ioff(); plt.show()
    return None

def desenhar_solucao_terminal(labirinto, caminho):
    if caminho is None: return
    labirinto_desenhado = [list(linha) for linha in labirinto]
    for posicao in caminho[1:-1]:
        labirinto_desenhado[posicao[0]][posicao[1]] = '*'
    print("\n--- Labirinto com Solução Final (Terminal) ---")
    for linha in labirinto_desenhado:
        print("".join(linha))

if __name__ == "__main__":
    meu_labirinto = [
        "S     # ###### ##",
        " # ##  #     ####",
        "    ##   ##     #",
        " # # ###   ### ##",
        " # # #   ##### ##",
        " # #   #  ####  #",
        "     ####      E#",
        " ## #######  ####"
    ]
    
    print("--- Labirinto Original ---")
    for linha in meu_labirinto:
        print(linha)
    
    escolha = ''
    while escolha.lower() not in ['ucs', 'greedy', 'a_star']:
        escolha = input("\nEscolha o algoritmo de busca (ucs, greedy, ou a_star): ")

    caminho_encontrado = buscar_no_labirinto_informado(meu_labirinto, algoritmo=escolha, velocidade=0.4)
    
    desenhar_solucao_terminal(meu_labirinto, caminho_encontrado)
    if caminho_encontrado:
        print(f"\nCaminho encontrado pelo {escolha.upper()} com {len(caminho_encontrado) - 1} passos.")