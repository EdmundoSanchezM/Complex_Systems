import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation

global unosxPaso 
global probabilidadUnoxPaso 
global anim_automata
global anim_densidad
global anim_log10
global anim_media
global anim_varianza
global anim_densidad_central
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
    global automataCelular
    indexColCentral = int(len(automataCelular[1])/2-1) 
    datosColCentral= automataCelular[:,indexColCentral]
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

# Hacemos el calculo por el paso correspondiente, juntamos la parte de obtener las 3 combinaciones posibles y la fun Indice regla
# esto provoca optimizar el codigo, pasamos de 3.3 s para el calculo de un ECA de 1kx1k a 0.07s
u = np.array([[4], [2], [1]]) #Arreglo para comvertir binario a decimal
def calculoPaso(x, regla):
    combinaciones3Celulas = np.vstack((np.roll(x, 1), x,
                   np.roll(x, -1))).astype(np.int8) #
    z = np.sum(combinaciones3Celulas * u, axis=0).astype(np.int8)#Representancion de las 3 celulas, int8 array
    return regla[7 - z] #Valor de z en la regla

def Animation_Automata(i):
    if(i!=0):
        automataCelular[i,:] = calculoPaso(automataCelular[i-1,:],regla).astype(np.int8)#Toma las 3 columnas, para llamar la funcion indiceRegla
        cax1.set_array(automataCelular)
        return cax1,

def Animation_Densidad(i):
    global unosxPaso 
    unosxPaso = np.count_nonzero(automataCelular == 1, axis=1)
    valor_y_densidad.append(unosxPaso[i])
    valor_x.append(i)
    ax1.plot(valor_x,valor_y_densidad, color ="red")
    return ax1,

def Animation_Log10(i):
    global unosxPaso 
    valor_y_log10.append(np.log10(unosxPaso[i]))
    ax2.plot(valor_x,valor_y_log10, color ="blue")
    return ax2,

def Animation_Varianza(i):
    global unosxPaso
    global probabilidadUnoxPaso
    valor_y_varianza.append(probabilidadUnoxPaso[i]-np.power(probabilidadUnoxPaso[i],2))
    ax3.plot(valor_x,valor_y_varianza, color ="purple")
    return ax3,

def Animation_Media(i,len_arreglo):
    global unosxPaso
    global probabilidadUnoxPaso
    probabilidadUnoxPaso = unosxPaso / len_arreglo
    valor_y_media.append(probabilidadUnoxPaso[i])
    ax4.plot(valor_x,valor_y_media, color ="green")
    return ax4,

def Animation_DensidadColCentral(i,indexColCentral):
    global automataCelular
    datosColCentral= automataCelular[:,indexColCentral]
    if (i == 0 and len(valor_y_densidad_central)!=1):
        valor_x_densidad_central.append(i)
        valor_y_densidad_central.append(datosColCentral[0])
    if (i > 0):
        valor_x_densidad_central.append(i)
        valor_y_densidad_central.append(valor_y_densidad_central[i-1] + datosColCentral[i])
    ax5.plot(valor_x_densidad_central,valor_y_densidad_central, color ="black")
    return ax5,

def GenerarAutomataCelular(arreglo,nPasos, reglaNumero,cmap,isAnimado):
    global probabilidadUnoxPaso
    global unosxPaso
    global automataCelular
    global regla
    #-Variables anim
    global anim_automata
    global anim_densidad
    global anim_log10
    global anim_media
    global anim_varianza
    global anim_densidad_central
    #-Variables globales para animacion
    global cax1
    global ax1
    global ax2
    global ax3
    global ax4
    global ax5
    global valor_x
    global valor_x_densidad_central
    global valor_y_densidad
    global valor_y_log10
    global valor_y_varianza
    global valor_y_media
    global valor_y_densidad_central
    valor_y_densidad = []
    valor_y_log10 = []
    valor_y_varianza = []
    valor_y_media = []
    valor_y_densidad_central = []
    valor_x = []
    valor_x_densidad_central=[]
    #-------
    reglaString = np.binary_repr(reglaNumero, width=8) #Representamos la regla ahora en base 2 como una cadena (8 bits) es un numero
    regla = np.array([int(bit) for bit in reglaString]).astype(np.int8)
    automataCelular = np.zeros((nPasos,len(arreglo))).astype(np.int8)
    probabilidadUnoxPaso = np.empty(nPasos, dtype = float).astype(np.int8)
    automataCelular[0,:] = arreglo #Fila 1
    if(isAnimado==1):
        #--Grafica automata--#
        fig,ax = plt.subplots(figsize=(16, 9))
        cax1 = ax.matshow(automataCelular, cmap=cmap)
        ax.axis(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(cax1, cax=cax)
        #--Grafica densidad--#
        plot1 = plt.figure(0)
        ax1 = plt.subplot()
        plot1.suptitle("Numbers of 1's for each step") 
        plt.xlabel("Steps")  
        plt.ylabel("Numbers of 1's")
        #--Grafica log10--#
        plot2 = plt.figure(2)
        ax2 = plt.subplot()
        plt.title("Log10(Numbers of 1's for each step)")  
        plt.xlabel("Steps")  
        plt.ylabel("Log10(Numbers of 1's)")
        #--Grafica Media--#
        plot4 = plt.figure(3)
        ax4 = plt.subplot()
        plt.title("Expected value or average")  
        plt.xlabel("Steps")  
        plt.ylabel("Expected value")
        #--Grafica Varianza--#
        plot3 = plt.figure(4)
        ax3 = plt.subplot()
        plt.title("Variance or second moment")  
        plt.xlabel("Steps")  
        plt.ylabel("Variance")
        #--Grafica Densidad central--#
        plot5 = plt.figure(5)
        ax5 = plt.subplot()
        plt.title("Central column density")  
        plt.xlabel("Steps")  
        plt.ylabel("Value")
        indexColCentral = int(len(automataCelular[0])/2-1) 
        #--Animaciones--#
        anim_automata = FuncAnimation(fig, Animation_Automata, frames=nPasos,interval=8,repeat=False)
        anim_densidad = FuncAnimation(plot1, Animation_Densidad, frames=nPasos,interval=8,repeat=False)
        anim_log10 = FuncAnimation(plot2, Animation_Log10, frames=nPasos,interval=8,repeat=False)
        anim_media = FuncAnimation(plot4, Animation_Media, fargs=(len(arreglo),), frames=nPasos,interval=8,repeat=False)
        anim_varianza = FuncAnimation(plot3, Animation_Varianza, frames=nPasos,interval=8,repeat=False)
        anim_densidad_central = FuncAnimation(plot5, Animation_DensidadColCentral, fargs=(indexColCentral,), frames=nPasos,interval=8,repeat=False)
        plt.show()
    else:
        for pasos in range (1,nPasos):
            automataCelular[pasos,:] = calculoPaso(automataCelular[pasos-1,:],regla)#Toma las 3 columnas, para llamar la funcion indiceRegla
        #despues empareja cada valor de nuestros indices con el valor en la regla 30, guardamos en el arreglo final
        unosxPaso = np.count_nonzero(automataCelular == 1, axis=1)
        probabilidadUnoxPaso = unosxPaso / len(arreglo)

def IniciarArchivo(Color0, Color1, Pasos, Regla, CelulasIniciales,isAnimado):
    CelulasIniciales = CelulasIniciales.astype(np.int8)
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    GenerarAutomataCelular(CelulasIniciales,Pasos,Regla,cmap,isAnimado)
    if(isAnimado==0):
        GraficaDensidad()
        GraficaLog10()
        GraficaMedia()
        GraficaVarianza()
        GraficaDensidadColCentral()
        cmap = colors.ListedColormap([Color0, Color1]) #0,1
        fig, ax = plt.subplots(figsize=(16, 9))
        im = ax.matshow(automataCelular,cmap=cmap)
        ax.axis(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()

def IniciarRandom(Color0, Color1, Pasos, Regla, TamanioAutomata, isAnimado):
    CelulasIniciales = np.random.randint(2, size=TamanioAutomata).astype(np.int8)
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    GenerarAutomataCelular(CelulasIniciales,Pasos,Regla,cmap,isAnimado)
    if(isAnimado==0):
        GraficaDensidad()
        GraficaLog10()
        GraficaMedia()
        GraficaVarianza()
        GraficaDensidadColCentral()
        cmap = colors.ListedColormap([Color0, Color1]) #0,1
        fig, ax = plt.subplots(figsize=(16, 9))
        im = ax.matshow(automataCelular,cmap=cmap)
        ax.axis(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()
    
def IniciarEspecifico(Color0, Color1, Pasos, Regla, TamanioAutomata, LugaresUnos, isAnimado):
    CelulasIniciales = np.zeros((TamanioAutomata,), dtype=int) 
    for i in LugaresUnos:
        CelulasIniciales[i] = 1 
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    GenerarAutomataCelular(CelulasIniciales,Pasos,Regla,cmap,isAnimado)
    if(isAnimado==0):
        GraficaDensidad()
        GraficaLog10()
        GraficaMedia()
        GraficaVarianza()
        GraficaDensidadColCentral()
        cmap = colors.ListedColormap([Color0, Color1]) #0,1
        fig, ax = plt.subplots(figsize=(16, 9))
        im = ax.matshow(automataCelular,cmap=cmap)
        ax.axis(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()

def IniciarProbabilidad(Color0, Color1, Pasos, Regla, TamanioAutomata, LugaresUnos,isAnimado):
    CelulasIniciales = np.random.choice([0,1], TamanioAutomata, p =[1-LugaresUnos, LugaresUnos]).astype(np.int8)
    cmap = colors.ListedColormap([Color0, Color1]) #0,1
    GenerarAutomataCelular(CelulasIniciales,Pasos,Regla,cmap,isAnimado)
    if(isAnimado==0):
        GraficaDensidad()
        GraficaLog10()
        GraficaMedia()
        GraficaVarianza()
        GraficaDensidadColCentral()
        cmap = colors.ListedColormap([Color0, Color1]) #0,1
        fig, ax = plt.subplots(figsize=(16, 9))
        im = ax.matshow(automataCelular,cmap=cmap)
        ax.axis(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()