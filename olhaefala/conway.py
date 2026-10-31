"""As duas coisas que John Conway provou sobre esta sequencia, em 1986.

A primeira e a constante: o comprimento do termo n cresce como lambda^n, com

    lambda = 1,303577269034...

que e raiz de um polinomio de grau 71. A segunda e o fenomeno do ATOMO: a partir
de certo ponto a string se parte em pedacos que evoluem sozinhos para sempre, e
nunca mais trocam um digito com o vizinho. Conway catalogou 92 desses pedacos.

Aqui nada disso e citado como verdade: a constante e medida, e as divisoes sao
TESTADAS, evoluindo os pedacos separados e comparando com a evolucao do todo.
"""

from .sequencia import passo

LAMBDA = 1.303577269034296391257099112152551890730702504659404875754861390628550


def razoes(comprimentos):
    """A razao entre cada comprimento e o anterior."""
    return [b / a for a, b in zip(comprimentos, comprimentos[1:])]


def distancia_da_constante(comprimentos):
    """Quanto cada razao se afasta da constante de Conway."""
    return [r - LAMBDA for r in razoes(comprimentos)]


def evolui(termo, passos):
    """Aplica a regra `passos` vezes."""
    for _ in range(passos):
        termo = passo(termo)
    return termo


def e_divisao(termo, corte, passos):
    """Cortar aqui e evoluir os dois lados da o mesmo que evoluir o todo?

    E a definicao operacional de divisao: nenhum digito de um lado interfere no
    outro, por mais passos que se de. Aqui `passos` diz ate onde foi conferido,
    e a tabela do README sempre informa esse numero.
    """
    if corte <= 0 or corte >= len(termo):
        return False
    esquerda, direita = termo[:corte], termo[corte:]
    for k in range(1, passos + 1):
        if evolui(esquerda, k) + evolui(direita, k) != evolui(termo, k):
            return False
    return True


def divisoes(termo, passos=8):
    """Todos os cortes que sobrevivem a `passos` passos."""
    return [c for c in range(1, len(termo)) if e_divisao(termo, c, passos)]


def pedacos(termo, passos=8):
    """O termo partido em todos os pedacos independentes."""
    cortes = [0] + divisoes(termo, passos) + [len(termo)]
    return [termo[a:b] for a, b in zip(cortes, cortes[1:])]


def ponto_fixo(termo):
    """O termo se repete sem mudar?"""
    return passo(termo) == termo


def procurar_pontos_fixos(ate_digitos=4):
    """Todas as strings de digitos 1 a 9 com ate `ate_digitos` que nao mudam."""
    from itertools import product

    saida = []
    for tamanho in range(1, ate_digitos + 1):
        for letras in product("123456789", repeat=tamanho):
            termo = "".join(letras)
            if ponto_fixo(termo):
                saida.append(termo)
    return saida
