"""_summary_

Author: Davi Paulino Conceição
Date: 26/10/2026

pipeline em Python voltado para um artigo científico (avaliação automatizada
de redações com a API do Gemini, extração de notas por competências C1–C5, cálculo de
concordância via QWK). Nome do arquivo: blindar_script.py

Descrição: Este script atua como um patch de proteção e resiliência para o arquivo
executar_experimento.py. Ele adiciona um mecanismo de parada automática após 3 falhas
consecutivas da API do Gemini (ex.: estouro de cota) e impede que falhas de rede/cota
queimem as tentativas válidas de correção do modelo, permitindo a retomada segura do experimento.
"""

# from pathlib import Path

# ARQUIVO_ALVO = Path("executar_experimento.py")

# # Lista de substituições (antigo, novo) para aumentar a tolerância a falhas
# PATCHES: tuple[tuple[str, str], ...] = (
#     # 1. Ignora falhas puras de rede/cota na contagem de tentativas do modelo
#     (
#         "        k = (j['id_teste'], j['condicao'], j['repeticao'])\n"
#         "        tentativas[k] = tentativas.get(k, 0) + 1\n",
#         "        k = (j['id_teste'], j['condicao'], j['repeticao'])\n"
#         "        if j.get('erro') and not j.get('resposta'):\n"
#         "            continue  # falha da API (cota, rede): não conta como tentativa do modelo\n"
#         "        tentativas[k] = tentativas.get(k, 0) + 1\n",
#     ),
#     # 2. Inicializa o contador de erros consecutivos antes do loop de redações
#     (
#         "n = 0\nfor r in amostra:",
#         "n = 0\nerros_seguidos = 0\nfor r in amostra:",
#     ),
#     # 3. Força o envio imediato do log (flush=True) e aborta se atingir 3 erros seguidos
#     (
#         "    print(r['id_teste'], args.cond, reg['agente']['status'] if reg['agente'] else 'ERRO')\n",
#         "    print(r['id_teste'], args.cond, reg['agente']['status'] if reg['agente'] else 'ERRO', flush=True)\n"
#         "    erros_seguidos = erros_seguidos + 1 if reg['erro'] else 0\n"
#         "    if erros_seguidos >= 3:\n"
#         "        sys.exit('3 falhas seguidas da API (provável cota). Aguarde e rode de novo: ele retoma de onde parou.')\n",
#     ),
# )


# def blindar() -> None:
#     """Aplica proteções de tolerância a falhas no script de experimentação."""
#     if not ARQUIVO_ALVO.exists():
#         print(f"[-] Arquivo alvo '{ARQUIVO_ALVO}' não encontrado.")
#         return

#     conteudo = ARQUIVO_ALVO.read_text(encoding="utf-8")

#     # Evita reaplicar se o código já contiver o mecanismo de segurança
#     if "erros_seguidos" in conteudo:
#         print("[*] O script já se encontra blindado. Nenhuma ação necessária.")
#         return

#     for antigo, novo in PATCHES:
#         assert conteudo.count(antigo) == 1, (
#             f"Falha de integridade: trecho não localizado ou duplicado:\n{antigo[:60]}..."
#         )
#         conteudo = conteudo.replace(antigo, novo)

#     ARQUIVO_ALVO.write_text(conteudo, encoding="utf-8")
#     print(f"[+] '{ARQUIVO_ALVO}' blindado com sucesso!")


# if __name__ == "__main__":
#     blindar()

from pathlib import Path
p = Path('executar_experimento.py')
t = p.read_text(encoding='utf-8')
if 'erros_seguidos' in t:
    raise SystemExit('já aplicado: nada a fazer')

velho1 = """        k = (j['id_teste'], j['condicao'], j['repeticao'])
        tentativas[k] = tentativas.get(k, 0) + 1
"""
novo1 = """        k = (j['id_teste'], j['condicao'], j['repeticao'])
        if j.get('erro') and not j.get('resposta'):
            continue  # falha da API (cota, rede): não conta como tentativa do modelo
        tentativas[k] = tentativas.get(k, 0) + 1
"""
velho2 = "n = 0\nfor r in amostra:"
novo2 = "n = 0\nerros_seguidos = 0\nfor r in amostra:"
velho3 = "    print(r['id_teste'], args.cond, reg['agente']['status'] if reg['agente'] else 'ERRO')\n"
novo3 = """    print(r['id_teste'], args.cond, reg['agente']['status'] if reg['agente'] else 'ERRO', flush=True)
    erros_seguidos = erros_seguidos + 1 if reg['erro'] else 0
    if erros_seguidos >= 3:
        sys.exit('3 falhas seguidas da API (provável cota). Aguarde e rode de novo: ele retoma de onde parou.')
"""
for velho, novo in ((velho1, novo1), (velho2, novo2), (velho3, novo3)):
    assert t.count(velho) == 1, 'trecho não encontrado: ' + velho[:50]
    t = t.replace(velho, novo)
p.write_text(t, encoding='utf-8')
print('script blindado')
