"""
Roda o corretor (Condição A ou B) sobre a amostra e grava uma linha JSON por chamada.

Author: Davi Paulino Conceição
Date: 26/10/2026

Projeto: Pipeline em Python voltado para um artigo científico sobre avaliação
automatizada de redações com a API do Gemini, extração de notas por competências
C1–C5 e cálculo de concordância com as avaliações humanas por meio do QWK.

Nome do arquivo: executar_experimento.py

Descrição:
Este script é responsável por executar os experimentos de avaliação automatizada
de redações. Ele carrega a amostra de textos, recupera os temas e textos
motivadores, prepara as mensagens e solicita ao modelo Gemini que avalie cada
redação conforme as instruções da condição experimental selecionada.

O programa registra as notas humanas, as respostas do modelo, as notas extraídas,
a quantidade de palavras, os tokens utilizados, a versão do modelo e a data da
execução. Os resultados são armazenados em um arquivo JSONL, permitindo retomar
experimentos interrompidos e evitar repetir avaliações já concluídas.

O script também permite controlar a temperatura, o número de redações processadas,
a repetição experimental, as tentativas de avaliação e o intervalo entre chamadas.
O modo dry-run permite verificar as mensagens preparadas sem consultar a API.

Abaixo está uma versão de referência reorganizada e comentada, mantida inativa
para consulta futura. Em seguida, encontra-se o código original funcional.
"""


# ============================================================
# VERSÃO MELHORADA — CÓDIGO DE REFERÊNCIA INATIVO
# ============================================================

# import argparse
# import ast
# import csv
# import json
# import os
# import sys
# import time
# from datetime import datetime, timezone
# from pathlib import Path
#
# from extrair_notas import extrair
#
#
# def configurar_argumentos() -> argparse.Namespace:
#     """Define as opções disponíveis para executar o experimento."""
#     parser = argparse.ArgumentParser(
#         description="Executa a avaliação automatizada de redações."
#     )
#
#     parser.add_argument("--cond", required=True, choices=["A", "B"])
#     parser.add_argument("--modelo", required=True)
#     parser.add_argument(
#         "--temperatura",
#         type=float,
#         default=None,
#         help="Se omitida, utiliza a temperatura padrão da API."
#     )
#     parser.add_argument("--amostra", default="../amostra_100.csv")
#     parser.add_argument(
#         "--prompts-csv",
#         default=os.path.expanduser(
#             "~/Downloads/Artigo/essay/essay-br/prompts.csv"
#         ),
#         help="Arquivo com os identificadores e as descrições dos temas."
#     )
#     parser.add_argument("--prompt-dir", default=".")
#     parser.add_argument("--saida", default=None)
#     parser.add_argument("--limite", type=int, default=None)
#     parser.add_argument("--repeticao", type=int, default=1)
#     parser.add_argument(
#         "--max-tentativas",
#         type=int,
#         default=2,
#         help="Máximo de tentativas de avaliação por redação."
#     )
#     parser.add_argument(
#         "--pausa",
#         type=float,
#         default=6.0,
#         help="Intervalo entre chamadas à API, em segundos."
#     )
#     parser.add_argument(
#         "--dry-run",
#         action="store_true",
#         help="Prepara as mensagens sem chamar a API."
#     )
#
#     return parser.parse_args()
#
#
# def carregar_temas(caminho_csv: str) -> dict:
#     """Carrega os temas e organiza seus textos motivadores."""
#     temas = {}
#
#     with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
#         for linha in csv.DictReader(arquivo):
#             descricao = linha["description"]
#
#             try:
#                 partes = ast.literal_eval(descricao)
#             except (ValueError, SyntaxError):
#                 partes = [descricao]
#
#             if isinstance(partes, str):
#                 partes = [partes]
#
#             temas[linha["id"]] = "\n\n".join(
#                 parte.strip()
#                 for parte in partes
#                 if isinstance(parte, str) and parte.strip()
#             )
#
#     return temas
#
#
# def carregar_amostra(caminho_csv: str) -> list:
#     """Carrega as redações e as notas humanas do arquivo CSV."""
#     with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
#         return list(csv.DictReader(arquivo))
#
#
# def carregar_progresso(caminho_saida: Path) -> tuple:
#     """Recupera tentativas anteriores e avaliações concluídas."""
#     tentativas = {}
#     concluidos = set()
#
#     if not caminho_saida.exists():
#         return tentativas, concluidos
#
#     with caminho_saida.open(encoding="utf-8") as arquivo:
#         for linha in arquivo:
#             if not linha.strip():
#                 continue
#
#             registro = json.loads(linha)
#             chave = (
#                 registro["id_teste"],
#                 registro["condicao"],
#                 registro["repeticao"]
#             )
#
#             # Falhas de rede sem resposta não consomem tentativas de avaliação.
#             if registro.get("erro") and not registro.get("resposta"):
#                 continue
#
#             tentativas[chave] = tentativas.get(chave, 0) + 1
#
#             agente = registro.get("agente")
#             if agente and agente["status"] not in ("sem_notas", "incompleto"):
#                 concluidos.add(chave)
#
#     return tentativas, concluidos
#
#
# def montar_mensagem(tema: str, texto: str) -> str:
#     """Monta o conteúdo enviado ao modelo para avaliar uma redação."""
#     return (
#         f"[Corrigir]\n\n"
#         f"Tema (proposta de redação e textos motivadores):\n"
#         f"{tema}\n\n"
#         f"Texto:\n{texto}"
#     )
#
#
# def registrar_notas_humanas(redacao: dict) -> dict:
#     """Organiza as notas humanas que servirão como referência."""
#     notas = {
#         competencia: int(redacao[competencia])
#         for competencia in ("C1", "C2", "C3", "C4", "C5")
#     }
#     notas["total"] = int(redacao["score"])
#     return notas
#
#
# def criar_registro(
#     redacao: dict,
#     args: argparse.Namespace,
#     numero_tentativa: int
# ) -> dict:
#     """Prepara os metadados de uma avaliação."""
#     return {
#         "id_teste": redacao["id_teste"],
#         "prompt_id": redacao["prompt"],
#         "condicao": args.cond,
#         "repeticao": args.repeticao,
#         "tentativa": numero_tentativa,
#         "modelo": args.modelo,
#         "temperatura": (
#             args.temperatura
#             if args.temperatura is not None
#             else "padrao"
#         ),
#         "humano": registrar_notas_humanas(redacao),
#         "palavras": len(redacao["texto"].split()),
#         "data_utc": datetime.now(timezone.utc).isoformat(
#             timespec="seconds"
#         )
#     }
#
#
# def consultar_gemini(
#     cliente,
#     tipos,
#     modelo: str,
#     mensagem: str,
#     prompt_sistema: str,
#     temperatura
# ) -> tuple:
#     """Consulta o Gemini e repete a chamada em caso de erro."""
#     configuracao = {
#         "system_instruction": prompt_sistema
#     }
#
#     if temperatura is not None:
#         configuracao["temperature"] = temperatura
#
#     resposta = None
#     erro = None
#     metadados = {}
#
#     for tentativa in range(5):
#         try:
#             resultado = cliente.models.generate_content(
#                 model=modelo,
#                 contents=mensagem,
#                 config=tipos.GenerateContentConfig(**configuracao)
#             )
#
#             resposta = resultado.text
#
#             uso = getattr(resultado, "usage_metadata", None)
#             metadados = {
#                 "tokens": {
#                     "entrada": getattr(uso, "prompt_token_count", None),
#                     "saida": getattr(uso, "candidates_token_count", None)
#                 },
#                 "modelo_retornado": getattr(
#                     resultado, "model_version", None
#                 )
#             }
#
#             break
#
#         except Exception as excecao:
#             erro = f"{type(excecao).__name__}: {excecao}"
#             time.sleep(15 * (tentativa + 1))
#
#     return resposta, erro, metadados
#
#
# def salvar_resultado(caminho_saida: Path, registro: dict) -> None:
#     """Acrescenta uma avaliação ao arquivo de resultados JSONL."""
#     with caminho_saida.open("a", encoding="utf-8") as arquivo:
#         arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
#
#
# def executar_experimento() -> None:
#     """Coordena o processamento das redações e o registro dos resultados."""
#     args = configurar_argumentos()
#     csv.field_size_limit(10**9)
#
#     caminho_saida = Path(
#         args.saida or f"resultados_{args.cond}.jsonl"
#     )
#     caminho_prompt = (
#         Path(args.prompt_dir) / f"prompt_{args.cond}_v2.txt"
#     )
#
#     prompt_sistema = caminho_prompt.read_text(encoding="utf-8")
#     temas = carregar_temas(args.prompts_csv)
#     amostra = carregar_amostra(args.amostra)
#     tentativas, concluidos = carregar_progresso(caminho_saida)
#
#     cliente = None
#     tipos = None
#
#     if not args.dry_run:
#         from google import genai
#         from google.genai import types
#
#         cliente = genai.Client()
#
#     processadas = 0
#     erros_seguidos = 0
#
#     for redacao in amostra:
#         chave = (
#             redacao["id_teste"],
#             args.cond,
#             args.repeticao
#         )
#
#         # Ignora avaliações concluídas ou que atingiram o limite de tentativas.
#         if chave in concluidos:
#             continue
#
#         if tentativas.get(chave, 0) >= args.max_tentativas:
#             continue
#
#         if args.limite is not None and processadas >= args.limite:
#             break
#
#         tema = temas.get(redacao["prompt"])
#         if not tema:
#             sys.exit(
#                 f"prompts.csv não contém o id {redacao['prompt']} "
#                 f"(redação {redacao['id_teste']})."
#             )
#
#         mensagem = montar_mensagem(tema, redacao["texto"])
#         registro = criar_registro(
#             redacao,
#             args,
#             tentativas.get(chave, 0) + 1
#         )
#
#         if args.dry_run:
#             print(
#                 redacao["id_teste"],
#                 "|",
#                 mensagem[:80].replace("\n", " "),
#                 "..."
#             )
#             processadas += 1
#             continue
#
#         resposta, erro, metadados = consultar_gemini(
#             cliente,
#             tipos,
#             args.modelo,
#             mensagem,
#             prompt_sistema,
#             args.temperatura
#         )
#
#         registro.update(metadados)
#         registro["resposta"] = resposta
#         registro["erro"] = None if resposta else erro
#         registro["agente"] = extrair(resposta) if resposta else None
#
#         salvar_resultado(caminho_saida, registro)
#         processadas += 1
#
#         status = (
#             registro["agente"]["status"]
#             if registro["agente"]
#             else "ERRO"
#         )
#         print(redacao["id_teste"], args.cond, status, flush=True)
#
#         erros_seguidos = erros_seguidos + 1 if registro["erro"] else 0
#         if erros_seguidos >= 3:
#             sys.exit(
#                 "Três falhas consecutivas da API. Aguarde e execute "
#                 "novamente para retomar o experimento."
#             )
#
#         time.sleep(args.pausa)
#
#     print("Chamadas feitas:", processadas, "->", caminho_saida)
#
#
# if __name__ == "__main__":
#     executar_experimento()


# ============================================================
# CÓDIGO ORIGINAL FUNCIONAL
# ============================================================

import argparse, ast, csv, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

from extrair_notas import extrair

csv.field_size_limit(10**9)

ap = argparse.ArgumentParser()
ap.add_argument('--cond', required=True, choices=['A', 'B'])
ap.add_argument('--modelo', required=True)
ap.add_argument('--temperatura', type=float, default=None, help='se omitida, usa o padrão da API')
ap.add_argument('--amostra', default='../amostra_100.csv')
ap.add_argument('--prompts-csv', default=os.path.expanduser('~/Downloads/Artigo/essay/essay-br/prompts.csv'), help='prompts.csv do Essay-BR (colunas id,description)')
ap.add_argument('--prompt-dir', default='.')
ap.add_argument('--saida', default=None)
ap.add_argument('--limite', type=int, default=None)
ap.add_argument('--repeticao', type=int, default=1)
ap.add_argument('--max-tentativas', type=int, default=2, help='tentativas por redação quando a resposta não traz as notas')
ap.add_argument('--pausa', type=float, default=6.0, help='segundos entre chamadas (limite da cota gratuita)')
ap.add_argument('--dry-run', action='store_true', help='não chama a API; só monta as mensagens')
args = ap.parse_args()

saida = Path(args.saida or f'resultados_{args.cond}.jsonl')
prompt = (Path(args.prompt_dir) / f'prompt_{args.cond}_v2.txt').read_text(encoding='utf-8')

temas = {}
for r in csv.DictReader(open(args.prompts_csv, encoding='utf-8')):
    try:
        partes = ast.literal_eval(r['description'])
        if isinstance(partes, str):
            partes = [partes]
    except (ValueError, SyntaxError):
        partes = [r['description']]
    temas[r['id']] = '\n\n'.join(p.strip() for p in partes if p.strip())

amostra = list(csv.DictReader(open(args.amostra, encoding='utf-8')))
tentativas, concluidos = {}, set()

if saida.exists():
    for l in open(saida, encoding='utf-8'):
        j = json.loads(l)
        k = (j['id_teste'], j['condicao'], j['repeticao'])

        if j.get('erro') and not j.get('resposta'):
            continue  # falha da API (cota, rede): não conta como tentativa do modelo

        tentativas[k] = tentativas.get(k, 0) + 1

        if j.get('agente') and j['agente']['status'] not in ('sem_notas', 'incompleto'):
            concluidos.add(k)

client = None

if not args.dry_run:
    from google import genai
    from google.genai import types

    client = genai.Client()  # lê GEMINI_API_KEY do ambiente; sem ferramentas ligadas

n = 0
erros_seguidos = 0

for r in amostra:
    chave = (r['id_teste'], args.cond, args.repeticao)

    if chave in concluidos or tentativas.get(chave, 0) >= args.max_tentativas:
        continue

    if args.limite is not None and n >= args.limite:
        break

    tema = temas.get(r['prompt'])

    if not tema:
        sys.exit(f"prompts.csv não tem o id {r['prompt']} (redação {r['id_teste']})")

    mensagem = (
        f"[Corrigir]\n\n"
        f"Tema (proposta de redação e textos motivadores):\n"
        f"{tema}\n\n"
        f"Texto:\n{r['texto']}"
    )

    reg = {
        'id_teste': r['id_teste'],
        'prompt_id': r['prompt'],
        'condicao': args.cond,
        'repeticao': args.repeticao,
        'tentativa': tentativas.get(chave, 0) + 1,
        'modelo': args.modelo,
        'temperatura': args.temperatura if args.temperatura is not None else 'padrao',
        'humano': {c: int(r[c]) for c in ('C1', 'C2', 'C3', 'C4', 'C5')} | {'total': int(r['score'])},
        'palavras': len(r['texto'].split()),
        'data_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }

    if args.dry_run:
        print(r['id_teste'], '|', mensagem[:80].replace('\n', ' '), '...')
        n += 1
        continue

    resposta, erro = None, None

    for tentativa in range(5):
        try:
            resp = client.models.generate_content(
                model=args.modelo,
                contents=mensagem,
                config=types.GenerateContentConfig(
                    system_instruction=prompt,
                    **({} if args.temperatura is None else {'temperature': args.temperatura})
                )
            )

            resposta = resp.text
            um = getattr(resp, 'usage_metadata', None)

            reg['tokens'] = {
                'entrada': getattr(um, 'prompt_token_count', None),
                'saida': getattr(um, 'candidates_token_count', None)
            }

            reg['modelo_retornado'] = getattr(resp, 'model_version', None)
            break

        except Exception as e:  # cota (429), erro de rede etc.
            erro = f'{type(e).__name__}: {e}'
            time.sleep(15 * (tentativa + 1))

    reg['resposta'] = resposta
    reg['erro'] = None if resposta else erro
    reg['agente'] = extrair(resposta) if resposta else None

    with open(saida, 'a', encoding='utf-8') as f:
        f.write(json.dumps(reg, ensure_ascii=False) + '\n')

    n += 1

    print(
        r['id_teste'],
        args.cond,
        reg['agente']['status'] if reg['agente'] else 'ERRO',
        flush=True
    )

    erros_seguidos = erros_seguidos + 1 if reg['erro'] else 0

    if erros_seguidos >= 3:
        sys.exit(
            '3 falhas seguidas da API (provável cota). Aguarde e rode de novo: '
            'ele retoma de onde parou.'
        )

    time.sleep(args.pausa)

print('chamadas feitas:', n, '->', saida)