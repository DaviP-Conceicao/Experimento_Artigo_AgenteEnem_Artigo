"""Métricas finais: QWK, concordância exata e adjacente, MAE, viés (por repetição, depois média e faixa), IC95% por bootstrap pareado,
variação entre repetições, extensão do texto, compressão, total declarado x soma e maiores divergências."""
import sys, json, numpy as np, collections
from metricas_lib import *
from scipy.stats import spearmanr

ids, H, words, A, DECL, STAT = montar()
ok = ~np.isnan(A['A']).any(axis=(0, 2)) & ~np.isnan(A['B']).any(axis=(0, 2))
okidx = np.where(ok)[0]
print('redações no conjunto pareado:', ok.sum(), '| fora:', [ids[i] for i in np.where(~ok)[0]])

# métricas por repetição no conjunto pareado
M = {c: [metricas(H[okidx], A[c][r][okidx]) for r in range(3)] for c in 'AB'}
def resumo(c, alvo, mt):
    v = [M[c][r][alvo][mt] for r in range(3)]
    return np.mean(v), min(v), max(v)

# bootstrap pareado (essays), média das 3 repetições
rng = np.random.default_rng(42); NB = 2000; m = len(okidx)
res = {(c, t, mt): [] for c in 'AB' for t in ALVOS for mt in METS}
for b in range(NB):
    s = okidx[rng.integers(0, m, m)]
    for c in 'AB':
        per = [metricas(H[s], A[c][r][s]) for r in range(3)]
        for t in ALVOS:
            for mt in METS:
                res[(c, t, mt)].append(np.nanmean([p[t][mt] for p in per]))
res = {k: np.array(v) for k, v in res.items()}
def ic(v): return np.nanpercentile(v, 2.5), np.nanpercentile(v, 97.5)

saida = {}
fmt = {'qwk': '{:.3f}', 'exata': '{:.3f}', 'adj': '{:.3f}', 'mae': '{:.1f}', 'vies': '{:+.1f}'}
for mt in METS:
    print(f'\n=== {mt.upper()}  (média das 3 repetições [faixa entre repetições]  IC95% bootstrap)  — A | B | B−A [IC95%]')
    for t in ALVOS:
        linha = []
        for c in 'AB':
            mu, lo, hi = resumo(c, t, mt)
            l, u = ic(res[(c, t, mt)])
            linha.append(f'{fmt[mt].format(mu)} [{fmt[mt].format(lo)}..{fmt[mt].format(hi)}] ic({fmt[mt].format(l)},{fmt[mt].format(u)})')
            saida[f'{c}|{t}|{mt}'] = dict(media=float(mu), min=float(lo), max=float(hi), ic=[float(l), float(u)])
        d = res[('B', t, mt)] - res[('A', t, mt)]
        dm = resumo('B', t, mt)[0] - resumo('A', t, mt)[0]
        l, u = ic(d)
        saida[f'dif|{t}|{mt}'] = dict(media=float(dm), ic=[float(l), float(u)])
        print(f'  {t:5s} A {linha[0]}  |  B {linha[1]}  |  Δ {fmt[mt].format(dm)} [{fmt[mt].format(l)}, {fmt[mt].format(u)}]' + ('  *' if (l > 0 or u < 0) else ''))
PASTA_SAIDA.mkdir(exist_ok=True)
json.dump(saida, open(PASTA_SAIDA / 'resultados_metricas.json', 'w'), indent=1)

# métricas na própria base de cada condição (99 redações) — verificação de sensibilidade
print('\n=== Sensibilidade: QWK total/exata total na base própria de cada condição (exclui só a falha daquela condição)')
for c in 'AB':
    vals = []
    for r in range(3):
        v = ~np.isnan(A[c][r]).any(axis=1)
        mm = metricas(H[v], A[c][r][v])['Total']
        vals.append((v.sum(), mm['qwk'], mm['exata'], mm['vies']))
    print(' ', c, [(int(n), round(q, 3), round(e, 3), round(b, 1)) for n, q, e, b in vals])

# variação entre repetições (conjunto pareado)
print('\n=== Variação entre as 3 repetições (total), conjunto pareado')
for c in 'AB':
    T = A[c][:, okidx, :].sum(2)  # (3, m)
    amp = T.max(0) - T.min(0)
    print(f'  {c}: amplitude média {amp.mean():.1f} pts | mediana {np.median(amp):.0f} | máx {amp.max():.0f} | idênticas nas 3: {np.mean(amp == 0):.1%} | amplitude > 100: {np.mean(amp > 100):.1%} | desvio-padrão médio dentro da redação {T.std(0, ddof=1).mean():.1f}')
    for k, nome in enumerate(COMP):
        Ck = A[c][:, okidx, k]; ampk = Ck.max(0) - Ck.min(0)
        print(f'     {nome}: iguais nas 3 repetições {np.mean(ampk == 0):.1%} | amplitude média {ampk.mean():.1f}')

# extensão do texto
print('\n=== Extensão do texto x erro (total), conjunto pareado — Spearman')
w = words[okidx]; ht = H[okidx].sum(1)
print('  palavras: média %.0f, dp %.0f, min %d, max %d' % (w.mean(), w.std(), w.min(), w.max()))
rho, p = spearmanr(w, ht); print(f'  palavras x nota humana: rho={rho:.3f} (p={p:.3g})')
for c in 'AB':
    T = A[c][:, okidx, :].sum(2)
    mean_total = T.mean(0); signed = mean_total - ht; absolute = np.abs(T - ht).mean(0)
    r1, p1 = spearmanr(w, mean_total); r2, p2 = spearmanr(w, signed); r3, p3 = spearmanr(w, absolute)
    print(f'  {c}: palavras x nota do agente (média das reps) rho={r1:.3f} (p={p1:.3g}) | palavras x erro com sinal rho={r2:.3f} (p={p2:.3g}) | palavras x erro absoluto rho={r3:.3f} (p={p3:.3g})')

# compressão e calibração
print('\n=== Compressão e viés por faixa da nota humana (total), conjunto pareado')
qs = np.quantile(ht, [0.25, 0.5, 0.75]); faixa = np.digitize(ht, qs)
print('  dp humano:', round(ht.std(), 1), '| cortes dos quartis:', qs)
for c in 'AB':
    T = A[c][:, okidx, :].sum(2)
    print(f'  {c}: dp do agente (média das reps) {np.mean([T[r].std() for r in range(3)]):.1f} | viés por quartil humano (Q1..Q4):', [round(float((T.mean(0) - ht)[faixa == q].mean()), 1) for q in range(4)], '| n por quartil', [int((faixa == q).sum()) for q in range(4)])

# soma_diferente
print('\n=== Total declarado x soma')
for c in 'AB':
    mais = menos = 0; n = 0
    for r in range(3):
        for j in range(len(ids)):
            if STAT[c][r, j] == 'soma_diferente':
                n += 1
                d = DECL[c][r, j] - A[c][r, j].sum()
                mais += d > 0; menos += d < 0
    print(f'  {c}: soma_diferente {n}/300; declarado > soma: {mais}; declarado < soma: {menos}')
print('  sensibilidade (total declarado em vez da soma, quando existe), QWK/exata/viés do total por repetição:')
for c in 'AB':
    linha = []
    for r in range(3):
        td = np.where(np.isnan(DECL[c][r]), A[c][r].sum(1), DECL[c][r])[okidx]
        mm = metricas(H[okidx], A[c][r][okidx], tot_a=td)['Total']
        ms = metricas(H[okidx], A[c][r][okidx])['Total']
        linha.append((round(mm['qwk'], 3), round(ms['qwk'], 3), round(mm['vies'], 1), round(ms['vies'], 1)))
    print('   ', c, '(QWK decl, QWK soma, viés decl, viés soma):', linha)

# maiores divergências
print('\n=== 10 maiores divergências (|média das 3 reps do total − humano|)')
for c in 'AB':
    T = A[c][:, okidx, :].sum(2).mean(0); d = T - ht
    ordem = np.argsort(-np.abs(d))[:10]
    print(' ', c, [(ids[okidx[j]], int(ht[j]), round(float(T[j])), int(w[j])) for j in ordem])
print('\n=== Redações com nota humana total 0 ou muito baixa (<=80)')
for j in np.where(H.sum(1) <= 80)[0]:
    print('  ', ids[j], 'humano', int(H[j].sum()), '| A:', [None if np.isnan(A['A'][r, j, 0]) else int(A['A'][r, j].sum()) for r in range(3)], '| B:', [None if np.isnan(A['B'][r, j, 0]) else int(A['B'][r, j].sum()) for r in range(3)])
