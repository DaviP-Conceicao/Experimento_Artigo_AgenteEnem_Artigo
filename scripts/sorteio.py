# Script de amostragem das 100 redações (semente 42), reproduzido do arquivo de notas do autor.
# Uso: copie para a pasta do Essay-BR clonado (a que contém essay-br/splits/testing.csv) e rode: python3 sorteio.py
# Saída: ../amostra_100.csv (contém o texto das redações; não vai para o repositório)
import ast
import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42
df = pd.read_csv('essay-br/splits/testing.csv',
                 converters={'essay': ast.literal_eval, 'competence': ast.literal_eval})
faixa = pd.qcut(df['score'], q=4, duplicates='drop')
_, amostra = train_test_split(df, test_size=100, stratify=faixa, random_state=SEED)
amostra = amostra.reset_index().rename(columns={'index': 'id_teste'})
amostra['texto'] = amostra['essay'].apply(lambda p: '\n'.join(p))
notas = pd.DataFrame(amostra['competence'].tolist(), index=amostra.index)
amostra[['C1', 'C2', 'C3', 'C4', 'C5']] = notas
amostra = amostra.drop(columns=['essay', 'competence'])
amostra.to_csv('../amostra_100.csv', index=False)
print(len(amostra), amostra['prompt'].nunique(), 'temas distintos')
print(amostra['score'].describe())
