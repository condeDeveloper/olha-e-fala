"""Os numeros do README, presos."""

import unittest

from olhaefala.conway import (
    LAMBDA,
    divisoes,
    e_divisao,
    evolui,
    pedacos,
    ponto_fixo,
    procurar_pontos_fixos,
    razoes,
)
from olhaefala.sequencia import comprimentos, digitos_usados, sequencia

TERMOS = sequencia("1", 46)
COMPRIMENTOS = comprimentos("1", 46)
RAZOES = razoes(COMPRIMENTOS)


class TestConstante(unittest.TestCase):
    def test_os_comprimentos_medidos(self):
        esperado = {5: 6, 10: 26, 20: 408, 30: 5808, 40: 82350, 45: 310036}
        for n, tamanho in esperado.items():
            self.assertEqual(COMPRIMENTOS[n], tamanho, "n=%d" % n)

    def test_as_razoes_medidas(self):
        esperado = {
            5: 1.000000000,
            10: 1.300000000,
            20: 1.350993377,
            30: 1.301658449,
            40: 1.304285850,
            45: 1.304064001,
        }
        for n, razao in esperado.items():
            self.assertAlmostEqual(RAZOES[n - 1], razao, places=9, msg="n=%d" % n)

    def test_a_convergencia_nao_e_monotona(self):
        # o termo 20 fica treze vezes mais longe da constante que o termo 10
        dez = abs(RAZOES[9] - LAMBDA)
        vinte = abs(RAZOES[19] - LAMBDA)
        self.assertGreater(vinte, dez)
        self.assertAlmostEqual(vinte / dez, 13.25, places=2)

    def test_a_melhor_aproximacao_da_faixa(self):
        distancias = [abs(r - LAMBDA) for r in RAZOES]
        melhor = min(range(len(distancias)), key=lambda i: distancias[i])
        self.assertEqual(melhor + 1, 44)
        self.assertAlmostEqual(distancias[melhor], 0.000026275, places=9)

    def test_a_pior_distancia_de_cada_faixa(self):
        # medido, nao chutado: o teto so cai de verdade depois do termo 35
        esperado = {
            20: (0.0474161, 20),
            25: (0.0083486, 27),
            30: (0.0025522, 31),
            35: (0.0014186, 35),
            40: (0.0008808, 42),
        }
        for de, (pior, onde) in esperado.items():
            distancias = [abs(RAZOES[n - 1] - LAMBDA) for n in range(de, 46)]
            maior = max(range(len(distancias)), key=lambda i: distancias[i])
            self.assertAlmostEqual(distancias[maior], pior, places=7, msg="de=%d" % de)
            self.assertEqual(de + maior, onde, "de=%d" % de)


class TestDigitos(unittest.TestCase):
    def test_a_tabela_de_sementes(self):
        esperado = {
            "1": ["1", "2", "3"],
            "2": ["1", "2", "3"],
            "3": ["1", "2", "3"],
            "7": ["1", "2", "3", "7"],
            "9": ["1", "2", "3", "9"],
            "22": ["2"],
        }
        for semente, digitos in esperado.items():
            self.assertEqual(digitos_usados(semente, 40), digitos, semente)


class TestPontoFixo(unittest.TestCase):
    def test_so_o_vinte_e_dois(self):
        self.assertEqual(procurar_pontos_fixos(4), ["22"])

    def test_quantas_strings_foram_olhadas(self):
        self.assertEqual(sum(9 ** k for k in range(1, 5)), 7380)

    def test_o_vinte_e_dois_e_fixo_mesmo(self):
        self.assertTrue(ponto_fixo("22"))
        self.assertEqual(evolui("22", 50), "22")


class TestPedacos(unittest.TestCase):
    ESPERADO = {10: (26, 3), 14: (78, 13), 18: (226, 46), 21: (528, 97)}

    def test_quantos_cortes_sobrevivem(self):
        for n, (digitos, cortes) in self.ESPERADO.items():
            self.assertEqual(len(TERMOS[n]), digitos, "n=%d" % n)
            self.assertEqual(len(divisoes(TERMOS[n], 6)), cortes, "n=%d" % n)

    def test_pedacos_e_cortes_mais_um(self):
        for n in self.ESPERADO:
            self.assertEqual(
                len(pedacos(TERMOS[n], 6)), len(divisoes(TERMOS[n], 6)) + 1, "n=%d" % n
            )

    def test_os_pedacos_remontam_o_termo(self):
        for n in (10, 14, 18, 21):
            self.assertEqual("".join(pedacos(TERMOS[n], 6)), TERMOS[n], "n=%d" % n)

    def test_cada_corte_e_mesmo_independente(self):
        termo = TERMOS[14]
        for corte in divisoes(termo, 6):
            self.assertTrue(e_divisao(termo, corte, 6), "corte=%d" % corte)
            for k in (1, 3, 6):
                self.assertEqual(
                    evolui(termo[:corte], k) + evolui(termo[corte:], k),
                    evolui(termo, k),
                )

    def test_quantos_pedacos_distintos(self):
        distintos = set()
        for n in range(10, 22):
            distintos.update(pedacos(TERMOS[n], 6))
        self.assertEqual(len(distintos), 60)

    def test_os_doze_mais_curtos(self):
        distintos = set()
        for n in range(10, 22):
            distintos.update(pedacos(TERMOS[n], 6))
        ordenados = sorted(distintos, key=lambda p: (len(p), p))[:12]
        self.assertEqual(
            ordenados,
            ["3", "12", "13", "22", "112", "113", "132", "211", "312", "1112", "1113", "1132"],
        )
