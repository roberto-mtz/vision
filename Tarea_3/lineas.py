from Tkinter import *
from PIL import Image, ImageTk
from math import floor, atan, fabs, pi, cos, sin, ceil
import time
import numpy

def ventana():
    #GUI de la aplicacion
    
    root = Tk()
    root.title('Bordes')
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='Detectar linea', command = boton_linea).pack(in_=frame, side=LEFT)
    root.mainloop()

def poner_imagen(image):
    #Carga imagen en ventana
    
    photo = ImageTk.PhotoImage(image)
    global label
    label = Label(image=photo)
    label.imagen = photo
    label.pack()

def cambiar_agrises(path_original):
    #Pone a grises la imagen
    
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
    #calculo de convolucion de las mascaras
    
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

def normalizacion(imagen):
    #normaliza utilizando todo el rango
    
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

    for a in range(x):
        for b in range(y):
            pixel_color = pixeles[a, b]
            nuevo_pixel = ( float(pixel_color[0]) - float(min) )*( float(255) / (float(max) - float(min)) )
            nuevo_pixel = int(floor(nuevo_pixel))
            tupla_promedio = (nuevo_pixel, nuevo_pixel, nuevo_pixel)
            imagen_nueva.putpixel((a, b), tupla_promedio)

    return imagen_nueva

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


def obtener_original(path_imagen_original):
    #cargar imagen original
    
    imagen = Image.open(path_imagen_original)
    return imagen

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
    return incluidos


def linea(imagen_Y, imagen_X, w, h, imagen):
    incluir = 1.0
    CERO = 0.00001
    resultado = list()
    for y in range(h):
        datos = list()
        for x in range(w):
            pixel_X = float(sum(imagen_X[x, y]))/3.0
            pixel_Y = float(sum(imagen_Y[x, y]))/3.0
            print str(pixel_X) + " " + str(pixel_Y)
            if fabs(pixel_X) > CERO:
                angulo = atan(pixel_Y/pixel_X)
            else:
                if fabs(pixel_X) + fabs(pixel_Y) <= CERO:
                    angulo = None
                elif pixel_X == 0.0 and pixel_Y == 255.0:
                    angulo = 90.0
                else:
                    angulo = 0.0
            if angulo is not None:
                rho = (x - w/2) * cos(angulo) + (h/2 - y) * sin(angulo)
                datos.append(('%.2f' % angulo, '%.0f' % rho))
            else:
                datos.append((None, None))
        resultado.append(datos)

    comb = dict()
    for y in xrange(h):
        for x in xrange(w):
            if x > 0 and y > 0 and x < w - 1 and y < h - 1:
                (angulo, rho) = resultado[y][x]
                if angulo is not None:
                    combinacion = (angulo, rho)
                    if combinacion in comb:
                        comb[combinacion] += 1
                    else:
                        comb[combinacion] = 1

    frec = frecuentes(comb, int(ceil(len(comb) * incluir)))
    for y in range(h):
        renglon = list()
        for x in range(w):
            (ang, rho) = resultado[y][x]
            if (ang, rho) in frec:
                if str(ang) == "90.00":
                    imagen.putpixel((x,y), (0,255,0))
                elif str(ang) == "0.00":
                    imagen.putpixel((x,y), (0,0,255))
                else:
                    imagen.putpixel((x,y), (255,0,0))

    imagen.save("Prueba.jpg")
    return imagen
                
            
def boton_linea():
    inicio = time.time()
    label.destroy()
    
    #A grises
    imagen = cambiar_agrises(path_imagen_original)
    imagen.save("paso_1.jpg")
        
    h_hori = numpy.array([[-1, -1, -1],[2, 2, 2],[-1, -1, -1]])
    h_verti = numpy.array([[-1, 2, -1],[-1, 2, -1], [-1, 2, -1]])
    h_ob45 = numpy.array([[-1, -1, 2],[-1, 2, -1], [2, -1, -1]])
    h_obn45 = numpy.array([[2, -1, -1],[-1, 2, -1], [-1, -1, 2]])
    
    imagen_hori = convolucion(imagen, numpy.multiply(1.0/1.0,h_verti))
    #imagen_hori = cambiar_umbral(imagen_hori, 0.1)
    imagen_hori.save("paso_2.jpg")
    imagen_verti = convolucion(imagen, numpy.multiply(1.0/1.0,h_hori))
    #imagen_hori = cambiar_umbral(imagen_hori, 0.1)
    imagen_verti.save("paso_3.jpg")
    
    pixeles_hori = imagen_hori.load()
    pixeles_verti = imagen_verti.load()
    x, y = imagen.size
    imagen = linea(pixeles_verti, pixeles_hori, x, y, imagen)
    
    #Pone en ventana
    poner_imagen(imagen)
    
    #Tiempo
    fin = time.time()
    tiempo = fin - inicio
    print "Tiempo que trascurrio -> " + str(tiempo)
    return tiempo

def boton_original():
    #carga imagen original
    
    label.destroy()
    imagen_original = obtener_original(path_imagen_original)
    poner_imagen(imagen_original)

def boton_prueba():
    #hace prueba de tiempo
    
    tiempo = 0.0
    for i in range(30):
        tiempo = tiempo + boton_bordes()
    promedio = tiempo / 30.0
    print "Tiempo promedio de " + path_imagen_original + " es = " + str(promedio)

path_imagen_original = "sine.gif"
ventana()