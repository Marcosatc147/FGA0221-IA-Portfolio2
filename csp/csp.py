
"""
PROJETO 5: PROBLEMAS DE SATISFAÇÃO DE RESTRIÇÕES (CSP)

Este script resolve o problema da Coloração de Mapas (Austrália) com uma
visualização gráfica do algoritmo de Backtracking, MRV e Forward Checking.
"""

import copy
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def preparar_visualizacao(coordenadas, restricoes, titulo):
    """Configura a janela e desenha o grafo base do mapa."""
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.canvas.manager.set_window_title(titulo)

    # Desenha as arestas (restrições)
    for estado, vizinhos in restricoes.items():
        x1, y1 = coordenadas[estado]
        for vizinho in vizinhos:
            x2, y2 = coordenadas[vizinho]
            ax.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=1, zorder=1)
    
    return fig, ax

def desenhar_passo_csp(ax, coordenadas, atribuicao, dominios, status_texto):
    """Desenha o estado atual do grafo de restrições."""
    ax.clear() # Limpa o frame anterior
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(status_texto, fontsize=12)

    # Redesenha as arestas
    for estado, vizinhos in restricoes.items():
        x1, y1 = coordenadas[estado]
        for vizinho in vizinhos:
            x2, y2 = coordenadas[vizinho]
            ax.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=1, zorder=1)

    # Desenha os nós (estados)
    for estado, (x, y) in coordenadas.items():
        cor_no = 'white'
        if estado in atribuicao:
            cor_no = atribuicao[estado].lower()

        # Desenha o círculo do nó
        circulo = plt.Circle((x, y), 0.5, facecolor=cor_no, edgecolor='black', linewidth=2, zorder=2)
        ax.add_patch(circulo)
        ax.text(x, y, estado, ha='center', va='center', fontsize=10, weight='bold')

        # Mostra o domínio atual para nós não atribuídos
        if estado not in atribuicao:
            dominio_str = "\n".join(dominios[estado])
            ax.text(x, y - 0.8, dominio_str, ha='center', va='top', fontsize=8, color='blue')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    plt.draw()
    plt.pause(0.8)

def backtracking_search_visual(atribuicao, variaveis, dominios, restricoes, ax, coordenadas):
    """Implementação do Backtracking com chamadas de visualização."""
    
    # Condição de parada: sucesso!
    if len(atribuicao) == len(variaveis):
        return atribuicao

    var = selecionar_variavel_mrv(atribuicao, variaveis, dominios)

    # Tenta cada valor no domínio da variável
    for valor in dominios[var]:
        dominios_locais = copy.deepcopy(dominios)
        atribuicao[var] = valor
        
        status = f"Tentando {var} = {valor}"
        desenhar_passo_csp(ax, coordenadas, atribuicao, dominios_locais, status)

        # Forward Checking
        if forward_check(var, valor, dominios_locais, restricoes):
            status = f"Forward Checking OK para {var} = {valor}. Propagando restrições..."
            desenhar_passo_csp(ax, coordenadas, atribuicao, dominios_locais, status)
            
            resultado = backtracking_search_visual(atribuicao, variaveis, dominios_locais, restricoes, ax, coordenadas)
            
            if resultado is not None:
                return resultado
        
        # Backtrack
        del atribuicao[var]
        status = f"Backtrack! Conflito com {var} = {valor}. Desfazendo atribuição."
        desenhar_passo_csp(ax, coordenadas, atribuicao, dominios, status)

    return None

# --- Funções Lógicas do CSP (sem alteração) ---
def selecionar_variavel_mrv(atribuicao, variaveis, dominios):
    variaveis_nao_atribuidas = [v for v in variaveis if v not in atribuicao]
    return min(variaveis_nao_atribuidas, key=lambda var: len(dominios[var]))

def forward_check(var, valor, dominios, restricoes):
    for vizinho in restricoes[var]:
        if valor in dominios[vizinho]:
            dominios[vizinho].remove(valor)
            if not dominios[vizinho]:
                return False
    return True

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    variaveis = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    dominios = {var: ['Red', 'Green', 'Blue'] for var in variaveis}
    restricoes = {
        'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'], 'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'], 'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
    }
    # Coordenadas para desenhar o grafo de forma parecida com o mapa
    coordenadas = {
        'WA': (1.5, 4.5), 'NT': (3.5, 6), 'SA': (4, 3.5), 'Q': (6, 5.5),
        'NSW': (7, 3.5), 'V': (6.5, 1.5), 'T': (7.5, 0.5)
    }

    print("--- Problema de Coloração de Mapas (Austrália) ---")
    
    fig, ax = preparar_visualizacao(coordenadas, restricoes, "Projeto 5: CSP - Coloração de Mapas")
    desenhar_passo_csp(ax, coordenadas, {}, dominios, "Estado Inicial")
    
    solucao = backtracking_search_visual({}, variaveis, dominios, restricoes, ax, coordenadas)

    if solucao:
        status_final = "Solução Encontrada!"
        desenhar_passo_csp(ax, coordenadas, solucao, dominios, status_final)
        print("\n--- Solução Final ---")
        for estado, cor in sorted(solucao.items()):
            print(f"- {estado}: {cor}")
        print("\nFeche a janela gráfica para terminar.")
        plt.ioff()
        plt.show()
    else:
        status_final = "Nenhuma solução encontrada!"
        desenhar_passo_csp(ax, coordenadas, {}, dominios, status_final)
        print("\n--- Nenhuma solução foi encontrada ---")