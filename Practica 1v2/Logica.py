import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation

global unosxPaso 
global probabilidadUnoxPaso

def GraficaVarianza():#Momento 2 = Sum(x^2*f(x)) - E[x]^2=> Momento 2 = 0*f(x) + 1*f(x) - (1*f(x=1))^2 = f(x=1) - f(x=1)^2
    global probabilidadUnoxPaso
    plot4 = plt.figure(3)
    plt.title("Variance or second moment")  
    plt.xlabel("Steps")  
    plt.ylabel("Variance")
    plt.plot(probabilidadUnoxPaso-np.power(probabilidadUnoxPaso,2), color ="purple") 

def GraficaMedia():#E[x] = Sum(x*f(x))=> E[x] = 0*f(x) + 1*f(x) = f(x=1) = Probabilidad de X=1, osea Probabilidad de uno
    global probabilidadUnoxPaso
    plot3 = plt.figure(2)
    plt.title("Expected value or average")  
    plt.xlabel("Steps")  
    plt.ylabel("Expected value")
    plt.plot(probabilidadUnoxPaso, color ="green") 
      
def GraficaDensidad():
    global unosxPaso
    plot1 = plt.figure(0)
    plt.title("Numbers of 1's for each step")  
    plt.xlabel("Steps")  
    plt.ylabel("Numbers of 1's")
    plt.plot(unosxPaso, color ="red") 

def GraficaLog10():
    global unosxPaso
    plot2 = plt.figure(1)
    plt.title("Log10(Numbers of 1's for each step)")  
    plt.xlabel("Steps")  
    plt.ylabel("Log10(Numbers of 1's)")
    plt.plot(np.log10(unosxPaso), color ="blue") 

def GraficaDensidadColCentral():
    indexColCentral = int(len(resultadoAutomata[1])/2-1) 
    datosColCentral= resultadoAutomata[:,indexColCentral]
    finalDatos = np.zeros((len(datosColCentral),1))
    finalDatos[0] = datosColCentral[0]
    for pasos in range (1,len(datosColCentral)):
        finalDatos[pasos] = finalDatos[pasos-1] + datosColCentral[pasos]
    #print(finalDatos)
    plot1 = plt.figure(4)
    plt.title("Central column density")  
    plt.xlabel("Steps")  
    plt.ylabel("Value")
    plt.plot(finalDatos, color ="black") 

"""     Ej: Regla 30 = 00011110 base 2
    Si vemos la combinacion de las 3 celulas nos permite formar combinaciones y cada combinacion tiene un respectivo valor de celula de salida
    En este caso 111 base 2 o 7 base 10 la salida es 0, por lo que tenemos
    Output: [0 0 0 1 1 1 1 0]
    Indice: [7 6 5 4 3 2 1 0] --Valor decimal de la combinacion que genera la salida
    Es decir si tenemos el caso 7. Tomamos 7 (numero max obtenido de las combinaciones) le restamos nuestro caso para obtener 0 (indice del arreglo de salida)
    Otro caso: Si tenemos el caso 3. 7 - 3 = 4 (indice en el arreglo de salida), salida 1
    Return: Arreglo con indices para la regla de las combinaciones de las celulas
def IndiceRegla(tresCelulas):
    izq, centro, der = tresCelulas
    index = 7 - (4*izq + 2*centro + der) #Representacion binaria de las 3 celulas, Se resta 7 para coincidir con la representacion binaria de la regla
    return int(index) """

# Hacemos el calculo por el paso correspondiente, juntamos la parte de obtener las 3 combinaciones posibles y la fun Indice regla
# esto provoca optimizar el codigo, pasamos de 3.3 s para el calculo de un ECA de 1kx1k a 0.07s
u = np.array([[4], [2], [1]]) #Arreglo para comvertir binario a decimal
def calculoPaso(x, regla):
    combinaciones3Celulas = np.vstack((np.roll(x, 1), x,
                   np.roll(x, -1))).astype(np.int8) #
    z = np.sum(combinaciones3Celulas * u, axis=0).astype(np.int8)#Representancion de las 3 celulas, int8 array
    return regla[7 - z] #Valor de z en la regla

def GenerarAutomataCelular(arreglo,nPasos, reglaNumero):
    global unosxPaso
    global probabilidadUnoxPaso
    reglaString = np.binary_repr(reglaNumero, width=8) #Representamos la regla ahora en base 2 como una cadena (8 bits) es un numero
    regla = np.array([int(bit) for bit in reglaString]).astype(np.int8)
    arregloAutomataCelular = np.zeros((nPasos,len(arreglo))).astype(np.int8)
    unosxPaso = np.empty(nPasos, dtype = int).astype(np.int8)
    probabilidadUnoxPaso = np.empty(nPasos, dtype = float).astype(np.int8)
    arregloAutomataCelular[0,:] = arreglo #Fila 1
    for pasos in range (1,nPasos):
        arregloAutomataCelular[pasos,:] = calculoPaso(arregloAutomataCelular[pasos-1,:],regla)#Toma las 3 columnas, para llamar la funcion indiceRegla
        #despues empareja cada valor de nuestros indices con el valor en la regla 30, guardamos en el arreglo final
    unosxPaso = np.count_nonzero(arregloAutomataCelular == 1, axis=1)
    probabilidadUnoxPaso = unosxPaso / len(arreglo)
    return arregloAutomataCelular

def IniciarArchivo(Color0, Color1, Pasos, Regla, CelulasIniciales):
    global resultadoAutomata
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla).astype(np.int8)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    GraficaDensidadColCentral()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    ax.axis(False)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()

def Mierda(i,ax,cmap):
    xd = resultadoAutomata[0:i,:]
    ax.imshow(xd,cmap=cmap)
    
def IniciarRandom(Color0, Color1, Pasos, Regla, TamanioAutomata):
    global resultadoAutomata
    CelulasIniciales = np.random.randint(2, size=TamanioAutomata).astype(np.int8)
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla).astype(np.int8)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    GraficaDensidadColCentral()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    #anim = FuncAnimation(fig, Mierda, frames=np.arange(0, Pasos), fargs=(ax,cmap,),interval=200,repeat=False)
    ax.axis(False)  
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()

def IniciarEspecifico(Color0, Color1, Pasos, Regla, TamanioAutomata, LugaresUnos):
    global resultadoAutomata
    CelulasIniciales = np.zeros((TamanioAutomata,), dtype=int) 
    for i in LugaresUnos:
        CelulasIniciales[i] = 1 
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    GraficaDensidadColCentral()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    ax.axis(False)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()

def IniciarProbabilidad(Color0, Color1, Pasos, Regla, TamanioAutomata, LugaresUnos):
    global resultadoAutomata
    CelulasIniciales = np.random.choice([0,1], TamanioAutomata, p =[1-LugaresUnos, LugaresUnos]).astype(np.int8)
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla).astype(np.int8)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    GraficaDensidadColCentral()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    ax.axis(False)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()