# test_calculo.py
import unittest
from calculadora import Circuito, QuadroDistribuicao


class TestCalculoEletrico(unittest.TestCase):
    def test_circuito_iluminacao(self):
        # 127V, 1270VA -> 10A
        c = Circuito("Sala", "ILUM", 1270, 127)
        self.assertAlmostEqual(c.corrente_projeto, 10.0)
        self.assertEqual(c.disjuntor, 10)  # Deve ser 10A ou maior
        # Mínimo 1.5mm para iluminação (norma diz 1.5, mas tabela pode dar mais se corrente alta)
        self.assertTrue(c.secao_cabo >= 1.5)

    def test_circuito_tug(self):
        # 127V, 2540VA -> 20A
        c = Circuito("Cozinha", "TUG", 2540, 127)
        self.assertAlmostEqual(c.corrente_projeto, 20.0)
        self.assertTrue(c.disjuntor >= 20)
        self.assertTrue(c.secao_cabo >= 2.5)  # Mínimo 2.5mm para força

    def test_demanda_total(self):
        quadro = QuadroDistribuicao()
        # Iluminação: 1000VA (fator 1.0 -> 1000VA)
        quadro.adicionar_circuito(Circuito("Luz", "ILUM", 1000, 127))
        # TUG: 2000VA (Total Ilum+TUG = 3000VA -> Fator 0.66 -> 1980VA)
        quadro.adicionar_circuito(Circuito("Tomadas", "TUG", 2000, 127))

        # TUE: 1 Chuveiro 5000W (Fator 1.0 -> 5000W)
        quadro.adicionar_circuito(Circuito("Chuveiro", "TUE", 5000, 220))

        demanda = quadro.calcular_demanda_total()
        # Esperado: (1000+2000)*0.66 + 5000*1.0 = 1980 + 5000 = 6980 VA
        self.assertAlmostEqual(demanda, 6980.0, delta=1.0)

    def test_dimensionamento_geral(self):
        quadro = QuadroDistribuicao()
        quadro.adicionar_circuito(
            Circuito("Chuveiro", "TUE", 5000, 220))  # 5000VA demanda

        # Entrada 220V
        res = quadro.dimensionar_geral(220)
        # Corrente demanda = 5000 / 220 = 22.72A
        self.assertAlmostEqual(res['corrente_demanda'], 22.72, delta=0.1)
        # Próximo comercial é 25A ou 32A
        self.assertTrue(res['disjuntor_geral'] >= 25)


if __name__ == '__main__':
    unittest.main()
