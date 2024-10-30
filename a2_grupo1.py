# -*- coding: utf-8 -*-
"""A2_Grupo1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16jQ3B-3EoQlhV1fBfyrFuKYcl5NrXHEI

# Integrantes do Grupo 1
### Enzo Neves
### Gabriel Alberto
### Gabriela Beatriz
### Pedro Artur
### Sabrina Menezes
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.compat import lzip
!pip install openpyxl

from os import rename
url = 'https://github.com/user-attachments/files/17535133/base.3.xlsx'
dados = pd.read_excel(url, engine='openpyxl')
dados = dados.rename(columns={'LN (PL)': 'LNPL'})
dados['NPL2'] = dados['NPL']** 2
dados.head()

colunas_com_faltantes = dados.columns[dados.isnull().any()].tolist()
print(colunas_com_faltantes)

from sklearn.impute import SimpleImputer

# Convert 'CAR' column to numeric, replacing non-numeric values with NaN
dados['CAR'] = pd.to_numeric(dados['CAR'], errors='coerce')

# Imputação com a média
imputer = SimpleImputer(strategy='mean')
dados['CAR'] = imputer.fit_transform(dados[['CAR']])
dados['NPM'] = imputer.fit_transform(dados[['NPM']])
dados['ROA'] = imputer.fit_transform(dados[['ROA']])
dados['ROE'] = imputer.fit_transform(dados[['ROE']])
dados['OEE'] = imputer.fit_transform(dados[['OEE']])

formula = 'CAR ~ ROA + ROE + OEE + NPL + GAP + LNPL'
results1 = smf.ols(formula, dados).fit()
print(results1.summary())
y_fitted = results1.fittedvalues
residuals1 = results1.resid

"""Tarefa 2"""

formula = 'CAR ~ ROA + ROE + OEE + NPL + GAP + LNPL + NPL2'
results2 = smf.ols(formula, dados).fit()
print(results2.summary())
y_fitted = results2.fittedvalues
residuals2 = results2.resid

def derivada_car_npl(npl):
  return 0.0178 + 2 * 0.9109 * npl

# Calculate critical NPL and second derivative outside the function
npl_critico = -0.0178 / (2 * 0.9109)
segunda_derivada = 2 * 0.9109

print(f"Ponto crítico (NPL): {npl_critico}")
print(f"Segunda derivada: {segunda_derivada}")

if segunda_derivada > 0:
  print("O ponto crítico é um ponto de mínimo.")
else:
  print("O ponto crítico é um ponto de máximo.")

"""TAREFA 3"""

dados['Banco'] = dados['Banco'].apply(lambda x: 1 if x in ['CAIXA ECONÔMICA FEDERAL - PRUDENCIAL','BB - PRUDENCIAL', 'BANRISUL - PRUDENCIAL','BANESTES - PRUDENCIAL','BCO DA AMAZONIA S.A. - PRUDENCIAL','BCO DO NORDESTE DO BRASIL S.A. - PRUDENCIAL'] else 0)

print(dados.head())

formula = 'CAR ~ ROA + ROE + OEE + NPL + GAP + LNPL + NPL2 + Banco'
results3 = smf.ols(formula, dados).fit()
print(results3.summary())
y_fitted = results3.fittedvalues
residuals3 = results3.resid

"""TAREFA 4

Resultados tarefa 1
"""

plt.figure(1)
plt.plot(results1.resid)
plt.xlabel('Data')
plt.ylabel('Resíduos')
plt.grid(True)
plt.show()

name1 = ['Lagrange multiplier statistic', 'p-value']
test1 = sms.het_breuschpagan(results1.resid, results1.model.exog)
lzip(name1, test1)

"""Resultados tarefa 2"""

plt.figure(1)
plt.plot(results2.resid)
plt.xlabel('Data')
plt.ylabel('Resíduos')
plt.grid(True)
plt.show()

name2 = ['Lagrange multiplier statistic', 'p-value']
test2 = sms.het_breuschpagan(results2.resid, results2.model.exog)
lzip(name2, test2)

"""Resultados tarefa 3"""

plt.figure(1)
plt.plot(results3.resid)
plt.xlabel('Data')
plt.ylabel('Resíduos')
plt.grid(True)
plt.show()

name3 = ['Lagrange multiplier statistic', 'p-value']
test3 = sms.het_breuschpagan(results3.resid, results3.model.exog)
lzip(name3, test3)