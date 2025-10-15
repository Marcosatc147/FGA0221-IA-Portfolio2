# Projetos de Métodos Clássicos de Inteligência Artificial

Este repositório contém os projetos desenvolvidos para a disciplina de Inteligência Artificial (FGA0221), lecionada pelo Prof. Fabiano Araujo Soares. O foco é a implementação e análise de métodos clássicos de IA, também conhecidos como GOFAI (Good Old-Fashioned Artificial Intelligence).

## Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Bibliotecas:**
    * `matplotlib`: Para a visualização gráfica dos algoritmos de busca.

## Configuração do Ambiente e Instalação

Para executar os projetos localmente, siga os passos abaixo. Recomenda-se o uso de um ambiente virtual (`venv`) para isolar as dependências.

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DO_SEU_REPOSITORIO]
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
    Instale as bibliotecas com o comando:
    ```bash
    pip install -r requirements.txt
    ```

---

## Projetos Desenvolvidos

### 1. Busca Não Informada (BFS vs. DFS)

* **Descrição:** Este projeto implementa e compara dois algoritmos de busca cega (não informada) — Busca em Largura (BFS) e Busca em Profundidade (DFS) — para resolver um labirinto 2D. O programa oferece uma visualização gráfica colorida que mostra o processo de exploração de cada algoritmo passo a passo, destacando as diferenças fundamentais em suas estratégias de busca (expansão em "onda" do BFS vs. "mergulho" profundo do DFS).
* **Conceitos Aplicados:** Formulação de Problemas, Função Sucessora, Estruturas de Fila (Queue) e Pilha (Stack), Busca em Grafo.
* **Arquivo:** `buscas/busca-n-informada.py`
* **Como Usar:**
    1.  Navegue até a pasta do projeto: `cd buscas`
    2.  Execute o script: `python busca-n-informada.py`
    3.  No terminal, escolha o algoritmo a ser executado (`bfs` ou `dfs`).
    4.  Uma janela gráfica será aberta, mostrando a animação da busca. Ao final, a janela pode ser fechada, e o resultado final será impresso no terminal.

### 2. Projeto de Busca Informada

* **(A ser desenvolvido)**
* **Objetivo:** Implementação de um algoritmo de busca heurística, como o A* (A-Star), para encontrar o caminho de custo mínimo em um grafo com custos variados.

### 3. Projeto de Busca Complexa

* **(A ser desenvolvido)**
* **Objetivo:** Implementação de um algoritmo de busca local, como o Hill-Climbing, para resolver um problema de otimização onde o caminho não importa, apenas o estado final.

### 4. Projeto de Algoritmo Genético

* **(A ser desenvolvido)**
* **Objetivo:** Implementação de um algoritmo genético para encontrar a solução de um problema complexo, inspirado nos princípios da evolução natural (seleção, crossover e mutação).

### 5. Projeto de Satisfação de Restrições (CSP)

* **(A ser desenvolvido)**
* **Objetivo:** Modelagem e resolução de um Problema de Satisfação de Restrições (CSP), como a Coloração de Mapas, utilizando o algoritmo de Backtracking combinado com heurísticas (MRV) e Forward Checking.

### 6. Projeto com Base de Conhecimento

* **(A ser desenvolvido)**
* **Objetivo:** Implementação de um agente lógico simples que utiliza uma Base de Conhecimento (KB) e inferência para tomar decisões em um ambiente simulado, como o Mundo de Wumpus.

---

## Autor

**Marcos Castilhos**
* **GitHub:** [github.com/marcosatc147]
