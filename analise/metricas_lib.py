"""Funções de métrica: QWK com níveis fixos, concordância exata/adjacente, MAE e viés, e montagem das matrizes."""
import sys, json, numpy as np
from carregar import *

ALVOS = COMP + ['Total']
METS = ['qwk', 'exata', 'adj', 'mae', 'vies']

def montar():
    dados = carregar()
    final = {c: resolver(dados[c])[0] for c in 'AB'}
    ids = sorted({k[0] for k in final['A']}, key=int)
    idx = {i: n for n, i in enumerate(ids)}
    H = np.zeros((len(ids), 5)); words = np.zeros(len(ids))
    for n, i in enumerate(ids):
        h = final['A'][(i, 1)]['humano']
        assert h['total'] == sum(h[c] for c in COMP), i
        assert final['B'][(i, 1)]['humano'] == h and final['B'][(i, 1)]['palavras'] == final['A'][(i, 1)]['palavras']
        H[n] = [h[c] for c in COMP]; words[n] = final['A'][(i, 1)]['palavras']
    A = {c: np.full((3, len(ids), 5), np.nan) for c in 'AB'}
    DECL = {c: np.full((3, len(ids)), np.nan) for c in 'AB'}
    STAT = {c: np.full((3, len(ids)), '', dtype=object) for c in 'AB'}
    for c in 'AB':
        for (i, rep), r in final[c].items():
            a = r.get('agente')
            STAT[c][rep - 1, idx[i]] = a['status'] if a else 'ERRO'
            if a and a['status'] in ('ok', 'soma_diferente'):
                A[c][rep - 1, idx[i]] = [a[k] for k in COMP]
                if a['total_declarado'] is not None:
                    DECL[c][rep - 1, idx[i]] = a['total_declarado']
    return ids, H, words, A, DECL, STAT

def qwk(hl, al, N):
    O = np.bincount(hl * N + al, minlength=N * N).reshape(N, N).astype(float)
    n = O.sum()
    E = np.outer(O.sum(1), O.sum(0)) / n
    w = (np.arange(N)[:, None] - np.arange(N)[None, :]) ** 2
    den = (w * E).sum()
    return np.nan if den == 0 else 1 - (w * O).sum() / den

def metricas(Hs, As, tot_a=None):
    out = {}
    tot_h = Hs.sum(1)
    tot_a = As.sum(1) if tot_a is None else tot_a
    for k, nome in enumerate(ALVOS):
        if k < 5:
            h, a, N, tol = Hs[:, k], As[:, k], 6, 80
        else:
            h, a, N, tol = tot_h, tot_a, 26, 100
        d = a - h
        out[nome] = dict(qwk=qwk((h // 40).astype(int), (a // 40).astype(int), N), exata=float(np.mean(a == h)),
                         adj=float(np.mean(np.abs(d) <= tol)), mae=float(np.mean(np.abs(d))), vies=float(np.mean(d)))
    return out
