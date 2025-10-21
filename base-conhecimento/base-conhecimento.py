# -*- coding: utf-8 -*-

"""
PROJETO 6: AGENTE BASEADO EM CONHECIMENTO - O MUNDO DE WUMPUS (VISUAL)

Esta versão implementa o agente lógico com uma interface gráfica que mostra
o conteúdo de sua Base de Conhecimento (KB) sendo construída passo a passo.
"""
import random
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CLASSE DO AGENTE (Lógica de Raciocínio) ---
class AgenteWumpus:
    def __init__(self, tamanho_mundo=4):
        self.tamanho = tamanho_mundo
        self.posicao = (1, 1)
        self.visitados = set()
        self.kb = set()
        self.tell(f"OK_1,1")
        self.tell(f"~P_1,1")
        self.tell(f"~W_1,1")

    def tell(self, fato): self.kb.add(fato)
    def ask(self, query): return query in self.kb

    def obter_adjacentes(self, pos):
        x, y = pos
        adj = []
        if x > 1: adj.append((x - 1, y))
        if x < self.tamanho: adj.append((x + 1, y))
        if y > 1: adj.append((x, y - 1))
        if y < self.tamanho: adj.append((x, y + 1))
        return adj

    def atualizar_kb_percepcoes(self, percepcoes):
        x, y = self.posicao
        # Inferência a partir da AUSÊNCIA de percepções
        if 'Brisa' not in percepcoes:
            for ax, ay in self.obter_adjacentes(self.posicao):
                self.tell(f"~P_{ax},{ay}")
        if 'Fedor' not in percepcoes:
            for ax, ay in self.obter_adjacentes(self.posicao):
                self.tell(f"~W_{ax},{ay}")

        # Adiciona percepções POSITIVAS à KB
        if 'Brisa' in percepcoes: self.tell(f"B_{x},{y}")
        if 'Fedor' in percepcoes: self.tell(f"S_{x},{y}")

    def inferir_casas_seguras(self):
        # Percorre todo o mundo conhecido para fazer novas inferências
        for x in range(1, self.tamanho + 1):
            for y in range(1, self.tamanho + 1):
                # Se uma casa é segura, não pode ter poço nem Wumpus
                if self.ask(f"~P_{x},{y}") and self.ask(f"~W_{x},{y}"):
                    self.tell(f"OK_{x},{y}")
                # Lógica de inferência por resolução (simplificada)
                # Se sinto brisa em (x,y) e sei que um vizinho é seguro de poços, o outro PODE ter um poço.
                if self.ask(f"B_{x},{y}"):
                    adjacentes = self.obter_adjacentes((x,y))
                    adjacentes_desconhecidos = [p for p in adjacentes if not self.ask(f"~P_{p[0]},{p[1]}")]
                    if len(adjacentes_desconhecidos) == 1:
                        px, py = adjacentes_desconhecidos[0]
                        # Se só resta uma possibilidade, inferimos que o poço está lá
                        # (Este agente cauteloso não usa essa informação para agir, mas a armazena)
                        # self.tell(f"P_{px},{py}")

    def decidir_proxima_acao(self, percepcoes):
        self.visitados.add(self.posicao)
        self.atualizar_kb_percepcoes(percepcoes)
        self.inferir_casas_seguras()
        
        casas_seguras_para_ir = []
        for x in range(1, self.tamanho + 1):
            for y in range(1, self.tamanho + 1):
                if self.ask(f"OK_{x},{y}") and (x, y) not in self.visitados:
                    casas_seguras_para_ir.append((x, y))
        
        if not casas_seguras_para_ir:
            return None
        else:
            self.posicao = casas_seguras_para_ir[0]
            return self.posicao

# --- CLASSE DO AMBIENTE (Simulação) ---
class MundoWumpus:
    def __init__(self, tamanho=4):
        self.tamanho = tamanho
        self.wumpus = (random.randint(1, tamanho), random.randint(1, tamanho))
        while self.wumpus == (1, 1): self.wumpus = (random.randint(1, tamanho), random.randint(1, tamanho))
        self.pocos = []
        for x in range(1, tamanho + 1):
            for y in range(1, tamanho + 1):
                if (x, y) != (1, 1) and random.random() < 0.2:
                    self.pocos.append((x, y))
    
    def obter_percepcoes(self, pos):
        percepcoes = []
        adj = self._obter_adjacentes(pos)
        if pos in self.pocos: percepcoes.append('MORTE')
        if pos == self.wumpus: percepcoes.append('MORTE')
        if any(p in self.pocos for p in adj): percepcoes.append('Brisa')
        if any(p == self.wumpus for p in adj): percepcoes.append('Fedor')
        return percepcoes

    def _obter_adjacentes(self, pos):
        x, y = pos; adj = []
        if x > 1: adj.append((x - 1, y))
        if x < self.tamanho: adj.append((x + 1, y))
        if y > 1: adj.append((x, y - 1))
        if y < self.tamanho: adj.append((x, y + 1))
        return adj

# --- LÓGICA DE VISUALIZAÇÃO ---
def preparar_visualizacao(tamanho):
    plt.ion()
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.canvas.manager.set_window_title('Projeto 6: Agente Lógico no Mundo de Wumpus')
    return fig, ax

def desenhar_mundo(ax, tamanho, mundo, titulo):
    """Desenha o mapa da verdade, com a posição real dos perigos."""
    ax.clear()
    ax.set_title(titulo)
    ax.set_xticks(range(tamanho + 1)); ax.set_yticks(range(tamanho + 1))
    ax.grid(True)
    ax.set_xlim(0.5, tamanho + 0.5); ax.set_ylim(0.5, tamanho + 0.5)
    for x in range(1, tamanho + 1):
        for y in range(1, tamanho + 1):
            if (x, y) == mundo.wumpus:
                ax.text(x, y, "W", ha='center', va='center', fontsize=20, color='red')
            if (x, y) in mundo.pocos:
                ax.text(x, y, "P", ha='center', va='center', fontsize=20, color='black')

def desenhar_passo_agente(ax, agente, percepcoes, passo):
    """Desenha o mapa mental (KB) do agente."""
    ax.clear()
    ax.set_title(f"Mapa Mental do Agente (Passo {passo})")
    ax.set_xticks(range(agente.tamanho + 1)); ax.set_yticks(range(agente.tamanho + 1))
    ax.grid(True)
    ax.set_xlim(0.5, agente.tamanho + 0.5); ax.set_ylim(0.5, agente.tamanho + 0.5)

    for x in range(1, agente.tamanho + 1):
        for y in range(1, agente.tamanho + 1):
            textos = []
            cor_fundo = 'white'
            if (x,y) in agente.visitados:
                cor_fundo = 'lightgray'
                if agente.ask(f"B_{x},{y}"): textos.append("Brisa")
                if agente.ask(f"S_{x},{y}"): textos.append("Fedor")
            
            if agente.ask(f"OK_{x},{y}") and (x,y) not in agente.visitados:
                textos.append("OK")
                cor_fundo = 'lightgreen'

            if not agente.ask(f"OK_{x},{y}") and (x,y) not in agente.visitados:
                 # Lógica de incerteza
                 adjacentes_visitados = [p for p in agente.obter_adjacentes((x,y)) if p in agente.visitados]
                 if any(agente.ask(f"B_{p[0]},{p[1]}") for p in adjacentes_visitados):
                     if not agente.ask(f"~P_{x},{y}"): textos.append("P?")
                 if any(agente.ask(f"S_{p[0]},{p[1]}") for p in adjacentes_visitados):
                     if not agente.ask(f"~W_{x},{y}"): textos.append("W?")

            # Desenha o fundo da célula
            rect = patches.Rectangle((x-0.5, y-0.5), 1, 1, facecolor=cor_fundo, zorder=1)
            ax.add_patch(rect)
            
            # Desenha o texto de conhecimento
            ax.text(x, y, "\n".join(textos), ha='center', va='center', fontsize=9, color='blue')

    # Desenha o Agente
    ax.text(agente.posicao[0], agente.posicao[1], "A", ha='center', va='center', fontsize=20, color='black', weight='bold', zorder=2)
    plt.draw(); plt.pause(1.5)

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    TAMANHO_MUNDO = 4
    mundo = MundoWumpus(tamanho=TAMANHO_MUNDO)
    agente = AgenteWumpus(tamanho_mundo=TAMANHO_MUNDO)
    
    fig, (ax_agente, ax_verdade) = preparar_visualizacao(TAMANHO_MUNDO)
    desenhar_mundo(ax_verdade, TAMANHO_MUNDO, mundo, "Mapa da Verdade (Realidade)")
    
    for passo in range(1, 16):
        percepcoes = mundo.obter_percepcoes(agente.posicao)
        
        desenhar_passo_agente(ax_agente, agente, percepcoes, passo)

        if 'MORTE' in percepcoes:
            ax_agente.set_title(f"AGENTE MORREU EM {agente.posicao}! Fim de Jogo.", color='red')
            plt.ioff(); plt.show()
            break
        
        proximo_movimento = agente.decidir_proxima_acao(percepcoes)
        
        if proximo_movimento is None:
            ax_agente.set_title("Exploração Segura Concluída!")
            plt.ioff(); plt.show()
            break
    else: # Executa se o loop terminar sem 'break'
        ax_agente.set_title("Exploração Segura Concluída!")
        plt.ioff(); plt.show()