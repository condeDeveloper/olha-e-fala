import unittest
from itertools import groupby

from olhaefala.sequencia import (
    comprimentos,
    digitos_usados,
    passo,
    passo_por_grupos,
    sequencia,
)


class TestPasso(unittest.TestCase):
    def test_os_primeiros_termos(self):
        self.assertEqual(
            sequencia("1", 8),
            ["1", "11", "21", "1211", "111221", "312211", "13112221", "1113213211"],
        )

    def test_string_vazia(self):
        self.assertEqual(passo(""), "")
        self.assertEqual(passo_por_grupos(""), "")

    def test_um_digito_so(self):
        for d in "123456789":
            self.assertEqual(passo(d), "1" + d)

    def test_as_duas_implementacoes_concordam(self):
        atual = "1"
        for _ in range(35):
            self.assertEqual(passo(atual), passo_por_grupos(atual))
            atual = passo(atual)

    def test_concordam_em_qualquer_semente(self):
        for semente in ("2", "7", "22", "1111", "123456789", "999"):
            atual = semente
            for _ in range(12):
                self.assertEqual(passo(atual), passo_por_grupos(atual), semente)
                atual = passo(atual)

    def test_o_resultado_tem_tamanho_par(self):
        # cada grupo vira dois caracteres: a contagem e o digito
        atual = "1"
        for _ in range(20):
            atual = passo(atual)
            self.assertEqual(len(atual) % 2, 0)

    def test_o_resultado_descreve_a_entrada(self):
        atual = "1"
        for _ in range(16):
            seguinte = passo(atual)
            lidos = [
                (int(seguinte[i]), seguinte[i + 1]) for i in range(0, len(seguinte), 2)
            ]
            grupos = [(sum(1 for _ in g), d) for d, g in groupby(atual)]
            self.assertEqual(lidos, grupos)
            atual = seguinte

    def test_recusa_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            sequencia("1", 0)


class TestComprimentos(unittest.TestCase):
    def test_os_vinte_primeiros(self):
        self.assertEqual(
            comprimentos("1", 20),
            [1, 2, 2, 4, 6, 6, 8, 10, 14, 20, 26, 34, 46, 62, 78, 102, 134, 176, 226, 302],
        )

    def test_nunca_diminui(self):
        c = comprimentos("1", 40)
        for antes, depois in zip(c, c[1:]):
            self.assertGreaterEqual(depois, antes)


class TestDigitos(unittest.TestCase):
    def test_de_um_so_saem_um_dois_e_tres(self):
        self.assertEqual(digitos_usados("1", 40), ["1", "2", "3"])

    def test_de_dois_e_de_tres_tambem(self):
        self.assertEqual(digitos_usados("2", 40), ["1", "2", "3"])
        self.assertEqual(digitos_usados("3", 40), ["1", "2", "3"])

    def test_um_digito_grande_fica_para_sempre(self):
        for d in "456789":
            self.assertEqual(digitos_usados(d, 30), ["1", "2", "3", d])

    def test_quatro_so_aparece_se_a_semente_trouxer(self):
        # "1112" tem tres uns seguidos, e isso nao gera "4" nenhum
        self.assertNotIn("4", "".join(sequencia("1112", 25)))
