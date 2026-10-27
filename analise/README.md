# Pacote de análise — Corretor de Redação ENEM

Reproduz todas as métricas da rodada final (gemini-3.5-flash-lite, 100 redações × 2 condições × 3 repetições) a partir dos dados brutos.
Não usa a API nem a chave: roda offline, em poucos segundos.

## Onde ficam os dados

Por padrão, os scripts leem os dados em `../dados` (raiz do repositório): `final_A.jsonl`, `final_B.jsonl`, `log_final.txt`, `log_final2.txt` e `log_final3.txt`.
Para usar outra pasta: `EXP_DIR=/caminho/da/pasta bash rodar_analise.sh`

## Como rodar

```bash
cd dados && sha256sum -c ../analise/SHA256SUMS      # confere se são os mesmos arquivos analisados (cinco "OK")
cd ../analise
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash rodar_analise.sh
python3 extras_resultados.py                         # nível 200 da C5, divergências, correlação crítica
```

As saídas ficam em `analise/saida/`: `integridade.txt`, `verificacao.txt`, `metricas.txt`, `resultados_metricas.json`, `extras.txt` e `extras.json`.
Os gráficos do artigo saem de `cd ../graficos && python3 graficos.py` (requer `matplotlib`; lê `saida/resultados_metricas.json`).

## O que cada arquivo faz

| Arquivo | Função |
| --- | --- |
| `carregar.py` | Lê os `.jsonl` e aplica a regra de resolução: para cada (redação, repetição) vale o último registro com notas lidas; se nenhum tiver, vale o último com resposta (a falha fica registrada). |
| `metricas_lib.py` | QWK com níveis fixos (6 por competência, 26 no total; notas ÷ 40), concordância exata, adjacente (80 pontos por competência, 100 no total), MAE e viés (agente − humano). |
| `metricas_main.py` | Métricas por repetição, depois média e faixa; IC95% por bootstrap pareado (2.000 reamostragens das redações, semente 42, percentil 2,5–97,5) aplicado à média das 3 repetições; variação entre repetições; Spearman entre nº de palavras e erro; compressão e viés por quartil; total declarado × soma; maiores divergências. |
| `integridade.py` | Linhas, chaves, falhas da API, temperatura, modelo retornado, tentativas, datas, status por repetição e tokens. |
| `verificar.py` | QWK próprio × scikit-learn com `labels`; contagens dos `.jsonl` × logs; conferência da redação 499; leitura independente (regex) das notas em 80 respostas sorteadas (semente 7). |
| `ver_falhas.py` | Mostra o início das respostas sem notas (o Menu) das redações 338 (A) e 612 (B). |
| `extras_resultados.py` | Nível 200 da C5, viés por nível humano da C5, maiores divergências e valor crítico de r (n = 98). |
| `SHA256SUMS` | Hash dos arquivos analisados em 18/10/2026. |

## Decisões de análise

- Nota do agente = soma de C1 a C5. O total declarado pelo agente é usado só na análise de sensibilidade.
- Conjunto pareado: as redações com notas válidas nas 3 repetições das duas condições (98 de 100; ficam fora a 338 e a 612, que só devolvem o Menu em A e em B, respectivamente).
- `sklearn.metrics.cohen_kappa_score` sem `labels` muda o QWK em até 0,005 em 6 de 36 casos; por isso os níveis são fixados.
- Os 30 contrastes B − A (5 competências + total × 5 métricas) não têm correção para comparações múltiplas: o que sair do IC é exploratório.

## Versões usadas na verificação

Python 3.13.16, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1. No teste deste pacote, os números saíram idênticos aos da análise original (diferença máxima 0).

## O que não está aqui

O experimento em si (execução do agente na API) está em `../scripts/`, e os prompts em `../prompts/`. As análises dos pilotos e do teste de temperatura 0 não fazem parte do repositório.
