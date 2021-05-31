import numpy as np
import time
import networkx as nx
import os

# Hacemos el calculo por el paso correspondiente, juntamos la parte de obtener las 3 combinaciones posibles y la fun Indice regla
# esto provoca optimizar el codigo, pasamos de 3.3 s para el calculo de un ECA de 1kx1k a 0.07s
u = np.array([[4], [2], [1]])  # Arreglo para comvertir binario a decimal


def calculoPaso(x, regla):
    combinaciones3Celulas = np.vstack((np.roll(x, 1), x,
                                       np.roll(x, -1))).astype(np.int8)
    # Representancion de las 3 celulas, int8 array
    z = np.sum(combinaciones3Celulas * u, axis=0).astype(np.int8)
    return regla[7 - z]  # Valor de z en la regla


def AutomataCelular(arreglo, regla):
    pasada = arreglo
    final = []
    condicion = True
    while condicion:
        # Toma las 3 columnas, para llamar la funcion indiceRegla
        actual = calculoPaso(pasada, regla)
        pasada = actual
        final = actual
        if ((actual == pasada).all()):
            condicion = False
    return [arreglo.tolist(), final.tolist()]


def CalculadoraCombinaciones(longitud):
    # Producto cartesiano de 0,1 de con longitud n.
    return np.array([0, 1])[np.rollaxis(
        np.indices((len([0, 1]),) * longitud), 0, longitud + 1)
        .reshape(-1, longitud)]


def regla_representacion(reglaNumero):
    reglaString = np.binary_repr(reglaNumero, width=8)
    return np.array([int(bit) for bit in reglaString]).astype(np.int8)


def ListaBinariatoNumero(lista):
    return int("".join(str(i) for i in lista), 2)


def crear_carpetas(dirName):
    try:
        os.makedirs(dirName)
        print("Directory ", dirName,  " Created ")
    except FileExistsError:
        print("Directory ", dirName,  " already exists")


def main():
    carpeta_22 = "Atractores_regla_22"
    carpeta_54 = "Atractores_regla_54"
    crear_carpetas(carpeta_22)
    crear_carpetas(carpeta_54)
    longitud_max = 31
    regla_22 = regla_representacion(22)
    regla_54 = regla_representacion(54)
    t0 = time.time()
    for longitud in range(2,longitud_max):
        combinaciones = CalculadoraCombinaciones(longitud)
        atractoresList_22 = []
        atractoresList_54 = []
        for inicial in combinaciones:
            atractores_22 = AutomataCelular(inicial, regla_22)
            atractoresList_22.append((ListaBinariatoNumero(
                atractores_22[0]), ListaBinariatoNumero(atractores_22[-1])))
            atractores_54 = AutomataCelular(inicial, regla_54)
            atractoresList_54.append((ListaBinariatoNumero(
                atractores_54[0]), ListaBinariatoNumero(atractores_54[-1])))

        atractor_22_nombre = os.path.join(
            carpeta_22, 'atractor_22_size_'+str(longitud)+'.graphml')
        atractor_54_nombre = os.path.join(
            carpeta_54, 'atractor_54_size_'+str(longitud)+'.graphml')
        g_22 = nx.MultiGraph(atractoresList_22)
        nx.write_graphml(g_22, atractor_22_nombre)
        g_54 = nx.MultiGraph(atractoresList_54)
        nx.write_graphml(g_54, atractor_54_nombre)
    t1 = time.time()
    total = t1-t0
    print(total)


if __name__ == "__main__":
    main()
