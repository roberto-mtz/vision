from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import time
import numpy

def ventana():
    root = Tk()
    root.title('Bordes')
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='Detectar bordes', command = boton_bordes).pack(in_=frame, side=LEFT)
    b1 = Button(text='Prueba tiempo', command = boton_prueba).pack(in_=frame, side=LEFT)
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

def boton_bordes():
    inicio = time.time()
    label.destroy()
    
    #A grises
    imagen_grises = cambiar_agrises(path_imagen_original)
    imagen_grises.save("paso_1.jpg")
    
    #Aplico mascara Sobel a 0 grados
    h = numpy.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    imagen_con = convolucion(imagen_grises, h)
    imagen_con.save("paso_2.jpg")
    
    #Aplico mascara Sobel a 45 grados
    h = numpy.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    imagen_con2 = convolucion(imagen_con, h)
    imagen_con2.save("paso_3.jpg")
    
    #Aplico gradiente horizontal
    h_hori = numpy.array([[-1, -2, -1],[0, 0, 0], [1, 2, 1]])
    imagen_con3 = convolucion(imagen_con2, h_hori)
    imagen_con3.save("paso_4.jpg")
    
    #Aplico gradiente vertical
    h_verti = numpy.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    imagen_con4 = convolucion(imagen_con3, h_verti)
    imagen_con4.save("paso_5.jpg")
    
    #Normalizo la imagen
    imagen_nor = normalizacion(imagen_con3)
    imagen_nor.save("paso_6.jpg")
    
    #Binarizo (umbral 0.5)
    umbral_valor = 0.5
    imagen_bin = cambiar_umbral(imagen_nor.convert("RGB"), umbral_valor)
    imagen_bin.save("paso_7.jpg")
    
    #Hace promedio
    imagen_final1 = cambiar_promedio(imagen_bin.convert("RGB"))
    imagen_final2 = cambiar_promedio(imagen_final1.convert("RGB"))
    imagen_final2.save("paso_8.jpg")
    
    #Pone en ventana
    poner_imagen(imagen_final2)
    
    #Tiempo
    fin = time.time()
    tiempo = fin - inicio
    print "Tiempo que trascurrio -> " + str(tiempo)
    return tiempo

def boton_original():
    label.destroy()
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)

def boton_prueba():
    tiempo = 0.0
    for i in range(30):
        tiempo = tiempo + boton_bordes()
    promedio = tiempo / 30.0
    print "Tiempo promedio de " + path_imagen_original + " es = " + str(promedio)

path_imagen_original = "fruta.jpg"
ventana()