####-------------------------------PARA CREAR LA TABLA PBI per capita
import pandas as pd
pd.options.mode.chained_assignment = None  # deshabilitar las advertencias de asignación en cadena
from matplotlib import pyplot as plt
import numpy as np

def cargarDF_PBI_POB(ruta1:str,ruta2:str):
    
    archivo_pbi = pd.read_excel(ruta1)
    archivo_pob = pd.read_excel(ruta2)
    
    df_pbi = pd.DataFrame(archivo_pbi)
    df_pob = pd.DataFrame(archivo_pob)
    
    #sacamos una fila entera para convertirla en cabeceras de columnas
    nom_col_pbi = df_pbi.iloc[1].tolist()
    nom_col_pob = df_pob.iloc[1].tolist()
    
    #asignamos las columnas
    df_pbi.columns = nom_col_pbi
    df_pob.columns = nom_col_pob
    
    #quitamos la fila que hicimos cabecera
    df_pbi = df_pbi[2:]
    df_pob = df_pob[2:]
    
    #quitamos filas de más (para poder tener las mismas filas en ambas tablas)
    df_pbi.drop([2,28,29,30],inplace=True)
    
    #reseteamos los indices
    df_pbi.reset_index(drop=True,inplace=True)
    df_pob.reset_index(drop=True,inplace=True)
    
    return df_pbi,df_pob

def limpiarDF(df):
    
    df = df.drop_duplicates()
    df = df.dropna()
    
    return df

def estabelecerDF_PBIpercapita(df_pbi,df_pob):
    
    departamentos = df_pbi['Departamento'][:-1].tolist()
    departamentos.append('Total')

    df_pbi_percapita = pd.DataFrame(departamentos,columns=['Departamento'])

    año = 2007
    for i in range(16):
        pbi_percapita_lista = []
        for pbi, pob in zip(df_pbi[año],df_pob[año]):
            pbi_percapita = round(pbi*1000/pob,2)
            pbi_percapita_lista.append(pbi_percapita)
        df_pbi_percapita[año]=pbi_percapita_lista
        
        año += 1
        
    df_pbi_percapita.drop([2007,2008,2009,2010,2022],axis=1,inplace=True)
    
    df_pbi_percapita1 = df_pbi_percapita.iloc[[-1]]
    df_pbi_percapita2 = df_pbi_percapita.iloc[:-1]
    
    df_pbi_percapita = pd.concat([df_pbi_percapita1,df_pbi_percapita2])
    df_pbi_percapita.reset_index(drop=True,inplace=True)
    
    return df_pbi_percapita
            
def cargarDF_gasto_educacion(ruta3):
    
    archivo_gasto_edu = pd.read_excel(ruta3)
    df_gasto_edu = pd.DataFrame(archivo_gasto_edu)
    nom_col_edu = df_gasto_edu.iloc[2].tolist()
    df_gasto_edu.columns = nom_col_edu
    df_gasto_edu = df_gasto_edu.drop([0,1,2])
    df_gasto_edu.reset_index(drop=True,inplace=True)
    df_gasto_edu.fillna("", inplace=True)
    
    año = 1999
    años_a_eliminar = []
    for i in range(12):
        años_a_eliminar.append(año)
        año += 1
    df_gasto_edu.drop(años_a_eliminar, axis=1, inplace=True)
    
    nombres_filas = df_gasto_edu['Nivel educativo /\nDepartamento'].tolist()
    filas_limpias = []
    for nombre_fila in nombres_filas:
        nombre_fila = nombre_fila.strip()
        nombre_fila = nombre_fila.strip('-')
        filas_limpias.append(nombre_fila)
    
    df_gasto_edu.drop('Nivel educativo /\nDepartamento', axis=1, inplace=True)
    df_gasto_edu.insert(0,'Departamento / Nivel educativo',filas_limpias)
    return df_gasto_edu

def establecer_relacion_pbi_educacion(df_gasto_edu,df_pbi_percapita):
    
    nombres_filas = df_gasto_edu['Departamento / Nivel educativo'].tolist()
    df_relacion_pbi_educacion = pd.DataFrame(nombres_filas,columns=['Departamento / Nivel educativo'])

    año = 2011
    
    for a in range(11):
        relacion_lista = []
        for departamento, pbi in zip(df_pbi_percapita['Departamento'],df_pbi_percapita[año]):
            for i in range(len(df_gasto_edu)):
                if df_gasto_edu['Departamento / Nivel educativo'][i] == departamento:
                    relacion_lista.append('')
                    for j in range(1,4):
                        relacion = df_gasto_edu[año][i+j]/pbi
                        relacion_lista.append(round(relacion,4))
                        
        df_relacion_pbi_educacion[año] = relacion_lista
        año += 1
    
    return df_relacion_pbi_educacion


####--------------------------------FUNCIONES DE LA BD ANALFABETISMO
def cargar_df_analfabetismo(ruta:str):
    archivo = pd.read_excel(ruta)
    df = pd.DataFrame(archivo)
    
    #sacamos los departamentos
    departamentos = df['TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022']
    departamentos = departamentos.iloc[10:].reset_index(drop=True)
    
    # limpiamos la data
    df = df.drop(columns=['TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022'])
    df = df[10:]
    df = df.reset_index(drop=True)
    
    #ingresamos las nuevas columnas
    columnas = []
    for año in range(2008,2023):
        columnas.append(año)
    
    df.columns = columnas
    
    #insertamos la columna departamento
    indice_callao = departamentos[departamentos == 'Prov. Const. del Callao'].index[0]
    departamentos[indice_callao] = 'Callao' # cambiamos el nombre a Callao
    df.insert(0,'Departamento',departamentos)
    
    #borramos las columnas que no utilizaremos
    df = df.drop(columns=[2008,2009,2010,2022])
    
    return df

def DF_con_tasa_promedio_analfabetismo(df):
    df = df.set_index('Departamento')
    df = df.transpose() #para que los departamentos sean las columnas
    
    promedios = []
    for departamento in df:
        prom = df[departamento].mean()
        promedios.append(round(prom,4))
    
    #para que los años vuelvan a ser las columnas
    df = df.transpose()
    
    #añadimos la columna de tasa promedio de analfabetismo
    df.insert(len(df.columns),'Tasa promedio',promedios)
    
    #reseteamos indices
    df.reset_index(inplace=True)
        
    return df

def grafico_analfabetismo_tasa_promedio_por_dpto(df):
    #filtramos solo las columnas necesarias para graficar
    df = df[['Departamento','Tasa promedio']]
    
    #ordenamos la data de mayor a menor
    df = df.sort_values(by='Tasa promedio', ascending=False)
    
    plt.figure(figsize=(8,8))
    plt.xticks(rotation=90)
    
    #pa las 4 tasas más grandes
    barras_grandes = plt.bar(df['Departamento'].iloc[:4], df['Tasa promedio'].iloc[:4], color='red',label='Tasas más grandes')
    #barras del medio
    plt.bar(df['Departamento'].iloc[4:21],df['Tasa promedio'].iloc[4:21], color='grey')
    #pa las 4 tasas más pequeñas
    barras_pequeñas = plt.bar(df['Departamento'].iloc[-4:], df['Tasa promedio'].iloc[-4:], color='green',label='Tasas más pequeñas')
    

    # Añadir etiquetas de valores encima de las barras más grandes
    for bar in barras_grandes:
        valor_Y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, valor_Y , round(valor_Y , 2), va='bottom', ha='center', fontsize=8, color='black',fontweight='bold',rotation=50)
    
    # Añadir etiquetas de valores encima de las barras más pequeñas
    for bar in barras_pequeñas:
        valor_Y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, valor_Y, round(valor_Y, 2), va='bottom', ha='center', fontsize=8, color='black',fontweight='bold',rotation=50)
    
    plt.title('TASA PROMEDIO DE ANALFABETISMO EN LOS DEPARTAMENTOS \nDEL PERÚ DESDE EL 2011 AL 2021 \n (Porcentaje respecto del total de la población mayor a 15 años)')
    plt.ylabel('% DE POBLACIÓN ANALFABETA')
    plt.xlabel('DEPARTAMENTOS')
    plt.legend()
    plt.show()
    
    return df

####---------------------------------FUNCIÓN ESTANDARIZADORA DE INPUTS
def pedir_departamento():
    dep = input('Ingrese el departamento a analizar: ').title()
    
    #nos cercioramos de que el departamento y nivel académico introducidos se encuentren escritos correctamente
    if ' De ' in dep:
        dep = dep.replace(' De ',' de ')
    
    if dep == 'Apurimac':
        dep = 'Apurímac'

    if dep == 'Callao':
        dep = 'Prov. Const. del Callao'
    
    elif dep == 'Ancash':
        dep = 'Áncash'
    
    elif dep == 'Huanuco':
        dep = 'Huánuco'
    
    elif dep == 'Junin':
        dep = 'Junín'
    
    elif 'Martin' in dep:
        dep = dep.replace('Martin','Martín')
    
    while dep not in df_pbi_percapita['Departamento'].tolist():
        dep = input('Error. Ingrese un departamento válido: ').title()
        if ' De ' in dep:
            dep = dep.replace(' De ',' de ')
        
        if dep == 'Callao':
            dep = 'Prov. Const. del Callao'
        
        elif dep == 'Ancash':
            dep = 'Áncash'
    
        elif dep == 'Huanuco':
            dep = 'Huánuco'
        
        elif dep == 'Junín':
            dep = 'Junin'
        
        elif 'Martin' in dep:
            dep = dep.replace('Martin','Martín')
            
    return dep

def pedir_nivel_acad():
    nivel_acad = input('Ingrese el nivel academico de interes: ').title()
    
    while nivel_acad not in ['Inicial','Primaria','Secundaria']:
        nivel_acad = input('Nivel académico no encontrado. \nIngrese "Inicial", "Primaria" o "Secundaria": ').title()
    
    return nivel_acad

def pedir_año():
    año = int(input('Ingrese el año a analizar: '))
    
    while año < 2011 or año > 2021:
        año = int(input('Ingrese un año entre 2011 y 2021: '))
    
    return año


####-------------------------------------GRÁFICOS
def grafico_ingreso(df_pbi_percapita,cant_departamentos,departamentos_a_comparar):
    plt.subplot(2,2,1)
    #sacamos los años para q posteriormente sean el eje x del grafico de lineas
    años = df_pbi_percapita.columns.tolist()[1:]
    
    #quitamos el total
    df_pbi_percapita = df_pbi_percapita.iloc[1:].reset_index(drop=True)
    
    datos = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_pbi_percapita)): #para q recorra fila por fila de df
            if df_pbi_percapita['Departamento'][i] == departamento:
                datos.append(df_pbi_percapita.iloc[i].tolist()[1:])
    
    for i in range(cant_departamentos):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(años,datos[i],label=departamentos_a_comparar[i],color=colores[i]) 
        
        # Encontrar el índice del máximo y mínimo
        indice_max = datos[i].index(max(datos[i]))
        indice_min = datos[i].index(min(datos[i]))
        
        # Añadir puntos para máximo y mínimo
        plt.scatter(años[indice_max], datos[i][indice_max], color=colores[i], marker='o', s=100, label=f'Máx: {max(datos[i]):.2f}')
        plt.scatter(años[indice_min], datos[i][indice_min], color=colores[i], marker='x', s=100, label=f'Mín: {min(datos[i]):.2f}')
    
    plt.xticks(años,rotation=90)    
    plt.title(f'EVOLUCION DEL INGRESO PER CAPITA DE LOS DEPARTAMENTOS \n{departamentos_a_comparar}')
    plt.xlabel('AÑOS')
    plt.ylabel('PBI PER CAPITA ANUAL (SOLES)')
    
    plt.grid(True)  #pa añadir cuadriculas
    plt.legend()

    

def grafico_gasto(df_gasto_edu,cant_departamentos,departamentos_a_comparar):
    plt.subplot(2,2,2)
    #sacamos los años para q posteriormente sean el eje x del grafico de lineas
    años = df_gasto_edu.columns.tolist()[1:]
    
    datos = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_gasto_edu)): #para q recorra fila por fila de df
            if df_gasto_edu['Departamento / Nivel educativo'][i] == departamento:
                df_filtrada = df_gasto_edu.iloc[i+1:i+4].reset_index(drop=True)
                
                #para cada año, calculamos el promedio del gasto en inicial, prim y sec
                gastos_promedio_añoX = []
                for año in años:
                    prom_año = round(df_filtrada[año].mean(),4)
                    gastos_promedio_añoX.append(prom_año)
                
                datos.append(gastos_promedio_añoX)
                    
    for i in range(cant_departamentos):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(años,datos[i],label=departamentos_a_comparar[i],color=colores[i]) 
        
        # Encontrar el índice del máximo y mínimo
        indice_max = datos[i].index(max(datos[i]))
        indice_min = datos[i].index(min(datos[i]))
        
        # Añadir puntos para máximo y mínimo
        plt.scatter(años[indice_max], datos[i][indice_max], color=colores[i], marker='o', s=100, label=f'Máx: {max(datos[i]):.2f}')
        plt.scatter(años[indice_min], datos[i][indice_min], color=colores[i], marker='x', s=100, label=f'Mín: {min(datos[i]):.2f}')
    
    plt.xticks(años,rotation=90)    
    plt.title(f'EVOLUCION DEL GASTO EN EDUCACIÓN POR ALUMNO DE LOS DEPARTAMENTOS \n{departamentos_a_comparar}')
    plt.xlabel('AÑOS')
    plt.ylabel('GASTO POR ALUMNO ANUAL (SOLES)')
    
    plt.grid(True)  #pa añadir cuadriculas
    plt.legend()

    
def grafico_analfabetismo(df_analfabetismo,cant_departamentos,departamentos_a_comparar):
    plt.subplot(2,2,3)
    #sacamos los años para q posteriormente sean el eje x del grafico de lineas
    años = df_analfabetismo.columns.tolist()[1:]
    
    datos = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_analfabetismo)): #para q recorra fila por fila de df
            if df_analfabetismo['Departamento'][i] == departamento:
                datos.append(df_analfabetismo.iloc[i].tolist()[1:])
    
    for i in range(cant_departamentos):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(años,datos[i],label=departamentos_a_comparar[i],color=colores[i]) 
        
        # Encontrar el índice del máximo y mínimo
        indice_max = datos[i].index(max(datos[i]))
        indice_min = datos[i].index(min(datos[i]))
        
        # Añadir puntos para máximo y mínimo
        plt.scatter(años[indice_max], datos[i][indice_max], color=colores[i], marker='o', s=100, label=f'Máx: {max(datos[i]):.2f}')
        plt.scatter(años[indice_min], datos[i][indice_min], color=colores[i], marker='x', s=100, label=f'Mín: {min(datos[i]):.2f}')
    
    plt.xticks(años,rotation=90)    
    plt.title(f'EVOLUCION DE LA TASA DE ANALFABETISMO DE LOS DEPARTAMENTOS \n{departamentos_a_comparar}')
    plt.xlabel('AÑOS')
    plt.ylabel('TASA DE ANALFABETISMO ANUAL')
    
    plt.grid(True)  #pa añadir cuadriculas
    plt.legend()

    
def grafico_relacion_ingreso_gasto(df_relacion_pbi_educacion,cant_departamentos,departamentos_a_comparar):
    plt.subplot(2,2,4)
    
    años = df_relacion_pbi_educacion.columns.tolist()[1:]
    
    datos = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_relacion_pbi_educacion)):
            if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
                df_filtrada = df_relacion_pbi_educacion.iloc[i+1:i+4].reset_index(drop=True)
                
                #para cada año, calculamos el promedio de la relacion en inicial, prim y sec
                relacion_promedio_añoX = []
                for año in años:
                    prom_año = round(df_filtrada[año].mean(),4)
                    relacion_promedio_añoX.append(prom_año)
                
                datos.append(relacion_promedio_añoX)
    
    for i in range(cant_departamentos):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(años,datos[i],label=departamentos_a_comparar[i],color=colores[i]) 
        
        # Encontrar el índice del máximo y mínimo
        indice_max = datos[i].index(max(datos[i]))
        indice_min = datos[i].index(min(datos[i]))
        
        # Añadir puntos para máximo y mínimo
        plt.scatter(años[indice_max], datos[i][indice_max], color=colores[i], marker='o', s=100, label=f'Máx: {max(datos[i]):.2f}')
        plt.scatter(años[indice_min], datos[i][indice_min], color=colores[i], marker='x', s=100, label=f'Mín: {min(datos[i]):.2f}') 
    
    plt.xticks(años,rotation=90)    
    plt.title(f'EVOLUCION PROMEDIO DE LA RELACION ENTRE EL \nGASTO PUBLICO POR ALUMNO y PBI PER CAPITA DE LOS \nDEPARTAMENTOS {departamentos_a_comparar}')
    plt.xlabel('AÑOS')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.grid()
    plt.legend()

def grafico_dashboard():
    cant_departamentos = int(input('Ingrese la cantidad de departamentos a comparar: '))
    
    departamentos_a_comparar = []
    for i in range(cant_departamentos):
        departamento = pedir_departamento()
        departamentos_a_comparar.append(departamento)
    
    plt.figure(figsize=(20,22))
    

    grafico_ingreso(df_pbi_percapita,cant_departamentos,departamentos_a_comparar)
    

    grafico_gasto(df_gasto_edu,cant_departamentos,departamentos_a_comparar)

    grafico_relacion_ingreso_gasto(df_relacion_pbi_educacion,cant_departamentos,departamentos_a_comparar)
    
    grafico_analfabetismo(df_analfabetismo,cant_departamentos,departamentos_a_comparar)
    
    plt.show()


#### -------------------------------------GRÁFICO CON OPCIONES
def graf_a():
    ###------------------pa todos los dptos, año específico y nivel académico
    año = pedir_año()
    nivel_acad = pedir_nivel_acad()

    #quitamos 'total' del df
    df_analisis = df_relacion_pbi_educacion[4:]
    df_analisis.reset_index(drop=True,inplace=True)

    #filtramos el nivel educativo de interes
    departamentos = df_pbi['Departamento'][:-1].tolist() #sacamos los dptos

    for i in range(len(df_analisis)):
        if df_analisis['Departamento / Nivel educativo'][i] != nivel_acad and df_analisis['Departamento / Nivel educativo'][i] not in departamentos:
            df_analisis.drop(i,inplace=True)

    df_analisis.reset_index(drop=True,inplace=True)

    #nos quedamos con el aÒo de interes
    años_a_borrar = list(range(2011, 2022))

    for year in años_a_borrar:
        if year == año:
            años_a_borrar.remove(year)
            
    df_analisis.drop(columns=años_a_borrar,inplace=True)

    #sacamos los valores de la relacion para el grafico
    df_analisis = df_analisis[df_analisis[año] != '']
    df_analisis.drop(columns=['Departamento / Nivel educativo'],inplace=True)
    df_analisis.insert(0,'Departamentos',departamentos)
    df_analisis.set_index('Departamentos',inplace=True)


    #graficamos
    plt.figure(figsize=(8,8))

    df_analisis.plot(kind='bar',legend=False,xlabel='DEPARTAMENTOS',ylabel='GASTO(SOLES)/PBI PER CÁPITA')
    plt.title(f'RELACION DEL PBI PER CAPITA Y EL GASTO PUBLICO POR \nALUMNO EN EDUCACION {nivel_acad.upper()} EN EL AÑO {str(año).upper()}')
    plt.show()

def graf_b():
    
    cant_departamentos = int(input('Ingrese la cantidad de departamentos a comparar: '))
    departamentos_a_comparar = []
    for i in range(cant_departamentos):
        departamento = pedir_departamento()
        departamentos_a_comparar.append(departamento)
    nivel_acad = pedir_nivel_acad()
    
    años = df_relacion_pbi_educacion.columns.tolist()[1:]
    
    datos = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_relacion_pbi_educacion)):
            if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
                df_filtrada = df_relacion_pbi_educacion.iloc[i+1:i+4].reset_index(drop=True)
                for j in range(3):
                    if df_filtrada['Departamento / Nivel educativo'][j] == nivel_acad:
                        data = df_filtrada.iloc[j].tolist()[1:]
                        datos.append(data)
    
    for i in range(cant_departamentos):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(años,datos[i],label=departamentos_a_comparar[i],color=colores[i]) 
    
    plt.xticks(años,rotation=90)    
    plt.title(f'EVOLUCION DE LA RELACION ENTRE EL GASTO PUBLICO EN \nEDUCACION {nivel_acad.upper()}/PBI PER CAPITA DE LOS DEPARTAMENTOS {departamentos_a_comparar}')
    plt.xlabel('Años')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.legend()
    plt.show()       

def graf_c():

    departamento_a_analizar = pedir_departamento()
    niveles_academicos = ['Inicial','Primaria','Secundaria']
    
    años = df_relacion_pbi_educacion.columns.tolist()[1:]
    
    datos = []
    for i in range(len(df_relacion_pbi_educacion)):
        if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento_a_analizar:
            inicial = df_relacion_pbi_educacion.iloc[i+1].tolist()[1:]
            datos.append(inicial)
            primaria = df_relacion_pbi_educacion.iloc[i+2].tolist()[1:]
            datos.append(primaria)
            secundaria = df_relacion_pbi_educacion.iloc[i+3].tolist()[1:]
            datos.append(secundaria)
    
    for i in range(3):
        colores = ['blue', 'green', 'red']
        plt.plot(años,datos[i],label=niveles_academicos[i],color=colores[i])
    
    plt.xticks(años,rotation=90)  
    plt.title(f'EVOLUCION DE LA RELACION ENTRE EL GASTO PUBLICO EN \nEDUCACION {niveles_academicos}/PBI PER CAPITA DEL DEPARTAMENTO {departamento_a_analizar.upper()}')
    plt.xlabel('Años')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.legend()
    plt.show()

def graf_d():

    cant_departamentos = int(input('Ingrese la cantidad de departamentos a comparar: '))
    departamentos_a_comparar = []
    for i in range(cant_departamentos):
        departamento = pedir_departamento()
        departamentos_a_comparar.append(departamento)
    año = pedir_año()
    niveles_academicos = ['Inicial','Primaria','Secundaria']
    
    datos_inicial = []
    datos_primaria = []
    datos_secundaria = []
    for departamento in departamentos_a_comparar:
        for i in range(len(df_relacion_pbi_educacion)):
            if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
                datos_inicial.append(df_relacion_pbi_educacion[año][i+1])
                datos_primaria.append(df_relacion_pbi_educacion[año][i+2])
                datos_secundaria.append(df_relacion_pbi_educacion[año][i+3])
    
    ancho_barras = 0.2
    x = np.arange(cant_departamentos)
    
    plt.bar(x - ancho_barras,datos_inicial,width=ancho_barras, label=niveles_academicos[0])
    plt.bar(x,datos_primaria,width=ancho_barras, label=niveles_academicos[1])
    plt.bar(x + ancho_barras,datos_secundaria,width=ancho_barras, label=niveles_academicos[2])
    
    plt.xticks(x, departamentos_a_comparar)
    plt.xlabel('DEPARTAMENTOS')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    plt.title(f'RELACION DEL PBI PER CAPITA Y EL GASTO PUBLICO POR ALUMNO \nEN EDUCACION {niveles_academicos} EN EL AÑO {str(año)} \nDE LOS DEPARTAMENTOS {departamentos_a_comparar}')
    plt.legend()
    plt.show()


def graf_e():

    cant_años = int(input('Ingrese la cantidad de años a comparar: '))
    años_a_comparar = []
    for i in range(cant_años):
        año = pedir_año()
        años_a_comparar.append(año)
    nivel_acad = pedir_nivel_acad()

    #quitamos 'total' del df
    df_analisis = df_relacion_pbi_educacion[4:]
    df_analisis.reset_index(drop=True,inplace=True)

    #filtramos el nivel educativo de interÈs
    departamentos = df_pbi['Departamento'][:-1].tolist() #sacamos los dptos
    
    años = list(range(2011, 2022))
    años_a_borrar = []

    for year in años:
        if year not in años_a_comparar:
            años_a_borrar.append(year)
            
    df_analisis.drop(columns=años_a_borrar,inplace=True)
    
    for i in range(len(df_analisis)):
        if df_analisis['Departamento / Nivel educativo'][i] != nivel_acad and df_analisis['Departamento / Nivel educativo'][i] not in departamentos:
            df_analisis.drop(i,inplace=True)
            
    df_analisis = df_analisis[df_analisis[años_a_comparar[0]] != '']
    df_analisis.drop(columns=['Departamento / Nivel educativo'],inplace=True)
    df_analisis.insert(0,'Departamentos',departamentos)
    df_analisis.set_index('Departamentos',inplace=True)
    
    for i in range(cant_años):
        colores = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        plt.plot(departamentos,df_analisis[años_a_comparar[i]],label=años_a_comparar[i],color=colores[i]) 
    
    plt.xticks(departamentos,rotation=90)
    plt.title(f'RELACION DEL PBI PER CAPITA Y EL GASTO PUBLICO POR \nALUMNO EN EDUCACION {nivel_acad.upper()} EN LOS AÑOS {años_a_comparar}')
    plt.xlabel('DEPARTAMENTOS')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.legend()
    plt.show()       


def graf_f():

    nivel_acad = pedir_nivel_acad()

    #quitamos 'total' del df
    df_analisis = df_relacion_pbi_educacion[4:]
    df_analisis.reset_index(drop=True,inplace=True)

    #filtramos el nivel educativo de interÈs
    departamentos = df_pbi['Departamento'][:-1].tolist() #sacamos los dptos
    
    for i in range(len(df_analisis)):
        if df_analisis['Departamento / Nivel educativo'][i] != nivel_acad and df_analisis['Departamento / Nivel educativo'][i] not in departamentos:
            df_analisis.drop(i,inplace=True)
            
    df_analisis = df_analisis[df_analisis[2011] != '']
    df_analisis.drop(columns=['Departamento / Nivel educativo'],inplace=True)
    df_analisis.insert(0,'Departamentos',departamentos)
    df_analisis.set_index('Departamentos',inplace=True)
    
    #regiones 
    costa = ['Áncash','Arequipa','Prov. Const. del Callao','Ica','La Libertad','Lambayeque','Lima','Moquegua','Piura','Tacna','Tumbes']
    sierra = ['Apurímac','Ayacucho','Cajamarca','Cusco','Huancavelica','Huánuco','Junín','Pasco','Puno']
    selva = ['Amazonas','Loreto','Madre de Dios','San Martín','Ucayali']
    
    df_costa = df_analisis[df_analisis.index.isin(costa)].copy()
    df_sierra = df_analisis[df_analisis.index.isin(sierra)].copy()
    df_selva = df_analisis[df_analisis.index.isin(selva)].copy()
    
    años = list(range(2011, 2022))
    prom_costa = ['Costa']
    prom_sierra = ['Sierra']
    prom_selva = ['Selva']
    for año in años:
        prom_costa.append(round(df_costa[año].mean(),4))
        prom_sierra.append(round(df_sierra[año].mean(),4))
        prom_selva.append(round(df_selva[año].mean(),4))
    
    columnas = ['Region'] + años
    
    df_regiones_prom = pd.DataFrame([prom_costa,prom_sierra,prom_selva],columns=columnas)
    
    regiones = df_regiones_prom['Region'].tolist()
    for i in range(3):
        colores = ['blue', 'green', 'red']
        plt.plot(años,df_regiones_prom.iloc[i][1:],label=regiones[i],color=colores[i])
    
    plt.xticks(años,rotation=90)  
    plt.title(f'EVOLUCION DE LA RELACION ENTRE EL GASTO PUBLICO EN \nEDUCACION {nivel_acad.upper()}/PBI PER CAPITA DE LAS REGIONES {regiones}')
    plt.xlabel('Años')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.legend()
    plt.show()
    
    return df_regiones_prom

def graf_g():
    # Regiones
    costa = ['Áncash', 'Arequipa', 'Prov. Const. del Callao', 'Ica', 'La Libertad', 'Lambayeque', 'Lima', 'Moquegua', 'Piura', 'Tacna', 'Tumbes']
    sierra = ['Apurímac', 'Ayacucho', 'Cajamarca', 'Cusco', 'Huancavelica', 'Huánuco', 'Junín', 'Pasco', 'Puno']
    selva = ['Amazonas', 'Loreto', 'Madre de Dios', 'San Martín', 'Ucayali']
    
    regiones = {'Costa': costa, 'Sierra': sierra, 'Selva': selva}
    
    año = pedir_año()
    
    # Creamos diccionarios de listas para almacenar datos de cada nivel académico en cada región
    datos_inicial = {'Costa': [], 'Sierra': [], 'Selva': []}
    datos_primaria = {'Costa': [], 'Sierra': [], 'Selva': []}
    datos_secundaria = {'Costa': [], 'Sierra': [], 'Selva': []}
    
    for region, departamentos in regiones.items():
        for departamento in departamentos:
            for i in range(len(df_relacion_pbi_educacion)):
                if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
                    datos_inicial[region].append(df_relacion_pbi_educacion[año][i+1])
                    datos_primaria[region].append(df_relacion_pbi_educacion[año][i+2])
                    datos_secundaria[region].append(df_relacion_pbi_educacion[año][i+3])
    
    prom_inicial = []
    prom_primaria = []
    prom_secundaria = []
    for region in regiones:
        prom_inicial.append(round(sum(datos_inicial[region]) / len(datos_inicial[region]), 4))
        prom_primaria.append(round(sum(datos_primaria[region]) / len(datos_primaria[region]), 4))
        prom_secundaria.append(round(sum(datos_secundaria[region]) / len(datos_secundaria[region]), 4))
    
    # Crear DataFrame
    df_promedios = pd.DataFrame({
        'Region': list(regiones.keys()),
        'Inicial': prom_inicial,
        'Primaria': prom_primaria,
        'Secundaria': prom_secundaria
    })
    
    # Generación del gráfico
    ancho_barras = 0.2
    x = np.arange(len(regiones))
    
    plt.bar(x - ancho_barras, prom_inicial, width=ancho_barras, label='Inicial')
    plt.bar(x, prom_primaria, width=ancho_barras, label='Primaria')
    plt.bar(x + ancho_barras, prom_secundaria, width=ancho_barras, label='Secundaria')
    
    plt.xticks(x, regiones.keys())
    plt.xlabel('REGIONES')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    plt.title(f'RELACION DEL PBI PER CAPITA Y EL GASTO PUBLICO POR ALUMNO \nEN LOS TRES NIVELES DE EDUCACIÓN PARA EL AÑO {str(año)} \nDE LAS REGIONES [Costa, Sierra, Selva]')
    plt.legend()
    plt.show()
    
    return df_promedios


'--------------------------------------------------------------------------------'
ruta1 = "C:/Sebastian/UNIVERSIDAD DEL PACÍFICO/2024-1/Técnicas de Programación/Proyecto/Para crear Tabla PBI per cápita/PBI POR DEPARTAMENTO 2007-2022.xlsx"
ruta2 = "C:/Sebastian/UNIVERSIDAD DEL PACÍFICO/2024-1/Técnicas de Programación/Proyecto/Para crear Tabla PBI per cápita/CRECIMIENTO POBLACIONAL 2007-2022.xlsx"
ruta3 = "C:/Sebastian/UNIVERSIDAD DEL PACÍFICO/2024-1/Técnicas de Programación/Proyecto/Para crear Tabla PBI per cápita/GASTO PÚBLICO EDUCACIÓN BÁSICA REGULAR.xlsx"
ruta4 = "C:/Sebastian/UNIVERSIDAD DEL PACÍFICO/2024-1/Técnicas de Programación/Proyecto/Para crear Tabla PBI per cápita/OPCIONAL. TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022.xlsx"

#ruta1 = "C:/Users/ws.mincholar/Downloads/PBI POR DEPARTAMENTO 2007-2022.xlsx"
#ruta2 = "C:/Users/ws.mincholar/Downloads/CRECIMIENTO POBLACIONAL 2007-2022.xlsx"
#ruta3 = "C:/Users/ws.mincholar/Downloads/GASTO PÚBLICO POR ALUMNO EN EDUCACIÓN BÁSICA REGULAR 2011-2021.xlsx"
#ruta4 = "C:/Users/sebas/Downloads/OPCIONAL. TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022.xlsx"

#---Carga  y limpueza de DF PBI y POBLACION
df_pbi,df_pob = cargarDF_PBI_POB(ruta1, ruta2)
df_pbi = limpiarDF(df_pbi)
df_pob = limpiarDF(df_pob)
#print(df_pbi)
#print(df_pob)

#---Creacion de nuevo df del pbi per cápita
df_pbi_percapita = estabelecerDF_PBIpercapita(df_pbi, df_pob)
#print(df_pbi_percapita)

#---Carga del df de gasto en público por alumno en educacion
df_gasto_edu = cargarDF_gasto_educacion(ruta3)
#print(df_gasto_edu)

#---Establecimiento de la relacion entre ingreso (pbi per capita) y gasto
df_relacion_pbi_educacion = establecer_relacion_pbi_educacion(df_gasto_edu, df_pbi_percapita)
#print(df_relacion_pbi_educacion)

#---Carga del df de analfabetismo
df_analfabetismo = cargar_df_analfabetismo(ruta4)
df_an_con_tasa_prom = DF_con_tasa_promedio_analfabetismo(df_analfabetismo)
#grafico_analfabetismo_tasa_promedio_por_dpto(df_an_con_tasa_prom)

#---Gráfico dashboard
grafico_dashboard()


print('''Opciones de graficos:

a) Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para el año de su elección, dentro del período 2011-2021

b) Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de los departamentos de su elección durante el periodo 2011-2021
    
c) Evolución de la relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita del departamento de su elección durante el periodo 2011-2021

d) Relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita de los departamentos de su elección para el año de su elección, dentro del período 2011-2021
    
e) Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para los años de su elección, dentro del período 2011-2021
  
f) Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de las regiones del Perú durante el periodo 2011-2021

g) Evolución de la relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita de las regiones del Perú para el año de su elección, dentro del período 2011-2021
    
    ''')

opcion = input('Ingrese la opcion de gráfico a utilizar: ').lower()

while opcion not in ['a','b','c','d','e','f','g','']:
    opcion = input('Ingrese la opcion de gráfico a utilizar: ').lower()


if opcion == 'a':
    print('\nGrafico: Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para el año de su elección, dentro del período 2011-2021\n')
    graf_a()
elif opcion == 'b':
    print('\nGrafico: Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de los departamentos de su elección durante el periodo 2011-2021\n')
    graf_b()
elif opcion == 'c':
    print('\nGrafico: Evolución de la relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita del departamento de su elección durante el periodo 2011-2021\n')
    graf_c()
elif opcion == 'd':
    print('\nGrafico: Relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita de los departamentos de su elección para el año de su elección, dentro del período 2011-2021\n')
    graf_d()
elif opcion == 'e':
    print('\nGrafico: Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para los año de su elección, dentro del período 2011-2021\n')
    graf_e()
elif opcion == 'f':
    print('\nGrafico: Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de las regiones del Perú durante el periodo 2011-2021\n')
    df = graf_f()
    print(df)
elif opcion == 'g':
    print('\nGrafico: Evolución de la relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita de las regiones del Perú para el año de su elección, dentro del período 2011-2021\n')
    df = graf_g()
    print(df)
elif opcion == '':
    print('No se eligió ninguna opción. Vuelva a ejecutar el código')