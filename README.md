# Olha e fala

Leia em voz alta o que você está vendo, e escreva o que disse:

```
1
11        um "1"
21        dois "1"
1211      um "2", um "1"
111221    um "1", um "2", dois "1"
312211    três "1", dois "2", um "1"
```

John Conway estudou essa brincadeira em 1986 e provou duas coisas sérias: o
comprimento do termo `n` cresce como `λⁿ`, com `λ = 1,303577269...` raiz de um
polinômio de grau 71; e a partir de certo ponto a cadeia **se parte em pedaços
que evoluem sozinhos para sempre**, dos quais ele catalogou 92.

Aqui nada disso é citado como verdade. A constante é medida termo a termo, e as
divisões são **testadas**: cortar, evoluir os dois lados separados e comparar
com a evolução do todo. Python puro, sem dependência nenhuma.

## Os quatro achados

1. **A razão entre comprimentos não converge de forma monótona.** O termo 10 cai
   a 0,0036 de `λ`; o termo 20 fica a **0,047**, treze vezes mais longe. A melhor
   aproximação dos 45 termos está no **44**, a 0,000026, e logo depois ela piora
   de novo.
2. **A cadeia do termo 21 se parte em 98 pedaços independentes**, confirmados
   corte a corte por seis passos de evolução. São 528 algarismos que nunca mais
   trocam informação entre si.
3. **Nos termos 10 a 21 aparecem 60 pedaços distintos** — Conway catalogou 92 ao
   todo. Os menores são `3`, `12`, `13` e `22`.
4. **Só uma string de até quatro algarismos não muda: o `22`.** Foram olhadas
   7.380 strings. E a sequência é fechada nos dígitos 1, 2 e 3: um dígito maior
   só aparece se a semente trouxer, e aí ele fica para sempre.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### As duas implementações do passo

| termos conferidos | divergências |
|---|---|
| 45 | 0 |

Uma percorre a cadeia com um contador na mão; a outra deixa o agrupamento com o
`groupby` da biblioteca. O erro clássico aqui é esquecer o último grupo, e ele
não apareceria num teste de poucos termos.

### O comprimento e a constante de Conway

| termo | comprimento | razão com o anterior | distância de λ |
|---|---|---|---|
| 5 | 6 | 1,000000000 | −0,303577269 |
| 10 | 26 | 1,300000000 | −0,003577269 |
| 20 | 408 | 1,350993377 | +0,047416108 |
| 30 | 5.808 | 1,301658449 | −0,001918820 |
| 40 | 82.350 | 1,304285850 | +0,000708581 |
| 45 | 310.036 | 1,304064001 | +0,000486732 |

A pior distância de cada faixa, que é o que diz de verdade como ela converge:

| a partir do termo | pior distância | em que termo |
|---|---|---|
| 20 | 0,0474161 | 20 |
| 25 | 0,0083486 | 27 |
| 30 | 0,0025522 | 31 |
| 35 | 0,0014186 | 35 |
| 40 | 0,0008808 | 42 |

### Quais dígitos aparecem

| semente | dígitos vistos em 40 termos |
|---|---|
| 1 | 1, 2, 3 |
| 2 | 1, 2, 3 |
| 3 | 1, 2, 3 |
| 7 | 1, 2, 3, 7 |
| 9 | 1, 2, 3, 9 |
| 22 | 2 |

### Os pedaços que evoluem sozinhos

| termo | algarismos | cortes que sobrevivem a 6 passos | pedaços |
|---|---|---|---|
| 10 | 26 | 3 | 4 |
| 14 | 78 | 13 | 14 |
| 18 | 226 | 46 | 47 |
| 21 | 528 | 97 | 98 |

Pedaços distintos nos termos 10 a 21: **60**. Com `--completo` a varredura vai
ao termo 25 e encontra 76.

## O que as medidas me corrigiram

- **Escrevi dois limiares de convergência de cabeça, e os dois quebraram.** Pus
  "depois do termo 25 a distância fica abaixo de 0,002": falhou no 26, com
  0,0029. Troquei por 30: falhou no 31, com 0,0026. Parei de chutar e passei a
  **medir a pior distância de cada faixa**, que é a tabela acima — e ela mostra
  que o teto só cai de verdade depois do termo 35.
- **Esperava convergência monótona.** O termo 20 está treze vezes mais longe de
  `λ` que o termo 10. Quem olhasse só um termo diria qualquer coisa sobre a
  constante.
- **Achei que a semente `22` fosse um caso de borda sem graça.** Ela é o único
  ponto fixo entre 7.380 strings, e é também a única semente cujo alfabeto não
  cresce: só o dígito 2, para sempre.
- **Precisei definir "divisão" de um jeito que o programa pudesse testar.** A
  definição de Conway é por catálogo de elementos; aqui ela virou uma pergunta
  operacional — cortar, evoluir os dois lados e comparar — e por isso toda
  tabela diz **por quantos passos** o corte foi conferido. Seis passos, nas
  tabelas acima.

## Como está organizado

```
olhaefala/sequencia.py  a regra, nas duas implementações, e o alfabeto
olhaefala/conway.py     a constante medida e as divisões testadas
ferramentas/medidor.py  roda tudo e imprime as tabelas acima
testes/                 29 testes
```

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # pedaços até o termo 25
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
