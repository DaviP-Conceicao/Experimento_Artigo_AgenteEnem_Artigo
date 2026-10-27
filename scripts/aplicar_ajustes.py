
"""_summary_

Author: Davi Paulino Conceição
Date: 26/10/2026

pipeline em Python voltado para um artigo científico (avaliação automatizada
de redações com a API do Gemini, extração de notas por competências C1–C5, cálculo de
concordância via QWK). Nome do arquivo: aplicar_ajustes.py

Descrição: A função desse script de grosso modo é como um atualizador. Ele começa
fazendo uma busca substituindo pontos de códigos específicos em outros arquivos
(extrair_notas.py e executar_experimento.py). Se o que ele busca ele tiver achado,
ele garante as alterações se o trecho for encontrado só uma vez.
"""

# from pathlib import Path

# # Dicionário declarativo: agrupa todas as alterações por arquivo alvo.
# # Vantagem: Abre e fecha cada arquivo apenas 1 vez no disco (muito mais rápido e seguro).
# AJUSTES: dict[str, list[tuple[str, str]]] = {
#     "extrair_notas.py": [
#         (
#             "    for linha in texto.splitlines():\n",
#             "    linhas = texto.splitlines()\n    for i, linha in enumerate(linhas):\n",
#         ),
#         (
#             "            n = re.search(r'(\\d{1,4})\\s*(?:/\\s*1\\.?000|\\*)?', s[re.search(r'NOTA\\s+TOTAL', s, re.I).end():])\n            if n:",
#             "            resto_t = s[re.search(r'NOTA\\s+TOTAL', s, re.I).end():]\n            n = re.search(r'(\\d{1,4})', resto_t) or re.search(r'(\\d{1,4})\\s*\\**\\s*/\\s*1\\.?000', ' '.join(linhas[i + 1:i + 3]))\n            if n:",
#         ),
#     ],
#     "executar_experimento.py": [
#         (
#             'mensagem = f"Tema (proposta de redação e textos motivadores):',
#             'mensagem = f"[Corrigir]\\n\\nTema (proposta de redação e textos motivadores):',
#         ),
#         (
#             "ap.add_argument('--pausa'",
#             "ap.add_argument('--max-tentativas', type=int, default=2, help='tentativas por redação quando a resposta não traz as notas')\nap.add_argument('--pausa'",
#         ),
#         (
#             "feitos = set()\nif saida.exists():\n    for l in open(saida, encoding='utf-8'):\n        j = json.loads(l)\n        feitos.add((j['id_teste'], j['condicao'], j['repeticao']))",
#             "tentativas, concluidos = {}, set()\nif saida.exists():\n    for l in open(saida, encoding='utf-8'):\n        j = json.loads(l)\n        k = (j['id_teste'], j['condicao'], j['repeticao'])\n        tentativas[k] = tentativas.get(k, 0) + 1\n        if j.get('agente') and j['agente']['status'] not in ('sem_notas', 'incompleto'):\n            concluidos.add(k)",
#         ),
#         (
#             "    if chave in feitos:\n        continue",
#             "    if chave in concluidos or tentativas.get(chave, 0) >= args.max_tentativas:\n        continue",
#         ),
#         (
#             "'condicao': args.cond, 'repeticao': args.repeticao,",
#             "'condicao': args.cond, 'repeticao': args.repeticao, 'tentativa': tentativas.get(chave, 0) + 1,",
#         ),
#     ],
# }


# def aplicar_lote(lote_ajustes: dict[str, list[tuple[str, str]]]) -> None:
#     """Carrega os arquivos, aplica as trocas em memória e regrava se tudo for válido."""
#     for caminho_str, substituicoes in lote_ajustes.items():
#         caminho = Path(caminho_str)
#         if not caminho.exists():
#             print(f"[-] Arquivo ignorado (não localizado): {caminho_str}")
#             continue

#         conteudo = caminho.read_text(encoding="utf-8")

#         for antigo, novo in substituicoes:
#             assert conteudo.count(antigo) == 1, (
#                 f"Falha em {caminho_str}: trecho ausente ou duplicado:\n{antigo[:60]}..."
#             )
#             conteudo = conteudo.replace(antigo, novo)

#         caminho.write_text(conteudo, encoding="utf-8")
#         print(f"[+] Ajustes aplicados com sucesso em: {caminho_str}")


# if __name__ == "__main__":
#     aplicar_lote(AJUSTES)


from pathlib import Path


def trocar(arq, antigo, novo):
    p = Path(arq)
    t = p.read_text(encoding='utf-8')
    assert t.count(antigo) == 1, f'{arq}: trecho não encontrado ou repetido:\n{antigo[:70]}'
    p.write_text(t.replace(antigo, novo), encoding='utf-8')

# --- extrair_notas.py: nota total na linha seguinte ("**NOTA TOTAL**" e depois "**560 / 1000**")
trocar('extrair_notas.py',
       "    for linha in texto.splitlines():\n",
       "    linhas = texto.splitlines()\n    for i, linha in enumerate(linhas):\n")
trocar('extrair_notas.py',
       """            n = re.search(r'(\\d{1,4})\\s*(?:/\\s*1\\.?000|\\*)?', s[re.search(r'NOTA\\s+TOTAL', s, re.I).end():])
            if n:""",
       """            resto_t = s[re.search(r'NOTA\\s+TOTAL', s, re.I).end():]
            n = re.search(r'(\\d{1,4})', resto_t) or re.search(r'(\\d{1,4})\\s*\\**\\s*/\\s*1\\.?000', ' '.join(linhas[i + 1:i + 3]))
            if n:""")

# --- executar_experimento.py: gatilho [Corrigir] e regra de nova tentativa
trocar('executar_experimento.py',
       'mensagem = f"Tema (proposta de redação e textos motivadores):',
       'mensagem = f"[Corrigir]\\n\\nTema (proposta de redação e textos motivadores):')
trocar('executar_experimento.py',
       "ap.add_argument('--pausa'",
       "ap.add_argument('--max-tentativas', type=int, default=2, help='tentativas por redação quando a resposta não traz as notas')\nap.add_argument('--pausa'")
trocar('executar_experimento.py',
       """feitos = set()
if saida.exists():
    for l in open(saida, encoding='utf-8'):
        j = json.loads(l)
        feitos.add((j['id_teste'], j['condicao'], j['repeticao']))""",
       """tentativas, concluidos = {}, set()
if saida.exists():
    for l in open(saida, encoding='utf-8'):
        j = json.loads(l)
        k = (j['id_teste'], j['condicao'], j['repeticao'])
        tentativas[k] = tentativas.get(k, 0) + 1
        if j.get('agente') and j['agente']['status'] not in ('sem_notas', 'incompleto'):
            concluidos.add(k)""")
trocar('executar_experimento.py',
       "    if chave in feitos:\n        continue",
       "    if chave in concluidos or tentativas.get(chave, 0) >= args.max_tentativas:\n        continue")
trocar('executar_experimento.py',
       "'condicao': args.cond, 'repeticao': args.repeticao,",
       "'condicao': args.cond, 'repeticao': args.repeticao, 'tentativa': tentativas.get(chave, 0) + 1,")
print('ajustes aplicados')
