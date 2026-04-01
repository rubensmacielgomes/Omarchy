def obter_valor(frase):
    while True:
        try:
            return float(input(frase))
        except ValueError:
            print("Erro: Digite apenas números! Use ponto para decimais (ex: 12.5)")


# Agora o seu programa fica MUITO mais curto:
while True:
    print("\n--- Calculadora Expert ENGENHARIA ELÉTRICA ---")
    opcao = input("Escolha (V, R, I ou S para Sair): ").upper()

    if opcao == "S":
        break

    if opcao == "V":
        r = obter_valor("Digite a Resistência (Ω): ")
        i = obter_valor("Digite a Corrente (A): ")
        print(f"Tensão = {r * i:.2f} V")

    # Repita o padrão para R e I...
    elif opcao == "R":
        v = obter_valor("Digite a Tensão (V): ")
        i = obter_valor("Digite a Corrente (A): ")
        print(f"Resistência = {v / i:.2f} Ω")

    elif opcao == "I":
        v = obter_valor("Digite a Tensão (V): ")
        r = obter_valor("Digite a Resistência (Ω): ")
        print(f"Corrente = {v / r:.2f} A")
