# -*- coding: utf-8 -*-
"""L12 Welliton - Decision Trees.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DBfaMNX4wkCZYVDk126R9jbGfw0DPqsS
"""

import scipy as sp
import numpy as np
import pandas as pd
import pylab as py 
import sklearn

from sklearn.tree import plot_tree
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
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

X = audioft_nmb.iloc[:,0:5].values
y = audioft_nmb['CLASS'].values

"""# **PIPELINE**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=123, stratify=y)

print('Labels counts in y:', np.bincount(y))
print('Labels counts in y_train:', np.bincount(y_train))
print('Labels counts in y_test:', np.bincount(y_test))

pipe = Pipeline([('z-score', StandardScaler()), 
                 ('reduce_dim', PCA(n_components=5)), 
                 ('classify', DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=0))])

pipe.fit(X_train, y_train)

y_test_pred = pipe.predict(X_test)
accuracy_score(y_test, y_test_pred)

"""# **GRID-SEARCH**"""

clf = DecisionTreeClassifier(criterion='entropy', random_state=0)

param_grid = {
 'reduce_dim__n_components': [1, 2, 3, 4, 5],
 'classify__max_depth': [1, 2, 3, 4, 5],
 'classify__min_samples_leaf': [1, 2, 3, 4, 5],
 'classify__ccp_alpha': clf.cost_complexity_pruning_path(X_train, y_train).ccp_alphas
}

grid = GridSearchCV(pipe, cv=2, n_jobs=1, param_grid=param_grid, scoring='accuracy')

grid.fit(X_train, y_train)

print(grid.cv_results_)

grid.cv_results_['mean_test_score']

"""- **Melhores Parâmetros**"""

print(grid.best_score_)
print(grid.best_params_)

clf = grid.best_estimator_

y_test_pred = clf.predict(X_test)
accuracy_score(y_test, y_test_pred)

"""- **Árvore de Decisão**"""

class_names=['KICK','SNARE','CLAP','TOM','CLS_HIHAT']
feature_names = audioft_nmb.columns

feature_names = feature_names.drop('CLASS')
feature_names = feature_names.drop('SOURCE_Natural')
feature_names = feature_names.drop('SOURCE_Synthesized')

plt.figure(figsize=(50,25))
clf2 = DecisionTreeClassifier(ccp_alpha=0.0, max_depth=5, min_samples_leaf=2)
clf2.fit(X_train,y_train)
plot_tree(clf2, filled=True, rounded=True, class_names=class_names, feature_names=feature_names)

plt.tight_layout()
plt.savefig('/content/drive/My Drive/Audio Dataset/Arvore.JPEG')

plt.show()

"""# **VERIFICAÇÃO E INTERPRETAÇÃO**"""

print(np.shape(X_test))
print(np.shape(y_test))

X_test1 = X_test[5,:]
y_test1 = y_test[5]

print(np.shape(X_test1))
print(np.shape(y_test1))

X_test1 = np.reshape(X_test1,(1,-1))
y_test1 = np.reshape(y_test1,(1))

print(np.shape(X_test1))
print(np.shape(y_test1))

y_test1_pred  = clf.predict(X_test1)
y_test1_pred

accuracy_score(y_test1, y_test1_pred)

X_test1

class_names[int(y_test1_pred)]

print('Name Class : ' + class_names[int(y_test1)])
print('Feature values: ')
for index, feature_name in enumerate(feature_names):
 print('{feature}:{value}'.format(feature = feature_name, value = X_test1[0][index]))

"""Analisando as condições da árvore para que seja identificado um sample da Classe "TOM", há 2 séries de condições em que há possibilidade da classificação ser alcançada, sendo uma delas a que contém a grande maioria das amostras, que foi o caso que satisfez e classificou nossa amostra particular de teste. 

**OPÇÃO 1 = 58 AMOSTRAS**

**OPÇÃO 2 = 9 AMOSTRAS**

**CONDIÇÂO:**

*Se*

- *(FREQ. RANGE <= 1.5) = TRUE*

- *(FREQ. RANGE <= 0.5) = TRUE*
 
- *(RMS <= 0.141) = TRUE*

- *(ZCR <= 83) = FALSE*

*Então*
- *class = 'TOM'*
"""