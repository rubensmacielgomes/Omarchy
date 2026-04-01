# main.py
from calculadora import Circuito, QuadroDistribuicao


def ler_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("Por favor, insira um valor positivo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número.")


def ler_int(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < 0:
                print("Por favor, insira um valor positivo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def main():
    print("=== Calculadora de Carga Elétrica Residencial (NBR 5410) ===")

    quadro = QuadroDistribuicao()

    tensao_entrada = ler_float(
        "Digite a tensão de entrada da residência (ex: 127, 220): "
    )

    while True:
        print("\n--- Adicionar Circuito ---")
        print("1. Iluminação")
        print("2. Tomada de Uso Geral (TUG)")
        print("3. Tomada de Uso Específico (TUE)")
        print("4. Finalizar e Calcular")

        opcao = input("Escolha uma opção: ")

        if opcao == "4":
            break

        if opcao not in ["1", "2", "3"]:
            print("Opção inválida.")
            continue

        nome = input("Nome do circuito (ex: Sala, Chuveiro): ")

        tipo_map = {"1": "ILUM", "2": "TUG", "3": "TUE"}
        tipo = tipo_map[opcao]

        potencia = ler_float("Potência do circuito em VA (ou Watts se FP=1): ")

        # Para TUE, pode ter tensão diferente (ex: bifásico)
        tensao_circuito = tensao_entrada
        if tipo == "TUE":
            resp_tensao = input(
                f"A tensão deste circuito é {tensao_entrada}V? (s/n): "
            ).lower()
            if resp_tensao == "n":
                tensao_circuito = ler_float("Digite a tensão do circuito: ")

        fp = 1.0
        if tipo == "TUE":
            fp_input = input("Fator de potência (Enter para 1.0): ")
            if fp_input:
                try:
                    fp = float(fp_input)
                except ValueError:
                    print("Valor inválido, usando 1.0")

        circuito = Circuito(nome, tipo, potencia, tensao_circuito, fp)
        quadro.adicionar_circuito(circuito)
        print(f"Circuito adicionado: {circuito}")

    if not quadro.circuitos:
        print("Nenhum circuito adicionado.")
        return

    print("\n=== Resultados do Dimensionamento ===")
    print(
        f"{'Circuito':<20} | {'Tipo':<5} | {'Potência':<10} | {'Corrente':<10} | {'Disjuntor':<10} | {'Cabo (mm²)':<10}"
    )
    print("-" * 80)

    for c in quadro.circuitos:
        print(
            f"{c.nome:<20} | {c.tipo:<5} | {c.potencia_va:<10.2f} | {c.corrente_projeto:<10.2f} | {c.disjuntor:<10} | {c.secao_cabo:<10}"
        )

    resultado_geral = quadro.dimensionar_geral(tensao_entrada)

    print("\n--- Padrão de Entrada ---")
    print(f"Demanda Total Calculada: {resultado_geral['demanda_total_va']:.2f} VA")
    print(f"Corrente de Demanda: {resultado_geral['corrente_demanda']:.2f} A")
    print(f"Disjuntor Geral Recomendado: {resultado_geral['disjuntor_geral']} A")
    print(f"Cabo de Entrada Recomendado: {resultado_geral['cabo_entrada']} mm²")
    print("\nNota: Os valores são baseados em tabelas simplificadas da NBR 5410.")
    print("Consulte sempre um engenheiro eletricista para o projeto final.")


if __name__ == "__main__":
    main()
