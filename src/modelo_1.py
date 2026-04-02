km = int(input("Digite a quantidade de quilômetros percorridos:"))
dias = int(input("Digite quantos dias você ficou com o carro:"))
preco_por_dia = 60
preco_por_km = 0.15
preco_a_pagar = km * preco_por_km + dias * preco_por_dia
print(f"O total a pagar é de R${preco_a_pagar:.2f}")
