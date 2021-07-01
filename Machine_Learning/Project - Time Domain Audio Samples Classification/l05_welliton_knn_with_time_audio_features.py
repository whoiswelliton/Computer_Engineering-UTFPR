# -*- coding: utf-8 -*-
"""L05 Welliton - KNN with Time Audio Features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1THyHhrvgkGnNdoTOdrDm7I3JMIiazjz4
"""

import os
import random
import librosa
import scipy
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from mlxtend.plotting import plot_decision_regions
from scipy.linalg import norm

#visualização
import seaborn
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

"""# **Dataset e Pré-Processamento**"""

df_audio = pd.read_csv('/content/drive/My Drive/Audio Dataset/timeaudiofeatures1.csv')

df_audio.shape

df_audio[95:105]

"""CLASSES:
- Kick = 0
- Snare = 1
- Clap = 2
- Tom = 3
- Closed Hihat = 4

TIPOS DE FEATURES:
1. *Valores Discretos* = **Zero-Crossing Rate**, Número de vezes que o sinal atravessa o valor zero por causa de uma oscilação

2. *Valores Contínuos* = **Root-Mean Square**, Valores médios de um sinal

3. *Valores Contínuos* = **Amplitude Envelope**, Valores máximos que representam os picos do sinal

4. *Valores Categóricos Ordinais* = **Low = 0 | Mid = 0.5 | High = 1**, Localização e faixa de alcance no domínio da frequência

5. *Valores Categóricos Ordinais* = **Fast = 0 | Slow = 1**, parâmetro que avalia o quão rápido o sinal decai  

6. *Valores Categóricos Nominais* = **Synthesized = 0 | Acoustic = 0.5 | Natural = 1**, Fonte sonora proveniente, se foi sintetizada, gerado de um instrumento ou uma fonte natural

**- CONVERTENDO CLASSES & VARIÁVEIS CATEGÓRICAS ORDINAIS**
"""

df_mod = df_audio

f = {'Low': 0, 'Mid': 1, 'High': 2}
t = {'Slow': 0, 'Fast': 1}
c = {'KICK': 0, 'SNARE': 1, 'CLAP': 2, 'TOM': 3, 'CLS HIHAT': 4}

df_mod['FREQ. RANGE'] = df_mod['FREQ. RANGE'].map(f)
df_mod['TIME DECAY'] = df_mod['TIME DECAY'].map(t)
df_mod['CLASS'] = df_mod['CLASS'].map(c)

df_mod[295:305]

"""**- CONVERTENDO VARIÁVEIS CATEGÓRICAS NOMINAIS (One-Hot Encoding)**"""

pd.get_dummies(df_mod)

"""Eliminando uma das colunas para evitar redundância"""

df_mod2 = pd.get_dummies(df_mod, drop_first=True)

df_mod2

"""Colocando a coluna das labels por último """

df_mod2.columns

new_colums = ['AMP', 'RMS', 'ZCR', 'FREQ. RANGE', 'TIME DECAY','SOURCE_Natural', 'SOURCE_Synthesized', 'CLASS']

df_mod2 = df_mod2[new_colums]

df_mod2

"""**- LIDANDO COM DADOS FALTANTES**"""

df_mod2[346:347]

#Eliminando linhas com valores faltantes
df_mod2 = df_mod2.dropna(axis=0)

#imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
#df_mod3 = df_mod2.values
#df_mod3 = imputer.fit_transform(df_mod2.values)
#df_mod3

"""# **KNN (k-Nearest Neighbor Model)**

Separando em array de Features (X) e array Classes (y), transformando de tabela para matriz
"""

X = df_mod2.iloc[:, 0:7].values
X[0:5]

y = df_mod2['CLASS'].values
y

audio_all =  pd.DataFrame(df_mod2)
audio_data = pd.DataFrame(X)
audio_labels = pd.DataFrame(y)
audio_data.to_csv('/content/drive/My Drive/Audio Dataset/audio_data.csv', index = False,header=["AMP", "RMS", "ZCR", "FREQ. RANGE", "TIME DECAY", "SOURCE_Natural","SOURCE_Synthesized"])
audio_labels.to_csv('/content/drive/My Drive/Audio Dataset/audio_labels.csv', index = False,header=["CLASS"])
audio_all.to_csv('/content/drive/My Drive/Audio Dataset/audio_all.csv', index = False)

"""Separando Base de Treino e Base de Teste"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, shuffle=True, random_state=123, stratify=y)
np.bincount(y_train)

print(X_train.size, X_test.size, y_train.size, y_test.size)

""" Normalização das Features de Treino"""

scaler = StandardScaler()
scaler.fit(X_train)
X_train_std = scaler.transform(X_train)
scaler.fit(X_test)
X_test_std = scaler.transform(X_test)
X_train_std

"""Visualizando os a Base de Treino Normalizada"""

plt.figure(figsize=(15, 10))

plt.scatter(X_train_std[y_train == 0, 0],
            X_train_std[y_train == 0, 1],
            marker='o',
            label='class 1 (Kicks)')

plt.scatter(X_train_std[y_train == 1, 0],
            X_train_std[y_train == 1, 1],
            marker='^',
            label='class 2 (Snares)')

plt.scatter(X_train_std[y_train == 2, 0],
            X_train_std[y_train == 2, 1],
            marker='s',
            label='Class 3 (Claps)')
plt.scatter(X_train_std[y_train == 3, 0],
            X_train_std[y_train == 3, 1],
            marker='X',
            label='Class 4 (Toms)')
plt.scatter(X_train_std[y_train == 4, 0],
            X_train_std[y_train == 4, 1],
            marker='p',
            label='Class 5 (Closed Hihats)')

plt.xlim((-1.5, 4.5))
plt.ylim((-1.5, 4.5))
plt.legend(loc='upper right')
plt.show()

"""Treinando o modelo"""

knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train_std, y_train)

"""Fazendo a avaliação"""

y_pred = knn_model.predict(X_test_std)
print(y_pred)
print(y_test)

accuracy_score(y_test, y_pred)