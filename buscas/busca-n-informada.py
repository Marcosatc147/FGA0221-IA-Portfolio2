# -*- coding: utf-8 -*-

"""
PROJETO 1 : BUSCA NÃO INFORMADA - BFS vs. DFS

Este script é uma ferramenta para visualizar e comparar os algoritmos
de Busca em Largura (BFS) e Busca em Profundidade (DFS) na resolução de um labirinto.

"""

# =============================================================================
# SEÇÃO 1: IMPORTAÇÕES E CONFIGURAÇÃO INICIAL
# =============================================================================
# Módulos padrowão do Python para funcionalidades básicas
import os
import time
from collections import deque # 'deque' é uma lista otimizada, ideal para implementar uma Fila (Queue)

# Importação da biblioteca Matplotlib para a visualização gráfica.
# O código a seguir garante que o "motor" gráfico correto seja usado
# para evitar erros em diferentes sistemas operacionais.
import matplotlib
matplotlib.use('TkAgg') # Especifica o backend 'TkAgg', que é universal e estável.
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# =============================================================================
# SEÇÃO 2: FUNÇÕES AUXILIARES E DE MODELAGEM DO PROBLEMA
# =============================================================================

def encontrar_posicao(labirinto, simbolo):
    """
    Função utilitária para encontrar as coordenadas de um símbolo ('S' ou 'E').
    Isso define nosso ESTADO INICIAL e o TESTE DE OBJETIVO.
    """
    for i, linha in enumerate(labirinto):
        for j, char in enumerate(linha):
            if char == simbolo:
                return (i, j)
    return None

def obter_vizinhos(labirinto, posicao):
    """
    Esta função é a implementação da nossa AÇÃO ou FUNÇÃO SUCESSORA.
    A partir de um estado (posição), ela retorna todos os estados válidos alcançáveis.
    """
    linha, coluna = posicao
    vizinhos = []
    # Define os 4 movimentos possíveis: Cima, Baixo, Esquerda, Direita.
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    # Percorre o labirinto
    for drow, dcol in movimentos:
        nova_linha, nova_coluna = linha + drow, coluna + dcol
        # Garante que o movimento está dentro dos limites do labirinto.
        if 0 <= nova_linha < len(labirinto) and 0 <= nova_coluna < len(labirinto[0]):
            # Garante que o movimento não leva a uma parede ('#').
            if labirinto[nova_linha][nova_coluna] != '#':
                vizinhos.append((nova_linha, nova_coluna))
    return vizinhos

# =============================================================================
# SEÇÃO 3: LÓGICA DE VISUALIZAÇÃO GRÁFICA
# =============================================================================

def preparar_visualizacao_grafica(labirinto, nome_algoritmo):
    """Prepara a janela do Matplotlib onde a animação ocorrerá."""
    plt.ion()  # Ativa o modo interativo, essencial para a animação.
    fig, ax = plt.subplots(figsize=(8, 6)) # Cria a figura e os eixos do gráfico.
    
    # Define um mapa de cores: cada número corresponderá a uma cor específica.
    # Esta é a legenda da nossa visualização.
    # 0: Parede (Preto), 1: Caminho (Branco), 2: Início (Verde), 3: Fim (Vermelho)
    # 4: Fronteira (Laranja), 5: Visitado (Cinza), 6: Caminho Final (Azul)
    cores = ['black', 'white', 'green', 'red', 'orange', 'gray', 'blue']
    cmap = mcolors.ListedColormap(cores)
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    fig.canvas.manager.set_window_title(f'Buscando Solução com {nome_algoritmo}')
    return fig, ax, cmap, norm

def visualizar_passo_grafico(ax, labirinto, visitados, fronteira, caminho_atual, cmap, norm, velocidade):
    """Desenha um único "frame" da animação da busca."""
    # 1. Converte o labirinto de caracteres para uma matriz de números.
    mapa_numerico = []
    for i, linha_str in enumerate(labirinto):
        linha_num = []
        for j, char in enumerate(linha_str):
            if char == '#': linha_num.append(0)
            elif char == 'S': linha_num.append(2)
            elif char == 'E': linha_num.append(3)
            else: linha_num.append(1)
        mapa_numerico.append(linha_num)

    # 2. Pinta as células de acordo com o estado da busca.
    for pos in visitados:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 5 # Visitado
    for caminho in fronteira:
        pos = caminho[-1]
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 4 # Fronteira
    for pos in caminho_atual:
        if mapa_numerico[pos[0]][pos[1]] in (4,5): mapa_numerico[pos[0]][pos[1]] = 6 # Caminho

    # 3. Usa o Matplotlib para desenhar a matriz como uma imagem.
    ax.clear()  # Limpa o desenho anterior.
    ax.imshow(mapa_numerico, cmap=cmap, norm=norm) # Desenha a nova matriz.
    ax.set_xticks([]); ax.set_yticks([]) # Remove os eixos para um visual mais limpo.
    plt.draw()
    plt.pause(velocidade) # Pausa para criar o efeito de animação.

# =============================================================================
# SEÇÃO 4: ALGORITMOS DE BUSCA
# =============================================================================

def buscar_no_labirinto(labirinto, algoritmo='bfs', velocidade=0.05, visualizar=True):
    """Função principal que executa a busca, acomodando tanto BFS quanto DFS."""
    inicio = encontrar_posicao(labirinto, 'S')
    fim = encontrar_posicao(labirinto, 'E')
    if not inicio or not fim: return None

    # DIFERENÇA ENTRE BFS E DFS: A ESTRUTURA DE DADOS DA FRONTEIRA
    if algoritmo == 'bfs':
        # BFS usa uma FILA (Queue): Primeiro que entra, primeiro que sai (FIFO).
        fronteira = deque([[inicio]]) 
    else: # algoritmo == 'dfs'
        # DFS usa uma PILHA (Stack): Último que entra, primeiro que sai (LIFO).
        fronteira = [[inicio]]

    # O conjunto de 'visitados' é essencial para uma Busca em Grafo.
    # Ele impede o algoritmo de entrar em loops e reexplorar os mesmos nós.
    visitados = {inicio}
    
    # Prepara a janela gráfica se a visualização estiver ativa.
    fig, ax, cmap, norm = (None, None, None, None)
    if visualizar:
        fig, ax, cmap, norm = preparar_visualizacao_grafica(labirinto, algoritmo.upper())

    # Loop principal da busca: continua enquanto houver nós na fronteira para explorar.
    while fronteira:
        # AQUI ESTÁ A SEGUNDA DIFERENÇA
        if algoritmo == 'bfs':
            caminho_atual = fronteira.popleft() # Pega o caminho MAIS ANTIGO da fila.
        else: # algoritmo == 'dfs'
            caminho_atual = fronteira.pop() # Pega o caminho MAIS RECENTE da pilha.

        # Última coordenada 
        posicao_atual = caminho_atual[-1]
        
        # Para DFS, marcamos como visitado ao explorar, para mostrar o "mergulho".
        if algoritmo == 'dfs':
             visitados.add(posicao_atual)

        # Atualiza a visualização a cada passo.
        if visualizar:
            visualizar_passo_grafico(ax, labirinto, visitados, fronteira, caminho_atual, cmap, norm, velocidade)

        # Verifica se a posição atual é a saída.
        if posicao_atual == fim:
            if visualizar:
                print("\nSolução encontrada! Feche a janela gráfica para terminar.")
                plt.ioff(); plt.show() # Mantém a janela final aberta.
            return caminho_atual

        # Expansão do nó: Obtém os vizinhos e os adiciona na fronteira.
        for vizinho in obter_vizinhos(labirinto, posicao_atual):
            if vizinho not in visitados:
                if algoritmo == 'bfs':
                    visitados.add(vizinho) # Para BFS, marcamos como visitado ao adicionar na fronteira.
                novo_caminho = list(caminho_atual)
                novo_caminho.append(vizinho)
                fronteira.append(novo_caminho)
    
    # Se o loop terminar e não encontrarmos o fim, não há solução.
    print("\nSolução não encontrada.")
    if visualizar: plt.ioff(); plt.show()
    return None

def desenhar_solucao_terminal(labirinto, caminho):
    """Função utilitária para desenhar a solução final no terminal."""
    if caminho is None: return
    labirinto_desenhado = [list(linha) for linha in labirinto]
    for posicao in caminho[1:-1]:
        labirinto_desenhado[posicao[0]][posicao[1]] = '*'
    print("\n--- Labirinto com Solução Final (Terminal) ---")
    for linha in labirinto_desenhado:
        print("".join(linha))

# =============================================================================
# SEÇÃO 5: EXECUÇÃO PRINCIPAL DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    # O labirinto é o PROBLEMA. Você pode criar o seu!
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
    
    # 1. Mostra o problema ao usuário.
    print("--- Labirinto Original ---")
    for linha in meu_labirinto:
        print(linha)
    
    # 2. Pergunta qual algoritmo usar.
    escolha = ''
    while escolha.lower() not in ['bfs', 'dfs']:
        escolha = input("\nEscolha o algoritmo de busca (bfs ou dfs): ")

    # 3. Chama a função principal de busca.
    caminho_encontrado = buscar_no_labirinto(meu_labirinto, algoritmo=escolha, velocidade=0.4, visualizar=True)
    
    # 4. Exibe os resultados finais no terminal.
    desenhar_solucao_terminal(meu_labirinto, caminho_encontrado)
    if caminho_encontrado:
        print(f"\nCaminho encontrado pelo {escolha.upper()} com {len(caminho_encontrado) - 1} passos.")