# Script para cálculo de tensão elétrica
print("--- Calculadora de Tensão (Lei de Ohm) ---")

resistencia = float(input("Digite o valor da resistência (em Ohms): "))
corrente = float(input("Digite o valor da corrente (em Amperes): "))

tensao = resistencia * corrente

print(f"Para uma resistência de {resistencia}Ω e corrente de {corrente}A:")
print(f"A tensão resultante é de {tensao} Volts.")
