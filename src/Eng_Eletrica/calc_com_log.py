import datetime


def obter_valor(frase):
    while True:
        try:
            return float(input(frase))
        except ValueError:
            print("Erro: Digite apenas números!")


def salvar_log(mensagem):
    # O 'with' abre o arquivo e o 'a' adiciona o texto ao final
    with open("historico_calculos.txt", "a") as arquivo:
        agora = datetime.datetime.now()
        data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"[{data_formatada}] {mensagem}\n")


while True:
    print("\n--- Sistema CMBRASILTEC (Calculadora + Registro) ---")
    opcao = input("V, R, I ou S para Sair: ").upper()

    if opcao == "S":
        print("Encerrando e salvando registros. Até logo!")
        break

    if opcao == "V":
        r = obter_valor("Digite a Resistência (Ω): ")
        i = obter_valor("Digite a Corrente (A): ")
        v = r * i
        res = f"Cálculo de Tensão: {r} R * {i} A = {v:.2f} V"
        print(res)
        salvar_log(res)

    # Repita o padrão para R e I...
    elif opcao == "R":
        v = obter_valor("Digite a Tensão (V): ")
        i = obter_valor("Digite a Corrente (A): ")
        r = v / i
        res = f"Cáculo de Resistência: {v} V / {i} A = {r:.2f} Ω"
        print(res)
        salvar_log(res)

    elif opcao == "I":
        v = obter_valor("Digite a Tensão (V): ")
        r = obter_valor("Digite a Resistência (Ω): ")
        i = v / r
        res = f"Cálculo de Corrente: {v} V / {r} R = {i:.2f} A"
        print(res)
        salvar_log(res)

    else:
        print("Opção inválida! Tente novamente!")
