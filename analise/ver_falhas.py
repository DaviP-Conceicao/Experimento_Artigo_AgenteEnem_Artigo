"""Mostra o início das respostas sem notas (Menu) da redação 338 (condição A) e da 612 (condição B)."""
import sys
from carregar import *
dados = carregar()
for c, i in (('A', '338'), ('B', '612')):
    final, por = resolver(dados[c])
    for rep in (1, 3):
        for r in por[(i, rep)]:
            print(f'--- cond {c} essay {i} rep {rep} tentativa {r["tentativa"]} palavras {r["palavras"]} humano {r["humano"]} saida_tokens {r["tokens"]}')
            print((r['resposta'] or '')[:1400])
            print()
