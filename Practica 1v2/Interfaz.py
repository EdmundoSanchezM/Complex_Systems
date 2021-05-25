#IMPORTAMOS LIBRERIAS NECESARIAS.
import tkinter 
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
import numpy as np
import Logica as cellularAutomaton
import matplotlib.pyplot as plt
#------------------------------CREAR VENTANA---------------------------------
root = tkinter.Tk()
root.wm_title("Elementary Cellular Automaton")
framet = tkinter.Frame(root)
frameColor0 = tkinter.Frame(root)
frameColor1 = tkinter.Frame(root)
frameCondicion = tkinter.Frame(root)
frameMainInformacion = tkinter.Frame(root)
frameStart = tkinter.Frame(root)
#------------------------------FUNCIONES---------------------------------
global color0
global color1
global arregloInicial
global detener
esBinario = tkinter.IntVar()
reglaValor = tkinter.StringVar()
tamEspacio = tkinter.StringVar()
numIteraciones = tkinter.StringVar()
esAleatorio = tkinter.IntVar()
esEspecifico = tkinter.IntVar()
posicionesUnos = tkinter.StringVar()
esAnimado = tkinter.IntVar()

color0 = "#ffffff"
color1 = "#000000"
arregloInicial = []
detener = False

def chageLabel():
    if(esEspecifico.get() == 0):
        labelEspecifico.grid_remove()
        las.grid_remove()
    else:
        las.grid()
        labelEspecifico.grid()

def colorto0():
    global color0
    color0 = colorchooser.askcolor()[1]
    showColor0.config(bg=color0)

def colorto1():
    global color1
    color1 = colorchooser.askcolor()[1]
    showColor1.config(bg=color1)

def saveCondic():
    celulasIniciales = cellularAutomaton.automataCelular[0,:]
    with open('celulasIniciales.txt', 'wb') as f:
        np.savetxt(f, np.column_stack(celulasIniciales), fmt='%1f')
    tkinter.messagebox.showinfo("Save condition", "Successfully saved") 

def fileselectD():
    global arregloInicial
    try:
        filename = askopenfilename()
        if (filename.find(".txt")!=-1):
            labelLoadCondicion.config(text = filename)
            arregloInicial = np.loadtxt(filename)
        else:
            arregloInicial = []
            labelLoadCondicion.config(text = "Choose a file .txt")
    except:
        arregloInicial = []
        labelLoadCondicion.config(text = "File Error")

def messageAnim():
    if(esAnimado.get() == 1):
        tkinter.messagebox.showwarning(title="Warning", message="If you have a lot of iterations and you need the results quickly, I don't recommend enable this option")

def stopcontAnim():
    global detener
    detener  ^= True
    if detener:
        cellularAutomaton.anim_automata.event_source.stop()
        cellularAutomaton.anim_densidad.event_source.stop()
        cellularAutomaton.anim_log10.event_source.stop()
        cellularAutomaton.anim_media.event_source.stop()
        cellularAutomaton.anim_varianza.event_source.stop()
        cellularAutomaton.anim_densidad_central.event_source.stop()
    else:
        cellularAutomaton.anim_automata.event_source.start()
        cellularAutomaton.anim_densidad.event_source.start()
        cellularAutomaton.anim_log10.event_source.start()
        cellularAutomaton.anim_media.event_source.start()
        cellularAutomaton.anim_varianza.event_source.start()
        cellularAutomaton.anim_densidad_central.event_source.start()

def deletePlt():
    plt.close("all")
    
def iniciar():
    plt.close("all")
    numPasos = int(numIteraciones.get())
    ruleEntero = int(reglaValor.get())
    animacion = int(esAnimado.get())
    if(esBinario.get() == 1):
        ruleString = reglaValor.get()
        ruleEntero = int(ruleString,2)
    if(len(arregloInicial) != 0):    
        cellularAutomaton.IniciarArchivo(color0,color1,numPasos,ruleEntero,arregloInicial,animacion)#color 0, color 1, pasos,regla,
    else:
        tamEsp = int(tamEspacio.get())
        if(esAleatorio.get()==1):
            cellularAutomaton.IniciarRandom(color0,color1,numPasos,ruleEntero,tamEsp,animacion)
        else:
            if '%' in posicionesUnos.get():
                unosEntero = int(posicionesUnos.get().replace('%',''))/100
                cellularAutomaton.IniciarProbabilidad(color0,color1,numPasos,ruleEntero,tamEsp,unosEntero,animacion)
            else:
                unosString = posicionesUnos.get().split(',')
                unosArray = list(map(int, unosString))
                cellularAutomaton.IniciarEspecifico(color0,color1,numPasos,ruleEntero,tamEsp,unosArray,animacion)

#------------------------------CREAR INTERFAZ---------------------------------

titulo = tkinter.Label(framet, text="Elementary Cellular Automaton.",font=("times new roman", 24))
titulo.pack(side="top")

#------------------------------COLOR 0---------------------------------

color0Label = tkinter.Label(frameColor0, text="Choose color to represent 0 in the cellular automaton:",font=("times new roman", 14))
color0Label.pack(side="top")
buttonColor0 = tkinter.Button(frameColor0, text = "Choose a color", command=colorto0,font=("times new roman", 14))
buttonColor0.pack(side="left")
showColor0 = tkinter.Label(frameColor0, text="This is the color to use in 0 value",font=("times new roman", 14))
showColor0.pack(side="left")

#------------------------------COLOR 1---------------------------------

color1Label = tkinter.Label(frameColor1, text="Choose color to represent 1 in the cellular automaton:",font=("times new roman", 14))
color1Label.pack(side="top")
buttonColor1 = tkinter.Button(frameColor1, text = "Choose a color", command=colorto1 ,font=("times new roman", 14))
buttonColor1.pack(side="left")
showColor1 = tkinter.Label(frameColor1, text="This is the color to use in 1 value",font=("times new roman", 14))
showColor1.pack(side="left")

#------------------------------CONDICIONES ARCHIVO---------------------------------

tittleCondicion = tkinter.Label(frameCondicion, text = "Initial condition with files" ,font=("times new roman", 18))
tittleCondicion.pack(side="top")
saveCondicion = tkinter.Button(frameCondicion, text = "Save condition", command=saveCondic ,font=("times new roman", 14))
saveCondicion.pack(side="top")
loadCondicion = tkinter.Button(frameCondicion, text = "Load condition", command=fileselectD ,font=("times new roman", 14))
loadCondicion.pack(side="left")
labelLoadCondicion = tkinter.Label(frameCondicion,text = "Choose File .txt",font=("Times New Roman",14))
labelLoadCondicion.pack(side="left")

#------------------------------CONDICION INICIAL USUARIO---------------------------------
tittleCondicionUsuario = tkinter.Label(frameMainInformacion, text = "Initial condition by user" ,font=("times new roman", 18))
tittleCondicionUsuario.grid(row = 0, column = 0,columnspan=2)

tamanioEspacio = tkinter.Label(frameMainInformacion, text = "Space size: " , font=("times new roman", 14))
tamanioEspacio.grid(row=1, column=0)
entradaEspacio = tkinter.Entry(frameMainInformacion,font=("times new roman", 14), textvariable = tamEspacio)
entradaEspacio.grid(row=1, column=1)

numeroIteracion = tkinter.Label(frameMainInformacion, text = "Number of iterations: ",font=("times new roman", 14))
numeroIteracion.grid(row=2, column=0)
entradaIteracion = tkinter.Entry(frameMainInformacion,font=("times new roman", 14), textvariable = numIteraciones)
entradaIteracion.grid(row=2, column=1)

reglaUsar = tkinter.Label(frameMainInformacion, text = "Rule to use: " ,font=("times new roman", 14))
reglaUsar.grid(row=3, column=0)
entradaRegla = tkinter.Entry(frameMainInformacion,font=("times new roman", 14), textvariable = reglaValor)
entradaRegla.grid(row=3, column=1)
binary = tkinter.Checkbutton(frameMainInformacion, text="Is binary?", variable=esBinario, font=("times new roman", 13))
binary.grid(row=4, column=1)


labelCondicion = tkinter.Label(frameMainInformacion, text = "Type of inicial condition: " , font=("times new roman", 14))
labelCondicion.grid(row=5,column = 0)
checkAleatoria = tkinter.Checkbutton(frameMainInformacion, text="Random", variable=esAleatorio, font=("times new roman", 14))
checkAleatoria.grid(row=5, column=1)
tipoCondicion = tkinter.Checkbutton(frameMainInformacion, text = "Specific" , variable=esEspecifico, command=chageLabel,font=("times new roman", 14))
tipoCondicion.grid(row=5,column = 3)

labelEspecifico = tkinter.Label(frameMainInformacion, text = "Indices to complete with 1 or use % \nat the end to assign probability to 1's:" , font=("times new roman", 14))
labelEspecifico.grid(row=6,column = 0)
las = tkinter.Entry(frameMainInformacion,font=("times new roman", 14), textvariable = posicionesUnos)
las.grid(row=6,column = 1)
labelEspecifico.grid_remove()
las.grid_remove()

#------------------------------ANIMACION -------------------
checkAnimado = tkinter.Checkbutton(frameMainInformacion, text="Enable Animation", variable=esAnimado, command=messageAnim, font=("times new roman", 14))
checkAnimado.grid(row=7, column=0)

buttonStop = tkinter.Button(frameMainInformacion, text="Stop/Continue animation", command=stopcontAnim, font=("times new roman", 14))
buttonStop.grid(row=7, column=1)

buttonDeletePlt = tkinter.Button(frameMainInformacion, text="Delete all plots", command=deletePlt, font=("times new roman", 14))
buttonDeletePlt.grid(row=8, column=0)

#------------------------------BOTON MAESTRO---------------------------------

buttonStart = tkinter.Button(frameStart, text = "Start", command=iniciar ,font=("times new roman", 14))
buttonStart.pack(side="top")

framet.grid(row=0,column=0,columnspan=1)
frameColor0.grid(row=1,column=0)
frameColor1.grid(row=2,column=0)
frameCondicion.grid(row=3,column=0)
frameMainInformacion.grid(row=4,column=0)
frameStart.grid(row=5,column=0)

tkinter.mainloop()