print("|       CONSUMO DE ENERGIA ELÉTRICA       |")
print("+-----------------------------------------+")
print("|    Preço por tipo e faixa de consumo    |")
print("+-----------------------------------------+")
print("| Tipo         |  Faixa  (KWh)  |  Preço  |")
print("+=========================================+")
print("| Residêncial  |  Até 500 KWh   |   0.40  |")
print("|     (R)      |  Acima de 500  |   0.65  |")
print("+=========================================+")
print("| Comercial    |  Até 1000 KWh  |   0.55  |")
print("|     (C)      |  Acima de 1000 |   0.60  |")
print("+=========================================+")
print("| Industrial   |  Até 5000 KWh  |   0.55  |")
print("|     (I)      |  Acima de 5000 |   0.60  |")
print("+=========================================+")

consumo = int(input("Consumo em KWh: "))
tipo = input("Tipo da instalação (R, C ou I): ").upper()
if tipo == "R":
    if consumo <= 500:
        preco = 0.40
    else:
        preco = 0.65
elif tipo == "I":
    if consumo <= 5000:
        preco = 0.55
    else:
        preco = 0.60
elif tipo == "C":
    if consumo <= 1000:
        preco = 0.55
    else:
        preco = 0.60
else:
    preco = 0
    print("Erro: Tipo de instalação inválido!")
custo = consumo * preco
print(f"Valor a pagar: R$ {custo:.2f}")
