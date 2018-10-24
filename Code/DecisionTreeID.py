def Entropia(matriz_datos,index=False,valor=0):
	valDif = matriz_datos[matriz_datos.columns[-1]].value_counts()
	l = len(data_matrix)
	if not index:
		#Estamos calculando la entropía de la variable de decisión
		for k in valDif:
			p = k[1]/l 
			E += p*log2(p)
	else:
		cnt = matriz_datos.groupby([matriz_datos.columns[index],matriz_datos.columns[-1]).size()



	return -E