
"""
Autor: Davi Paulino Conceição
Data: 26/10/2026
Projeto: Análise de redações com modelos de inteligência artificial.

Descrição:
    Consulta os modelos disponibilizados pela API do Google Gemini
    para a chave de API configurada no ambiente.

    O script percorre os modelos retornados pela API e exibe somente
    aqueles que possuem suporte à ação generateContent.

    Para cada modelo compatível, apresenta:
        - Nome técnico do modelo, utilizado nas chamadas à API;
        - Nome de exibição, quando disponibilizado.

Dependências:
    - Biblioteca google-genai;
    - Variável de ambiente GEMINI_API_KEY configurada com uma chave válida.

Objetivo:
    Facilitar a identificação do nome exato dos modelos disponíveis,
    permitindo selecionar um modelo para utilização nos experimentos.

Segurança:
    A chave da API deve ser mantida em uma variável de ambiente.
    Não insira credenciais diretamente no código nem as publique.
"""

# ============================================================================
# VERSÃO DE REFERÊNCIA — DOCUMENTAÇÃO DO FUNCIONAMENTO
#
# Esta seção é exclusivamente explicativa.
# Todas as linhas estão comentadas e não são executadas.
# O código original ativo está preservado no final do arquivo.
# ============================================================================

# # 1. Importar o cliente da biblioteca oficial Google Gen AI.
# # Esse cliente permite interagir com os serviços de inteligência
# # artificial disponibilizados pelo Google.
#
# # from google import genai
#
# # 2. Inicializar o cliente da API.
# # Por padrão, o cliente procura a chave de autenticação na variável
# # de ambiente GEMINI_API_KEY.
# # A chave não precisa ser escrita diretamente no código.
#
# # client = genai.Client()
#
# # 3. Consultar os modelos disponíveis para o cliente.
# # A operação models.list() retorna os modelos que a API disponibiliza
# # para a chave e o contexto de acesso utilizados.
#
# # modelos = client.models.list()
#
# # 4. Percorrer os modelos retornados.
# # Cada elemento representa um modelo disponibilizado pela API.
#
# # for modelo in modelos:
#
# #     # 5. Obter as ações suportadas pelo modelo.
# #     # getattr permite consultar o atributo supported_actions
# #     # sem provocar erro caso ele não esteja presente.
# #     # Se o atributo estiver ausente ou for vazio, utiliza-se
# #     # uma lista vazia como alternativa.
#
# #     acoes = getattr(modelo, "supported_actions", None) or []
#
# #     # 6. Filtrar os modelos que aceitam geração de conteúdo.
# #     # Somente modelos que contenham generateContent na lista
# #     # de ações suportadas serão exibidos.
#
# #     if "generateContent" in acoes:
#
# #         # 7. Mostrar o nome técnico e o nome de exibição.
# #         # O nome técnico pode ser utilizado para identificar o modelo
# #         # em chamadas posteriores à API.
# #         # O nome de exibição é consultado de forma segura:
# #         # se não estiver disponível, será exibida uma string vazia.
#
# #         print(
# #             modelo.name,
# #             "|",
# #             getattr(modelo, "display_name", "")
# #         )
#
# # 8. Resultado esperado.
# # O terminal apresenta uma linha para cada modelo compatível,
# # no formato:
# #
# # nome_tecnico_do_modelo | Nome de exibição
# #
# # A lista depende dos modelos disponibilizados pela API no momento
# # da execução e das permissões associadas à chave utilizada.

# ============================================================================
# CÓDIGO ORIGINAL — ATIVO
#
# Preservado sem alterações em relação ao arquivo recebido.
# ============================================================================

"""Lista os modelos que a sua chave da API enxerga (copie o código exato do modelo escolhido)."""
from google import genai

client = genai.Client()  # lê a chave da variável de ambiente GEMINI_API_KEY
for m in client.models.list():
    acoes = getattr(m, "supported_actions", None) or []
    if "generateContent" in acoes:
        print(m.name, "|", getattr(m, "display_name", ""))










"""Lista os modelos que a sua chave da API enxerga (copie o código exato do modelo escolhido)."""
from google import genai

client = genai.Client()  # lê a chave da variável de ambiente GEMINI_API_KEY
for m in client.models.list():
    acoes = getattr(m, "supported_actions", None) or []
    if "generateContent" in acoes:
        print(m.name, "|", getattr(m, "display_name", ""))
