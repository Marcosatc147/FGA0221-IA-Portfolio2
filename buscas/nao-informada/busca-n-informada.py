"""
PROJETO 1: BUSCA NÃO INFORMADA (BFS vs. DFS)

Este script implementa e compara visualmente os algoritmos de busca cega:
- Busca em Largura (BFS)
- Busca em Profundidade (DFS)
"""

# Importa bibliotecas essenciais do Python
from collections import deque  # Estrutura de dados otimizada para Fila (Queue), usada no BFS

# Importa a biblioteca de visualização Matplotlib
import matplotlib
matplotlib.use('TkAgg')  # Define o "motor" gráfico para máxima compatibilidade
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def encontrar_posicao(labirinto, simbolo):
    """
    Localiza as coordenadas (linha, coluna) de um símbolo específico ('S' ou 'E') no labirinto.
    Esta função é usada para determinar o estado inicial e o objetivo da busca.
    """
    for i, linha in enumerate(labirinto):
        for j, char in enumerate(linha):
            if char == simbolo:
                return (i, j)
    return None  # Retorna None se o símbolo não for encontrado


def obter_vizinhos(labirinto, posicao):
    """
    Retorna uma lista de posições vizinhas válidas a partir de uma posição atual.
    Esta é a implementação da "Função Sucessora", que define as ações possíveis.
    """
    linha, coluna = posicao
    vizinhos = []
    # Define os 4 movimentos possíveis: Cima, Baixo, Esquerda, Direita
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for dr, dc in movimentos:  # dr = delta-linha, dc = delta-coluna
        nova_linha, nova_coluna = linha + dr, coluna + dc

        # Verifica se o movimento está dentro dos limites do labirinto
        if 0 <= nova_linha < len(labirinto) and 0 <= nova_coluna < len(labirinto[0]):
            # Verifica se a nova posição não é uma parede
            if labirinto[nova_linha][nova_coluna] != '#':
                vizinhos.append((nova_linha, nova_coluna))
    return vizinhos


def preparar_visualizacao_grafica(labirinto, nome_algoritmo):
    """
    Configura a janela, o título e o mapa de cores para a animação gráfica com Matplotlib.
    """
    plt.ion()  # Ativa o modo interativo, que permite que a janela seja atualizada
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define quais cores serão usadas para cada número na matriz do labirinto
    cores = ['black', 'white', 'green', 'red', 'orange', 'lightgray', 'blue']
    cmap = mcolors.ListedColormap(cores)
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    return fig, ax, cmap, norm


def visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo):
    """
    Desenha um único "frame" da animação, mostrando o estado atual da busca.
    """
    # 1. Converte o labirinto de caracteres para uma matriz numérica para poder ser desenhado
    mapa_numerico = []
    for i, linha_str in enumerate(labirinto):
        linha_num = []
        for j, char in enumerate(linha_str):
            if char == '#': linha_num.append(0)    # 0 = Parede
            elif char == 'S': linha_num.append(2)  # 2 = Início
            elif char == 'E': linha_num.append(3)  # 3 = Fim
            else: linha_num.append(1)              # 1 = Caminho
        mapa_numerico.append(linha_num)
    
    # 2. Pinta as células com base no estado atual da busca
    for pos in visitados:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 5 # 5 = Visitado
    for pos in fronteira_coords:
        if mapa_numerico[pos[0]][pos[1]] == 1: mapa_numerico[pos[0]][pos[1]] = 4 # 4 = Fronteira
    for pos in caminho_atual:
        if mapa_numerico[pos[0]][pos[1]] in (4,5): mapa_numerico[pos[0]][pos[1]] = 6 # 6 = Caminho Atual

    # 3. Limpa a tela e desenha a nova matriz
    ax.clear()
    ax.imshow(mapa_numerico, cmap=cmap, norm=norm)
    ax.set_xticks([]); ax.set_yticks([]) # Remove os eixos x e y para um visual mais limpo

    # 4. Escreve o custo 'g' (profundidade) em cada célula visitada
    for pos, g_cost in visitados.items():
        ax.text(pos[1], pos[0], f"g={g_cost}", ha='center', va='center', fontsize=6, color='black')

    # 5. Atualiza o título da janela com informações do passo atual
    pos_atual = caminho_atual[-1]
    g_atual = visitados.get(pos_atual, 0)
    ax.set_title(f"Algoritmo: {algoritmo.upper()} | Expandindo: {pos_atual} | g={g_atual} (Profundidade)")

    # 6. Exibe o desenho e pausa por um curto período
    plt.draw()
    plt.pause(velocidade)


def buscar_no_labirinto_nao_informado(labirinto, algoritmo='bfs', velocidade=0.05):
    """
    Função principal de busca. Executa BFS ou DFS e controla a visualização.
    """
    inicio = encontrar_posicao(labirinto, 'S')
    fim = encontrar_posicao(labirinto, 'E')
    if not inicio or not fim: return None

    # DIFERENÇA ENTRE BFS E DFS 
    if algoritmo == 'bfs':
        # BFS usa uma FILA (Queue), onde o primeiro a entrar é o primeiro a sair.
        fronteira = deque([[inicio]]) 
    else: # algoritmo == 'dfs'
        # DFS usa uma PILHA (Stack), onde o último a entrar é o primeiro a sair.
        fronteira = [[inicio]]

    # O dicionário 'visitados' armazena as posições já visitadas e sua profundidade (g_cost).
    # Isso evita loops e reprocessamento, caracterizando uma busca em grafo.
    visitados = {inicio: 0}

    # Prepara a janela gráfica para a animação
    fig, ax, cmap, norm = preparar_visualizacao_grafica(labirinto, algoritmo.upper())

    # Loop principal: continua enquanto houver nós na fronteira para explorar
    while fronteira:
        # A operação de retirada da fronteira define o comportamento do algoritmo
        if algoritmo == 'bfs':
            caminho_atual = fronteira.popleft() # Retira o nó mais antigo (o menos profundo)
        else: # algoritmo == 'dfs'
            caminho_atual = fronteira.pop() # Retira o nó mais recente (o mais profundo)
        
        posicao_atual = caminho_atual[-1]
        
        if algoritmo == 'dfs' and posicao_atual not in visitados:
            visitados[posicao_atual] = len(caminho_atual) - 1

        # Prepara uma lista de coordenadas da fronteira para a visualização
        fronteira_coords = [caminho[-1] for caminho in fronteira]
        # Chama a função para desenhar o passo atual
        visualizar_passo_grafico(ax, labirinto, visitados, fronteira_coords, caminho_atual, cmap, norm, velocidade, algoritmo)

        # TESTE DE OBJETIVO: Verifica se a posição atual é a saída
        if posicao_atual == fim:
            print("\nSolução encontrada! Feche a janela gráfica para terminar.")
            plt.ioff(); plt.show() # Mantém a janela final aberta para análise
            return caminho_atual

        # EXPANSÃO DO NÓ: Para cada vizinho da posição atual...
        for vizinho in obter_vizinhos(labirinto, posicao_atual):
            # ...se o vizinho ainda não foi visitado...
            if vizinho not in visitados:
                # ...cria um novo caminho e o adiciona à fronteira.
                novo_caminho = list(caminho_atual)
                novo_caminho.append(vizinho)
                fronteira.append(novo_caminho)
                
                if algoritmo == 'bfs':
                    # No BFS, marcamos como visitado ao adicionar à fronteira para evitar duplicatas.
                    visitados[vizinho] = len(novo_caminho) - 1

    # Se a fronteira esvaziar e o objetivo não for encontrado, não há solução.
    print("\nSolução não encontrada.")
    plt.ioff(); plt.show()
    return None


def desenhar_solucao_terminal(labirinto, caminho):
    """
    Imprime o labirinto com o caminho final destacado no terminal.
    """
    if caminho is None: return
    labirinto_desenhado = [list(linha) for linha in labirinto]
    for posicao in caminho[1:-1]:
        labirinto_desenhado[posicao[0]][posicao[1]] = '*'
    print("\n--- Labirinto com Solução Final (Terminal) ---")
    for linha in labirinto_desenhado:
        print("".join(linha))


# Bloco principal: executado quando o script é iniciado
if __name__ == "__main__":
    print(__doc__)
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
    
    # Apresenta o problema ao usuário
    print("--- Labirinto Original ---")
    for linha in meu_labirinto:
        print(linha)
    
    # Pede ao usuário para escolher o algoritmo
    escolha = ''
    while escolha.lower() not in ['bfs', 'dfs']:
        escolha = input("\nEscolha o algoritmo de busca (bfs ou dfs): ")

    # Chama a função principal de busca com os parâmetros escolhidos
    caminho_encontrado = buscar_no_labirinto_nao_informado(meu_labirinto, algoritmo=escolha, velocidade=0.30)
    
    # Exibe os resultados finais no terminal
    desenhar_solucao_terminal(meu_labirinto, caminho_encontrado)
    if caminho_encontrado:
        print(f"\nCaminho encontrado pelo {escolha.upper()} com {len(caminho_encontrado) - 1} passos.")
