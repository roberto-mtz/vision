from Tkinter import *
from PIL import Image, ImageTk
from math import floor

def ventana():
    root = Tk()
    root.title('Filtros')
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='Grises', command = boton_grises).pack(in_=frame, side=LEFT)
    b3 = Button(text='Promedio', command = boton_promedio).pack(in_=frame, side=LEFT)
    b4 = Button(text='Diferencia').pack(in_=frame, side=LEFT)
    b5 = Button(text='Gaussian').pack(in_=frame, side=LEFT)
    b6 = Button(text='Umbral', command = boton_umbral).pack(in_=frame, side=LEFT)
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

def cambiar_umbral(imagen, umbral_valor):
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

def obtener_original(path_imagen_original):
    imagen = Image.open(path_imagen_original)
    return imagen

def boton_grises():
    label.destroy()
    imagen_grises = cambiar_agrises(path_imagen_original)
    poner_imagen(imagen_grises)

def boton_original():
    label.destroy()
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)

def boton_promedio():
    label.destroy()
    imagen_grises = cambiar_agrises(path_imagen_original)
    imagen_prom = cambiar_promedio(imagen_grises.convert("RGB"))
    poner_imagen(imagen_prom)

def boton_umbral():
    label.destroy()
    umbral_valor = 0.8
    imagen_grises = cambiar_agrises(path_imagen_original)
    imagen_umb = cambiar_umbral(imagen_grises.convert("RGB"), umbral_valor)
    poner_imagen(imagen_umb)
    
path_imagen_original = "paris.gif"
ventana()
