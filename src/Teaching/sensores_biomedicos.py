import numpy as np


def filtro_passa_baixa(sinal, alpha=0.1):
    # Filtro simples para suavizar sinal de sensor cardíaco
    sinal_filtrado = np.zeros_like(sinal)
    for i in range(1, len(sinal)):
        sinal_filtrado[i] = alpha * sinal[i] + (1 - alpha) * sinal_filtrado[i - 1]
    return sinal_filtrado
