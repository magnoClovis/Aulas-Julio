# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 00:20:32 2022

@author: clovi
"""

import math 

def process_thread(x, y, params): 
  '''
  y: nível do tanque em um tempo t especifico (variável dependente)
  params: dicionario com os valores das demais constantes da formula
  '''

  nivel_tanque = y
  coef_descarga = params['coef_descarga']
  raio_topo = params['raio_topo']
  raio_base = params['raio_base']
  altura = params['altura']
  fluxo_entrada = x

  vazao = coef_descarga*math.sqrt(nivel_tanque)
  alfa = (raio_topo - raio_base) / altura
  denom = math.pi*(raio_base + ( alfa * nivel_tanque))**2
  h_linha = (fluxo_entrada-vazao)/denom

  return h_linha


def softPLC_thread(x, y, params, href = 0):
    altura = params['altura']
    if href == 0:
        href = altura*0.95
    
    if y[-1] > href*0.95:
      x = 0
    elif y[-1] < href*0.80:
      x = params['fluxo_entrada']
    
    return x


def rungeKutta(f, x, y, d, params, tempo, href = 0):
  '''
  f: função que será integrada
  x: tempo (no nosso caso o parametro x não tem muita importancia)
  y: lista onde serão armazenados os valores do nível do tanque a cada tempo t
  d: frequencia de atualização dos valores na lista 
  params: parametros da função a ser integrada (definição de suas constantes)
  tempo: tempo total de observação
  '''
  x = params['fluxo_entrada']
  var = []
  for t in range(len(tempo)-1):
      if t%2 == 0:
        x = softPLC_thread(x, y, params, href)
      f1 = d * f(x, y[t], params) 
      f2 = d * f((x + (d / 2)), y[t] + (f1 / 2), params) 
      f3 = d * f((x + (d / 2)), y[t] + (f2 / 2) , params) 
      f4 = d * f(x+d, y[t]+f3, params)  
      y.append(y[t] + (f1 + 2*f2 + 2*f3 + f4)/6)
      var.append((y[-1],x,params['coef_descarga']))

  return y, var


'''
params = {"coef_descarga": 1, "nivel_tanque": 0, "raio_topo": 2, "raio_base": 0.5, "altura": 3, "fluxo_entrada": 2.3}


f = lambda x, y, params: process_thread(x, y, params) # lambda expression para poder simplificar e generalizar a equação principal de modo que possa ser usada dentro de rungeKutta
y = [0] # o primeiro valor de y é o nível inicial, no nosso caso vamos usar o exemplo de antes e adotar o nível inicial como sendo 0.7m
x = params['fluxo_entrada']
freq = 10
d = 1/freq
tempo_total = int(50/d)
tempo = [t for t in range(tempo_total)]
tempo = [t*d for t in tempo] # coloca o valor real do tempo em segundos 
Y, var = rungeKutta(f=f, x=x, d=d, y=y, params=params, tempo=tempo)

'''