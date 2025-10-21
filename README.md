# Projetos de Métodos Clássicos de Inteligência Artificial

Este repositório contém os projetos desenvolvidos para a disciplina de Inteligência Artificial (FGA0221), lecionada pelo Prof. Fabiano Araujo Soares. O foco é a implementação e análise de métodos clássicos de IA, também conhecidos como GOFAI (Good Old-Fashioned Artificial Intelligence).

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12 (ou compatível)
* **Bibliotecas:**
    * `matplotlib`: Para a visualização gráfica dos algoritmos.
    * `numpy`: Utilizado em algumas visualizações e cálculos.

## Configuração do Ambiente e Instalação

Para executar os projetos localmente, siga os passos abaixo. Recomenda-se o uso de um ambiente virtual (`venv`) para isolar as dependências.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Marcosatc147/FGA0221-IA-Portfolio2.git
    cd FGA0221-IA-Portfolio2
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o venv
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no Linux ou macOS
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Certifique-se de ter um arquivo `requirements.txt` na raiz do projeto com o seguinte conteúdo:
    ```
    matplotlib
    numpy
    ```
    Em seguida, instale as bibliotecas com o comando:
    ```bash
    pip install -r requirements.txt
    ```

---

## Projetos Desenvolvidos

*Observação: Os nomes dos arquivos podem variar ligeiramente dependendo de como você os salvou.*

### 1. Busca Não Informada (BFS vs. DFS)

* **Descrição:** Implementa e compara visualmente BFS e DFS na resolução de um labirinto 2D. A visualização gráfica mostra o processo de exploração passo a passo e o custo (`g`) de cada célula.
* **Conceitos:** Formulação de Problemas, Fila (BFS), Pilha (DFS), Busca em Grafo (Visitados).
* **Arquivo:** `buscas/nao-informada/busca-n-informada.py` (ou similar)
* **Como Usar:** Execute o script e escolha `bfs` or `dfs` no terminal para ver a animação.

### 2. Busca Informada (UCS vs. Greedy vs. A\*)

* **Descrição:** Laboratório visual que compara UCS (como base), Greedy Best-First e A\* na resolução do mesmo labirinto. A visualização mostra os valores de `g(n)`, `h(n)` e `f(n)` para cada algoritmo.
* **Conceitos:** Heurística Admissível (Distância de Manhattan), Fila de Prioridade (`heapq`), UCS, Greedy, A\*.
* **Arquivo:** `buscas/informada/busca-informada.py` (ou similar)
* **Como Usar:** Execute o script e escolha `ucs`, `greedy` or `a_star` no terminal para ver a animação comparativa.

### 3. Busca Complexa (Local Search)

* **Descrição:** Explora algoritmos de Busca Local para o problema de otimização das N-Rainhas (minimizar ataques).
    * **Hill Climbing:** Implementação visual (`busca-complexa.py`) que mostra a subida de encosta e o problema do mínimo local. Destaca rainhas em conflito.
    * **Simulated Annealing:** Implementação visual (`simulated_annealing.py`) que demonstra como a aceitação probabilística de piores movimentos (controlada pela temperatura) pode escapar de mínimos locais. Usa parâmetros otimizados.
    * **Análise Comparativa:** Script (`hc-vs-sa.py`) que executa Hill Climbing e Simulated Annealing 100 vezes para comparar suas taxas de sucesso empiricamente.
* **Conceitos:** Busca Local, Otimização, Função Objetivo, Mínimos Locais, Hill Climbing, Simulated Annealing, Análise Estatística.
* **Arquivos:** `buscas/complexa/busca-complexa.py`, `buscas/simulated_annealing.py`, `buscas/hc-vs-sa.py` (ou similares)
* **Como Usar:** Execute os scripts visuais individualmente. Execute o script de análise para obter o relatório de taxa de sucesso no terminal.

### 4. Algoritmo Genético

* **Descrição:** Resolve o problema das N-Rainhas utilizando um Algoritmo Genético. A visualização mostra o melhor indivíduo (tabuleiro) de cada geração e um gráfico da evolução do fitness da população.
* **Conceitos:** Algoritmo Genético, População, Fitness, Seleção (Torneio), Crossover (Ponto Único), Mutação, Elitismo.
* **Arquivo:** `algoritmo-genetico/algoritmo_genetico.py` (ou similar)
* **Como Usar:** Execute o script. Observe a janela gráfica mostrando o melhor tabuleiro à esquerda e a curva de fitness à direita.

### 5. Projeto de Satisfação de Restrições (CSP)

* **Descrição:** Implementa a resolução de CSPs usando Backtracking com otimizações.
    * **Coloração de Mapas:** Script visual (`csp_mapa_visual.py`) que resolve o problema da coloração da Austrália, mostrando o grafo de restrições, a atribuição de cores, o Forward Checking (redução de domínios) e o Backtrack.
    * **Alocação de Aulas (Timetabling):** Script de terminal (`csp_timetabling.py`) que resolve um problema mais complexo de alocação de aulas, introduzindo restrições duras vs. suaves (preferências) e buscando a solução ótima (menor penalidade). Inclui um laboratório para testar diferentes cenários.
* **Conceitos:** CSP (Variáveis, Domínios, Restrições), Backtracking, Heurística MRV, Forward Checking, Restrições Duras/Suaves, Otimização CSP.
* **Arquivos:** `csp/csp_mapa_visual.py`, `csp/csp_timetabling.py` (ou similares)
* **Como Usar:** Execute o script do mapa para a visualização gráfica. Execute o script de timetabling (altere `CENARIO_TESTE` para experimentar) para análise via terminal.

### 6. Projeto com Base de Conhecimento

* **Descrição:** Implementa um agente lógico simples para o Mundo de Wumpus. O agente usa uma Base de Conhecimento (KB) e regras de inferência (baseadas na ausência de percepções) para determinar casas seguras e explorar o ambiente. A visualização gráfica mostra o "mapa mental" do agente sendo construído passo a passo em comparação com o mapa real.
* **Conceitos:** Agente Baseado em Conhecimento, Base de Conhecimento (KB), Inferência Lógica (Proposicional Simplificada), Ciclo Perceber-Raciocinar-Agir.
* **Arquivo:** `banco-conhecimento/base-conhecimento.py` (ou similar)
* **Como Usar:** Execute o script. Observe a janela gráfica com os dois mapas (mental vs. real) e acompanhe o raciocínio do agente.

---

## Autor

**Marcos Castilhos**
* [**GitHub**](github.com/marcosatc147)
