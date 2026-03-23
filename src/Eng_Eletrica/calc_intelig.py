# O loop começa aqui
while True:
    print("\n--- Calculadora Lei de Ohm (Digite 'S' para sair) ---")
    print("O que você deseja calcular? ")
    print("V - Tensão | R - Resistência | I - Corrente")
    opcao = input("Escolha (V, R, I ou S para Sair): ").upper()

    if opcao == "S":
        print("Encerrando a calculadora. Até logo!")
        break  # Este comando "quebra" o loop e sai do programa

    if opcao == "V":
        try:
            r = float(input("Digite a Resistência (Ω): "))
            i = float(input("Digite a Corrente (A): "))
            print(f"Resultado: Tensão = {r * i:.2f} Volts")
        except ValueError:
            print("Erro: Por favor, digite apenas números para Resistência e Corrente!")

    elif opcao == "R":
        try:
            v = float(input("Digite a Tensão (V): "))
            i = float(input("Digite a Corrente (A): "))
            print(f"Resultado: Resistência = {v / i:.2f} Ω")
        except ValueError:
            print("Erro: Por favor, digite apenas números para Tensão e Corrente!")

    elif opcao == "I":
        try:
            v = float(input("Digite a Tensão (V): "))
            r = float(input("Digite a Resistência (Ω): "))
            print(f"Resultado: Corrente = {v / r:.2f} Amperes")
        except ValueError:
            print("Erro: Por favor, digite apenas números para Tensão e Resistência!")

    else:
        print("Opção inválida! Escolha entre V, R ou I.")
