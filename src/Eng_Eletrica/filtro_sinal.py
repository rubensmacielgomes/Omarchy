import numpy as np


def filtro_media_movel(sinal, janela=5):
    """
    Simula a suavização de um sinal de sensor (ex: ECG ou Oximetria)
    para remover ruídos de alta frequência.
    """
    return np.convolve(sinal, np.ones(janela), "valid") / janela


# Simulação de sinal de sensor com ruído
sinal_puro = np.sin(np.linspace(0, 10, 100))
ruido = np.random.normal(0, 0.2, 100)
sinal_com_ruido = sinal_puro + ruido

sinal_suave = filtro_media_movel(sinal_com_ruido)

print(f"Processamento concluído: {len(sinal_suave)} amostras filtradas.")
