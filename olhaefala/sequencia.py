"""A regra inteira: leia em voz alta o que voce esta vendo.

    1
    11      (um "1")
    21      (dois "1")
    1211    (um "2", um "1")
    111221  (um "1", um "2", dois "1")

Duas implementacoes do mesmo passo, de proposito. A primeira percorre a string
com um contador na mao; a segunda usa `itertools.groupby`, que e a biblioteca
fazendo o agrupamento. Elas sao comparadas termo a termo, e e isso que impede
que um erro de borda - o ultimo grupo, quase sempre - passe batido.
"""

from itertools import groupby


def passo(termo):
    """Um passo da regra, contando os grupos na mao."""
    if not termo:
        return ""
    saida = []
    atual = termo[0]
    quantos = 0
    for c in termo:
        if c == atual:
            quantos += 1
        else:
            saida.append("%d%s" % (quantos, atual))
            atual = c
            quantos = 1
    saida.append("%d%s" % (quantos, atual))
    return "".join(saida)


def passo_por_grupos(termo):
    """O mesmo passo, deixando o agrupamento com a biblioteca."""
    return "".join(
        "%d%s" % (sum(1 for _ in grupo), digito) for digito, grupo in groupby(termo)
    )


def sequencia(inicio="1", quantos=20, regra=passo):
    """Os `quantos` primeiros termos a partir de `inicio`, inclusive ele."""
    if quantos < 1:
        raise ValueError("%d nao e uma quantidade de termos" % quantos)
    saida = [inicio]
    atual = inicio
    for _ in range(quantos - 1):
        atual = regra(atual)
        saida.append(atual)
    return saida


def comprimentos(inicio="1", quantos=20):
    """O comprimento de cada termo."""
    return [len(t) for t in sequencia(inicio, quantos)]


def digitos_usados(inicio="1", quantos=30):
    """Quais digitos aparecem em algum termo."""
    vistos = set()
    for termo in sequencia(inicio, quantos):
        vistos.update(termo)
    return sorted(vistos)
