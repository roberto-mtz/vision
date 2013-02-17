from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import numpy
import random

def ventana():
    root = Tk()
    root.title('Tarea 2')
    global frame
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    #b2 = Button(text='S&P', command = boton_sp).pack(in_=frame, side=LEFT)
    #b3 = Button(text='Quitar S&P', command = boton_quitar_sp).pack(in_=frame, side=LEFT)
    b4 = Button(text='Bordes', command = boton_bordes).pack(in_=frame, side=LEFT)
    root.mainloop()

def poner_imagen(image):
    photo = ImageTk.PhotoImage(image)
    global label
    label = Label(image=photo)
    label.imagen = photo
    label.pack()

def BFS(imagen, inicio, color):
    pixeles = imagen.load()
    altura, ancho = imagen.size

    fila, columna = inicio
    original = pixeles[fila, columna]

    cola = []
    cola.append((fila, columna))
    masa = []

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

    return imagen, masa

def cambiar_agrises(path_original):
    imagen = Image.open(path_imagen_original).convert("RGB")
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

def cambiar_promedio(imagen):
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

def diferencia(imagen):
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
                veces =veces - 1
            try:
                pixel_este = pixeles[a, b+1]
            except IndexError:
                pixel_este = (0, 0, 0)
                veces =veces - 1
            try:
                pixel_oeste = pixeles[a, b-1]
            except IndexError:
                pixel_oeste = (0, 0, 0)
                veces =veces - 1

            Rojos_suma = pixel_norte[0] + pixel_sur[0] + pixel_este[0] + pixel_oeste[0] + pixel_color[0]
            Verdes_suma = pixel_norte[1]+ pixel_sur[1] + pixel_este[1] + pixel_oeste[1] + pixel_color[1]
            Azul_suma = pixel_norte[2]+ pixel_sur[2] + pixel_este[2] + pixel_oeste[2] + pixel_color[2]

            Rojo_prom = Rojos_suma/veces
            Verde_prom = Verdes_suma/veces
            Azul_prom = Azul_suma/veces

            Rojo_dif = pixel_color[0] - Rojo_prom
            Verde_dif = pixel_color[1] - Verde_prom
            Azul_dif = pixel_color[2] - Azul_prom

            tupla_promedio = (Rojo_dif, Verde_dif, Azul_dif)
            colores.append(tupla_promedio)
            imagen_nueva_prom.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva_prom

def normalizacion(imagen):
    pixeles = imagen.load()
    x, y = imagen.size
    min = 0
    max = 0
    imagen_nueva = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            max_ant = max
            max_new = pixel_color[0]
            min_ant = min
            min_new = pixel_color[0]
            if (max_new >= max_ant):
                max = max_new
            elif (min_new <= min_ant):
                min = min_new
            elif (min == 0 and max == 255):
                break

    print min
    print max
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            try:
                nuevo_pixel = ( float(pixel_color[0]) - float(min) )*( float(255) / (float(max) - float(min)) )
                nuevo_pixel = int(floor(nuevo_pixel))
            except:
                nuevo_pixel = 255
            tupla_promedio = (nuevo_pixel, nuevo_pixel, nuevo_pixel)
            imagen_nueva.putpixel((a, b), tupla_promedio)

    return imagen_nueva

def cambiar_umbral(imagen, umbral_valor):
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            valor_canal = float(pixel_color[0])
            color_nor = valor_canal/255.0
            if(color_nor > umbral_valor):
                poner_pixel = 255
            else:
                poner_pixel = 0
            tupla_pixel = (poner_pixel, poner_pixel, poner_pixel)
            imagen_nueva.putpixel((a, b), tupla_pixel)
    return imagen_nueva

def cambiar_SP(imagen, inten, pola):
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            valor_canal = float(pixel_color[0])
            color_nor = valor_canal/255.0
            
            if(inten > random.random()):
                poner_pixel = random.choice([int(floor(255.0 * pola)), 0])
            else:
                poner_pixel = pixel_color[0]
        
            tupla_pixel = (poner_pixel, poner_pixel, poner_pixel)
            imagen_nueva.putpixel((a, b), tupla_pixel)

    return imagen_nueva

def quitar_SP(imagen):
    pixeles = imagen.load()
    x, y = imagen.size
    imagen_nueva_prom = Image.new("RGB", (x, y))
    
    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            veces = 4
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
        
            
            arreglo = [pixel_norte[0], pixel_sur[0], pixel_este[0], pixel_oeste[0]]
            arreglo.sort()
            resultado = int(floor(mediana(arreglo)))
            tupla_promedio = (resultado, resultado, resultado)
            imagen_nueva_prom.putpixel((a, b), tupla_promedio)
    
    return imagen_nueva_prom

def mediana(arreglo):
    if len(arreglo) % 2 == 1:
        return arreglo[(len(arreglo)+1)/2-1]
    else:
        izq = arreglo[len(arreglo)/2-1]
        der = arreglo[len(arreglo)/2]
        return (float(izq + izq)) / 2.0

def obtener_original(path_imagen_original):
    imagen = Image.open(path_imagen_original)
    return imagen

def boton_bordes():
    label.destroy()
    #Pongo a grises
    imagen_grises = cambiar_agrises(path_imagen_original)
    imagen_grises.save("paso_1.jpg")
    
    #Agrego diferencia
    imagen_prom = diferencia(imagen_grises.convert("RGB"))
    imagen_prom.save("paso_2.jpg")
    
    #Agrego normalizacion
    imagen_nor = normalizacion(imagen_prom)
    imagen_nor.save("paso_3.jpg")
    
    #Agrego umbral para binarizar
    umbral_valor = 0.04
    imagen_bin = cambiar_umbral(imagen_nor.convert("RGB"), umbral_valor)
    imagen_bin.save("paso_4.jpg")
    
    #Pongo promedio
    imagen_prom = cambiar_promedio(imagen_bin.convert("RGB"))
    imagen_prom.save("paso_5.jpg")
    
    #Agrego umbral para binarizar
    umbral_valor = 0.08
    imagen_bin2 = cambiar_umbral(imagen_prom.convert("RGB"), umbral_valor)
    imagen_bin2.save("paso_6.jpg")
    
    #####
    
    #Pongo promedio
    imagen_prom = cambiar_promedio(imagen_bin2.convert("RGB"))
    imagen_prom.save("paso_7.jpg")
    
    #Pongo promedio
    imagen_prom = cambiar_promedio(imagen_prom.convert("RGB"))
    imagen_prom.save("paso_8.jpg")
    
    #Agrego umbral para binarizar
    umbral_valor = 0.5
    imagen_BFS = cambiar_umbral(imagen_prom.convert("RGB"), umbral_valor)
    imagen_BFS.save("paso_9.jpg")
    aplicar_BFS(imagen_BFS)



def aplicar_BFS(imagen_BFS):
    pixeles = imagen_BFS.load()
    x, y = imagen_BFS.size
    colores = []
    for a in range(x):
        for b in range(y):
            if pixeles[a, b] == (0, 0, 0):
                color = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
                imagen_BFS, masa = BFS(imagen_BFS.convert("RGB"), (a, b), color)

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

    pixeles = imagen_BFS.load()
    for a in range(x):
        for b in range(y):
            for n in range(len(colores)):
               if colores[n][0] == pixeles[a,b]:
                    colores[n][1] = colores[n][1] + 1 

    print colores

    suma = 0
    for i in range(len(colores)):
        suma = suma + colores[i][1]

    global frame
    y = frame.winfo_height()

    prom = []
    for i in range(len(colores)):
        promedio = float(colores[i][1])/float(suma)*100.0
        if promedio > 3.0:
            print "Porcentajes: "
            print "Figura " + str(i) + ": " + str(promedio)
            prom.append((i, promedio, colores[i][0]))

    maxim = 0.0
    for i in range(len(prom)):
        if maxim < prom[i][1]:
            maxim = prom[i][1]
            fig = prom[i][0]
            color_max = prom[i][2]

    print "Fondo fig: " + str(fig)
    imagen_BFS = pinta_fondo(imagen_BFS, color_max)
    poner_imagen(imagen_BFS)

    for i in range(len(colores)):
        promedio = float(colores[i][1])/float(suma)*100.0
        if promedio > 3.0:
            print "Identifico . . ."
            label_fig = Label(text = str(i)) 
            label_fig.place(x = colores[i][2][0],  y = colores[i][2][1] + y)


def pinta_fondo(imagen_BFS, color_max):   
    pixeles = imagen_BFS.load()
    x, y = imagen_BFS.size
    for a in range(x):
        for b in range(y):
            if pixeles[a, b] == color_max:
                color = (100,100,100)
                imagen_BFS, masa = BFS(imagen_BFS.convert("RGB"), (a, b), color)
                return imagen_BFS
    

def boton_original():
    label.destroy()
    global imagen_original
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)

def boton_sp():
    label.destroy()
    global imagen_original
    imagen_original = cambiar_SP(imagen_original.convert("RGB"), 0.1, 0.9)
    poner_imagen(imagen_original)

def boton_quitar_sp():
    label.destroy()
    global imagen_original
    imagen_original = quitar_SP(imagen_original.convert("RGB"))
    poner_imagen(imagen_original)

path_imagen_original = "figuras2.jpg"
imagen_original = obtener_original(path_imagen_original)
ventana()