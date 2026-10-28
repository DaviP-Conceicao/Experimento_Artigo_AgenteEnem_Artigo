#!/bin/bash
# rodar_final.sh
# Autor: Davi Paulino Conceição
#
# Roda a rodada final do experimento: 3 repetições, condições A e B, modelo gemini-3.5-flash-lite.
# Ordem: repetição 1 (A e depois B), repetição 2 (A e B), repetição 3 (A e B), como descrito na Metodologia.
# Cada chamada grava uma linha em final_A.jsonl ou final_B.jsonl. Se uma execução falhar
# (por exemplo, cota diária esgotada), o script para e informa onde; ao rodá-lo de novo,
# executar_experimento.py pula o que já foi concluído e continua de onde parou.
#
# Versão usada na rodada, com os caminhos da máquina do autor: roda dentro de ~/Downloads/Artigo/exp,
# pasta que continha executar_experimento.py, extrair_notas.py, amostra_100.csv e os prompts.
# Os demais parâmetros ficam no padrão do script (pausa de 6 s, 2 tentativas, temperatura padrão da API).
# Antes: exportar GEMINI_API_KEY (nunca colocar a chave no código). Uso: bash rodar_final.sh
# Para repetir a partir de uma cópia do repositório, veja a versão com caminhos relativos no README.md.

cd ~/Downloads/Artigo/exp || exit 1
for r in 1 2 3; do
  for c in A B; do
    python3 executar_experimento.py --cond $c --modelo gemini-3.5-flash-lite --repeticao $r --saida final_$c.jsonl || { echo "PAROU na repeticao $r, condicao $c"; exit 1; }
  done
done
echo "TUDO CONCLUIDO"
