# Corretor de Redação ENEM: critérios do Inep no prompt

Material do artigo **"Incluir os critérios do Inep no *prompt* melhora um corretor de redações do ENEM baseado em LLM? Um experimento com o *Essay-BR*"**, de Davi Paulino Conceição (IFSP, Câmpus São João da Boa Vista), 2026.

Este repositório reúne os prompts, as respostas brutas do modelo e o código de análise, para que as métricas do artigo possam ser reproduzidas e conferidas.

## Pergunta e desenho do estudo

Acrescentar ao prompt de um agente corretor os quadros dos níveis dos critérios do Inep (Cartilha do Participante 2026) melhora a concordância das notas do agente com as notas humanas?

| Item | Descrição |
| --- | --- |
| Modelo | `gemini-3.5-flash-lite`, chamado pela API do Google AI Studio (biblioteca `google-genai` 2.31.0), temperatura padrão, sem ferramentas |
| Corpus | Essay-BR (Marinho, Anchiêta e Moura, 2021): amostra aleatória de 100 redações do conjunto de teste, estratificada pelos quartis da nota total humana (semente 42; 52 temas distintos) |
| Condição A | Prompt do agente com sete correções conferidas na Cartilha (`prompts/prompt_A_v2.txt`) |
| Condição B | Condição A acrescida dos quadros literais dos seis níveis de C1 a C5 (`prompts/prompt_B_v2.txt`) |
| Repetições | 3 por redação e condição (600 chamadas, 17 e 18/10/2026) |
| Conjunto pareado | 98 redações (ficam de fora a 338 na condição A e a 612 na B, em que o agente só devolveu o menu) |
| Métricas | QWK, concordância exata e adjacente, MAE e viés com sinal; IC95% por *bootstrap* pareado (2.000 reamostragens, semente 42) |

## Resultados principais

| Métrica (nota total) | Condição A | Condição B | B − A (IC95%) |
| --- | --- | --- | --- |
| QWK | 0,522 | 0,498 | −0,024 (−0,072 a 0,021) |
| Concordância exata | 8,2% | 9,2% | +1,0 p.p. (−3,1 a 5,4) |
| Viés com sinal (pontos) | −99,2 | −107,6 | −8,4 (−18,4 a +0,7) |

Não houve evidência de melhora com a condição B. A competência 4 foi a única em que o IC95% da diferença excluiu zero (QWK −0,068; viés −2,7 pontos), achado exploratório entre 30 contrastes sem correção para comparações múltiplas. Todos os números estão em `analise/saida/metricas.txt`.

## Estrutura

```
.
├── prompts/    prompts das condições A e B (SHA-256 em prompts/SHA256SUMS)
├── scripts/    amostragem, execução do experimento na API e extração das notas (ver scripts/LEIA-ME.md)
├── dados/      respostas brutas (final_A.jsonl, final_B.jsonl), logs e notas humanas da amostra
├── analise/    cálculo das métricas, verificações de integridade e saídas (analise/saida/)
├── graficos/   gráficos do artigo (QWK por competência e viés por quartil)
└── figuras/    capturas de tela do agente no Voiceflow (ver figuras/LEIA-ME.md)
```

## Como reproduzir a análise (offline, em poucos segundos)

```bash
cd dados && sha256sum -c ../analise/SHA256SUMS     # cinco "OK": são os arquivos analisados no artigo
cd ../analise
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash rodar_analise.sh
python3 extras_resultados.py
```

Versões usadas: Python 3.13.16, NumPy 2.5.3, SciPy 1.18.1 e scikit-learn 1.9.1. Os detalhes de cada script estão em `analise/README.md`.

## Como repetir o experimento

Repetir as chamadas à API **não reproduz exatamente** os números do artigo: o modelo foi usado com a temperatura padrão e a nota de uma mesma redação varia entre as repetições (amplitude média de 60,0 pontos na condição A e de 55,9 na B). O que se reproduz é o procedimento. A amostra, ao contrário, é reproduzível: o `sorteio.py` gera a mesma amostra de 100 redações a partir do Essay-BR.

Organize as pastas lado a lado: o clone do Essay-BR (`essay/`) e este repositório.

```bash
# 1) Corpus e amostra (gera ../amostra_100.csv, que contém o texto das redações e não vai para o repositório)
git clone https://github.com/rafaelanchieta/essay.git
pip install pandas scikit-learn
cp corretor-redacao-enem/scripts/sorteio.py essay/ && (cd essay && python3 sorteio.py)

# 2) Chamadas à API (3 repetições, condições A e B; a cota gratuita diária limita a rodada: 600 chamadas em dois dias)
pip install google-genai==2.31.0
export GEMINI_API_KEY="sua-chave"        # nunca coloque a chave no código
cd corretor-redacao-enem/scripts
for rep in 1 2 3; do for cond in A B; do
  python3 executar_experimento.py --cond $cond --modelo gemini-3.5-flash-lite --repeticao $rep \
      --amostra ../../amostra_100.csv --prompts-csv ../../essay/essay-br/prompts.csv \
      --prompt-dir ../prompts --saida final_$cond.jsonl
done; done
```

O script retoma de onde parou se a cota acabar (3 falhas seguidas da API encerram a execução). Para testar sem chamar a API, acrescente `--dry-run --limite 3`. Para analisar uma nova rodada, aponte `EXP_DIR` para a pasta com os `.jsonl` e os logs (ver `analise/README.md`).

## Sobre os dados

- As redações completas **não são redistribuídas** aqui. Os arquivos `.jsonl` trazem as respostas do agente, que citam trechos das redações ao apontar erros.
- As notas humanas vêm do Essay-BR, mapeadas para a escala do ENEM; não são notas oficiais do Inep.
- Os quadros dos níveis do prompt B reproduzem a Cartilha do Participante do Enem 2026 (Inep/MEC).

## Uso de inteligência artificial

O autor declara o uso de Claude (Anthropic), Gemini (Google) e ChatGPT (OpenAI) na elaboração do trabalho. O prompt original do agente foi gerado com o Gemini a partir de instruções do autor, e os scripts em Python foram gerados com apoio de IA e documentados pelo autor. A declaração completa está na subseção "Declaração de uso de inteligência artificial", na Metodologia do artigo.

## Licença e citação

O código, os prompts e as respostas brutas estão sob a licença MIT (arquivo `LICENSE`). O Essay-BR e a Cartilha do Inep seguem as licenças e condições de seus autores. Para citar, use `CITATION.cff`.

Contato: davi.paulino@aluno.ifsp.edu.br
