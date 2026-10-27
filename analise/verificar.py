"""Verificações: QWK próprio x scikit-learn, contagens dos .jsonl x logs, conferência manual da redação 499 e leitura independente (regex) de respostas sorteadas."""
import sys, re, json, numpy as np, collections
from metricas_lib import *
from sklearn.metrics import cohen_kappa_score

ids, H, words, A, DECL, STAT = montar()
ok = ~np.isnan(A['A']).any(axis=(0, 2)) & ~np.isnan(A['B']).any(axis=(0, 2)); okidx = np.where(ok)[0]

# 1) QWK próprio x scikit-learn com labels explícitos (e sem labels, para mostrar a diferença)
maxdif = 0; difsem = []
for c in 'AB':
    for r in range(3):
        mm = metricas(H[okidx], A[c][r][okidx])
        for k, nome in enumerate(ALVOS):
            if k < 5: h, a, N = H[okidx, k], A[c][r][okidx, k], 6
            else: h, a, N = H[okidx].sum(1), A[c][r][okidx].sum(1), 26
            hl, al = (h // 40).astype(int), (a // 40).astype(int)
            sk = cohen_kappa_score(hl, al, weights='quadratic', labels=list(range(N)))
            sk_sem = cohen_kappa_score(hl, al, weights='quadratic')
            maxdif = max(maxdif, abs(sk - mm[nome]['qwk'])); difsem.append((c, r + 1, nome, round(sk_sem - sk, 4)))
print('1) QWK: maior diferença |próprio − sklearn(labels explícitos)| em 36 combinações x 6 alvos =', f'{maxdif:.2e}')
print('   sklearn SEM labels vs COM labels (maior diferença):', max(difsem, key=lambda t: abs(t[3])), '| número de casos com diferença > 0.001:', sum(1 for t in difsem if abs(t[3]) > 0.001), 'de', len(difsem))

# 2) Recontar chamadas pelos logs
cont = collections.Counter()
for arq in LOGS:
    for l in open(arq, encoding='utf-8'):
        m = re.match(r'^(\d+) ([AB]) (\S+)$', l.strip())
        if m: cont[(m.group(2), m.group(3))] += 1
dados = carregar()
for c in 'AB':
    jl = collections.Counter(('ERRO' if not r.get('agente') else r['agente']['status']) for r in dados[c])
    lg = {k[1]: v for k, v in cont.items() if k[0] == c}
    print(f'2) {c}: status nas linhas do .jsonl {dict(jl)} | status nos 3 logs {lg} | iguais: {dict(jl) == lg}')

# 3) Conferência manual direta no .jsonl cru: redação 499, condição A, repetições 1..3 (última resposta com notas)
for c in 'AB':
    for rep in (1, 2, 3):
        recs = [r for r in dados[c] if r['id_teste'] == '499' and r['repeticao'] == rep and r.get('agente') and r['agente']['status'] in ('ok', 'soma_diferente')]
        a = recs[-1]['agente']
        j = ids.index('499')
        print(f'3) 499 {c} rep{rep}: cru', [a[k] for k in COMP], 'soma', sum(a[k] for k in COMP), '| matriz', A[c][rep - 1, j].tolist(), 'soma', A[c][rep - 1, j].sum())

# 4) Conferir o parser no texto de algumas respostas sorteadas: reler as notas direto da resposta por regex independente
rng = np.random.default_rng(7); falhas = 0; n = 0
for c in 'AB':
    sel = rng.choice(len(dados[c]), 40, replace=False)
    for s in sel:
        r = dados[c][s]
        if not r.get('agente') or r['agente']['status'] not in ('ok', 'soma_diferente'): continue
        txt = r['resposta']; n += 1
        lidas = []
        for k in range(1, 6):
            m = re.search(r'C%d[^\n|]*\|\s*\**\s*(\d{1,3})' % k, txt)
            lidas.append(int(m.group(1)) if m else None)
        if lidas != [r['agente'][x] for x in COMP]:
            falhas += 1; print('   divergência', c, r['id_teste'], r['repeticao'], lidas, [r['agente'][x] for x in COMP])
print(f'4) leitura independente por regex em {n} respostas sorteadas: {falhas} divergências')
