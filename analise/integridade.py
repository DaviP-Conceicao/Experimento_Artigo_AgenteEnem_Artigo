"""Integridade dos dados: linhas, chaves (redação, repetição), falhas da API, temperaturas, modelo retornado, tentativas, datas, status por repetição, tokens."""
import sys, collections, statistics as st
from carregar import *
dados = carregar()
for c in 'AB':
    regs = dados[c]
    final, por = resolver(regs)
    print(f'===== Condição {c}: {len(regs)} linhas, {len(final)} chaves (id, rep)')
    ids = sorted({k[0] for k in final}); print('  redações distintas:', len(ids), '| repetições:', sorted({k[1] for k in final}))
    n_api = sum(1 for r in regs if r.get('erro')); print('  registros de falha da API (erro):', n_api)
    print('  temperaturas:', {r['temperatura'] for r in regs}, '| modelos retornados:', collections.Counter(r.get('modelo_retornado') for r in regs))
    print('  tentativas por chave:', collections.Counter(len(v) for v in por.values()))
    dts = sorted(r['data_utc'] for r in regs); print('  de', dts[0], 'a', dts[-1])
    for rep in (1, 2, 3):
        cnt = collections.Counter(final[k]['agente']['status'] if final[k].get('agente') else 'ERRO_API' for k in final if k[1] == rep)
        print(f'  rep {rep}: n={sum(cnt.values())}', dict(cnt))
    tot = collections.Counter(final[k]['agente']['status'] if final[k].get('agente') else 'ERRO_API' for k in final)
    print('  total das 300 chaves:', dict(tot))
    falhas = [(k, final[k]['humano']['total'], final[k]['agente']['status']) for k in sorted(final) if final[k].get('agente') and final[k]['agente']['status'] in FALHA + ('possivel_anulacao',)]
    print('  chaves sem nota válida (id, rep), humano, status:', falhas)
    # chamadas efetivas (linhas) por dia UTC
    dias = collections.Counter(r['data_utc'][:10] for r in regs); print('  linhas por dia (UTC):', dict(dias))
    ent = [r['tokens']['entrada'] for r in regs if r.get('tokens') and r['tokens'].get('entrada')]
    sai = [r['tokens']['saida'] for r in regs if r.get('tokens') and r['tokens'].get('saida')]
    print('  tokens médios por chamada: entrada', round(st.mean(ent)), 'saída', round(st.mean(sai)), '| total entrada', sum(ent), 'saída', sum(sai))
# redações com falha em ambas
