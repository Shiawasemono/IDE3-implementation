import pandas as pd
import numpy as np
from anytree import Node, RenderTree, ContStyle
from anytree.exporter import DotExporter
import operator
import string

def entropia_inicial(columna):
	return columna == ''

def entropia(matriz_datos, columna='', valor=0):
	# Calculamos las clases existentes y las repeticiones en las mismas.
	if(entropia_inicial(columna)):
		columna = matriz_datos.columns[-1]
	valores_diferentes = matriz_datos[columna].value_counts()
	# Convertimos la serie generada con la operación anterior en una lista de duplas
	# para trabajar con el número de apariciones de cada clase.
	valores_diferentes = list(zip(valores_diferentes.index, valores_diferentes.values))
	len_matriz_datos = len(matriz_datos)
	entropia = 0
	if columna == matriz_datos.columns[-1]:
		#Estamos calculando la entropía de la variable de decisión
		for valor in valores_diferentes:
			probabilidad_valor = valor[1]/len_matriz_datos 
			entropia += probabilidad_valor*np.log2(probabilidad_valor)
	else:
		# Calculamos la entropía de una variable instanciada con un valor dado
		# Extracción del data frame filtrado por las dos columnas necesarias(index y variable de decisión)
		matriz_datos_filtrada = matriz_datos.groupby([columna,matriz_datos.columns[-1]]).size()
		# Zipeo de la información
		matriz_datos_filtrada = dict(zip(matriz_datos_filtrada.index,matriz_datos_filtrada.values))
		# Array con la información que será filtrada por valor
		info_filtrada = []
		for valor in matriz_datos_filtrada:
			if(valor[0] == valor):
				info_filtrada.append(matriz_datos_filtrada[valor])

		# Cálculo de la entropía
		len_matriz_datos = sum(info_filtrada)
		for valor in info_filtrada:
			probabilidad_valor = valor/len_matriz_datos
			entropia += probabilidad_valor*np.log2(probabilidad_valor)
	return -entropia

def ganancia(matriz_datos,columna):
	# Ganancia de un valor se define como: EntropiaGen + Sum (- valor/filastotales * entropia(matriz,indice,valor))
	entropia_general = entropia(matriz_datos)
	len_matriz_datos = len(matriz_datos)
	valores_diferentes = matriz_datos[columna].value_counts()
	valores_diferentes = list(zip(valores_diferentes.index, valores_diferentes.values))
	sumatorio = 0
	for valor in valores_diferentes:
		probabilidad_valor = valor[1] / len_matriz_datos
		entropia_particular = probabilidad_valor * entropia(matriz_datos,columna,valor[0])
		sumatorio -= entropia_particular
	ganancia = entropia_general + sumatorio
	return ganancia

def DecisionTreeID(nombre_fichero):
	matriz_datos = pd.read_csv(nombre_fichero)
	return decisionTree(matriz_datos)

def reducir_matriz(matriz, columna, fila):
    matriz_aux = matriz[matriz[columna] != fila]
    matriz_aux = matriz_aux.drop(columns = [columna])
    return matriz_aux

def decisionTree(matriz_datos, padre=None, rama=''):
	"""
		:param pandas.DataFrame matriz_datos es la matriz a partir de la cual generar el nodo siguiente
		:param str padre nodo padre del nodo a generar (en este caso será la columna de la que salió el arco)
	"""
	clasesDecision = matriz_datos[matriz_datos.columns[-1]].value_counts() # Cojo todos los valores que haya en la variable de decisión
	clasesDecision = list(clasesDecision.index)
	unicoValor = len(clasesDecision) == 1 or len(matriz_datos.columns.tolist()) == 1
	if not unicoValor and len(matriz_datos.columns.tolist()) == 2: # si solo quedan dos columnas debo comprobar que en la que no es de decision quede un unico valor
		clasesDecision = matriz_datos[matriz_datos.columns[0]].value_counts() # Cojo todos los valores que haya en la variable de decisión
		clasesDecision = list(clasesDecision.index)
		unicoValor = unicoValor or len(clasesDecision) == 1
	if unicoValor: # Si solo está la variable de decisión O solo existe una clase en la variable de decisión
        # Caso base
		name = matriz_datos.mode()[matriz_datos.columns[-1]].iloc[0] + '\nid='
		name += ''.join(np.random.choice(list(string.ascii_uppercase) + list(string.digits), size=4))
		name = rama + '\n' + name
		return Node(name=name, parent=padre, rama=rama)
		#return Node(name=matriz_datos.mode()[matriz_datos.columns[-1]].iloc[0], parent=padre, rama=rama)
		
	variables = matriz_datos.columns[:-1].tolist()
	ganancia_max = ['',-1] # La ganancia es siempre positiva, por lo que al comparar cualquiera sera mayor
	for columna in variables:
		ganancia_act = ganancia(matriz_datos, columna)
		if ganancia_max[1] < ganancia_act:
			ganancia_max = [columna, ganancia_act]

	name = ganancia_max[0] + '\nid=' # Genero nombres con id's aleatorias para la separacion de los nodos en el grafo
	name += ''.join(np.random.choice(list(string.ascii_uppercase) + list(string.digits), size=4))

	if rama == '':
		nodo = Node(name=name)
	else:
		name = rama + '\n' + name
		nodo = Node(name=name,parent=padre,rama=rama)

	hijos = matriz_datos[ganancia_max[0]].value_counts()
	hijos = list(hijos.index)
    
	for hijo in hijos:
		matriz_hijo = reducir_matriz(matriz_datos,ganancia_max[0],hijo)
		decisionTree(matriz_hijo, nodo, hijo)

	return nodo
    
if __name__ == '__main__':
	arbol = DecisionTreeID('data.csv')
	DotExporter(arbol).to_picture('arboldata.png')