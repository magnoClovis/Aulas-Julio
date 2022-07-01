# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 01:27:25 2022

@author: clovi
"""

import socket
import time
import tanque


def system(i,href):
    params = {"coef_descarga": 1, "nivel_tanque": 0, "raio_topo": 2, "raio_base": 0.5, "altura": 3, "fluxo_entrada": 2.3}
    
    f = lambda x, y, params: tanque.process_thread(x, y, params) # lambda expression para poder simplificar e generalizar a equação principal de modo que possa ser usada dentro de rungeKutta
    y = [0] # o primeiro valor de y é o nível inicial, no nosso caso vamos usar o exemplo de antes e adotar o nível inicial como sendo 0.7m
    x = params['fluxo_entrada']
    freq = 10
    d = 1/freq
    tempo_total = int(i/d)
    tempo = [t for t in range(tempo_total)]
    tempo = [t*d for t in tempo] # coloca o valor real do tempo em segundos 
    Y, var = tanque.rungeKutta(f=f, x=x, d=d, y=y, params=params, tempo=tempo, href=href)
    
    return Y, var


s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 60000))
s.listen(5)

i = 1

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    #href = s.recv(1024)
    #href = href.decode()
    #href = float(href)
    Y, var = system(i,2)
    clientsocket.send(bytes(f"\nNivel: {str(round(var[i][0],2))}\tFluxo de Entrada: {str(var[i][1])}\tFluxo de saida: {str(var[i][2])}", "utf-8"))  
    i+=1
    time.sleep(1)
    clientsocket.close()
      