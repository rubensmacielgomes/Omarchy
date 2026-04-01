valor = float(input("Digite o valor da casa: R$ "))
salario = float(input("Digite o seu salario: R$ "))
anos = int(input("Quantos anos para pagar? "))
meses = anos * 12
prestacao = valor / meses
(
    print("Infelizmente você não pode obter o empréstimo!")
    if prestacao > salario * 0.3
    else print(f"Valor da prestação: R$ {prestacao:.2f}. Empréstimo OK!")
)
