# -*- coding: utf-8 -*-
"""L11 Welliton - Model Selection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C00BVIO5VkumTX4OfZshhbc2oVQcgKxH
"""

import scipy as sp
import numpy as np
import pandas as pd
import pylab as py 
import sklearn

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

#visualização
import seaborn as sns
import IPython.display as ipd
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions
from mlxtend.plotting import scatterplotmatrix

from google.colab import drive
drive.mount('/content/drive')

audioft_str = pd.read_csv('/content/drive/My Drive/Audio Dataset/audioft_cleanStr.csv')
audioft_nmb = pd.read_csv('/content/drive/My Drive/Audio Dataset/audioft_cleanNmb.csv')

X = audioft_nmb.iloc[:,0:7].values
y = audioft_nmb['CLASS'].values

"""# **PIPELINE**

1. Pre-processing

Já feito nos trabalhos anteriores.

2. Transformação/Conversão dos dados

Já feito nos trabalhos anteriores.
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=1, stratify=y)

print(X_train.size, X_test.size, y_train.size, y_test.size)

"""3. Normalização"""

scaler = StandardScaler()

scaler.fit(X_train)
X_train_std = scaler.transform(X_train)

scaler.fit(X_test)
X_test_std = scaler.transform(X_test)

"""4. Redução de Dimensionalidade & Classificador"""

pipe = Pipeline([('z-score', StandardScaler()), ('reduce_dim', PCA(n_components=3)), ('classify', KNeighborsClassifier(n_neighbors=1))])

pipe.fit(X_train_std, y_train)

y_train_pred = pipe.predict(X_train_std)
accuracy_score(y_train, y_train_pred)

y_test_pred = pipe.predict(X_test_std)
accuracy_score(y_test, y_test_pred)

"""# **GRID-SEARCH**"""

param_grid = {'reduce_dim__n_components': [1, 2, 3, 4], 'classify__n_neighbors': [2, 3, 4, 5]}

grid = GridSearchCV(pipe, cv=2, n_jobs=1, param_grid=param_grid, scoring='accuracy')

grid.fit(X_train_std, y_train)

print(grid.cv_results_)

grid.cv_results_['mean_test_score']

"""Exibindo parâmetros ideias encontrados a partir do melhor Score obtido"""

print(grid.best_score_)
print(grid.best_params_)

clf = grid.best_estimator_

y_test_pred = clf.predict(X_test_std)
accuracy_score(y_test, y_test_pred)