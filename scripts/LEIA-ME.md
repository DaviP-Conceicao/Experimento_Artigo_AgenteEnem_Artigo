# Scripts

Todos foram gerados com apoio de IA e documentados pelo autor (cabeçalho de cada arquivo).

| Arquivo | Função |
| --- | --- |
| `sorteio.py` | Sorteia as 100 redações do conjunto de teste do Essay-BR (estratos pelos quartis da nota total, semente 42). Rodar dentro do clone do Essay-BR |
| `executar_experimento.py` | Envia o prompt A ou B e a redação ao modelo e grava uma linha por chamada em `.jsonl` |
| `rodar_final.sh` | Roda a rodada final (3 repetições, condições A e B) chamando `executar_experimento.py` na ordem descrita na Metodologia. Versão usada pelo autor, com os caminhos da máquina dele; a versão com caminhos relativos está no `README.md` |
| `extrair_notas.py` | Lê as cinco notas e o total declarado na resposta do agente e classifica o resultado (`ok`, `soma_diferente`, `incompleto`, `sem_notas`, `possivel_anulacao`) |
| `listar_modelos.py` | Lista os modelos que a chave da API enxerga e aceitam `generateContent` |
| `aplicar_ajustes.py` | Histórico: patch aplicado durante o experimento (gatilho `[Corrigir]`, nova tentativa e leitura do total na linha seguinte). O `executar_experimento.py` e o `extrair_notas.py` deste repositório já incluem essas alterações; rodar o patch de novo falha por desenho |
| `blindar_script.py` | Histórico: patch que interrompe a execução após 3 falhas seguidas da API e não conta falha de cota como tentativa. Já incluído no `executar_experimento.py` |

Antes de rodar: instale `google-genai` (versão 2.31.0 no experimento) e exporte `GEMINI_API_KEY`. Nunca coloque a chave no código nem no repositório. Os comandos completos estão no `README.md` da raiz.
