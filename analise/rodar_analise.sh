#!/bin/bash
# Roda as três etapas na ordem e guarda a saída de texto em saida/.
set -e
cd "$(dirname "$0")"
mkdir -p saida
python3 integridade.py | tee saida/integridade.txt
python3 verificar.py   | tee saida/verificacao.txt
python3 metricas_main.py | tee saida/metricas.txt
echo
echo "Pronto. Resultados em: $(pwd)/saida"
