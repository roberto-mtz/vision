import math
import sys

def resolucion(c, x, y):
    #c = ax * bx
    resultado = math.floor(math.sqrt(c/(x*y)))
    return resultado

def main():
    tam = int(sys.argv[1])
    relacionx = int(sys.argv[2])
    relaciony = int(sys.argv[3])
    pixel = sys.argv[4]

    if(pixel == "Kilo"):
        tam = tam*1024
    if(pixel == "Mega"):
        tam = tam*1024*1024
    if(pixel == "Giga"):
        tam = tam*1024*1024*1024

    print "Tam = %s" %tam    
    print "X = %s" %relacionx
    print "Y = %s" %relaciony

    resultado = resolucion(tam, relacionx, relaciony)
    print resultado

main()
