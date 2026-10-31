"""Roda as medidas e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # pedacos ate o termo 25

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time

from olhaefala.conway import (
    LAMBDA,
    divisoes,
    pedacos,
    procurar_pontos_fixos,
    razoes,
)
from olhaefala.sequencia import (
    comprimentos,
    digitos_usados,
    passo,
    passo_por_grupos,
    sequencia,
)

COMPLETO = "--completo" in sys.argv
ATE_PEDACOS = 25 if COMPLETO else 21
PASSOS_DA_DIVISAO = 6
TERMOS = 46


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def main():
    comeco = time.time()
    termos = sequencia("1", TERMOS)

    print("## As duas implementacoes do passo\n")
    divergencias = sum(1 for t in termos[:-1] if passo(t) != passo_por_grupos(t))
    print("| termos conferidos | divergencias |")
    print("|---|---|")
    print("| %d | %d |" % (TERMOS - 1, divergencias))

    print("\n## O comprimento e a constante de Conway\n")
    c = comprimentos("1", TERMOS)
    r = razoes(c)
    print("| termo | comprimento | razao com o anterior | distancia de lambda |")
    print("|---|---|---|---|")
    for n in (5, 10, 20, 30, 40, TERMOS - 1):
        print(
            "| %d | %s | %.9f | %+.9f |"
            % (n, milhar(c[n]), r[n - 1], r[n - 1] - LAMBDA)
        )
    print()
    print("lambda = %.12f" % LAMBDA)

    print("\n## Quais digitos aparecem\n")
    print("| semente | digitos vistos em 40 termos |")
    print("|---|---|")
    for semente in ("1", "2", "3", "7", "9", "22"):
        print("| %s | %s |" % (semente, ", ".join(digitos_usados(semente, 40))))

    print("\n## Pontos fixos\n")
    fixos = procurar_pontos_fixos(4)
    print("strings de 1 a 4 digitos que nao mudam: %s" % (fixos or "nenhuma"))
    print("conferidas: %d" % sum(9 ** k for k in range(1, 5)))

    print("\n## Os pedacos que evoluem sozinhos\n")
    print("| termo | digitos | cortes que sobrevivem a %d passos | pedacos |" % PASSOS_DA_DIVISAO)
    print("|---|---|---|---|")
    for n in (10, 14, 18, ATE_PEDACOS):
        termo = termos[n]
        cortes = divisoes(termo, PASSOS_DA_DIVISAO)
        print("| %d | %s | %d | %d |" % (n, milhar(len(termo)), len(cortes), len(cortes) + 1))

    distintos = {}
    for n in range(10, ATE_PEDACOS + 1):
        for p in pedacos(termos[n], PASSOS_DA_DIVISAO):
            distintos[p] = distintos.get(p, 0) + 1
    print()
    print("pedacos distintos nos termos 10 a %d: %d" % (ATE_PEDACOS, len(distintos)))
    print("Conway catalogou 92 elementos ao todo.")
    print("os doze mais curtos: %s" % ", ".join(sorted(distintos, key=lambda p: (len(p), p))[:12]))

    print("\n## Os primeiros termos\n")
    for n in range(8):
        print("%2d: %s" % (n, termos[n]))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
