# [[teaching_10_03_26]] <- Link no estilo Obsidian
# Estudo sobre Delta e Raízes Quadradas

import math


def resolver_equacao(a, b, c):
    # Cálculo do delta
    delta = b**2 - 4 * a * c

    if delta > 0:
        # Duas soluções reais
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        return f"Duas soluções: x1 = {x1}, x2 = {x2}"
    elif delta == 0:
        # Uma solução real
        x = -b / (2 * a)
        return f"Uma solução real: x = {x}"
    else:
        # Nenhuma solução real
        return "Nenhuma solução nos números reais (R)"


# Exemplo de uso (Exercício 121)
print(resolver_equacao(-4, -16, 84))

# /home/rmg_lg/Documentos/Obsidian Vault/Teaching_10_03_26.md
