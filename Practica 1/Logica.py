import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

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

#Ej: Regla 30 = 00011110 base 2
    #Si vemos la combinacion de las 3 celulas nos permite formar combinaciones y cada combinacion tiene un respectivo valor de celula de salida
    #En este caso 111 base 2 o 7 base 10 la salida es 0, por lo que tenemos
    #Output: [0 0 0 1 1 1 1 0]
    #Indice: [7 6 5 4 3 2 1 0] --Valor decimal de la combinacion que genera la salida
    #Es decir si tenemos el caso 7. Tomamos 7 (numero max obtenido de las combinaciones) le restamos nuestro caso para obtener 0 (indice del arreglo de salida)
    #Otro caso: Si tenemos el caso 3. 7 - 3 = 4 (indice en el arreglo de salida), salida 1
    #Return: Arreglo con indices para la regla de las combinaciones de las celulas
def IndiceRegla(tresCelulas):
    izq, centro, der = tresCelulas
    index = 7 - (4*izq + 2*centro + der) #Representacion binaria de las 3 celulas, Se resta 7 para coincidir con la representacion binaria de la regla
    return int(index)

def GenerarAutomataCelular(arreglo,nPasos, reglaNumero):
    global unosxPaso
    global probabilidadUnoxPaso
    reglaString = np.binary_repr(reglaNumero, width=8) #Representamos la regla ahora en base 2 como una cadena (8 bits) es un numero
    regla = np.array([int(bit) for bit in reglaString])
    arregloAutomataCelular = np.zeros((nPasos,len(arreglo)))
    unosxPaso = np.empty(nPasos, dtype = int)
    probabilidadUnoxPaso = np.empty(nPasos, dtype = float)
    arregloAutomataCelular[0,:] = arreglo #Fila 1
    unosxPaso[0] = np.count_nonzero(arregloAutomataCelular[0,:] == 1)
    probabilidadUnoxPaso[0] = unosxPaso[0] / len(arreglo)
    for pasos in range (1,nPasos):
        combinaciones3Celulas = np.stack(
            [ 
                np.roll(arregloAutomataCelular[pasos - 1, :], 1), #Movemos a la derecha nuestro arreglo
                arregloAutomataCelular[pasos - 1, :], # t actual
                np.roll(arregloAutomataCelular[pasos - 1, :], -1),#Movemos a la izquierda nuestro arreglo
            ]
        )#Obtenemos nuestras combinaciones posibles de 3 celulas
        arregloAutomataCelular[pasos,:] = regla[np.apply_along_axis(IndiceRegla, 0, combinaciones3Celulas)]#Toma las 3 columnas, para llamar la funcion indiceRegla
        #despues empareja cada valor de nuestros indices con el valor en la regla 30, guardamos en el arreglo final
        unosxPaso[pasos] = np.count_nonzero(arregloAutomataCelular[pasos,:] == 1)
        probabilidadUnoxPaso[pasos] = unosxPaso[pasos] / len(arreglo)
    return arregloAutomataCelular

def IniciarArchivo(Color0, Color1, Pasos, Regla, CelulasIniciales):
    global resultadoAutomata
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    ax.axis(False)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()

def IniciarRandom(Color0, Color1, Pasos, Regla, TamanioAutomata):
    global resultadoAutomata
    CelulasIniciales = np.random.randint(2, size=TamanioAutomata)
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
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
    CelulasIniciales = np.random.choice([0,1], TamanioAutomata, p =[1-LugaresUnos, LugaresUnos])
    resultadoAutomata = GenerarAutomataCelular(CelulasIniciales,Pasos,Regla)
    GraficaDensidad()
    GraficaLog10()
    GraficaMedia()
    GraficaVarianza()
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    fig, ax = plt.subplots(figsize=(16, 9))
    im = ax.matshow(resultadoAutomata,cmap=cmap)
    ax.axis(False)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1)
    plt.colorbar(im, cax=cax)
    plt.show()