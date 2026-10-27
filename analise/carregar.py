"""Leitura dos dados brutos da rodada final (final_A.jsonl e final_B.jsonl) e regra de resolução das tentativas.

Pasta dos dados: por padrão, ../dados em relação a esta pasta (raiz do repositório).
Para usar outra pasta:  EXP_DIR=/caminho/da/pasta python3 metricas_main.py
Regra de resolução: para cada (redação, repetição) vale o último registro com notas lidas e status concluído;
se nenhum tiver, vale o último registro com resposta (a falha fica registrada).
"""
import collections, json, os
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTA_EXP = Path(os.environ.get('EXP_DIR', AQUI.parent / 'dados')).expanduser()
PASTA_SAIDA = AQUI / 'saida'
ARQ = {'A': PASTA_EXP / 'final_A.jsonl', 'B': PASTA_EXP / 'final_B.jsonl'}
LOGS = [PASTA_EXP / n for n in ('log_final.txt', 'log_final2.txt', 'log_final3.txt')]
COMP = ['C1', 'C2', 'C3', 'C4', 'C5']
FALHA = ('sem_notas', 'incompleto')


def carregar():
    """Retorna {condição: [registros, na ordem do arquivo]}"""
    for f in ARQ.values():
        if not f.exists():
            raise SystemExit(f'Arquivo não encontrado: {f}\nColoque os dados em {PASTA_EXP} ou defina EXP_DIR.')
    return {c: [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()] for c, f in ARQ.items()}


def resolver(regs):
    """Para cada (id, repetição): registro final = último com notas lidas e status concluído; senão o último com agente (falha)."""
    por = collections.defaultdict(list)
    for r in regs:
        por[(r['id_teste'], r['repeticao'])].append(r)
    final = {}
    for k, lst in por.items():
        concl = [r for r in lst if r.get('agente') and r['agente']['status'] not in FALHA]
        com_ag = [r for r in lst if r.get('agente')]
        final[k] = (concl[-1] if concl else (com_ag[-1] if com_ag else lst[-1]))
    return final, por
