# 1.Estrutura Padrão (if, elif, else)
idade = 20

if idade < 18:
    print("Menor de idade")
elif idade >= 60:
    print("Idoso")
else:
    print("Adulto")

# 2.Operador Ternário (Condicional em uma linha)
status = "Acesso permitido" if idade >= 18 else "Acesso negado"

# 3.Match Case (Estrutural Pattern Matching)
comando = "sair"

match comando:
    case "iniciar":
        print("Iniciando sistema...")
    case "sair":
        print("Saindo...")
    case _:
        print("Comando desconhecido")  # O '_' funciona como o 'else'


# 4.Uso de Dicionários (Dispatch Table)
def acao_abrir():
    return "Abrindo arquivo"


def acao_salvar():
    return "Salvando arquivo"


opcoes = {"abrir": acao_abrir, "salvar": acao_salvar}

# O método .get() permite definir um valor padrão (o 'else')
resultado = opcoes.get("abrir", lambda: "Ação inválida")()

# 5.Avaliação de Curto-Circuito (and / or)
# Se 'nome' for uma string vazia (Falso), ele assume "Convidado"
usuario = "" or "Convidado"
print(usuario)
