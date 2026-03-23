# calculadora.py
from normas import (
    FATORES_DEMANDA_ILUM_TUG,
    FATORES_DEMANDA_TUE,
    selecionar_disjuntor,
    selecionar_cabo
)


class Circuito:
    def __init__(self, nome, tipo, potencia_va, tensao, fp=1.0):
        """
        tipo: 'ILUM' (Iluminação), 'TUG' (Tomada Uso Geral), 'TUE' (Tomada Uso Específico)
        """
        self.nome = nome
        self.tipo = tipo
        self.potencia_va = potencia_va
        self.tensao = tensao
        self.fp = fp
        self.corrente_projeto = self.calcular_corrente()
        self.disjuntor = selecionar_disjuntor(self.corrente_projeto)
        self.secao_cabo, self.capacidade_cabo = selecionar_cabo(
            self.corrente_projeto, self.disjuntor)

    def calcular_corrente(self):
        return self.potencia_va / self.tensao

    def __repr__(self):
        return (f"Circuito(nome='{self.nome}', tipo='{self.tipo}', "
                f"P={self.potencia_va}VA, V={self.tensao}V, "
                f"Ib={self.corrente_projeto:.2f}A, In={self.disjuntor}A, "
                f"Cabo={self.secao_cabo}mm²)")


class QuadroDistribuicao:
    def __init__(self):
        self.circuitos = []

    def adicionar_circuito(self, circuito):
        self.circuitos.append(circuito)

    def calcular_demanda_total(self):
        # Separar potências
        potencia_ilum_tug = 0
        circuitos_tue = []

        for c in self.circuitos:
            if c.tipo in ['ILUM', 'TUG']:
                # Considerando W para demanda se FP=1, ou VA se simplificado
                potencia_ilum_tug += c.potencia_va * c.fp
            elif c.tipo == 'TUE':
                circuitos_tue.append(c)

        # Demanda Iluminação + TUG
        # Encontrar o fator na tabela (interpolação ou faixas)
        # A tabela normas.py usa chaves como limite inferior da faixa?
        # Vamos ajustar a lógica de busca na tabela
        fator_ilum_tug = 0.24  # Valor padrão para cargas altas

        # Ordenar chaves para buscar a faixa correta
        faixas = sorted(FATORES_DEMANDA_ILUM_TUG.keys())
        for faixa in faixas:
            if potencia_ilum_tug >= faixa:
                fator_ilum_tug = FATORES_DEMANDA_ILUM_TUG[faixa]
            else:
                break

        demanda_ilum_tug = potencia_ilum_tug * fator_ilum_tug

        # Demanda TUE
        qtd_tue = len(circuitos_tue)
        fator_tue = FATORES_DEMANDA_TUE.get(
            qtd_tue, FATORES_DEMANDA_TUE[10] if qtd_tue >= 10 else 1.0)

        potencia_tue_total = sum(c.potencia_va * c.fp for c in circuitos_tue)
        demanda_tue = potencia_tue_total * fator_tue

        demanda_total = demanda_ilum_tug + demanda_tue
        return demanda_total

    def dimensionar_geral(self, tensao_entrada):
        demanda = self.calcular_demanda_total()
        corrente_demanda = demanda / tensao_entrada
        disjuntor_geral = selecionar_disjuntor(corrente_demanda)
        secao_cabo, capacidade = selecionar_cabo(
            corrente_demanda, disjuntor_geral)

        return {
            "demanda_total_va": demanda,
            "corrente_demanda": corrente_demanda,
            "disjuntor_geral": disjuntor_geral,
            "cabo_entrada": secao_cabo
        }
