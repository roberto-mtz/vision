from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
from math import floor, atan, fabs, pi, cos, sin, ceil, sqrt, degrees, atan2
from random import randint
import random
import time
import numpy

def ventana():
    #GUI de la aplicacion
    
    root = Tk()
    root.title('Poli')
    global frame
    frame = Frame()
    frame.pack(padx=5,pady=5)
    poner_imagen(obtener_original(path_imagen_original))
    b1 = Button(text='Original', command = boton_original).pack(in_=frame, side=LEFT)
    b2 = Button(text='Detectar poli', command = boton_esq).pack(in_=frame, side=LEFT)
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

def crea_elipse(min, max, cuantos, dim):
    imagen_elipse = Image.new('RGB', (dim, dim), (255, 255, 255))
    dibuja = ImageDraw.Draw(imagen_elipse)
    x, y = imagen_elipse.size
    for i in range(cuantos):
        eX, eY = randint(min,max), randint(min,max)
        bbox =  (eX*4/2, eY*4/2, eX*4, eY*4)
        dibuja.ellipse(bbox, fill="green")
        print "Elipse con es (%s, %s)" %(x, y)
    return imagen_elipse

def obtener_votos(imagen_hori, imagen_verti, imagen, radio):
    pixeles_hori = imagen_hori.load()
    pixeles_verti = imagen_verti.load()
    dim_x, dim_y = imagen.size
    votos = []
    for pos in range(dim_x):
        votos.append([0] * dim_x)
    for y_m in range(dim_x):
        y = dim_y / 2 - y_m
        for x_m in range(dim_x):
            x = x_m - dim_x / 2
            gra_y = pixeles_hori[y_m, x_m][0]
            gra_x = pixeles_verti[y_m, x_m][0]
            gra = sqrt(gra_x ** 2 + gra_y ** 2)
            if fabs(gra) > 0:
                x_c = int(round(x - radio * (gra_x/gra)))
                y_c = int(round(y - radio * (gra_y/gra)))
                x_c_m = x_c + dim_x /2
                y_c_m = dim_y / 2 - y_c
                if  y_c_m >= 0 and x_c_m < dim_x and y_c_m < dim_y and x_c_m >= 0:
                    votos[y_c_m][x_c_m] = votos[y_c_m][x_c_m] + 1

    for rango in range(1, int(round(dim_x * 0.1))):
        agrega = True
        while agrega:
            agrega = False
            for y in range(dim_y):
                for x in range(dim_x):
                    v = votos[y][x]
                    if v > 0:
                        for dx in range(-rango, rango):
                            for dy in range(-rango, rango):
                                if not (dx == 0 and dy == 0):
                                    if y + dy < dim_x and y + dy >= 0 and x + dx >= 0 and x + dx < dim_x:
                                        w = votos[y + dy][x + dx]
                                        if w > 0:
                                            if v - rango >= w:
                                                votos[y][x] = v + w
                                                votos[y + dy][x + dx] = 0
                                                agrega = True

    return votos

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
    
    print colores
    
    suma = 0
    for i in range(len(colores)):
        suma = suma + colores[i][1]
    
    global frame
    y = frame.winfo_height()
    
    #Obtenemos porcentajes
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

    #Itentificamos fondo y lo pintamos a gris
    print "Fondo fig: " + str(fig)
    imagen_BFS = pinta_fondo(imagen_BFS, color_max)
    #poner_imagen(imagen_BFS)

    #Agregamos etiquetas segun su centro de masa
    """
    for i in range(len(colores)):
        promedio = float(colores[i][1])/float(suma)*100.0
        if promedio > 1.5:
            print "Identifico . . ."
            label_fig = Label(text = str(i))
            label_fig.place(x = colores[i][2][0],  y = colores[i][2][1] + y)
    """
    return imagen_BFS, colores, elipses

def filtro_median(imagen):
    #Saco la mediana de los pixeles vecinos para eliminar
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
            resultado = int(ceil(mediana(arreglo)))
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

def diferencia(imagen1, imagen2):
    pixeles1 = imagen1.load()
    pixeles2 = imagen2.load()
    x, y = imagen1.size
    imagen_nueva_prom = Image.new("RGB", (x, y))
    for a in range(x):
        for b in range(y):
            dif = pixeles1[a, b][0]-pixeles2[a,b][0]
            if dif > 255:
                dif = 255
            if dif < 0:
                dif = 0
            imagen_nueva_prom.putpixel((a, b), (dif, dif, dif))
    
    return imagen_nueva_prom

def boton_esq():
    #Cambiamos a grises
    imagen = cambiar_agrises(path_imagen_original)
    imagen.save("paso_1.jpg")
    
    #Agregamos filtro de la mediana
    imagen_median = cambiar_promedio(imagen)
    for i in range(10):
        imagen_median = cambiar_promedio(imagen_median)
    imagen_median.save("paso_2.jpg")

    #Sacamos la diferencia
    imagen_dif = diferencia(imagen_median, imagen)
    imagen_dif.save("paso_3.jpg")

    #Ponemos un umbral y tenemos bordes
    imagen_um = cambiar_umbral(imagen_dif, 0.3) #ESTE UMBRAL CAMBIA
    imagen_um.save("paso_4.jpg")

    #Agrego Laplaciana para bordes
    umbral_valor = 0.5
    h_lap = numpy.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    imagen_lap, puntos = convolucion(imagen, numpy.multiply(1.0/1.0,h_lap))
    imagen_lap = cambiar_umbral(imagen_lap, 0.1)
    imagen_BFS = cambiar_umbral(imagen_lap, umbral_valor)
    imagen_BFS.save("paso_5.jpg")

    #Agregamos BFS
    imagen_BFS, colores, poligonos = aplicar_BFS(imagen_BFS)
    imagen_BFS.save("paso_6.jpg")

    esq_pix = imagen_um.load()
    dibuja = ImageDraw.Draw(imagen_lap)

    corte = []
    for poli in poligonos:
        for i in range(len(poli)):
            esq = esq_pix[poli[i][0], poli[i][1]]
            if esq[0] == 255:
                dibuja.ellipse((poli[i][0]-6,poli[i][1]-6,poli[i][0]+6,poli[i][1]+6), fill="black")
                cor = (poli[i][0], poli[i][1])
                corte.append((poli[i][0], poli[i][1]))
                break

    #Agregamos BFS
    imagen_BFS, colores, poligonos = aplicar_BFS(imagen_lap)
    imagen_BFS.save("paso_ALGO.jpg")

    
    x, y = imagen.size
    imagen_nueva = Image.new("RGB", (x, y))
    dibuja = ImageDraw.Draw(imagen_nueva)

    cont = 0
    for poli in poligonos:
        cor = (corte[cont][0], corte[cont][1])
        dibuja.ellipse((cor[0]-6,cor[1]-6,cor[0]+6,cor[1]+6), fill="red")
        for i in range(len(poli)):
            cor_ant = cor
            esq = esq_pix[poli[i][0], poli[i][1]]
            if esq[0] == 255:
                dibuja.ellipse((poli[i][0]-6,poli[i][1]-6,poli[i][0]+6,poli[i][1]+6), fill="red")
                cor = (poli[i][0], poli[i][1])
            if cor != "NULL" and cor_ant != cor and cor_ant != "NULL":
                dibuja.line((cor_ant[0], cor_ant[1], cor[0], cor[1]), fill="red")
        dibuja.line((corte[cont][0], corte[cont][1], cor[0], cor[1]), fill="red")
        cont = cont + 1

    imagen_nueva.save("paso_7.jpg")

def boton_poli():
    inicio = time.time()
    label.destroy()
    
    max = 0
    suma = 0.0
    
    #A grises
    imagen = cambiar_agrises(path_imagen_original)
    imagen.save("paso_1.jpg")
    votos = list()
        
    #A grises
    imagen = cambiar_agrises(path_imagen_original)
    imagen.save("paso_1.jpg")
    
    #Agrego Laplaciana
    h_lap = numpy.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    imagen_prom, puntos = convolucion(imagen, numpy.multiply(1.0/1.0,h_lap))
    imagen_prom = cambiar_umbral(imagen_prom, 0.1)
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
    
    #Agrego umbral para binarizar
    umbral_valor = 0.08
    imagen_bin2 = cambiar_umbral(imagen_prom.convert("RGB"), umbral_valor)
    imagen_bin2.save("paso_6.jpg")
    
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
    imagen_BFS, colores, poligonos = aplicar_BFS(imagen_BFS)
    imagen_BFS.save("paso_10.jpg")

    x, y = imagen_BFS.size

    pixeles = imagen_BFS.load()
    bordes_detectados = []

    h_Y = numpy.array([[-4, 5, 5], [-4, 5, 5], [-4, -4, -4]])
    h_X = numpy.array([[5, 5, 5], [-4, 5, -4], [-4, -4, -4]])
    #h_Y = numpy.array([[1, 1, 1], [-1, -2, 1], [-1, -1, -1]])
    #h_X = numpy.array([[-1 , -1, -1], [-1, -2, 1], [1, 1, 1]])
    imagen.save("paso_ANTES.jpg")
    imagen_hori, puntos_GX = convolucion(imagen, numpy.multiply(1.0/1.0,h_X))
    imagen_hori.save("paso_sobelX.jpg")
    pixeles_GX = imagen_hori.load()
    imagen_verti, puntos_GY = convolucion(imagen, numpy.multiply(1.0/1.0,h_Y))
    imagen_verti.save("paso_sobelY.jpg")
    pixeles_GY = imagen_verti.load()
    
    dibuja = ImageDraw.Draw(imagen_BFS)
    x, y = imagen_BFS.size
    puntos = numpy.zeros(x*y).reshape((x, y))

    lados = []
    
    for poli in poligonos:
        fig = []
        x, y = imagen_BFS.size
        puntos = numpy.zeros(x*y).reshape((x, y))
        for i in range(len(poli)):
            gx = puntos_GX[poli[i][0], poli[i][1]]
            gy = puntos_GY[poli[i][0], poli[i][1]]
            tangente = atan2(gy, gx)
            tan = degrees(tangente)
            fig.append((poli[i][0], poli[i][1], tan))
            #if tan > 89.0 and tan < 92.0:
                #dibuja.ellipse((poli[i][0]-3,poli[i][1]-3,poli[i][0]+3,poli[i][1]+3), fill="red")
        arreglado = sorted(fig, key=lambda tup: tup[2])
        lados.append(arreglado)
        #print arreglado

    color = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
    for i in range(len(lados)):
        cont = 0
        for j in range(len(lados[i])):
            cambio = lados[i][j][2] - lados[i][j-1][2]
            #cambio = fabs(cambio)
            #print cambio
            #time.sleep(0.1)
            if cambio > 10.0:
                color = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
            if cambio < -5.0:
                color = (random.randint(0,255), random.randint(0,255), random.randint(0, 255))
                #print " "
                #print " "
                cont = cont + 1
            dibuja.ellipse((lados[i][j][0]-3,lados[i][j][1]-3,lados[i][j][0]+3, lados[i][j][1]+3), fill=color)
        print "LADOS == " + str(cont)

    poner_imagen(imagen_BFS)
    imagen_BFS.save("paso_11.jpg")
    
    
    #Tiempo
    fin = time.time()
    tiempo = fin - inicio
    print "Tiempo que trascurrio -> " + str(tiempo)
    
    return tiempo

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

    cuantos = 1
    radio = 50
    
#imagen = crea_elipse(20, 60, cuantos=2, dim=250)
#imagen.save("circulo.gif")
path_imagen_original = "star2.png"
ventana()
