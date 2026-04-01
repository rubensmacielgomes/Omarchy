salario = float(input("Digite o valor do seu salario: "))
pc_aumento = 0.15
if salario > 1250:
    pc_aumento = 0.10
aumento = salario * pc_aumento
print(
    f"Seu salario era de R${salario:.2f} e com o aumento de {pc_aumento * 100}% ficou R${salario + aumento:.2f}"
)