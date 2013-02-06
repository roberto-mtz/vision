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
    b4 = Button(text='Diferencia', command = boton_diferencia).pack(in_=frame, side=LEFT)
    b5 = Button(text='Gaussian', command = boton_convolucion).pack(in_=frame, side=LEFT)
    b6 = Button(text='Umbral', command = boton_umbral).pack(in_=frame, side=LEFT)
    root.mainloop()

def poner_imagen(image):
    #image = Image.open()
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

    #imagen_nueva.save(path_imagen)
    #print colores
    return imagen_nueva

def convolucion(f, h):
    pixeles = f.load()
    x, y = f.size
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
            suma = int(floor(suma))
            tupla_promedio = (suma, suma, suma)
            F.putpixel((a,b),tupla_promedio)
     
    return F

def cambiar_promedio(imagen):
    #imagen = Image.open(path_imagen_original).convert("RGB")
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

    imagen_nueva_prom.save("hola_pruebo.gif")

    return imagen_nueva_prom

def diferencia(imagen):
    #imagen = Image.open(path_imagen_original).convert("RGB")                                                    
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

#imagen_nueva_prom.save("hola_pruebo.gif")

    return imagen_nueva_prom


def cambiar_umbral(imagen, umbral_valor):
    #imagen = Image.open(path_imagen_original).convert("RGB")
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
    
    #imagen_nueva.save(path_imagen)
    #print colores
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
    imagen_prom1 = cambiar_promedio(imagen_grises.convert("RGB"))
    poner_imagen(imagen_prom1)

def boton_diferencia():
    label.destroy()
    imagen_grises = cambiar_agrises(path_imagen_original)
    #imagen_grises = obtener_original(path_imagen_original)
    imagen_prom = diferencia(imagen_grises.convert("RGB"))
    poner_imagen(imagen_prom)

def boton_convolucion():
    label.destroy()
    imagen_grises = cambiar_agrises(path_imagen_original)
    #h = [[0, 0.2, 0],[0.2, 0.2, 0.2],[0,0.2,0]]
    h = [[(1.0/16.0)*1.0, (1.0/16.0)*2.0, (1.0/16.0)*1.0],[(1.0/16.0)*2.0, (1.0/16.0)*4.0, (1.0/16.0)*2.0],[(1.0/16.0)*1.0, (1.0/16.0)*2.0, (1.0/16.0)*1.0]]
    imagen_con = convolucion(imagen_grises, h)
    poner_imagen(imagen_con)

def boton_umbral():
    label.destroy()
    umbral_valor = 0.5
    imagen_grises = cambiar_agrises(path_imagen_original)
    imagen_umb = cambiar_umbral(imagen_grises.convert("RGB"), umbral_valor)
    poner_imagen(imagen_umb)
    

path_imagen_original = "paris.gif"
ventana()
