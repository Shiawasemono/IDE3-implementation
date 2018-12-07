import pandas as pd
import numpy as np
from anytree import Node, RenderTree, ContStyle
from anytree.exporter import DotExporter
import operator
import string

def entropia(matriz_datos,col='',valor=0):
	# Calculamos las clases existentes y las repeticiones en las mismas.
	if(col == ''):
		col = matriz_datos.columns[-1]
	valDif = matriz_datos[col].value_counts()
	# Convertimos la serie generada con la operación anterior en una lista de duplas
	# para trabajar con el número de apariciones de cada clase.
	valDif = list(zip(valDif.index, valDif.values))
	l = len(matriz_datos)
	E = 0
	if col == matriz_datos.columns[-1]:
		#Estamos calculando la entropía de la variable de decisión
		for k in valDif:
			p = k[1]/l 
			E += p*np.log2(p)
	else:
		# Calculamos la entropía de una variable instanciada con un valor dado
		# Extracción del data frame filtrado por las dos columnas necesarias(index y variable de decisión)
		cnt = matriz_datos.groupby([col,matriz_datos.columns[-1]]).size()
		# Zipeo de la información
		dic = dict(zip(cnt.index,cnt.values))
		# Array con la información que será filtrada por valor
		a = []
		for k in dic:
			if(k[0] == valor):
				a.append(dic[k])

		# Cálculo de la entropía
		l = sum(a)
		for k in a:
			p = k/l
			E += p*np.log2(p)
	return -E

def ganancia(matriz_datos,col):
	# Ganancia de un valor se define como: EntropiaGen + Sum (- valor/filastotales * entropia(matriz,indice,valor))
	enGen = entropia(matriz_datos)
	filas = len(matriz_datos)
	valDif = matriz_datos[col].value_counts()
	valDif = list(zip(valDif.index,valDif.values))
	Sum = 0
	for k in valDif:
		p = k[1]/filas
		E = p*entropia(matriz_datos,col,k[0])
		Sum -= E
	G = enGen + Sum
	return G

def DecisionTreeID(nombre_fichero):
	matriz_datos = pd.read_csv(nombre_fichero)
	return decisionTree(matriz_datos)

def reducir_matriz(matriz,columna,fila):
	
	matriz_aux = matriz[matriz[columna] == fila]
	matriz_aux = matriz_aux.drop(columns = [columna])

	return matriz_aux

def decisionTree(matriz_datos, padre=None, rama=''):
	# :param pandas.DataFrame matriz_datos es la matriz a partir de la cual generar el nodo siguiente
	# :param str padre nodo padre del nodo a generar (en este caso será la columna de la que salió el arco)
	clasesDecision = matriz_datos[matriz_datos.columns[-1]].value_counts() # Cojo todos los valores que haya en la variable de decisión
	clasesDecision = list(clasesDecision.index)
	unicoValor = len(clasesDecision) == 1 or len(matriz_datos.columns.tolist()) == 1
	if not unicoValor and len(matriz_datos.columns.tolist()) == 2: # si solo quedan dos columnas debo comprobar que en la que no es de decision quede un unico valor
		clasesDecision = matriz_datos[matriz_datos.columns[0]].value_counts() # Cojo todos los valores que haya en la variable de decisión
		clasesDecision = list(clasesDecision.index)
		unicoValor = unicoValor or len(clasesDecision) == 1
	if unicoValor: # Si solo está la variable de decisión O solo existe una clase en la variable de decisión
        # Caso base
		referencia = matriz_datos.mode()[matriz_datos.columns[-1]].iloc[0]
		name = referencia + '\nid='
		name += ''.join(np.random.choice(list(string.ascii_uppercase) + list(string.digits), size=4))
		name = rama + '\n' + name
		return Node(name=name, parent=padre, rama=rama, ref=referencia)
		
	variables = matriz_datos.columns[:-1].tolist()
	ganancia_max = ['',-1] # La ganancia es siempre positiva, por lo que al comparar cualquiera sera mayor
	for columna in variables:
		ganancia_act = ganancia(matriz_datos, columna)
		if ganancia_max[1] < ganancia_act:
			ganancia_max = [columna, ganancia_act]
	referencia = ganancia_max[0]
	name = referencia + '\nid=' # Genero nombres con id's aleatorias para la separacion de los nodos en el grafo
	name += ''.join(np.random.choice(list(string.ascii_uppercase) + list(string.digits), size=4))

	if rama == '':
		nodo = Node(name=name, ref=referencia)
	else:
		name = rama + '\n' + name
		nodo = Node(name=name,parent=padre,rama=rama, ref=referencia)

	hijos = matriz_datos[ganancia_max[0]].value_counts()
	hijos = list(hijos.index)
    
	for hijo in hijos:
		matriz_hijo = reducir_matriz(matriz_datos,ganancia_max[0],hijo)
		decisionTree(matriz_hijo, nodo, hijo)

	return nodo

def predict(nombre_fichero, arbol):
	datos = pd.read_csv(nombre_fichero)
	encontrado = False
	nodoActual = arbol

	while not encontrado:
		if not nodoActual.children:
			encontrado = True
		else:
			nodo = nodoActual.ref
			
			for child in nodoActual.children:
				if child.rama in datos[nodo].iloc[0]:
					nodoActual = child

	return nodoActual.ref
    
if __name__ == '__main__':
	arbol = DecisionTreeID('data.csv')
	print(predict('data (copia).csv', arbol))
