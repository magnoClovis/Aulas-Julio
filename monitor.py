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
    s.connect((socket.gethostname(),60000))
    
    
    full_msg = ""
    while True:
        #href = input("Input href: ")
        #s.send(bytes(href,"utf-8"))
        msg = s.recv(1024) # 1024 é o buffer
        
        print(msg.decode("utf-8"))
        with open('historiador.txt', 'a', encoding='utf8') as f:
            f.writelines(str(msg))
        f.close()
        controle()


controle()