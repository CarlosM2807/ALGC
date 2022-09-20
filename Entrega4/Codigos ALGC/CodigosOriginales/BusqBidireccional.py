import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys
import queue

# DIJKSTRA NORMAL

def fila(ind, c):
    return ind/c

def columna(ind, c):
    return ind%c

def id(fil, col, c):
    return fil*c + col


#######################
# RELLENA DICCIONARIO #
#######################

def completaDiccionario(diccionarioEntero,clave,hijo,peso):
    if clave not in diccionarioEntero:
        diccionarioEntero[clave] = {}
    diccionarioEntero[clave][hijo] = peso
    return diccionarioEntero

##########################################################
# GENERA EL LABERINTO (LOS EJES) CON LISTA DE ADYACENCIA #
##########################################################

# GRAPH, UN DICCIONARIO DE DICCIONARIOS (QUE CONTIENE LOS NODOS HIJOS CON SUS PESOS)

def creaLaberintoLista(f,c,prob,semilla,semilla2):
    graph={}
    numero = SyncRNG(seed = semilla)
    numero2 = SyncRNG(seed = semilla2)
    for i in range(f):
        for j in range(c):
            if(i>0 and numero.rand()<prob):
                pesoEje = numero2.randi()%12+1
                graph = completaDiccionario(graph,id(i, j, c),id(i-1, j, c),pesoEje)
                graph = completaDiccionario(graph,id(i-1, j, c),id(i, j, c),pesoEje)
            if(j>0 and numero.rand()<prob):
                pesoEje = numero2.randi()%12+1
                graph = completaDiccionario(graph,id(i, j, c),id(i, j-1, c),pesoEje)
                graph = completaDiccionario(graph,id(i, j-1, c),id(i, j, c),pesoEje)
    return graph


#########################
# ALGORITMO DE DIJKSTRA #
#######################################################
# MISMO QUE DIJKSTRA PERO CON 2 COLAS PERO TOD0 IGUAL #
#######################################################

def dijkstra(graph,inicio,destino):
    dist = {}
    prev = {}
    cola = queue.PriorityQueue()  # CREAMOS LA COLA DE PRIORIDAD

    dist2 = {}
    prev2 = {}
    cola2 = queue.PriorityQueue()

    infinity = 999999999
    dist[inicio] = 0
    dist2[destino] = 0
    recorridos = []

    for vertex in graph:
        if(vertex != inicio):
            dist[vertex] = infinity
            prev[vertex] = None
        cola.put((infinity,vertex))          # RELLENO LA COLA DE PRIORIDAD
    cola.put((0,inicio))                     # PRIORIDAD 0 AL NODO INCIAL

    for vertex in graph:
        if(vertex != destino):
            dist2[vertex] = infinity
            prev2[vertex] = None
        cola2.put((infinity,vertex))
    cola2.put((0,destino))

    
    # MIENTRAS LA COLA NO ESTE VACIA

    while(cola and cola2):

        # OBTENGO EL NODO DE MENOR DISTANCIA TENTATIVA QUE ESTE EN LA COLA (nodoMenorDist)
        # EN ESTE CASO EL MAS ARRIBA DE LA COLA DE PRIORIDAD

        u = cola.get()
        u2 = cola2.get()

        # OBTENGO SUS HIJOS

        hijos = graph[u[1]].items()
        hijos2 = graph[u2[1]].items()

        # GUARDO VA RECORRIENDO LA COLA 1

        recorridos.append(u[1])

        # COMPRUEBA SI YA ESTA RECORRIDA, Y SI LO ESTA PARA

        if(u2[1] in recorridos):
            casillaCorte = u2[1]
            break

        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF
        
        for v,peso in hijos:
            if peso+dist[u[1]] < dist[v]:
                dist[v] = peso + dist[u[1]]
                prev[v] = u[1]
                cola.put((dist[u[1]]+peso,v))

        for v,peso in hijos2:
            if peso+dist2[u2[1]] < dist2[v]:
                dist2[v] = peso + dist2[u2[1]]
                prev2[v] = u2[1]
                cola2.put((dist2[u2[1]]+peso,v))
        
        # SI LLEGA AL DESTINO ACABA EL WHILE
        
        if(u[1] == destino):
            break
        if(u2[1] == inicio):
            break

    # RETORNO EL NODOACUTAL, ES DECIR DESTINO, PARA PODER HACER BACKTRACKING LUEGO, LAS DISTANCIAS TENTATIVAS Y LOS PADRES DE CADA NODO

    return dist,prev,dist2,prev2,casillaCorte,u2[1]

########################################3####################
# A* IGUAL PERO AÑADIENDO LO MISMO QUE EN DIJKSTRA ANTERIOR #
#############################################################

def astar(graph,inicio,destino):
    dist = {}
    prev = {}
    cola = queue.PriorityQueue()  # CREAMOS LA COLA DE PRIORIDAD

    dist2 = {}
    prev2 = {}
    cola2 = queue.PriorityQueue()

    infinity = 999999999
    dist[inicio] = 0
    dist2[destino] = 0
    recorridos = []

    for vertex in graph:
        if(vertex != inicio):
            dist[vertex] = infinity
            prev[vertex] = None
        cola.put((infinity,vertex))          # RELLENO LA COLA DE PRIORIDAD
    cola.put((0,inicio))                     # PRIORIDAD 0 AL NODO INCIAL

    for vertex in graph:
        if(vertex != destino):
            dist2[vertex] = infinity
            prev2[vertex] = None
        cola2.put((infinity,vertex))
    cola2.put((0,destino))

    
    # MIENTRAS LA COLA NO ESTE VACIA

    while(cola and cola2):

        # OBTENGO EL NODO DE MENOR DISTANCIA TENTATIVA QUE ESTE EN LA COLA (nodoMenorDist)
        # EN ESTE CASO EL MAS ARRIBA DE LA COLA DE PRIORIDAD

        u = cola.get()
        u2 = cola2.get()

        # OBTENGO SUS HIJOS

        hijos = graph[u[1]].items()
        hijos2 = graph[u2[1]].items()

        # GUARDO VA RECORRIENDO LA COLA 1

        recorridos.append(u[1])

        if(u2[1] in recorridos):
            casillaCorte = u2[1]
            break
        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF
        

        for v,peso in hijos:
            if peso+dist[u[1]] < dist[v]:
                dist[v] = peso + dist[u[1]]
                prev[v] = u[1]
                cola.put((dist[u[1]]+distManhattan(u[1],destino),v))

        for v,peso in hijos2:
            if peso+dist2[u2[1]] < dist2[v]:
                dist2[v] = peso + dist2[u2[1]]
                prev2[v] = u2[1]
                cola2.put((dist2[u2[1]]+distManhattan(u2[1],destino),v))

        # SI LLEGA AL DESTINO ACABA EL WHILE
        
        if(u[1] == destino):
            break
        if(u2[1] == inicio):
            break

    # RETORNO EL NODOACUTAL, ES DECIR DESTINO, PARA PODER HACER BACKTRACKING LUEGO, LAS DISTANCIAS TENTATIVAS Y LOS PADRES DE CADA NODO

    return dist,prev,dist2,prev2,casillaCorte,u2[1]


######################################################
# HALLA LA DISTANCIA DE MANHATTAN (NUEVA HEURISTICA) #
######################################################

def distManhattan(nodo, destino):

    nodox = int((fila(nodo,c)))
    nodoy = int((columna(nodo,c)))
    destinox = int((fila(destino,c)))
    destinoy = int((columna(destino,c)))

    return (abs(nodox-destinox) + abs(nodoy-destinoy))

###########################################################
# DEVUELVE ARRAY CON LAS HABITACIONES DEL CAMINO SOLUCION #
###########################################################

def retornaCaminoSol(inicio,corte,prev):
    caminoSolucion = []
    flag = True                                 # FLAG QUE NOS DICE SI EXISTE O NO SOLUCION
    while corte != inicio:                     # COMIENZA EL BACKTRACKING
        try:
            caminoSolucion.insert(0,corte)     # VA INSERTANDO EN EL ARRAY, LAS HABITACIONES QUE FORMAN PARTE DE ESTE CAMINO SOLUCION
            corte = prev[corte]

        except KeyError:                        # SI FALLA, NO ENCUENTRA LA CLAVE QUIERE DECIR QUE NO EXISTE CAMINO ENTRE LA HABITACION DE INICIO Y LA DE DESTINO
            flag = False                        # FALSE PUESTO QUE NO TIENE SOLUCION
            break
    
    caminoSolucion.insert(0,inicio)             # POR ULTIMO INSERTA LA CASILLA INICIAL
    
    return caminoSolucion,flag

###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def listatraspasaAMatriz(mat,f,c,inicio,fin,camino_solucion,E,menordist,menordist2,sep):
    mat = np.zeros(((f*2)+1,(c*2)+1))
    
    # GENERA EL LABERINTO

    for i in range(0,(f)):
        for j in range(0,(c)):
            mat[i*2+1][j*2+1] = -5
            for n in range(13):
                if((i<f-1) and E.get(id(i+1,j,c)) and (id(i,j, c) in E.get(id(i+1,j,c)))):
                    mat[ i*2+2 ][ j*2+1 ] = -5
                if((j<c-1) and E.get(id(i, j+1, c)) and (id(i, j, c) in E.get(id(i, j+1, c)))):
                    mat[ i*2+1 ][ j*2+2 ] = -5
    
    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO, PERO RECORRIDAS POR DIJKSTRA CON SU DISTANCIA TENTATIVA
    # PARA LOS RESULTADOS OBTENIDOS CON COLA 1

    for n in menordist:
        color = menordist[n]
        mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = color
    
    # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO PERO RECORRIDAS POR DIJKSTRA CON LA MENOR DE LAS DISTANCIAS TENTATIVAS PARA LA COLA 1

    for d in range(len(E)):
        if(d in E):
            for j in range(len(E[d])):

                # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR
                
                color = menorValor(menordist[d], menordist[list(E[d].keys())[j]])
                mat[int(((int((fila(d,c)))*2+1)+(int((fila(list(E[d].keys())[j],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(list(E[d].keys())[j],c)))*2+1))/2)] = color


    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO, PERO RECORRIDAS POR DIJKSTRA CON SU DISTANCIA TENTATIVA
    # PARA LOS RESULTADOS OBTENIDOS CON COLA 2

    for n in menordist2:
        color = menordist2[n]
        if(color == -1):   # SI ES -1 YA ESTA PINTADO POR LA COLA 1 ENTONCES PASS
            pass
        else:
            mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = color
    
   # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO PERO RECORRIDAS POR DIJKSTRA CON LA MENOR DE LAS DISTANCIAS TENTATIVAS PARA LA COLA 2

    for d in range(len(E)):
        if(d in E):
            for j in range(len(E[d])):

                # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR
                
                color = menorValor(menordist2[d], menordist2[list(E[d].keys())[j]])
                if(color == -1):            # SI ES -1 YA ESTA PINTADO POR LA COLA 1 ENTONCES PASS
                    pass
                else:
                    mat[int(((int((fila(d,c)))*2+1)+(int((fila(list(E[d].keys())[j],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(list(E[d].keys())[j],c)))*2+1))/2)] = color


    # PINTA LAS HABITACIONES DEL CAMINO SOLUCION

    for k in range(len(camino_solucion)):
        mat[int((fila(camino_solucion[k],c)))*2+1][int((columna(camino_solucion[k],c)))*2+1] = 250

    # PINTA LOS CAMINOS DE LAS HABTACIONES DEL CAMINO SOLUCION
   
    for m in range(len(camino_solucion)-1):

        if(m == sep):           # SI LA HABITACION ES LA DE SEPARACION ENTRE CAMINO 1 Y CAMINO 2, ENTONCES PASS, YA QUE TOMA 2 HABITACIONES QUE NO SON PADRE E HIJO ENTONCES PINTA CAMINO INCORRECTO
            pass
        else:
            mat[int(((int((fila(camino_solucion[m],c)))*2+1)+(int((fila(camino_solucion[m+1],c)))*2+1))/2)][int(((int((columna(camino_solucion[m],c)))*2+1)+(int((columna(camino_solucion[m+1],c)))*2+1))/2)] = 250

    # PINTA LA CASILLA DE INICIO Y FIN DEL CAMINO
    
    mat[int((fila(inicio,c)))*2+1][int((columna(inicio,c)))*2+1] = 280
    mat[int((fila(fin,c)))*2+1][int((columna(fin,c)))*2+1] = 280

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

eleccion = int(input("INTRODUCE --------> 0 PARA DIJKSTRA // 1 PARA A* :"))

numero3 = SyncRNG(seed = semilla3)


print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+\n")

graph = {}
matrizPintar = []

t3 = time.time() 

graph = creaLaberintoLista(f,c,probabilidad,semilla,semilla2)     # RELLENA LA LISTA DE ADYACENCIA, Y EL DICCIONARIO DE DICCIONARIOS (Graph)

t2 = time.time()
t3 = t2-t3

# GENERO CON LA SEMILLA INTRODUCIDA LA HABITACION DE INICIO Y FIN DEL CAMINO

habitacionInicio = (numero3.randi() % (f*c))
habitacionFin = (numero3.randi() % (f*c))

if(habitacionFin == habitacionInicio):
    habitacionFin = (numero3.randi() % (f*c))

print("Casilla INICIO: ", habitacionInicio)
print("Casilla FIN: ", habitacionFin)
print("\n")

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA

##############
# ALGORITMOS #
##############

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

if(eleccion == 0):
    menor_distancia,predecesores,menor_distancia2,predecesores2,casillaCorte, encuentra = dijkstra(graph,habitacionInicio,habitacionFin)   # SE LLEVA A CABO EL ALGORITMO
if(eleccion == 1):
    menor_distancia,predecesores,menor_distancia2,predecesores2,casillaCorte, encuentra = astar(graph,habitacionInicio,habitacionFin)   # SE LLEVA A CABO EL ALGORITMO

##################################################################################

caminoSolucion,sepuede = retornaCaminoSol(habitacionInicio,casillaCorte,predecesores)    # CAMINO 1 ---> COLA 1

separacionCaminos = len(caminoSolucion)-1 # TIENE LA HABITACION O NODO DONDE SE PASA DE UN CAMINO A OTRO, PARA QUE POSTERIORMENTE EL PASILLO DE ESA HABITACION CON LA SIGUIENTE NO SE PINTE

caminoSolucion2,sepuede2 = retornaCaminoSol(habitacionFin,casillaCorte,predecesores2)    # CAMINO 2 ---> COLA 2

caminoSolucion.extend(caminoSolucion2)                  # FUSION EN UN UNICO CAMINO

t1 = time.time()
t1 = t1-t0


for clave in menor_distancia:                    # RECORRO EL ARRAY DE DISTANCIAS TENTATIVAS PARA SUSTITUIR LA DISTANCIA TENTATIVA DE                                                 # LAS HABITACIONES POR DONDE EL ALGORITMO NO HA PASADO, SUSTITUYENDO EL 99999999 POR -1
    if(menor_distancia[clave] > 99999):          # Y EN LA MATRIZ SE HAN DIBUJADAS DE COLOR AZUL
        menor_distancia[clave] = -1

for clave in menor_distancia2:
    if(menor_distancia2[clave] > 99999):
        menor_distancia2[clave] = -1


if(sepuede == True  and sepuede2 == True):
    print("<---------- EXISTE CAMINO ---------->\n")

    print("Camino solucion =====> ", caminoSolucion)
    print("\nEl tiempo en generar la estructura del grafo es: ", t3, " segundos")
    print("\nEl tiempo del algoritmo DIJKSTRA BUSQUEDA BIDIRECCIONAL es: ",t1, " segundos")
                                                                                                                            
    matrizPintar = listatraspasaAMatriz(matrizPintar,f,c,habitacionInicio,habitacionFin,caminoSolucion,graph,menor_distancia,menor_distancia2,separacionCaminos)

    cmap=copy.copy(plt.get_cmap("inferno"))
    cmap.set_under("blue")                          # LAS CASILLAS CON VALOR INFERIOR A 0, SON PINTADAS DE COLOR AZUL

    sb.heatmap(matrizPintar,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=None, fmt="")
    plt.show()                                      # MUESTRA EL RESULTADO

else:
    print("No existe camino entre esos nodos")