from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import numpy
import random

def ventana():
    root = Tk()
    root.title('Lab 2')
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='S&P', command = boton_sp).pack(in_=frame, side=LEFT)
    b3 = Button(text='Quitar S&P', command = boton_quitar_sp).pack(in_=frame, side=LEFT)
    b4 = Button(text='Bordes', command = boton_bordes).pack(in_=frame, side=LEFT)
    root.mainloop()

def poner_imagen(image):
    photo = ImageTk.PhotoImage(image)
    global label
    label = Label(image=photo)
    label.imagen = photo
    label.pack()

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
            nuevo_pixel = ( float(pixel_color[0]) - float(min) )*( float(255) / (float(max) - float(min)) )
            nuevo_pixel = int(floor(nuevo_pixel))
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
    umbral_valor = 0.1
    imagen_bin = cambiar_umbral(imagen_nor.convert("RGB"), umbral_valor)
    imagen_bin.save("paso_4.jpg")
    
    #Pongo promedio
    imagen_prom = cambiar_promedio(imagen_bin.convert("RGB"))
    imagen_prom.save("paso_5.jpg")
    poner_imagen(imagen_prom)

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

path_imagen_original = "cerro.jpg"
imagen_original = obtener_original(path_imagen_original)
ventana()