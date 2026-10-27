
"""
_summary_

Author: Davi Paulino Conceição
Date: 26/10/2026

Projeto: Pipeline em Python voltado para um artigo científico sobre avaliação
automatizada de redações com a API do Gemini, extração de notas por competências
C1–C5 e cálculo de concordância com as avaliações humanas por meio do QWK.

Nome do arquivo: extrair_notas.py

Descrição:
Este script é responsável por extrair e organizar as notas presentes nas
respostas produzidas pelo agente de correção automatizada.

A função extrair() recebe o texto da resposta e procura as notas das cinco
competências da redação (C1, C2, C3, C4 e C5), além da nota total declarada.
As notas válidas das competências pertencem ao conjunto {0, 40, 80, 120, 160, 200}.

Após a extração, o script calcula a soma das competências quando possível e
classifica o resultado com um status. Entre os status estão: "ok", quando as
notas foram extraídas e não há divergência na soma; "soma_diferente", quando
a nota total declarada difere da soma das competências; "incompleto", quando
somente parte das notas foi encontrada; "sem_notas", quando nenhuma nota foi
identificada; e "possivel_anulacao", quando o texto sugere uma possível anulação
sem apresentar notas das competências.

O arquivo pode ser importado por outros scripts, como executar_experimento.py,
ou executado diretamente pela linha de comando para analisar um arquivo de texto.

Abaixo está uma versão de referência reorganizada e comentada, mantida inativa
para consulta futura. Ao final, encontra-se o código original funcional.
"""


# ============================================================================
# VERSÃO DE REFERÊNCIA MELHORADA — INATIVA
# ============================================================================
#
# Esta versão separa algumas responsabilidades em funções auxiliares para
# facilitar a leitura, a manutenção e os testes futuros.
#
# Todo este bloco está comentado intencionalmente. Ele não será executado
# enquanto permanecer assim.
#
# import re
# import sys
# from pathlib import Path
#
#
# # Conjunto de notas permitidas para cada competência.
# NIVEIS_VALIDOS = {0, 40, 80, 120, 160, 200}
#
# # Competências que devem aparecer no resultado final.
# COMPETENCIAS = tuple(f"C{i}" for i in range(1, 6))
#
#
# def localizar_notas_competencias(texto: str) -> dict:
#     """
#     Procura as notas C1 a C5 nas linhas do texto recebido.
#
#     Reconhece linhas que começam com o identificador da competência,
#     mesmo quando há elementos de formatação Markdown antes dele.
#
#     Retorna um dicionário contendo somente as competências encontradas.
#     Cada nota precisa pertencer ao conjunto NIVEIS_VALIDOS.
#     """
#     notas = {}
#
#     # Examina cada linha individualmente para localizar as competências.
#     for linha in texto.splitlines():
#         linha = linha.strip()
#
#         # Identifica o código da competência no começo da linha.
#         correspondencia = re.match(r"^[\s|*#>\-]*C([1-5])\b", linha)
#
#         # Ignora linhas que não identificam uma competência.
#         if not correspondencia:
#             continue
#
#         competencia = f"C{correspondencia.group(1)}"
#
#         # Preserva a primeira nota encontrada para cada competência,
#         # evitando que repetições posteriores sobrescrevam o resultado.
#         if competencia in notas:
#             continue
#
#         # Isola o conteúdo posterior ao identificador da competência.
#         restante = linha[correspondencia.end():]
#
#         # Em tabelas, a nota costuma aparecer depois de uma barra vertical
#         # ou de uma tabulação. Quando não há separador, examina o restante.
#         colunas = re.split(r"\||\t", restante)
#         candidatos = colunas[1:] if len(colunas) > 1 else [restante]
#
#         # Procura um número isolado que corresponda a uma nota válida.
#         for candidato in candidatos:
#             numero = re.search(
#                 r"(?<![\d.,])(\d{1,3})(?![\d.,]*\d)",
#                 candidato
#             )
#
#             # Só aceita valores pertencentes à escala prevista.
#             if numero and int(numero.group(1)) in NIVEIS_VALIDOS:
#                 notas[competencia] = int(numero.group(1))
#                 break
#
#     return notas
#
#
# def localizar_nota_total(texto: str) -> int | None:
#     """
#     Procura a nota total declarada na resposta.
#
#     Primeiro examina o conteúdo da linha que contém "NOTA TOTAL".
#     Se necessário, procura uma nota no formato de pontuação sobre 1.000
#     nas duas linhas seguintes, seguindo a estratégia do código original.
#
#     Retorna um inteiro quando encontra a nota ou None quando não encontra.
#     """
#     linhas = texto.splitlines()
#
#     for indice, linha in enumerate(linhas):
#         correspondencia = re.search(r"NOTA\s+TOTAL", linha, re.I)
#
#         # Ignora linhas sem o rótulo esperado.
#         if not correspondencia:
#             continue
#
#         # Examina primeiro o texto posterior ao rótulo.
#         restante = linha[correspondencia.end():]
#         numero = re.search(r"(\d{1,4})", restante)
#
#         # Se não encontrou número na mesma linha, verifica as próximas duas.
#         if not numero:
#             proximas_linhas = " ".join(linhas[indice + 1:indice + 3])
#             numero = re.search(
#                 r"(\d{1,4})\s*\**\s*/\s*1\.?000",
#                 proximas_linhas
#             )
#
#         # Retorna a primeira nota total encontrada.
#         if numero:
#             return int(numero.group(1))
#
#     return None
#
#
# def determinar_status(
#     texto: str,
#     notas: dict,
#     total_declarado: int | None
# ) -> str:
#     """
#     Classifica o resultado da extração.
#
#     A classificação diferencia extração completa, divergência na soma,
#     possível anulação, ausência de notas e extração incompleta.
#     """
#     todas_encontradas = all(
#         notas.get(competencia) is not None
#         for competencia in COMPETENCIAS
#     )
#
#     # Quando todas as competências foram encontradas, verifica a soma.
#     if todas_encontradas:
#         soma = sum(notas[competencia] for competencia in COMPETENCIAS)
#
#         # A ausência de nota total declarada não impede o status "ok".
#         if total_declarado is None or total_declarado == soma:
#             return "ok"
#
#         return "soma_diferente"
#
#     # Investiga uma possível anulação quando nenhuma competência foi extraída.
#     nenhuma_encontrada = not any(
#         notas.get(competencia) is not None
#         for competencia in COMPETENCIAS
#     )
#
#     if nenhuma_encontrada and re.search(
#         r"anulad|nota\s*0\s*\(",
#         texto,
#         re.I
#     ):
#         return "possivel_anulacao"
#
#     # Nenhuma nota foi localizada e não há indício reconhecido de anulação.
#     if nenhuma_encontrada:
#         return "sem_notas"
#
#     # Pelo menos uma nota foi encontrada, mas faltam outras competências.
#     return "incompleto"
#
#
# def extrair(texto: str) -> dict:
#     """
#     Extrai as notas da resposta e devolve um resultado padronizado.
#
#     O dicionário final contém C1 a C5, total declarado, soma calculada
#     quando aplicável e status da extração.
#     """
#     # Extrai as notas individuais e a nota total declarada.
#     notas_encontradas = localizar_notas_competencias(texto)
#     total_declarado = localizar_nota_total(texto)
#
#     # Garante que todas as competências apareçam no resultado.
#     resultado = {
#         competencia: notas_encontradas.get(competencia)
#         for competencia in COMPETENCIAS
#     }
#
#     # Soma somente os valores encontrados.
#     # A soma só será apresentada como total calculado se a extração estiver
#     # completa e o status for "ok" ou "soma_diferente".
#     soma_parcial = sum(
#         nota for nota in resultado.values()
#         if nota is not None
#     )
#
#     # Classifica a extração conforme as regras definidas acima.
#     status = determinar_status(
#         texto,
#         resultado,
#         total_declarado
#     )
#
#     # Acrescenta os campos complementares esperados pelo pipeline.
#     resultado.update({
#         "total_declarado": total_declarado,
#         "total_somado": (
#             soma_parcial
#             if status in ("ok", "soma_diferente")
#             else None
#         ),
#         "status": status,
#     })
#
#     return resultado
#
#
# if __name__ == "__main__":
#     # Permite analisar um arquivo de texto diretamente pelo terminal.
#     # Exemplo: python3 extrair_notas.py resposta.txt
#     if len(sys.argv) != 2:
#         raise SystemExit(
#             "Uso: python3 extrair_notas.py arquivo_com_resposta.txt"
#         )
#
#     # Lê o arquivo em UTF-8 e exibe o dicionário de notas extraídas.
#     caminho = Path(sys.argv[1])
#     texto = caminho.read_text(encoding="utf-8")
#     print(extrair(texto))


# ============================================================================
# CÓDIGO ORIGINAL FUNCIONAL — MANTIDO
# ============================================================================
#
# O código abaixo é a versão original recebida.
# Ele permanece ativo e preserva a lógica usada pelo projeto.


"""Extrai as notas C1-C5 e a nota total da resposta do agente (tabela em Markdown ou texto com tabulação).

Uso como módulo: from extrair_notas import extrair
Uso na linha de comando: python3 extrair_notas.py arquivo_com_resposta.txt
"""
import re
import sys

NIVEIS = {0, 40, 80, 120, 160, 200}


def extrair(texto: str) -> dict:
    notas = {}
    total = None
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        s = linha.strip()
        m = re.match(r'^[\s|*#>\-]*C([1-5])\b', s)
        if m and m.group(1) not in notas:
            resto = s[m.end():]
            # pula o rótulo ("– Norma culta", ": Tema/Repertório") até a primeira barra, tabulação ou o próprio número
            partes = re.split(r'\||\t', resto)
            candidatos = partes[1:] if len(partes) > 1 else [resto]
            for c in candidatos:
                n = re.search(r'(?<![\d.,])(\d{1,3})(?![\d.,]*\d)', c)
                if n and int(n.group(1)) in NIVEIS:
                    notas['C' + m.group(1)] = int(n.group(1))
                    break
            continue
        if re.search(r'NOTA\s+TOTAL', s, re.I) and total is None:
            resto_t = s[re.search(r'NOTA\s+TOTAL', s, re.I).end():]
            n = re.search(r'(\d{1,4})', resto_t) or re.search(r'(\d{1,4})\s*\**\s*/\s*1\.?000', ' '.join(linhas[i + 1:i + 3]))
            if n:
                total = int(n.group(1))
    out = {f'C{i}': notas.get(f'C{i}') for i in range(1, 6)}
    soma = sum(v for v in out.values() if v is not None)
    if all(v is not None for v in out.values()):
        status = 'ok' if (total is None or total == soma) else 'soma_diferente'
    elif re.search(r'anulad|nota\s*0\s*\(', texto, re.I) and not any(v is not None for v in out.values()):
        status = 'possivel_anulacao'
    elif not any(v is not None for v in out.values()):
        status = 'sem_notas'
    else:
        status = 'incompleto'
    out.update({'total_declarado': total, 'total_somado': soma if status in ('ok', 'soma_diferente') else None, 'status': status})
    return out


if __name__ == '__main__':
    print(extrair(open(sys.argv[1], encoding='utf-8').read()))
