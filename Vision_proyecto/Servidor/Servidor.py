#!/usr/bin/python
from threading import Thread
from PIL import Image, ImageTk, ImageDraw
from math import floor, atan, fabs, pi, cos, sin, ceil, sqrt, degrees, atan2
from random import randint
import random
import time
import numpy
import socket

#Clase hilos, genera un hilo por conexion
class Hilos(Thread):
      def __init__(self, socket2, direccion):
            Thread.__init__(self)
            self.socket2 = socket2
            self.datos = direccion[0]   

      def run(self):
            while 1:
                  msj = self.socket2.recv(1024)
                  print "Comienzo imagen . . . e"
                  print msj
                  numero = msj.split(".")
                  img_1 = deteccion_esquinas("img/"+str(numero[0])+".png", 1)
                  img_1.save("paso_2.jpg")
                  img_2 = deteccion_esquinas("uploads/"+str(msj), 4)
                  img_2.save("paso_3.jpg")
                  img_dif = diferencia(img_1, img_2)
                  img_dif.save("paso_4.jpg")
                  esq_1 = distancia(img_1)
                  val = distancia(img_dif)
                  prom = str(100-((val*100)/esq_1))
                  print prom
                  self.socket2.sendall(str(prom))
                  self.socket2.close()
                  break
                  

def cambiar_agrises(path_original):
    #Pone a grises la imagen
    
    imagen = Image.open(path_original).convert("RGB")
    pixeles = imagen.load()
    x, y = imagen.size
    
    imagen_nueva = Image.new("RGB", (x, y))
    
    colores = []
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            promedio = sum(pixel_color)/3
            tupla_promedio = (promedio, promedio, promedio)
            colores.append(tupla_promedio)
            imagen_nueva.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva

#Centros de masa
def obtener_centros(imagen, votos):
    suma = 0.0
    max = 0
    dim_x, dim_y = imagen.size
    #print 'Dimx = %d, Dimy = %d' % (dim_x, dim_y)
    for x in range(dim_x):
        for y in range(dim_y):
            v = votos[y][x]
            suma += v
            if v > max:
                max = v
    prom = suma / (dim_x * dim_y)
    umbral = (max + prom) / 2.0
    centros = []
    for x in range(dim_x):
        for y in range(dim_y):
            v = votos[y][x]
            if v > umbral:
                #print 'Centro en %d, %d. ' % (y,x)
                centros.append((y,x))
    return centros, max

def BFS(imagen, inicio, color):
    #Busqueda de anchura para determinar una figura
    pixeles = imagen.load()
    altura, ancho = imagen.size
    
    fila, columna = inicio
    original = pixeles[fila, columna]
    
    cola = []
    cola.append((fila, columna))
    masa = []
    c = []
    
    while len(cola) > 0:
        (fila, columna) = cola.pop(0)
        actual = pixeles[fila, columna]
        if actual == original or actual == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidato = (fila + dy, columna + dx)
                    if candidato[0] >= 0 and candidato[0] < altura and candidato[1] >= 0 and candidato[1] < ancho:
                        contenido = pixeles[candidato[0], candidato[1]]
                        if contenido == original:
                            pixeles[candidato[0], candidato[1]] = color
                            imagen.putpixel((candidato[0], candidato[1]), color)
                            cola.append(candidato)
                            masa.append((candidato[0], candidato[1]))
                            c.append((candidato[0], candidato[1]))
    
    return imagen, masa, c

def pinta_fondo(imagen_BFS, color_max):
    #pintamos fondo de manera que obtenemos el color que predomina en la imagen
    pixeles = imagen_BFS.load()
    x, y = imagen_BFS.size
    for a in range(x):
        for b in range(y):
            if pixeles[a, b] == color_max:
                color = (100,100,100)
                imagen_BFS, masa, c = BFS(imagen_BFS.convert("RGB"), (a, b), color)
                return imagen_BFS

def aplicar_BFS(imagen_BFS):
    #aplica busqueda de anchura a todas las figuras encontradas con color aleatorio
    pixeles = imagen_BFS.load()
    x, y = imagen_BFS.size
    colores = []
    elipses = []
    for a in range(x):
        for b in range(y):
            if pixeles[a, b] == (255, 255, 255):
                color = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
                imagen_BFS, masa, c = BFS(imagen_BFS.convert("RGB"), (a, b), color)
                elipses.append(c)
                x_suma = 0
                y_suma = 0
                for i in range(len(masa)):
                    x_suma = x_suma + masa[i][0]
                    y_suma = y_suma + masa[i][1]
                
                x_centro = x_suma/len(masa)
                y_centro = y_suma/len(masa)
                colores.append([color, 0, (x_centro, y_centro)])
                pixeles = imagen_BFS.load()
                masa = []
    
    #suma la cantidad de colores diferentes en la imagen
    pixeles = imagen_BFS.load()
    for a in range(x):
        for b in range(y):
            for n in range(len(colores)):
                if colores[n][0] == pixeles[a,b]:
                    colores[n][1] = colores[n][1] + 1
    #print colores
    suma = 0
    for i in range(len(colores)):
        suma = suma + colores[i][1]
    
    #Obtenemos porcentajes
    prom = []
    for i in range(len(colores)):
        promedio = float(colores[i][1])/float(suma)*100.0
        if promedio > 3.0:
            #print "Porcentajes: "
            #print "Figura " + str(i) + ": " + str(promedio)
            prom.append((i, promedio, colores[i][0]))
    
    maxim = 0.0
    for i in range(len(prom)):
        if maxim < prom[i][1]:
            maxim = prom[i][1]
            fig = prom[i][0]
            color_max = prom[i][2]
    
    #Itentificamos fondo y lo pintamos a gris
    #print "Fondo fig: " + str(fig)
    imagen_BFS = pinta_fondo(imagen_BFS, color_max)
    return imagen_BFS, colores, elipses

def cambiar_promedio(imagen):
    #efecto borrado
    
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva_prom = Image.new("RGB", (x, y))
    
    colores = []
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            veces = 5
            suma = 0
            promedio = 0
            
            try:
                pixel_norte = pixeles[a-1,b]
            except IndexError:
                pixel_norte = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_sur = pixeles[a+1, b]
            except IndexError:
                pixel_sur = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_este = pixeles[a, b+1]
            except IndexError:
                pixel_este = (0, 0, 0)
                veces = veces - 1
            try:
                pixel_oeste = pixeles[a, b-1]
            except IndexError:
                pixel_oeste = (0, 0, 0)
                veces = veces - 1
            
            Rojos_suma = pixel_norte[0] + pixel_sur[0] + pixel_este[0] + pixel_oeste[0] + pixel_color[0]
            Verdes_suma = pixel_norte[1]+ pixel_sur[1] + pixel_este[1] + pixel_oeste[1] + pixel_color[1]
            Azul_suma = pixel_norte[2]+ pixel_sur[2] + pixel_este[2] + pixel_oeste[2] + pixel_color[2]
            
            Rojo_prom = Rojos_suma/veces
            Verdes_prom = Verdes_suma/veces
            Azul_prom = Azul_suma/veces
            
            tupla_promedio = (Rojo_prom, Verdes_prom, Azul_prom)
            colores.append(tupla_promedio)
            imagen_nueva_prom.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva_prom

#Diferencia entre dos imagenes
def diferencia(imagen1, imagen2):
    pixeles1 = imagen1.load()
    pixeles2 = imagen2.load()
    x, y = imagen1.size
    imagen_nueva_prom = Image.new("RGB", (x, y))
    for a in range(x):
        for b in range(y):
            try:
                dif = pixeles1[a, b][0]-pixeles2[a,b][0]
                if dif > 255:
                    dif = 255
                if dif < 0:
                    dif = 0
                imagen_nueva_prom.putpixel((a, b), (dif, dif, dif))
            except:
                pass
            
    
    return imagen_nueva_prom

def cambiar_umbral(imagen, umbral_valor):
    #dado un umbral pone en completamente blanco o negro
    
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            valor_canal = float(pixel_color[0])
            color_nor = valor_canal/255.0
            if(color_nor>=umbral_valor):
                poner_pixel = 255
            else:
                poner_pixel = 0
            tupla_pixel = (poner_pixel, poner_pixel, poner_pixel)
            imagen_nueva.putpixel((a, b), tupla_pixel)
    return imagen_nueva

def convolucion(f, h):
    #calculo de convolucion de las mascaras
    
    pixeles = f.load()
    x, y = f.size
    puntos_num = numpy.zeros(x*y).reshape((x, y))
    
    F = Image.new("RGB", (x, y))
    i = len(h[0])
    j = len(h[0])
    for a in range(x):
        for b in range(y):
            suma = 0
            for c in range(i):
                c1 = c - i/2
                for d in range(j):
                    d1 = d - j/2
                    try:
                        suma = suma + (pixeles[a+c1, b+d1][0])*(h[c][d])
                    except:
                        pass
            puntos_num[a, b] = (suma)
            suma = int(floor(suma))
            tupla_promedio = (suma, suma, suma)
            F.putpixel((a,b),tupla_promedio)
    
    return F, puntos_num

def deteccion_esquinas(ruta_img, tam):
    #Cambiamos a grises
    imagen = cambiar_agrises(ruta_img)
    #imagen.save("paso_1.jpg")
    size = 160, 284
    imagen.thumbnail(size, Image.ANTIALIAS)
    imagen.save("paso_1.jpg")
    #Agregamos filtro de la mediana
    imagen_median = cambiar_promedio(imagen)
    for i in range(4):
        imagen_median = cambiar_promedio(imagen_median)
    #imagen_median.save("paso_2.jpg")
    
    #Sacamos la diferencia
    imagen_dif = diferencia(imagen_median, imagen)
    #imagen_dif.save("paso_3.jpg")
    
    #Ponemos un umbral y tenemos bordes
    imagen_um = cambiar_umbral(imagen_dif, 0.3) #ESTE UMBRAL CAMBIA
    #imagen_um.save("paso_4.jpg")
    
    #Agrego Laplaciana para bordes
    umbral_valor = 0.5
    h_lap = numpy.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    imagen_lap, puntos = convolucion(imagen, numpy.multiply(1.0/1.0,h_lap))
    imagen_lap = cambiar_umbral(imagen_lap, 0.1)
    imagen_BFS = cambiar_umbral(imagen_lap, umbral_valor)
    #imagen_BFS.save("paso_5.jpg")
    
    #Agregamos BFS
    imagen_BFS, colores, figuras = aplicar_BFS(imagen_BFS)
    #imagen_BFS.save("paso_6.jpg")
    
    esq_pix = imagen_um.load()
    dibuja = ImageDraw.Draw(imagen_lap)
    
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    dibuja = ImageDraw.Draw(imagen_nueva)
    
    for fig in figuras:
        for i in range(len(fig)):
            esq = esq_pix[fig[i][0], fig[i][1]]
            if esq[0] == 255:
                dibuja.ellipse((fig[i][0]-tam,fig[i][1]-tam,fig[i][0]+tam,fig[i][1]+tam), fill="white")
    
    return imagen_nueva

#Cuenta la cantidad de pix blancos
def distancia(img):
    pix = img.load()
    x, y = img.size
    val = 0
    for a in range(x):
        for b in range(y):
            if pix[a,b][0] == 255:
                val = val + 1
    return val

#Se crea un hilo para cada conexion
def main():  
      socket1 = socket.socket()  
      socket1.bind(("localhost", 6699))  
      print "Haz iniciado satisfactoriamente el servidor\nmuestro los mensajes."
      socket1.listen(1)  
      clientes = []
      
      while (1):
            socket2, direccion = socket1.accept()
            #for cli in clientes:
            #   cli.socket2.close()
            print direccion[0] + " conectado."
            hilo = Hilos(socket2, direccion)
            hilo.start()
            clientes.append(hilo)
            
      print "cerando"
      socket1.close()
        

main()
