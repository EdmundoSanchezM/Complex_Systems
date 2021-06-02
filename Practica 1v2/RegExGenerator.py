import random
import numpy as np

regex_22 = "(0+1(01)*00)(0+0(01)*00)*"
regex_54 = "(0+1(11)*10)(0+0(11)*10)*"


def fun_klee(num_veces, regex_klee):
    cadena_klee = ""
    for i in range(0, num_veces):
        cadena_klee += regex_klee
    return cadena_klee


def logica(longitud, regla):
    cont_long = 0
    cadena = ""
    klee_r = bool(random.getrandbits(1))
    lado_1_izq = bool(random.getrandbits(1))
    regex_rule = regex_22 if regla == 22 else regex_54
    if lado_1_izq:
        cadena += regex_rule[1]
        cont_long += 1
    else:
        klee = bool(random.getrandbits(1))
        cadena += regex_rule[3]
        cont_long += 1
        if klee:
            valor_klee = int(random.randint(0, longitud-cont_long)/2)
            cadena += fun_klee(valor_klee, regex_rule[5:7])
            cont_long += valor_klee
        if not klee_r and cont_long+1 < longitud:
            valor_klee = int((longitud-cont_long+1)/2)
            cadena += fun_klee(valor_klee, regex_rule[5:7])
            cont_long += valor_klee
        cadena += regex_rule[9:11]
        cont_long += 2
    if klee_r or lado_1_izq:
        while cont_long < longitud:
            lado_1_izq = bool(random.getrandbits(1))
            if lado_1_izq:
                cadena += regex_rule[13]
                cont_long += 1
            else:
                klee = bool(random.getrandbits(1))
                cadena += regex_rule[15]
                cont_long += 1
                if klee:
                    valor_klee = int(random.randint(0, longitud-cont_long)/2)
                    cadena += fun_klee(valor_klee, regex_rule[17:19])
                    cont_long += valor_klee
                cadena += regex_rule[21:23]
                cont_long += 2
    return cadena


def start_RegEx(longitud, regla):
    cadena_generada = logica(longitud, regla)
    arreglo_RegEx = np.array(list(cadena_generada)).astype(np.int8)
    return arreglo_RegEx


if __name__ == "__main__":
    main()
