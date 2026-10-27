

"""
Autor: Davi Paulino Conceição
Data: 26/10/2026
Projeto: Análise de concordância entre avaliações humanas e avaliações
         automatizadas por agentes de IA.

Descrição:
    Gera gráficos para visualizar os resultados da avaliação automatizada
    de redações, comparando as condições A e B com as notas humanas.

    Figura 1 — Concordância por competência:
        Apresenta o QWK (Kappa ponderado quadrático) das competências C1
        a C5 e da nota total, incluindo intervalos de confiança de 95%,
        comparação entre as condições A e B e faixas de interpretação.

    Figura 2 — Viés por quartil:
        Apresenta a diferença entre as notas atribuídas pelo agente e
        as notas humanas, agrupadas em quartis da nota humana.

    Entrada:
        Arquivo resultados_metricas.json, contendo as métricas calculadas
        anteriormente pelo pipeline de análise.

    Saídas:
        fig_qwk.png
        fig_vies_quartil.png

Observações:
    A versão original utilizava um caminho absoluto para localizar o JSON; no repositório,
    o caminho é relativo a este arquivo (../analise/saida/). Rode de dentro de graficos/:
    os gráficos PNG são salvos no diretório de trabalho atual.
    O arquivo JSON precisa conter todas as chaves utilizadas pelo script.
"""

# ============================================================================
# VERSÃO DE REFERÊNCIA — DOCUMENTAÇÃO DO FUNCIONAMENTO
#
# Esta seção é exclusivamente para consulta.
# Todas as linhas estão comentadas e não são executadas.
#
# A versão abaixo descreve a organização lógica do script original.
# O código funcional preservado encontra-se no final deste arquivo.
# ============================================================================

# # 1. Importar as bibliotecas necessárias.
# # json permite carregar as métricas armazenadas em formato JSON.
# # numpy permite organizar os valores em arrays numéricos.
# # matplotlib gera os gráficos e salva as figuras em arquivos PNG.
# # FuncFormatter permite personalizar a apresentação dos números nos eixos.
#
# # import json
# # import numpy as np
# # import matplotlib
#
# # 2. Selecionar um backend sem interface gráfica.
# # O backend Agg permite gerar imagens sem abrir uma janela de gráfico.
#
# # matplotlib.use('Agg')
#
# # 3. Importar os módulos de visualização.
#
# # import matplotlib.pyplot as plt
# # from matplotlib.ticker import FuncFormatter
#
# # 4. Definir o caminho do arquivo de resultados.
# # O caminho deve apontar para o diretório que contém
# # resultados_metricas.json.
#
# # SAIDA = '/caminho/para/o/diretorio/saida/'
#
# # 5. Carregar as métricas produzidas pela etapa anterior.
# # O dicionário J armazena os resultados que serão consultados
# # durante a construção dos gráficos.
#
# # with open(SAIDA + 'resultados_metricas.json',
# #           'r', encoding='utf-8') as arquivo:
# #     J = json.load(arquivo)
#
# # 6. Configurar a aparência dos gráficos.
# # As cores identificam as condições A e B.
# # As demais configurações controlam fontes, eixos e grade.
#
# # CA = '#2F6DB5'
# # CB = '#E07B39'
# # INK = '#2B2B2B'
# # GRID = '#E4E4E4'
#
# # 7. Configurar a formatação decimal.
# # A função substitui o ponto decimal por vírgula nos rótulos do eixo.
#
# # virg = FuncFormatter(
# #     lambda valor, _: f'{valor:.1f}'.replace('.', ',')
# # )
#
# # 8. Definir as categorias avaliadas.
# # A lista inclui as cinco competências e a nota total.
#
# # K = ['C1', 'C2', 'C3', 'C4', 'C5', 'Total']
#
# # --------------------------------------------------------------------------
# # FIGURA 1 — QWK POR COMPETÊNCIA
# # --------------------------------------------------------------------------
#
# # 9. Criar a figura e definir as posições das categorias.
#
# # fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=200)
# # x = np.arange(len(K))
# # w = 0.17
#
# # 10. Adicionar faixas de fundo para contextualizar os valores de QWK.
#
# # ax.axhspan(0.21, 0.40, color='#F3F3F3', zorder=0)
# # ax.axhspan(0.41, 0.60, color='#E6EEF8', zorder=0)
#
# # 11. Para cada condição, consultar a média do QWK e os limites
# # inferior e superior do intervalo de confiança de 95%.
#
# # Para a condição A:
# #     consultar as chaves no formato A|competência|qwk
# #
# # Para a condição B:
# #     consultar as chaves no formato B|competência|qwk
# #
# # A estrutura esperada para cada resultado inclui:
# #     media — valor médio do QWK;
# #     ic    — limites inferior e superior do intervalo de confiança.
#
# # 12. Desenhar os pontos e as barras de erro.
# # As barras representam os intervalos de confiança.
# # Os valores numéricos são apresentados próximos aos pontos.
#
# # 13. Configurar os eixos, a legenda e a grade.
# # O eixo horizontal contém C1, C2, C3, C4, C5 e Total.
# # O eixo vertical representa o QWK.
#
# # 14. Adicionar uma anotação para a diferença da competência C4.
# # O script utiliza a chave dif|C4|qwk para representar a diferença
# # entre as condições B e A, com o valor indicado no gráfico.
#
# # 15. Salvar a primeira figura como fig_qwk.png e liberar a memória
# # associada à figura com plt.close(fig).
#
# # --------------------------------------------------------------------------
# # FIGURA 2 — VIÉS DA NOTA TOTAL POR QUARTIL DA NOTA HUMANA
# # --------------------------------------------------------------------------
#
# # 16. Definir os valores de viés usados no gráfico.
# # Esses valores estão explicitamente definidos no script original.
# # qa representa a condição A e qb representa a condição B.
#
# # qa = [18.7, -90.6, -109.4, -215.5]
# # qb = [13.3, -105.0, -105.0, -233.6]
#
# # 17. Identificar os quatro quartis.
# # Q1 representa as notas humanas mais baixas.
# # Q4 representa as notas humanas mais altas.
#
# # 18. Criar a figura e desenhar barras para cada condição.
# # Os valores positivos indicam que o agente atribuiu nota superior
# # à humana; valores negativos indicam nota inferior à humana.
#
# # 19. Adicionar os rótulos numéricos às barras.
# # A formatação utiliza vírgula decimal e sinal negativo tipográfico.
#
# # 20. Configurar os eixos e a linha de referência em zero.
# # O eixo vertical representa o viés da nota total, em pontos.
# # O eixo horizontal apresenta os quartis da nota humana.
#
# # 21. Adicionar legenda, grade e título explicativo.
#
# # 22. Salvar a segunda figura como fig_vies_quartil.png e liberar
# # a memória associada à figura.
#
# # 23. Exibir a mensagem 'ok' quando o script chegar ao final.
#
# ============================================================================
# CÓDIGO ORIGINAL — ATIVO
#
# A partir daqui, o código original foi preservado sem alterações.
# ============================================================================

import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path
SAIDA=str(Path(__file__).resolve().parent.parent/'analise'/'saida')+'/'  # no repositório: ../analise/saida/
J=json.load(open(SAIDA+'resultados_metricas.json'))
CA, CB, INK, GRID = '#2F6DB5', '#E07B39', '#2B2B2B', '#E4E4E4'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.edgecolor':'#9A9A9A','axes.labelcolor':INK,
    'xtick.color':INK,'ytick.color':INK,'axes.spines.top':False,'axes.spines.right':False})
virg = FuncFormatter(lambda v,_: f'{v:.1f}'.replace('.',','))
K=['C1','C2','C3','C4','C5','Total']

# --- Figura 1: QWK por competência, A e B, com IC95% e faixas de Altman
fig,ax=plt.subplots(figsize=(7.4,4.3),dpi=200)
x=np.arange(len(K)); w=0.17
ax.axhspan(0.21,0.40,color='#F3F3F3',zorder=0); ax.axhspan(0.41,0.60,color='#E6EEF8',zorder=0)
ax.text(6.2,0.26,'razoável',ha='right',va='center',fontsize=9,color='#777'); ax.text(6.2,0.57,'moderada',ha='right',va='center',fontsize=9,color='#4F76A8')
for c,col,off,lab in (('A',CA,-w,'Condição A'),('B',CB,w,'Condição B')):
    m=np.array([J[f'{c}|{k}|qwk']['media'] for k in K]); lo=np.array([J[f'{c}|{k}|qwk']['ic'][0] for k in K]); hi=np.array([J[f'{c}|{k}|qwk']['ic'][1] for k in K])
    ax.errorbar(x+off,m,yerr=[m-lo,hi-m],fmt='o',color=col,ms=7,capsize=4,lw=1.8,label=lab,zorder=3)
    for xi,mi in zip(x+off,m): ax.text(xi+(-0.07 if c=='A' else 0.07),mi,f'{mi:.3f}'.replace('.',','),ha='right' if c=='A' else 'left',va='center',fontsize=8,color=col)
ax.set_xticks(x); ax.set_xticklabels(K); ax.set_ylim(0,0.7); ax.set_xlim(-0.6,6.25)
ax.yaxis.set_major_formatter(virg); ax.set_ylabel('QWK (IC95% por bootstrap)'); ax.grid(axis='y',color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True)
d=J['dif|C4|qwk']; ax.annotate('Único IC da diferença\nB − A fora de zero\n(−0,068)',xy=(3+w,0.243),xytext=(1.55,0.075),fontsize=8.5,color=INK,arrowprops=dict(arrowstyle='-',color='#999',lw=0.8),ha='left',va='center')
ax.legend(loc='upper left',frameon=False,ncol=2,bbox_to_anchor=(0,1.02))
ax.set_title('Concordância com as notas humanas (QWK)',loc='left',fontsize=12.5,fontweight='bold',color=INK,pad=26)
fig.tight_layout(); fig.savefig('fig_qwk.png'); plt.close(fig)

# --- Figura 2: viés da nota total por quartil da nota humana
qa=[18.7,-90.6,-109.4,-215.5]; qb=[13.3,-105.0,-105.0,-233.6]; nomes=['Q1\nmais baixas','Q2','Q3','Q4\nmais altas']
fig,ax=plt.subplots(figsize=(7.4,4.2),dpi=200); x=np.arange(4); w=0.36
for vals,col,off,lab in ((qa,CA,-w/2,'Condição A'),(qb,CB,w/2,'Condição B')):
    b=ax.bar(x+off,vals,w,color=col,label=lab,zorder=3)
    for xi,v in zip(x+off,vals): ax.text(xi,v+(7 if v>0 else -7),f'{v:+.1f}'.replace('.',',').replace('-','−'),ha='center',va='bottom' if v>0 else 'top',fontsize=9,color=col)
ax.axhline(0,color=INK,lw=1); ax.set_xticks(x); ax.set_xticklabels(nomes); ax.set_ylim(-275,60)
ax.set_ylabel('Viés da nota total (agente − humano, pontos)'); ax.set_xlabel('Quartil da nota humana (n = 25, 24, 24 e 25)')
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f'{v:.0f}'.replace('-','−'))); ax.grid(axis='y',color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True)
ax.legend(loc='lower left',frameon=False); ax.set_title('O agente subestima mais as redações\nque os humanos pontuaram melhor',loc='left',fontsize=12.5,fontweight='bold',color=INK)
fig.tight_layout(); fig.savefig('fig_vies_quartil.png'); plt.close(fig)
print('ok')


