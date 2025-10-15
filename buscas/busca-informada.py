# -*- coding: utf-8 -*-

"""
PROJETO 2: LABORATÓRIO DE BUSCA INFORMADA (UCS vs. Greedy vs. A*)

Este script implementa e compara visualmente os seguintes algoritmos de busca
baseados em custo e/ou heurística para resolver um labirinto 2D.

- Algoritmos Implementados:
  - Busca de Custo Uniforme (UCS): Prioriza o menor custo acumulado (g(n)).
  - Busca Gulosa (Greedy Best-First): Prioriza a menor distância estimada ao alvo (h(n)).
  - A* (A-Star): Prioriza a soma do custo acumulado e da estimativa (f(n) = g(n) + h(n)).
"""

# Importa bibliotecas essenciais
import heapq  # Essencial para implementar a Fila de Prioridade (Priority Queue)

# Importa e configura a biblioteca de visualização Matplotlib
import matplotlib
matplotlib.use('TkAgg')  # Define o "motor" gráfico para máxima compatibilidade
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def encontrar_posicao(labirinto, simbolo):
    """
    Localiza as coordenadas (linha, coluna) de um símbolo ('S' ou 'E') no labirinto.
    Define o estado inicial e o objetivo da busca.
    """
    for i, linha in enumerate(labirinto):
        for j, char in enumerate(linha):
            if char == simbolo:
                return (i, j)
    return None


def obter_vizinhos(labirinto, posicao):
    """
    Implementação da "Função Sucessora". Retorna uma lista de posições vizinhas
    válidas (não são paredes e estão dentro do labirinto) a partir de uma posição atual.
    """
    linha, coluna = posicao
    vizinhos = []
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, Baixo, Esquerda, Direita

    for dr, dc in movimentos:
        nova_linha, nova_coluna = linha + dr, coluna + dc
        if 0 <= nova_linha < len(labirinto) and 0 <= nova_coluna < len(labirinto[0]):
            if labirinto[nova_linha][nova_coluna] != '#':
                vizinhos.append((nova_linha, nova_coluna))
    return vizinhos


def heuristica_manhattan(posicao_a, posicao_b):
    """
    Calcula a Distância de Manhattan, nossa função heurística h(n).
    A Distância de Manhattan é a soma das distâncias horizontal e vertical,
    representando o número mínimo de movimentos em uma grade para ir de A para B.
    É uma heurística "admissível" porque nunca superestima o custo real.
    """
    (x1, y1) = posicao_a
    (x2, y2) = posicao_b
    return abs(x1 - x2) + abs(y1 - y2)


def preparar_visualizacao_grafica(labirinto, nome_algoritmo):
    """
    Configura a janela, o título e o mapa de cores para a animação gráfica.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define o "livro de regras" de cores para a visualização
    cores = ['black', 'white', 'green', 'red', 'orange', 'lightgray', 'blue']
    cmap = mcolors.ListedColormap(cores)
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Define um título inicial para a janela
    fig.canvas.manager.set_window_title(f'Buscando Solução com {nome_algoritmo}')
    return fig, ax, cmap, norm


def visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo, fim):
    """
    Desenha um único frame da animação, mostrando o estado atual e o "pensamento" do algoritmo.
    """
    # Converte o labirinto de caracteres para uma matriz numérica
    mapa_numerico = []
    for i, linha_str in enumerate(labirinto):
        linha_num = []
        for j, char in enumerate(linha_str):
            if char == '#': linha_num.append(0)
            elif char == 'S': linha_num.append(2)
            elif char == 'E': linha_num.append(3)
            else: linha_num.append(1)
        mapa_numerico.append(linha_num)
    
    # Pinta as células de acordo com o estado da busca
    for pos in visitados:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 5  # Visitado
    for pos in fronteira_coords:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 4  # Fronteira
    for pos in caminho_atual:
        if mapa_numerico[pos[0]][pos[1]] in (4,5): mapa_numerico[pos[0]][pos[1]] = 6  # Caminho Atual

    # Desenha a matriz e os textos
    ax.clear()
    ax.imshow(mapa_numerico, cmap=cmap, norm=norm)
    ax.set_xticks([]); ax.set_yticks([])

    # Adiciona o texto (g, h, f) em cada célula para mostrar o "pensamento"
    for pos, g_cost in visitados.items():
        h_cost = heuristica_manhattan(pos, fim)
        f_cost = g_cost + h_cost
        texto_display = ""
        if algoritmo == 'ucs':
            texto_display = f"g={g_cost}"
        elif algoritmo == 'greedy':
            texto_display = f"h={h_cost}"
        elif algoritmo == 'a_star':
            texto_display = f"{f_cost}\ng={g_cost} h={h_cost}"
        ax.text(pos[1], pos[0], texto_display, ha='center', va='center', fontsize=6, color='black')

    # Atualiza o título da janela com um placar dinâmico
    pos_atual = caminho_atual[-1]
    g_atual = visitados.get(pos_atual, 0)
    h_atual = heuristica_manhattan(pos_atual, fim)
    f_atual = g_atual + h_atual
    ax.set_title(f"Algoritmo: {algoritmo.upper()} | Expandindo: {pos_atual} | g={g_atual}, h={h_atual}, f={f_atual}")

    # Exibe o frame e pausa
    plt.draw()
    plt.pause(velocidade)


def buscar_no_labirinto_informado(labirinto, algoritmo='a_star', velocidade=0.05):
    """
    Função principal que executa UCS, Greedy ou A* usando uma Fila de Prioridade.
    """
    inicio = encontrar_posicao(labirinto, 'S')
    fim = encontrar_posicao(labirinto, 'E')
    if not inicio or not fim: return None

    # A 'fronteira' é uma Fila de Prioridade (Priority Queue), implementada com heapq.
    # Ela armazena tuplas: (prioridade, caminho). O heapq sempre manterá a tupla
    # de menor 'prioridade' no topo, pronta para ser retirada.
    fronteira = [(0, [inicio])]
    
    # 'visitados' armazena o menor custo g(n) encontrado até agora para cada nó.
    # Isso é essencial para o A* e UCS garantirem a otimalidade.
    visitados = {inicio: 0}
    
    fig, ax, cmap, norm = preparar_visualizacao_grafica(labirinto, algoritmo.upper())

    while fronteira:
        # Retira o caminho com a MENOR prioridade da fila.
        # A 'prioridade' é f(n) para A*, h(n) para Greedy, e g(n) para UCS.
        _, caminho_atual = heapq.heappop(fronteira)
        posicao_atual = caminho_atual[-1]

        # Otimização: se já encontramos um caminho mais curto para este nó, ignoramos o atual.
        if visitados[posicao_atual] < len(caminho_atual) - 1:
            continue

        # Chama a função de visualização para o passo atual
        fronteira_coords = [caminho[-1] for _, caminho in fronteira]
        visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo, fim)

        # TESTE DE OBJETIVO
        if posicao_atual == fim:
            print("\nSolução encontrada! Feche a janela gráfica para terminar.")
            plt.ioff(); plt.show()
            return caminho_atual

        # EXPANSÃO DO NÓ
        for vizinho in obter_vizinhos(labirinto, posicao_atual):
            # g(n) = Custo para chegar ao vizinho. Assumimos custo 1 por passo.
            novo_g_cost = visitados[posicao_atual] + 1
            
            if vizinho not in visitados or novo_g_cost < visitados[vizinho]:
                visitados[vizinho] = novo_g_cost
                
                # A 'prioridade' é calculada de forma diferente para cada um.
                prioridade = 0
                if algoritmo == 'ucs':
                    # A prioridade é apenas o custo do passado, g(n).
                    prioridade = novo_g_cost
                elif algoritmo == 'greedy':
                    # A prioridade é apenas a estimativa do futuro, h(n).
                    prioridade = heuristica_manhattan(vizinho, fim)
                elif algoritmo == 'a_star':
                    # A prioridade é o equilíbrio entre passado e futuro, g(n) + h(n).
                    h_cost = heuristica_manhattan(vizinho, fim)
                    prioridade = novo_g_cost + h_cost

                novo_caminho = list(caminho_atual)
                novo_caminho.append(vizinho)
                # Adiciona o novo caminho na Fila de Prioridade com sua prioridade calculada.
                heapq.heappush(fronteira, (prioridade, novo_caminho))

    print("\nSolução não encontrada.")
    plt.ioff(); plt.show()
    return None

def desenhar_solucao_terminal(labirinto, caminho):
    """Imprime a solução final no terminal."""
    if caminho is None: return
    labirinto_desenhado = [list(linha) for linha in labirinto]
    for posicao in caminho[1:-1]:
        labirinto_desenhado[posicao[0]][posicao[1]] = '*'
    print("\n--- Labirinto com Solução Final (Terminal) ---")
    for linha in labirinto_desenhado:
        print("".join(linha))

# Bloco principal de execução
if __name__ == "__main__":
    # Definição do problema: o labirinto em si
    # Você pode criar o seu! 
    # Apenas se atente ao tamanho, precisa ser nxn
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

    caminho_encontrado = buscar_no_labirinto_informado(meu_labirinto, algoritmo=escolha, velocidade=0.30)
    
    desenhar_solucao_terminal(meu_labirinto, caminho_encontrado)
    if caminho_encontrado:
        print(f"\nCaminho encontrado pelo {escolha.upper()} com {len(caminho_encontrado) - 1} passos.")