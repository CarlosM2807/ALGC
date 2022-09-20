import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys

# DIJKSTRA NORMAL

def fila(ind, c):
    return ind/c

def columna(ind, c):
    return ind%c

def id(fil, col, c):
    return fil*c + col


#############
# RELLENA V #
#############

def rellenaNodos(f,c):
    V = {}
    for n in range(f*c):
        for i in range(f):
            for j in range(c):              # V ES UN DICCIONARIO DE DICCIONARIOS VACIOS
                V[n] = {}                   # QUE LUEGO SE RELLENARA EN EL METODO CREALABERINTOLISTA
    return V


#########################
# LISTA DE ADYACENCIA E #
#########################

def rellenaHabs(f,c):
    L = []
    for i in range(f):
        for j in range(c):
            L.append([])                    # RELLENA LA LISTA DE LISTAS VACIAS            
    return L

##########################################################
# GENERA EL LABERINTO (LOS EJES) CON LISTA DE ADYACENCIA #
##########################################################

# V ES MI GRAPH, UN DICCIONARIO DE DICCIONARIOS (QUE CONTIENE LOS NODOS HIJOS CON SUS PESOS)

def creaLaberintoLista(f,c,prob,semilla,semilla2,V,E):
    numero = SyncRNG(seed = semilla)
    numero2 = SyncRNG(seed = semilla2)

    for i in range (f):
        for j in range (c):
            if(i > 0 and numero.rand() < prob):
                peso = numero2.randi()%12+1
                E[id(i, j, c)].append((id(i-1, j, c),peso))
                E[id(i-1, j, c)].append((id(i, j, c),peso))

                V[id(i, j, c)][id(i-1, j, c)] = peso
                V[id(i-1, j, c)][id(i, j, c)] = peso

            if(j > 0 and numero.rand() < prob):
                peso = numero2.randi()%12+1
                E[id(i, j, c)].append((id(i, j-1, c),peso))
                E[id(i, j-1, c)].append((id(i, j, c),peso))

                V[id(i, j, c)][id(i, j-1, c)] = peso
                V[id(i, j-1, c)][id(i, j, c)] = peso
    return E,V

#########################
# ALGORITMO DE DIJKSTRA #
#########################

def dijkstra(graph,inicio,destino):
    dist = {}
    prev = {}
    nodosSinVisitar = graph
    infinity = 999999999

    for node in nodosSinVisitar:
        dist[node] = infinity
    dist[inicio] = 0

    # MIENTRAS LA COLA NO ESTE VACIA

    while(nodosSinVisitar):
        nodoMenorDist = None

        # OBETENGO EL NODO DE MENOR DISTANCIA TENTATIA QUE ESTE EN LA COLA (nodoMenorDist)

        for node in nodosSinVisitar:
            if nodoMenorDist is None:
                nodoMenorDist = node
            elif dist[node] < dist[nodoMenorDist]:
                nodoMenorDist = node

        # OBTENGO SUS HIJOS
            
        if(nodoMenorDist == destino):
            break
        
        hijos = graph[nodoMenorDist].items()

        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF

        for v, peso in hijos:
            if peso + dist[nodoMenorDist] < dist[v]:
                dist[v] = peso + dist[nodoMenorDist]
                prev[v] = nodoMenorDist

        # SACO EL NODO DE MENOR DISTANCIA DE LA COLA

        nodosSinVisitar.pop(nodoMenorDist)

        # SI LLEGA AL DESTINO ACABA EL WHILE

    nodoActual = destino

    # RETORNO EL NODOACUTAL, ES DECIR DESTINO, PARA PODER HACER BACKTRACKING LUEGO, LAS DISTANCIAS TENTATIVAS Y LOS PADRES DE CADA NODO

    return dist,nodoActual,prev

###########################################################
# DEVUELVE ARRAY CON LAS HABITACIONES DEL CAMINO SOLUCION #
###########################################################

def retornaCaminoSol(inicio,nodoAct,prev):
    caminoSolucion = []
    flag = True                                 # FLAG QUE NOS DICE SI EXISTE O NO SOLUCION
    while nodoAct != inicio:                     # COMIENZA EL BACKTRACKING
        try:
            caminoSolucion.insert(0,nodoAct)     # VA INSERTANDO EN EL ARRAY, LAS HABITACIONES QUE FORMAN PARTE DE ESTE CAMINO SOLUCION
            nodoAct = prev[nodoAct]
        except KeyError:                        # SI FALLA, NO ENCUENTRA LA CLAVE QUIERE DECIR QUE NO EXISTE CAMINO ENTRE LA HABITACION DE INICIO Y LA DE DESTINO
            flag = False                        # FALSE PUESTO QUE NO TIENE SOLUCION
            break

    caminoSolucion.insert(0,inicio)             # POR ULTIMO INSERTA LA CASILLA INICIAL

    return caminoSolucion,flag


###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def listatraspasaAMatriz(mat,f,c,inicio,fin,camino_solucion,menordist,E):
    mat = np.zeros(((f*2)+1,(c*2)+1))

    # GENERA EL LABERINTO

    for i in range(0,(f)):
        for j in range(0,(c)):
            mat[i*2+1][j*2+1] = -5
            for n in range(13):
                if((i<f-1) and (id(i+1,j,c),n) in E[id(i,j,c)]):
                    mat[ i*2+2 ][ j*2+1 ] = -5
                if((j<c-1) and (id(i,j+1,c),n) in E[id(i,j,c)]):
                    mat[ i*2+1 ][ j*2+2 ] = -5
    
    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO, NI RECORRIDAS POR DIJKSTRA CON SU DISTANCIA TENTATIVA

    for n in menordist:
        valor = menordist[n]
        mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = valor
    
    # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO NI RECORRIDAS POR DIJKSTRA CON LA MENOR DE LAS DISTANCIAS TENTATIVAS

    for d in range(len(E)):
        for j in range(len(E[d])):

            # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR
             
            color = menorValor(menordist[d], menordist[E[d][j][0]])
            mat[int(((int((fila(d,c)))*2+1)+(int((fila(E[d][j][0],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(E[d][j][0],c)))*2+1))/2)] = color

    # PINTA LAS HABITACIONES DEL CAMINO SOLUCION

    for k in range(len(camino_solucion)):
        mat[int((fila(camino_solucion[k],c)))*2+1][int((columna(camino_solucion[k],c)))*2+1] = 500

    # PINTA LOS CAMINOS DE LAS HABTACIONES DEL CAMINO SOLUCION

    for m in range(len(camino_solucion)-1):
        mat[int(((int((fila(camino_solucion[m],c)))*2+1)+(int((fila(camino_solucion[m+1],c)))*2+1))/2)][int(((int((columna(camino_solucion[m],c)))*2+1)+(int((columna(camino_solucion[m+1],c)))*2+1))/2)] = 500
    
    # PINTA LA CASILLA DE INICIO Y FIN DEL CAMINO
    mat[int((fila(inicio,c)))*2+1][int((columna(inicio,c)))*2+1] = 550
    mat[int((fila(fin,c)))*2+1][int((columna(fin,c)))*2+1] = 550

    return mat

###############################################################################
# RETORNA LA MENOR DE LAS DOS DISTANCIAS TENTATIVAS QUE RECIBE COMO PARAMETRO #
###############################################################################

def menorValor(x,y):
    if(x <= y):
        return x
    else:
        return y


############################################
#############  M  A  I  N  #################
############################################

f = int(input("Introduce el tamaño de la f: "))
c = int(input("Introduce el tamaño de la c: "))
probabilidad = float(input("Introduce la probabilidad: "))

if(probabilidad < 0 or probabilidad > 1):
    print("Introduce una probabilidad entre 0 y 1")
    probabilidad = float(input("Introduce la probabilidad: "))

# SOLICITO LAS SEMILLAS

semilla = int(input("Semilla para la generacion del laberinto: "))
semilla2 = int(input("Semilla para los pesos de los ejes: "))
semilla3 = int(input("Semilla para el inicio/fin del recorrido: "))


numero3 = SyncRNG(seed = semilla3)


print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+\n")

graph = {}
matrizPintar = []
listaAdyacencia = {}

Inic = rellenaHabs(f,c)                                    # CREA LA LISTA DE ADYACENCIA PARA E
graph = rellenaNodos(f,c)                                  # CREA EL DICCIONARIO DE DICCIONARIOS

listaAdyacencia,graph = creaLaberintoLista(f,c,probabilidad,semilla,semilla2,graph,Inic)     # RELLENA LA LISTA DE ADYACENCIA, Y EL DICCIONARIO DE DICCIONARIOS (Graph)

# GENERO CON LA SEMILLA INTRODUCIDA LA HABITACION DE INICIO Y FIN DEL CAMINO

habitacionInicio = (numero3.randi() % (len(graph)))
habitacionFin = (numero3.randi() % (len(graph)))

if(habitacionFin == habitacionInicio):
    habitacionFin = (numero3.randi() % (len(graph)))


print("Casilla INICIO: ", habitacionInicio)
print("Casilla FIN: ", habitacionFin)
print("\n")

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA

#############
# ALGORITMO #
#############

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

menordist,currentNode,predecesores = dijkstra(graph,habitacionInicio,habitacionFin)  # SE LLEVA A CABO EL ALGORITMO

t1 = time.time()
t1 = t1-t0

##################################################################################

caminoSolucion, sepuede = retornaCaminoSol(habitacionInicio,currentNode,predecesores) # SE PUEDE CONTIENE EL FLAG ES DECIR, SI EXISTE UN CAMINO ENTRE ESOS 2 NODOS O NO
                                                                                      # CAMINOSOLUCION ES UN ARRAY CON LAS HABITACIONES DEL CAMINO

for clave in menordist:                                                               # RECORRO EL ARRAY DE DISTANCIAS TENTATIVAS PARA SUSTITUIR LA DISTANCIA TENTATIVA DE 
                                                                                      # LAS HABITACIONES POR DONDE EL ALGORITMO NO HA PASADO, SUSTITUYENDO EL 99999999 POR -1
    if(menordist[clave] > 99999):                                                     # Y EN LA MATRIZ SE HAN DIBUJADAS DE COLOR AZUL
        menordist[clave] = -1

if(sepuede == True):
    print("<---------- EXISTE CAMINO ---------->\n")
    print("Camino solucion =====> ", caminoSolucion)
    print("El tiempo el algoritmo DIJKSTRA NORMAL es: ",t1, " segundos")

    matrizPintar = listatraspasaAMatriz(matrizPintar,f,c,habitacionInicio,habitacionFin,caminoSolucion,menordist,listaAdyacencia)

    cmap=copy.copy(plt.get_cmap("inferno"))
    cmap.set_under("blue")                              # LAS CASILLAS CON VALOR INFERIOR A 0, SON PINTADAS DE COLOR AZUL

    sb.heatmap(matrizPintar,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=None, fmt="")
    plt.show()                                          # MUESTRA EL RESULTADO

else:
    print("No existe camino entre esos nodos")