"""
PROJETO 3 (ANÁLISE): BUSCA COMPLEXA - HILL-CLIMBING vs. SIMULATED ANNEALING
"""
import random
import math
import time

def calcular_ataques(estado):
    """
    Função Objetivo: Calcula o número total de pares de rainhas se atacando.
    """
    n = len(estado)
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            if estado[i] == estado[j] or abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
    return ataques

# --- VERSÕES "BATCH" (SILENCIOSAS) DOS ALGORITMOS ---

def hill_climbing_batch(n_rainhas=8):
    """Versão do Hill-Climbing sem visualização, otimizada para execuções rápidas."""
    estado_atual = [random.randint(0, n_rainhas - 1) for _ in range(n_rainhas)]
    while True:
        ataques_atuais = calcular_ataques(estado_atual)
        if ataques_atuais == 0:
            return 0
        
        melhor_vizinho = None
        melhores_ataques = ataques_atuais
        
        for coluna in range(n_rainhas):
            posicao_original = estado_atual[coluna]
            for linha in range(n_rainhas):
                if linha == posicao_original: continue
                estado_vizinho = list(estado_atual)
                estado_vizinho[coluna] = linha
                ataques_vizinho = calcular_ataques(estado_vizinho)
                if ataques_vizinho < melhores_ataques:
                    melhores_ataques = ataques_vizinho
                    melhor_vizinho = estado_vizinho
        
        if melhores_ataques >= ataques_atuais:
            return ataques_atuais
        
        estado_atual = melhor_vizinho

def simulated_annealing_batch(n_rainhas=8, temperatura_inicial=100.0, taxa_resfriamento=0.995):
    """Versão do Simulated Annealing sem visualização."""
    estado_atual = [random.randint(0, n_rainhas - 1) for _ in range(n_rainhas)]
    temperatura = temperatura_inicial
    
    while temperatura > 0.1:
        ataques_atuais = calcular_ataques(estado_atual)
        if ataques_atuais == 0:
            return 0

        coluna = random.randint(0, n_rainhas - 1)
        nova_linha = random.randint(0, n_rainhas - 1)
        estado_vizinho = list(estado_atual)
        estado_vizinho[coluna] = nova_linha
        ataques_vizinho = calcular_ataques(estado_vizinho)
        
        delta_energia = ataques_vizinho - ataques_atuais
        
        if delta_energia < 0 or (temperatura > 0 and random.random() < math.exp(-delta_energia / temperatura)):
            # --- CORREÇÃO APLICADA AQUI ---
            # Atualiza o estado para a CONFIGURAÇÃO do vizinho, não para o NÚMERO DE ATAQUES.
            estado_atual = estado_vizinho
            
        temperatura *= taxa_resfriamento
        
    return calcular_ataques(estado_atual)

# --- FUNÇÃO DE ANÁLISE (BANCADA DE TESTES) ---

def executar_analise(nome_algoritmo, funcao_busca, n_execucoes, n_rainhas, **kwargs):
    """Executa um algoritmo de busca N vezes, mede o tempo e calcula a taxa de sucesso."""
    print(f"\n--- Iniciando Análise para o Algoritmo: {nome_algoritmo.upper()} ---")
    print(f"Executando {n_execucoes} vezes para um tabuleiro de {n_rainhas} rainhas...")
    
    sucessos = 0
    tempo_inicial = time.time()
    
    for i in range(n_execucoes):
        print(f"  Execução {i+1}/{n_execucoes}...", end='\r')
        ataques_finais = funcao_busca(n_rainhas=n_rainhas, **kwargs)
        if ataques_finais == 0:
            sucessos += 1
            
    tempo_final = time.time()
    tempo_total = tempo_final - tempo_inicial
    taxa_sucesso = (sucessos / n_execucoes) * 100
    
    print("\n\n--- Relatório de Análise Concluído ---")
    print(f"Algoritmo Testado: {nome_algoritmo.upper()}")
    print(f"Tempo Total de Execução: {tempo_total:.2f} segundos")
    print(f"Soluções Encontradas (Sucessos): {sucessos} de {n_execucoes}")
    print(f"Taxa de Sucesso: {taxa_sucesso:.2f}%")
    print("-" * 40)

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---

if __name__ == "__main__":
    NUM_RAINHAS = 8
    NUM_EXECUCOES = 100

    params_sa = {
        'temperatura_inicial': 1000.0,
        'taxa_resfriamento': 0.999
    }

    executar_analise(
        'Hill-Climbing',
        hill_climbing_batch,
        n_execucoes=NUM_EXECUCOES,
        n_rainhas=NUM_RAINHAS
    )

    executar_analise(
        'Simulated Annealing',
        simulated_annealing_batch,
        n_execucoes=NUM_EXECUCOES,
        n_rainhas=NUM_RAINHAS,
        **params_sa
    )