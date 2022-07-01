# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 01:27:27 2022

@author: clovi
"""

import socket
import os
import sys

def controle():
    s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(),65432))
    
    if not os.path.exists("historiador.txt"): # se o arquivo não existir, isso indica que o programa está iniciando então é solicitado href para ser enviado ao servidor
        href = input("Input href: ")
        s.sendall(bytes(href,"utf-8"))
        
        with open('historiador.txt', 'a', encoding='utf8') as f: # coloca no topo do arquivo o valor digitado de Href
            f.write(f"Href: {href} m")
            f.write("\n\n")
        f.close()
    
    
    while True:
        msg = s.recv(1024) # 1024 é o buffer
        
        print(msg.decode("utf-8"))
        with open('historiador.txt', 'a', encoding='utf8') as f:
            f.write(str(msg))
            f.write("\n")
            
        f.close()
        s.close()
        controle()



if os.path.exists("historiador.txt"):  # se o arquivo já existir antes do início, então ele será apagado para começar outro do zero
    os.remove("historiador.txt")

controle()