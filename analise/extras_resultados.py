
"""
Resumo de estatísticas complementares para a seção de Resultados.

Author: Davi Paulino Conceição
Date: 26/10/2026

Projeto: Pipeline em Python voltado para um artigo científico sobre avaliação
automatizada de redações com a API do Gemini, extração de notas por competências
C1–C5 e análise de concordância com as avaliações humanas por meio do QWK.

Nome do arquivo: extras_resultados.py

Descrição:
Este script calcula estatísticas complementares que não são geradas diretamente
pelo metricas_main.py. Ele utiliza os dados preparados pelo módulo metricas_lib
e o diretório de saída definido em carregar.

As análises incluem:
- Desvio-padrão das notas totais humanas e das condições experimentais A e B.
- Frequência de notas 200 na competência C5.
- Viés médio da competência C5 para cada nível de nota humana.
- Identificação das dez maiores divergências em cada condição.
- Comparação das competências responsáveis pelas maiores diferenças.
- Identificação de redações cuja nota humana total é zero.
- Cálculo do valor crítico de correlação para um teste bilateral com
  significância de 5%.

Os resultados textuais são gravados em extras.txt, enquanto as estatísticas
estruturadas selecionadas são armazenadas em extras.json.

Abaixo está uma versão de referência reorganizada e comentada, mantida inativa
para consulta futura. Ao final, encontra-se o código original funcional.
"""


# ============================================================================
# VERSÃO DE REFERÊNCIA MELHORADA — INATIVA
# ============================================================================
#
# Esta versão organiza o processamento em funções menores, separando a
# preparação dos dados, as análises estatísticas e a gravação dos resultados.
#
# Todo o bloco permanece comentado e não será executado.
#
# import json
# from pathlib import Path
#
# import numpy as np
# from scipy import stats
#
# from metricas_lib import montar
# from carregar import PASTA_SAIDA
#
#
# CONDICOES = ("A", "B")
# COMPETENCIAS = ("C1", "C2", "C3", "C4", "C5")
# NIVEIS_NOTA = (0, 40, 80, 120, 160, 200)
# NUM_REPETICOES = 3
#
#
# def preparar_dados():
#     """
#     Carrega os dados e identifica as redações válidas nas duas condições.
#
#     O conjunto pareado inclui redações sem valores NaN em todas as
#     competências e repetições de A e B.
#     """
#     ids, notas_humanas, palavras, avaliacoes, declaradas, status = montar()
#
#     # Mantém somente redações com dados completos em ambas as condições.
#     validas = (
#         ~np.isnan(avaliacoes["A"]).any(axis=(0, 2))
#         & ~np.isnan(avaliacoes["B"]).any(axis=(0, 2))
#     )
#
#     indices = np.where(validas)[0]
#
#     # Calcula a nota total humana de cada redação.
#     totais_humanos = notas_humanas.sum(axis=1)
#
#     # Calcula a média das três repetições para cada competência.
#     medias = {
#         condicao: avaliacoes[condicao].mean(axis=0)
#         for condicao in CONDICOES
#     }
#
#     # Soma as competências depois de calcular a média das repetições.
#     totais_medios = {
#         condicao: medias[condicao].sum(axis=1)
#         for condicao in CONDICOES
#     }
#
#     return {
#         "ids": ids,
#         "humanas": notas_humanas,
#         "palavras": palavras,
#         "avaliacoes": avaliacoes,
#         "indices": indices,
#         "totais_humanos": totais_humanos,
#         "medias": medias,
#         "totais_medios": totais_medios,
#     }
#
#
# def registrar(mensagem, linhas):
#     """
#     Acrescenta uma mensagem ao relatório textual e a imprime no terminal.
#
#     A lista acumulada será utilizada posteriormente para criar extras.txt.
#     """
#     linhas.append(mensagem)
#     print(mensagem)
#
#
# def analisar_desvios_padrao(dados, registrar_linha):
#     """
#     Calcula os desvios-padrão das notas totais no conjunto pareado.
#
#     Para cada condição, compara o desvio-padrão dos totais em cada repetição
#     com o desvio-padrão dos totais calculados a partir da média das repetições.
#     """
#     indices = dados["indices"]
#     humanas = dados["totais_humanos"]
#     avaliacoes = dados["avaliacoes"]
#     totais_medios = dados["totais_medios"]
#
#     registrar_linha("\n== Desvio-padrão da nota total")
#     registrar_linha(f"Humano: {humanas[indices].std():.1f}")
#
#     for condicao in CONDICOES:
#         # Calcula um desvio-padrão para cada repetição experimental.
#         desvios = [
#             avaliacoes[condicao][repeticao][indices].sum(axis=1).std()
#             for repeticao in range(NUM_REPETICOES)
#         ]
#
#         # Calcula o desvio-padrão dos totais obtidos após a média das repetições.
#         desvio_da_media = totais_medios[condicao][indices].std()
#
#         registrar_linha(
#             f"{condicao}: por repetição "
#             f"{[round(valor, 1) for valor in desvios]} | "
#             f"média dos 3 desvios {np.mean(desvios):.1f} | "
#             f"desvio da média das repetições {desvio_da_media:.1f}"
#         )
#
#
# def analisar_c5(dados, registrar_linha, resultado):
#     """
#     Examina a frequência da nota 200 em C5 e o viés por nível humano.
#
#     Também contabiliza redações cuja média de C5 é 200 e redações com
#     nota zero em C5 nas três repetições.
#     """
#     indices = dados["indices"]
#     humanas = dados["humanas"]
#     avaliacoes = dados["avaliacoes"]
#     medias = dados["medias"]
#
#     total = len(indices)
#     notas_c5_humanas = humanas[indices, 4]
#
#     quantidade_200 = int((notas_c5_humanas == 200).sum())
#     percentual_200 = 100 * quantidade_200 / total
#
#     registrar_linha("\n== C5 nível 200")
#     registrar_linha(
#         f"Humano: {quantidade_200} de {total} redações "
#         f"({percentual_200:.1f}%)"
#     )
#
#     resultado["c5_200"] = {"humano": [quantidade_200, total]}
#
#     for condicao in CONDICOES:
#         # Formato esperado: repetições × redações do conjunto × competências.
#         c5_repeticoes = avaliacoes[condicao][:, indices, 4]
#         quantidade = int((c5_repeticoes == 200).sum())
#         tamanho = c5_repeticoes.size
#
#         # Conta redações cuja nota C5 foi 200 em todas as repetições.
#         media_200 = int((c5_repeticoes.mean(axis=0) == 200).sum())
#
#         # Conta redações que receberam zero em C5 em todas as repetições.
#         zeros_todas = int((c5_repeticoes.max(axis=0) == 0).sum())
#
#         registrar_linha(
#             f"{condicao}: {quantidade} de {tamanho} respostas "
#             f"({100 * quantidade / tamanho:.1f}%) | "
#             f"redações com média 200: {media_200} | "
#             f"C5 = 0 nas 3 repetições: {zeros_todas} redações"
#         )
#
#         resultado["c5_200"][condicao] = [quantidade, tamanho]
#
#     registrar_linha(
#         "\n== Viés da C5 (agente − humano, média das 3 repetições) "
#         "por nível humano da C5"
#     )
#
#     for condicao in CONDICOES:
#         notas_agente = medias[condicao][indices, 4]
#         notas_humanas = humanas[indices, 4]
#
#         # Calcula a diferença média entre agente e avaliador humano
#         # separadamente para cada nível de nota humana.
#         for nivel in NIVEIS_NOTA:
#             grupo = notas_humanas == nivel
#             quantidade = int(grupo.sum())
#
#             # Evita calcular a média de um grupo vazio.
#             vies = (
#                 np.mean(notas_agente[grupo] - notas_humanas[grupo])
#                 if quantidade
#                 else float("nan")
#             )
#
#             registrar_linha(
#                 f"{condicao} C5 humano {nivel:3d}: "
#                 f"n={quantidade:2d} viés {vies:+.1f}"
#             )
#
#         # Agrupa as redações com nota humana C5 igual a 0 ou 40.
#         grupo_baixo = notas_humanas <= 40
#         quantidade = int(grupo_baixo.sum())
#
#         vies_baixo = (
#             np.mean(
#                 notas_agente[grupo_baixo] - notas_humanas[grupo_baixo]
#             )
#             if quantidade
#             else float("nan")
#         )
#
#         registrar_linha(
#             f"{condicao} C5 humano 0 ou 40: "
#             f"n={quantidade} viés {vies_baixo:+.1f}"
#         )
#
#
# def analisar_divergencias(dados, registrar_linha, resultado):
#     """
#     Identifica as dez maiores divergências por condição experimental.
#
#     A divergência é o valor absoluto da diferença entre a nota total média
#     do agente e a nota total humana.
#     """
#     ids = dados["ids"]
#     indices = dados["indices"]
#     humanas = dados["humanas"]
#     palavras = dados["palavras"]
#     medias = dados["medias"]
#     totais_humanos = dados["totais_humanos"]
#     totais_medios = dados["totais_medios"]
#
#     registrar_linha(
#         "\n== 10 maiores divergências de cada condição "
#         "(|média das 3 repetições do total − humano|)"
#     )
#
#     maiores = {}
#
#     for condicao in CONDICOES:
#         # Calcula a diferença absoluta no conjunto pareado.
#         diferencas = np.abs(
#             totais_medios[condicao][indices] - totais_humanos[indices]
#         )
#
#         # Ordena da maior para a menor divergência.
#         # kind="stable" mantém a ordem original em caso de empate.
#         ordem = np.argsort(-diferencas, kind="stable")[:10]
#
#         maiores[condicao] = [ids[indices[posicao]] for posicao in ordem]
#         registrar_linha(f"{condicao}: {maiores[condicao]}")
#
#     # Combina as listas sem repetir IDs e preservando a ordem de aparição.
#     uniao = list(dict.fromkeys(maiores["A"] + maiores["B"]))
#     registrar_linha(f"União: {len(uniao)} redações {uniao}")
#
#     # Verifica se todas as redações selecionadas foram subestimadas
#     # nas duas condições experimentais.
#     subestimadas = all(
#         totais_medios[condicao][ids.index(identificador)]
#         < totais_humanos[ids.index(identificador)]
#         for condicao in CONDICOES
#         for identificador in uniao
#     )
#     registrar_linha(
#         f"Todas subestimam em A e B: {subestimadas}"
#     )
#
#     # Cabeçalho da tabela detalhada de divergências.
#     registrar_linha(
#         "\nid | palavras | humano | A | B | C5 humano | C5 A | C5 B | "
#         "competência de maior diferença (A / B)"
#     )
#
#     linhas_resultado = []
#
#     for identificador in uniao:
#         # Recupera a posição da redação nos dados carregados.
#         indice = ids.index(identificador)
#         maiores_diferencas = {}
#
#         for condicao in CONDICOES:
#             # A diferença positiva indica nota humana maior que a do agente.
#             diferencas = np.round(
#                 humanas[indice] - medias[condicao][indice],
#                 6
#             )
#
#             # Registra todas as competências empatadas na maior diferença.
#             maiores_diferencas[condicao] = [
#                 COMPETENCIAS[k]
#                 for k in range(5)
#                 if diferencas[k] == diferencas.max()
#             ]
#
#         # Organiza os dados da redação em um registro estruturado.
#         linha = {
#             "id": identificador,
#             "palavras": int(palavras[indice]),
#             "humano": int(totais_humanos[indice]),
#             "A": int(round(totais_medios["A"][indice])),
#             "B": int(round(totais_medios["B"][indice])),
#             "c5h": int(humanas[indice, 4]),
#             "c5A": int(round(medias["A"][indice, 4])),
#             "c5B": int(round(medias["B"][indice, 4])),
#             "maior": maiores_diferencas,
#         }
#         linhas_resultado.append(linha)
#
#         registrar_linha(
#             f"{linha['id']} | {linha['palavras']} | {linha['humano']} | "
#             f"{linha['A']} | {linha['B']} | {linha['c5h']} | "
#             f"{linha['c5A']} | {linha['c5B']} | "
#             f"{maiores_diferencas['A']} / {maiores_diferencas['B']}"
#         )
#
#     resultado["divergencias"] = linhas_resultado
#
#     # Identifica redações em que C5 é a única competência com maior
#     # diferença nas duas condições, sem empate com outras competências.
#     somente_c5 = [
#         linha["id"]
#         for linha in linhas_resultado
#         if linha["maior"]["A"] == ["C5"]
#         and linha["maior"]["B"] == ["C5"]
#     ]
#
#     demais = [
#         linha["id"]
#         for linha in linhas_resultado
#         if linha["id"] not in somente_c5
#     ]
#
#     registrar_linha(
#         f"C5 é a única competência de maior diferença (A e B) em "
#         f"{len(somente_c5)} de {len(linhas_resultado)}; demais: {demais}"
#     )
#
#
# def analisar_notas_humanas_zero(dados, registrar_linha):
#     """
#     Lista redações cuja soma das notas humanas é zero.
#
#     Para cada uma, apresenta os totais de A e B em cada repetição.
#     """
#     indices = dados["indices"]
#     totais_humanos = dados["totais_humanos"]
#     ids = dados["ids"]
#     avaliacoes = dados["avaliacoes"]
#
#     registrar_linha(
#         "\n== Redações com nota humana total zero no conjunto pareado"
#     )
#
#     for indice in indices:
#         if totais_humanos[indice] != 0:
#             continue
#
#         totais_a = [
#             int(avaliacoes["A"][repeticao][indice].sum())
#             for repeticao in range(NUM_REPETICOES)
#         ]
#         totais_b = [
#             int(avaliacoes["B"][repeticao][indice].sum())
#             for repeticao in range(NUM_REPETICOES)
#         ]
#
#         registrar_linha(
#             f"{ids[indice]}: A {totais_a} | B {totais_b}"
#         )
#
#
# def calcular_correlacao_critica(tamanho_amostra):
#     """
#     Calcula o valor absoluto crítico de Pearson para p < 0,05 bilateral.
#
#     O cálculo utiliza a distribuição t de Student e os graus de liberdade
#     n - 2, conforme a fórmula aplicada no código original.
#     """
#     graus_liberdade = tamanho_amostra - 2
#     t_critico = stats.t.ppf(0.975, graus_liberdade)
#
#     return t_critico / np.sqrt(
#         graus_liberdade + t_critico**2
#     )
#
#
# def salvar_resultados(linhas, resultado):
#     """
#     Grava o relatório textual e o resultado estruturado em JSON.
#
#     O diretório de saída é fornecido pelo módulo carregar.
#     """
#     PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
#
#     arquivo_texto = PASTA_SAIDA / "extras.txt"
#     arquivo_json = PASTA_SAIDA / "extras.json"
#
#     arquivo_texto.write_text(
#         "\n".join(linhas) + "\n",
#         encoding="utf-8"
#     )
#
#     with arquivo_json.open("w", encoding="utf-8") as arquivo:
#         json.dump(
#             resultado,
#             arquivo,
#             indent=1,
#             ensure_ascii=False
#         )
#
#
# def executar():
#     """Executa as análises complementares e salva os resultados."""
#     dados = preparar_dados()
#     linhas = []
#     resultado = {}
#
#     # Usa uma função auxiliar para centralizar a impressão e o registro.
#     registrar_linha = lambda mensagem="": registrar(mensagem, linhas)
#
#     registrar_linha(
#         f"Redações no conjunto pareado: {len(dados['indices'])}"
#     )
#
#     analisar_desvios_padrao(dados, registrar_linha)
#     analisar_c5(dados, registrar_linha, resultado)
#     analisar_divergencias(dados, registrar_linha, resultado)
#     analisar_notas_humanas_zero(dados, registrar_linha)
#
#     # Calcula o limite crítico da correlação para o tamanho do conjunto.
#     n = len(dados["indices"])
#     valor_critico = calcular_correlacao_critica(n)
#
#     registrar_linha(
#         f"\n== |r| mínimo com p < 0,05 (bilateral), "
#         f"n = {n}: {valor_critico:.3f}"
#     )
#
#     resultado["r_critico"] = float(valor_critico)
#
#     salvar_resultados(linhas, resultado)
#
#
# if __name__ == "__main__":
#     # A execução só ocorre quando o arquivo é chamado diretamente.
#     executar()


# ============================================================================
# CÓDIGO ORIGINAL FUNCIONAL — MANTIDO
# ============================================================================
#
# O bloco abaixo preserva o código original enviado para documentação.
# Ele continua ativo e utiliza os módulos e as estruturas de dados originais.


"""Números complementares da seção de Resultados que não saem do metricas_main.py:
nível 200 da C5, viés por nível humano da C5, maiores divergências (tabela), competência com a maior diferença,
desvio-padrão do total por repetição e limite de detecção da correlação.
Uso:  EXP_DIR=/caminho/da/pasta python3 extras_resultados.py   (grava saida/extras.txt e saida/extras.json)"""
import json, numpy as np
from scipy import stats
from metricas_lib import montar
from carregar import PASTA_SAIDA

ids, H, words, A, DECL, STAT = montar()
ok = ~np.isnan(A['A']).any(axis=(0, 2)) & ~np.isnan(A['B']).any(axis=(0, 2))
oi = np.where(ok)[0]
Ht = H.sum(1)
media = {c: A[c].mean(0) for c in 'AB'}          # (redações, competências), média das 3 repetições
tot = {c: media[c].sum(1) for c in 'AB'}
out, L = {}, []
def p(s=''): L.append(s); print(s)

p(f'redações no conjunto pareado: {len(oi)}')
# desvio-padrão do total (população, como no metricas_main.py)
p('\n== desvio-padrão da nota total')
p(f'humano {Ht[oi].std():.1f}')
for c in 'AB':
    per = [A[c][r][oi].sum(1).std() for r in range(3)]
    p(f'{c}: por repetição {[round(x, 1) for x in per]} | média dos 3 desvios {np.mean(per):.1f} | desvio da média das repetições {tot[c][oi].std():.1f}')

# nível 200 da C5
p('\n== C5 nível 200')
n200 = int((H[oi, 4] == 200).sum()); p(f'humano: {n200} de {len(oi)} redações ({100*n200/len(oi):.1f}%)')
out['c5_200'] = {'humano': [n200, len(oi)]}
for c in 'AB':
    r = A[c][:, oi, 4]; k = int((r == 200).sum())
    p(f'{c}: {k} de {r.size} respostas ({100*k/r.size:.1f}%) | redações com média 200: {int((r.mean(0) == 200).sum())} | C5 = 0 nas 3 repetições: {int((r.max(0) == 0).sum())} redações')
    out['c5_200'][c] = [k, int(r.size)]
p('\n== viés da C5 (agente − humano, média das 3 repetições) por nível humano da C5')
for c in 'AB':
    m = media[c][oi, 4]; h = H[oi, 4]
    for lv in (0, 40, 80, 120, 160, 200):
        s = h == lv
        p(f'{c} C5 humano {lv:3d}: n={int(s.sum()):2d} viés {np.mean(m[s]-h[s]):+.1f}')
    s = h <= 40; p(f'{c} C5 humano 0 ou 40: n={int(s.sum())} viés {np.mean(m[s]-h[s]):+.1f}')

# maiores divergências
p('\n== 10 maiores divergências de cada condição (|média das 3 repetições do total − humano|)')
top = {}
for c in 'AB':
    d = np.abs(tot[c][oi] - Ht[oi]); o = np.argsort(-d, kind='stable')[:10]
    top[c] = [ids[oi[i]] for i in o]; p(f'{c}: {top[c]}')
uniao = list(dict.fromkeys(top['A'] + top['B']))
p(f'união: {len(uniao)} redações {uniao}')
p(f'todas subestimam em A e B: {all(tot[c][ids.index(i)] < Ht[ids.index(i)] for c in "AB" for i in uniao)}')
linhas = []
p('\nid | palavras | humano | A | B | C5 humano | C5 A | C5 B | competência de maior diferença (A / B)')
for i in uniao:
    n = ids.index(i)
    mx = {}
    for c in 'AB':
        g = np.round(H[n] - media[c][n], 6); mx[c] = [f'C{k+1}' for k in range(5) if g[k] == g.max()]
    linhas.append(dict(id=i, palavras=int(words[n]), humano=int(Ht[n]), A=int(round(tot['A'][n])), B=int(round(tot['B'][n])),
                       c5h=int(H[n, 4]), c5A=int(round(media['A'][n, 4])), c5B=int(round(media['B'][n, 4])), maior=mx))
    l = linhas[-1]; p(f"{l['id']} | {l['palavras']} | {l['humano']} | {l['A']} | {l['B']} | {l['c5h']} | {l['c5A']} | {l['c5B']} | {mx['A']} / {mx['B']}")
out['divergencias'] = linhas
so_c5 = [l['id'] for l in linhas if l['maior']['A'] == ['C5'] and l['maior']['B'] == ['C5']]
p(f'C5 é a única competência de maior diferença (A e B) em {len(so_c5)} de {len(linhas)}; demais: {[l["id"] for l in linhas if l["id"] not in so_c5]}')

# zeros humanos
p('\n== redações com nota humana total zero no conjunto pareado')
for i in oi:
    if Ht[i] == 0:
        p(f'{ids[i]}: A {[int(A["A"][r][i].sum()) for r in range(3)]} | B {[int(A["B"][r][i].sum()) for r in range(3)]}')

# limite de detecção da correlação (n = conjunto pareado)
n = len(oi); t = stats.t.ppf(0.975, n - 2); rc = t / np.sqrt(n - 2 + t * t)
p(f'\n== |r| mínimo com p < 0,05 (bilateral), n = {n}: {rc:.3f}')
out['r_critico'] = float(rc)
(PASTA_SAIDA / 'extras.txt').write_text('\n'.join(L) + '\n', encoding='utf-8')
json.dump(out, open(PASTA_SAIDA / 'extras.json', 'w'), indent=1, ensure_ascii=False)
