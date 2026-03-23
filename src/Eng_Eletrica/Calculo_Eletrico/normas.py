# normas.py

# Tabelas e constantes baseadas na NBR 5410

# Fatores de demanda para iluminação e tomadas de uso geral (TUG)
# Tabela baseada na NBR 5410 (simplificada para uso residencial típico)
FATORES_DEMANDA_ILUM_TUG = {
    0: 1.0,      # Até 1000 VA (ou W para FP=1)
    1000: 0.86,  # 1001 a 2000
    2000: 0.75,  # 2001 a 3000
    3000: 0.66,  # 3001 a 4000
    4000: 0.59,  # 4001 a 5000
    5000: 0.52,  # 5001 a 6000
    6000: 0.45,  # 6001 a 7000
    7000: 0.40,  # 7001 a 8000
    8000: 0.35,  # 8001 a 9000
    9000: 0.31,  # 9001 a 10000
    10000: 0.24,  # Acima de 10000 (valor aproximado para >10kVA)
}

# Fatores de demanda para Tomadas de Uso Específico (TUE)
# Baseado no número de circuitos de TUE
FATORES_DEMANDA_TUE = {
    1: 1.00,
    2: 1.00,
    3: 0.84,
    4: 0.76,
    5: 0.70,
    6: 0.65,
    7: 0.60,
    8: 0.57,
    9: 0.54,
    10: 0.52,  # 10 ou mais
}

# Capacidade de condução de corrente (Capacidade) aproximada para cabos de cobre, isolação PVC 70°C,
# Instalação em eletroduto embutido em alvenaria (Método B1), 2 condutores carregados.
# Seção (mm²) -> Corrente (A)
CAPACIDADE_CABOS = {
    1.5: 17.5,
    2.5: 24,
    4.0: 32,
    6.0: 41,
    10.0: 57,
    16.0: 76,
    25.0: 101,
    35.0: 125,
    50.0: 151,
    70.0: 192,
    95.0: 232,
}

# Disjuntores comerciais comuns (A)
DISJUNTORES_DISPONIVEIS = [10, 16, 20, 25, 32, 40, 50, 63, 70, 80, 100, 125]


def selecionar_disjuntor(corrente_projeto):
    """Seleciona o menor disjuntor comercial maior ou igual à corrente de projeto."""
    for disjuntor in DISJUNTORES_DISPONIVEIS:
        if disjuntor >= corrente_projeto:
            return disjuntor
    # Retorna o maior se exceder (ou tratar erro)
    return DISJUNTORES_DISPONIVEIS[-1]


def selecionar_cabo(corrente_projeto, disjuntor):
    """
    Seleciona a seção do cabo adequada.
    Critério simplificado: Iz (capacidade do cabo) >= In (disjuntor) >= Ib (corrente projeto).
    """
    for secao, capacidade in CAPACIDADE_CABOS.items():
        if capacidade >= disjuntor:
            return secao, capacidade
    return None, None
