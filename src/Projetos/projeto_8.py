"""
Balcão de Atendimento!
"""

ultimo = 10
fila = list(range(1, ultimo + 1))
while True:
    print(f"Existem {len(fila)} clientes na fila.")
    print(f"Fila atual: {fila}")
    print("Digite 'F' para adicionar um cliente ao fim da fila.")
    print("ou 'A' para realizar o atendimento. 'S' para sair.")
    operacao = input("Operação (F, A ou S): ")
    x = 0
    sair = False
    while x < len(operacao):
        if operacao[x].upper() == "A":
            if len(fila) > 0:
                atendido = fila.pop(0)
                print(f"Cliente {atendido} foi atendido.")
            else:
                print("Fila vazia! Ninguém para atender!")
        elif operacao[x].upper() == "F":
            ultimo += 1
            fila.append(ultimo)
        elif operacao[x].upper() == "S":
            sair = True
            break
        else:
            print(
                f"Operação inválida: {operacao[x]} na posição {x}! Digite apenas F, A ou S!"
            )
        x = x + 1
    if sair:
        break
