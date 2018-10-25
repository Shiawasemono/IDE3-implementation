import pandas as pd
import operator

def entropia(matriz_datos):
        return 1

def ganancia(input):
    return 1

def DecisionTreeID(nombre_fichero):
    matriz_datos = pd.read_csv(nombre_fichero)
    matriz_datos_original = pd.read_csv(nombre_fichero) # Realmente necesario? Demanding?

    # variable_decision = matriz_datos[matriz_datos.columns[-1]] # "La variable de decisión aparecerá la última en la lista (...)"
    entropia_inicial = entropia(matriz_datos)
    
    arbol_terminado = False
    arbol = None
    padre_actual = None
    siguiente_nodo = None
    
    while not arbol_terminado:
        dict_ganancias = {} # creo diccionario de ganancias vacío
        atributos = matriz_datos.loc[matriz_datos.columns[:-1]]
        for column in atributos: # por cada columna que me quede en la matriz de datos
            entropias = []
            # calculo entropia de cada caso
            dict_ganancias[column] = ganancia(entropias) # calculo ganancia y la meto en el diccionario
        ganancia_maxima = max(dict_ganancias.items(), key=operator.itemgetter(1))[0] # cojo ganancia maxima
        # inserto nuevos nodos en arbol
        matriz_datos = matriz_datos.drop(columns = [ganancia_maxima]) # actualizo matriz_datos (elimino la columna escogida como atributo)
        arbol_terminado = len(matriz_datos.columns) == 1 # actualizo arbol_terminado

        # Borrar esto:
        print('asd')
        arbol_terminado = True

    return matriz_datos