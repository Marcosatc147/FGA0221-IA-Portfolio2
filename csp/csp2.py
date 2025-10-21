# -*- coding: utf-8 -*-

"""
PROJETO 5 (LABORATÓRIO): CSP - ALOCAÇÃO DE AULAS

Esta versão final inclui um "laboratório de testes" para experimentar
diferentes configurações de variáveis, domínios e restrições, e analisar
o impacto no resultado da busca. (Versão com correção de sintaxe)
"""
import time
import copy
import os

# --- 1. FUNÇÕES DO MODELO CSP ---

def gerar_dominios_iniciais(variaveis, professores, salas, horarios):
    """Gera o domínio completo para cada disciplina (produto cartesiano)."""
    dominio_completo = []
    for prof in professores:
        for sala in salas:
            for horario in horarios:
                dominio_completo.append((prof, sala, horario))
    return {var: copy.deepcopy(dominio_completo) for var in variaveis}

def aplicar_restricoes_iniciais(dominios, restricoes_duras):
    """Pré-processa os domínios aplicando restrições unárias e de requisitos."""
    dominios_podados = copy.deepcopy(dominios)
    for disciplina, valores in dominios.items():
        valores_validos = []
        for valor in valores:
            if restricoes_duras['requisito_sala'](disciplina, valor) and \
               restricoes_duras['capacitacao_prof'](disciplina, valor):
                valores_validos.append(valor)
        dominios_podados[disciplina] = valores_validos
    return dominios_podados

def is_consistent(disciplina, valor, atribuicao, restricoes_duras):
    """Verifica se uma nova atribuição viola alguma RESTRIÇÃO DURA com as já existentes."""
    return restricoes_duras['recurso_unico'](disciplina, valor, atribuicao)

def calcular_penalidade(solucao, restricoes_suaves):
    """Calcula o "score" de uma solução baseado na violação de RESTRIÇÕES SUAVES."""
    penalidade = 0
    violacoes = []
    for funcao_penalidade in restricoes_suaves:
        p, v = funcao_penalidade(solucao)
        penalidade += p
        violacoes.extend(v)
    return penalidade, violacoes

def imprimir_passo_terminal(variaveis, atribuicao, melhor_score, status_texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- Buscando Melhor Alocação ---")
    print(f"Melhor Score Encontrado: {melhor_score if melhor_score != float('inf') else 'N/A'}")
    print(f"Status: {status_texto}\n")
    print("Atribuição Parcial:")
    for disciplina in variaveis:
        if disciplina in atribuicao:
            prof, sala, horario = atribuicao[disciplina]
            print(f"- {disciplina:<10}: Professor {prof:<10} | {sala:<10} | {horario:<10}")
        else:
            print(f"- {disciplina:<10}: (não atribuído)")
    time.sleep(0.01)

def backtracking_otimizado_terminal(variaveis, atribuicao, variaveis_restantes, dominios, estado_busca, restricoes_duras, restricoes_suaves):
    if estado_busca['melhor_score'] == 0: return

    if not variaveis_restantes:
        score_atual, violacoes = calcular_penalidade(atribuicao, restricoes_suaves)
        status = f"Solução Válida Encontrada! Score: {score_atual}."
        imprimir_passo_terminal(variaveis, atribuicao, estado_busca['melhor_score'], status)
        time.sleep(0.5)
        if score_atual < estado_busca['melhor_score']:
            estado_busca['melhor_score'] = score_atual
            estado_busca['melhor_solucao'] = copy.deepcopy(atribuicao)
            status = f"NOVA MELHOR SOLUÇÃO! Score: {score_atual}"
            imprimir_passo_terminal(variaveis, atribuicao, estado_busca['melhor_score'], status)
            time.sleep(0.5)
        return

    var = variaveis_restantes[0]
    for valor in dominios[var]:
        if is_consistent(var, valor, atribuicao, restricoes_duras):
            atribuicao[var] = valor
            status = f"Tentando {var}..."
            imprimir_passo_terminal(variaveis, atribuicao, estado_busca['melhor_score'], status)
            backtracking_otimizado_terminal(variaveis, atribuicao, variaveis_restantes[1:], dominios, estado_busca, restricoes_duras, restricoes_suaves)
            if estado_busca['melhor_score'] == 0: return
            del atribuicao[var]

# --- 2. LABORATÓRIO DE TESTES ---
if __name__ == "__main__":
    CENARIO_TESTE = 1
    print(f"--- EXECUTANDO CENÁRIO DE TESTE #{CENARIO_TESTE} ---")

    VARIAVEIS = ['IA', 'Cálculo', 'Física', 'Química']
    SALAS = ['Sala 101', 'Lab A']
    HORARIOS = ['Seg-Manhã', 'Seg-Tarde', 'Ter-Manhã']

    if CENARIO_TESTE == 2:
        PROFESSORES = ['Fabiano', 'Newton', 'Einstein']
    else:
        PROFESSORES = ['Fabiano', 'Newton', 'Einstein', 'Marie']

    RESTRICOES_DURAS = {
        'requisito_sala': lambda disc, val: not ((disc in ['IA', 'Cálculo'] and val[1] != 'Sala 101') or \
                                                 (disc in ['Física', 'Química'] and val[1] != 'Lab A')),
        'capacitacao_prof': lambda disc, val: not (disc == 'IA' and val[0] != 'Fabiano'),
        'recurso_unico': lambda disc, val, atr: not any(
            (val[0] == v[0]) or \
            (val[1] == v[1] and val[2] == v[2]) \
            for v in atr.values()
        )
    }
    
    # --- CORREÇÃO DE SINTAXE APLICADA AQUI ---
    RESTRICOES_SUAVES = [
        lambda sol: (
            sum(1 for v in sol.values() if v[0] == 'Einstein' and 'Tarde' in v[2]),
            [f"Einstein alocado à tarde ({d})" for d, v in sol.items() if v[0] == 'Einstein' and 'Tarde' in v[2]]
        ),
        lambda sol: (
            sum(1 for v in sol.values() if v[0] == 'Marie' and v[1] != 'Sala 101'),
            [f"Marie alocada fora da Sala 101 ({d})" for d, v in sol.items() if v[0] == 'Marie' and v[1] != 'Sala 101']
        )
    ]
    
    if CENARIO_TESTE == 3:
        RESTRICOES_SUAVES.append(
            lambda sol: (1, [f"Física não alocada na Sala 101"]) if 'Física' in sol and sol['Física'][1] != 'Sala 101' else (0, [])
        )

    print("Configurando o problema...")
    dominios = gerar_dominios_iniciais(VARIAVEIS, PROFESSORES, SALAS, HORARIOS)
    dominios_podados = aplicar_restricoes_iniciais(dominios, RESTRICOES_DURAS)
    
    if any(not d for d in dominios_podados.values()):
        problema_insolúvel = True
    else:
        problema_insolúvel = False
        estado_da_busca = {'melhor_solucao': None, 'melhor_score': float('inf')}
        print("\nIniciando busca...")
        tempo_inicial = time.time()
        backtracking_otimizado_terminal(VARIAVEIS, {}, list(VARIAVEIS), dominios_podados, estado_da_busca, RESTRICOES_DURAS, RESTRICOES_SUAVES)
        tempo_total = time.time() - tempo_inicial

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- Relatório Final (Cenário #{CENARIO_TESTE}) ---")
    if not problema_insolúvel:
        print(f"Tempo Total de Execução: {tempo_total:.2f} segundos")
        if estado_da_busca['melhor_solucao']:
            score_final, violacoes_finais = calcular_penalidade(estado_da_busca['melhor_solucao'], RESTRICOES_SUAVES)
            print(f"\n--- Melhor Solução Encontrada (Score de Penalidade: {score_final}) ---")
            for disc, val in sorted(estado_da_busca['melhor_solucao'].items()):
                print(f"- {disc:<10}: Professor {val[0]:<10} | {val[1]:<10} | {val[2]:<10}")
            if violacoes_finais:
                print("\nPreferências Violadas:"); [print(f"  - {v}") for v in violacoes_finais]
            else:
                print("\nNenhuma preferência foi violada. Solução ótima encontrada!")
        else:
            print("\nNenhuma solução válida foi encontrada.")
    else:
        print("\nNenhuma solução válida foi encontrada (detectado na fase de pré-processamento).")