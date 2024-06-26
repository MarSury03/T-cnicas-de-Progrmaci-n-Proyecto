import pandas as pd
pd.options.mode.chained_assignment = None  # deshabilitar las advertencias de asignación en cadena
from matplotlib import pyplot as plt

ruta1 = "C:/Users/Usuario/Downloads/1. PBI POR DEPARTAMENTO 2007-2022.xlsx"
ruta2 = "C:/Users/Usuario/Downloads/2. CRECIMIENTO POBLACIONAL 2007-2022.xlsx"
ruta3 = "C:/Users/Usuario/Downloads/3. GASTO PÚBLICO POR ALUMNO EN EDUCACIÓN BÁSICA REGULAR 2011-2021.xlsx"
ruta4 = "C:/Users/Usuario/Downloads/4. TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2008-2022.xlsx"

# CARGAR Y LIMPIAR BASES DE DATOS

def cargar_y_limpiar_DF_PBI_POB(ruta1,ruta2):
    
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
    
    #quitamos las columnas con los años que no vamos a trabajar
    df_pbi.drop([2007,2008,2009,2010,2022],axis=1,inplace=True)
    df_pob.drop([2007,2008,2009,2010,2022],axis=1,inplace=True)
    
    return df_pbi,df_pob


def cargar_y_limpiar_DF_gasto_educacion(ruta3):
    
    archivo_gasto_edu = pd.read_excel(ruta3)
    df_gasto_edu = pd.DataFrame(archivo_gasto_edu)

    # Extraemos la fila 3 para usarla como nombres de las columnas
    nom_col_edu = df_gasto_edu.iloc[2].tolist()
    df_gasto_edu.columns = nom_col_edu

    # Eliminamos las tres primeras filas (incluyendo la que usamos como cabecera)
    df_gasto_edu = df_gasto_edu.drop([0, 1, 2])
    df_gasto_edu.reset_index(drop=True, inplace=True)

    # Rellenamos valores nulos con cadenas vacías
    df_gasto_edu.fillna("", inplace=True)

    # Eliminamos columnas correspondientes a los años 1999-2010
    años_a_eliminar = list(range(1999, 2011))
    df_gasto_edu.drop(años_a_eliminar, axis=1, inplace=True)

    # Limpiamos los nombres de las filas eliminando espacios y guiones
    nombres_filas = df_gasto_edu['Nivel educativo /\nDepartamento'].tolist()
    filas_limpias = []
    for nombre_fila in nombres_filas:
        nombre_fila = nombre_fila.strip().strip('-')
        filas_limpias.append(nombre_fila)

    # Reemplazamos la columna de nombres de filas con las filas limpias
    df_gasto_edu.drop('Nivel educativo /\nDepartamento', axis=1, inplace=True)
    df_gasto_edu.insert(0, 'Departamento / Nivel educativo', filas_limpias)
    
    return df_gasto_edu


def cargar_y_limpiar_DF_analfabetismo(ruta4):
    archivo = pd.read_excel(ruta4)
    df = pd.DataFrame(archivo)
    
    # Extraemos los departamentos desde la columna adecuada
    departamentos = df['TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022']
    departamentos = departamentos.iloc[10:].reset_index(drop=True)
    
    # Eliminamos la columna innecesaria y las filas iniciales
    df = df.drop(columns=['TASA DE ANALFABETISMO DE LA POBLACIÓN DE 15 Y MÁS AÑOS DE EDAD, SEGÚN ÁMBITO GEOGRÁFICO, 2012 - 2022'])
    df = df[10:]
    df = df.reset_index(drop=True)
    
    # Creamos las nuevas columnas con los años y ajustamos los nombres de las columnas
    columnas = []
    for año in range(2008, 2023):
        columnas.append(año)
    
    df.columns = columnas
    
    # Insertamos la columna de Departamento al inicio
    df.insert(0, 'Departamento', departamentos)
    
    # Eliminamos las columnas que no utilizaremos (2008, 2009, 2010, 2022)
    df = df.drop(columns=[2008, 2009, 2010, 2022])
    
    return df


# ESTABLECER RELACIONES ENTRE BASES DE DATOS

def establecer_DF_PBIpercapita(df_pbi, df_pob):
    
    # Obtenemos la lista de departamentos, excluyendo la última fila, y luego agregamos 'Total'
    departamentos = df_pbi['Departamento'][:-1].tolist()
    departamentos.append('Total')

    # Creamos un nuevo DataFrame para el PBI per cápita con los departamentos como primera columna
    df_pbi_percapita = pd.DataFrame(departamentos, columns=['Departamento'])

    # Calculamos el PBI per cápita para los años 2011 a 2021
    for año in range(2011, 2022):
        pbi_per_capita_anno = []
        for pbi, pob in zip(df_pbi[año], df_pob[año]):
            pbi_per_capita = round(pbi * 1000 / pob, 2)
            pbi_per_capita_anno.append(pbi_per_capita)
        df_pbi_percapita[año] = pbi_per_capita_anno
    
    # Reorganizamos las filas para poner 'Total' al principio
    df_pbi_percapita1 = df_pbi_percapita.iloc[[-1]]
    df_pbi_percapita2 = df_pbi_percapita.iloc[:-1]
    df_pbi_percapita = pd.concat([df_pbi_percapita1, df_pbi_percapita2])
    df_pbi_percapita.reset_index(drop=True, inplace=True)
    
    return df_pbi_percapita


def establecer_DF_relacion_pbi_educacion(df_gasto_edu, df_pbi_percapita):
    nombres_filas = df_gasto_edu['Departamento / Nivel educativo'].tolist()
    df_relacion_pbi_educacion = pd.DataFrame(nombres_filas, columns=['Departamento / Nivel educativo'])

    año = 2011
    
    for a in range(11):
        relacion_lista = []
        
        # Iteramos sobre cada departamento y su correspondiente PBI per cápita en el año actual
        for departamento, pbi in zip(df_pbi_percapita['Departamento'], df_pbi_percapita[año]):
            for i in range(len(df_gasto_edu)):
                if df_gasto_edu['Departamento / Nivel educativo'][i] == departamento:
                    relacion_lista.append('')
                    
                    # Calculamos la relación entre el gasto educativo y el PBI per cápita para los tres niveles educativos
                    for j in range(1, 4):
                        relacion = df_gasto_edu[año][i + j] / pbi
                        relacion_lista.append(round(relacion, 4))
                        
        # Añadimos la lista de relaciones calculadas al DataFrame df_relacion_pbi_educacion
        df_relacion_pbi_educacion[año] = relacion_lista
        año += 1
    
    return df_relacion_pbi_educacion


def establecer_DF_tasa_promedio_analfabetismo(df):
    # Establecemos el índice del DataFrame como 'Departamento'
    df = df.set_index('Departamento')
    
    # Transponemos el DataFrame para que los departamentos sean las columnas
    df = df.transpose()
    
    # Calculamos los promedios de cada departamento
    promedios = []
    for departamento in df:
        promedio = df[departamento].mean()
        promedios.append(round(promedio, 4))
    
    # Volvemos a transponer el DataFrame para que los años sean las columnas nuevamente
    df = df.transpose()
    
    # Añadimos la columna de 'Tasa promedio' de analfabetismo
    df.insert(len(df.columns), 'Tasa promedio', promedios)
    
    # Reseteamos los índices del DataFrame
    df.reset_index(inplace=True)
    
    return df


# GRAFICAR BASE DE DATOS PRINCIPAL (PROBLEMA)

def grafico_analfabetismo_tasa_promedio_por_dpto(df):
    # Filtramos solo las columnas necesarias para graficar
    df = df[['Departamento', 'Tasa promedio']]
    
    # Ordenamos la data de mayor a menor según la tasa promedio
    df = df.sort_values(by='Tasa promedio', ascending=False)
    
    # Configuramos la figura del gráfico
    plt.figure(figsize=(8, 8))
    plt.xticks(rotation=90)
    
    # Barras para las 4 tasas más altas (rojo)
    barras_grandes = plt.bar(df['Departamento'].iloc[:4], df['Tasa promedio'].iloc[:4], color='red', label='Tasas más altas')
    
    # Barras para el rango intermedio (gris)
    plt.bar(df['Departamento'].iloc[4:21], df['Tasa promedio'].iloc[4:21], color='grey')
    
    # Barras para las 4 tasas más bajas (verde)
    barras_pequeñas = plt.bar(df['Departamento'].iloc[-4:], df['Tasa promedio'].iloc[-4:], color='green', label='Tasas más bajas')

    # Añadimos etiquetas de valores encima de las barras más altas
    for bar in barras_grandes:
        valor_Y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, valor_Y, round(valor_Y, 2), va='bottom', ha='center', fontsize=8, color='black', fontweight='bold', rotation=50)
    
    # Añadimos etiquetas de valores encima de las barras más bajas
    for bar in barras_pequeñas:
        valor_Y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, valor_Y, round(valor_Y, 2), va='bottom', ha='center', fontsize=8, color='black', fontweight='bold', rotation=50)
    
    # Configuramos el título y etiquetas de los ejes
    plt.title('TASA PROMEDIO DE ANALFABETISMO EN LOS DEPARTAMENTOS \nDEL PERÚ DESDE EL 2011 AL 2021 \n (Porcentaje respecto del total de la población mayor a 15 años)')
    plt.ylabel('% DE POBLACIÓN ANALFABETA')
    plt.xlabel('DEPARTAMENTOS')
    
    # Mostramos la leyenda
    plt.legend()
    
    # Mostramos el gráfico
    plt.show()
    

# ESTANDARIZAR INPUTS

def pedir_departamento():
    while True:
        dep = input('Ingrese el departamento a analizar: ').strip().title()
        
        # Corregimos errores comunes en el ingreso del nombre del departamento
        correcciones = {
            'De ': 'de ',
            'Apurimac': 'Apurímac',
            'Callao': 'Prov. Const. del Callao',
            'Ancash': 'Áncash',
            'Huanuco': 'Huánuco',
            'Junin': 'Junín',
            'Martin': 'Martín'
        }
        
        # Aplicamos las correcciones definidas
        for error, correccion in correcciones.items():
            if error in dep:
                dep = dep.replace(error, correccion)
        
        # Validamos que el departamento ingresado sea válido
        if dep in df_pbi_percapita['Departamento'].tolist():
            return dep
        else:
            # Solicitamos al usuario que ingrese nuevamente si el departamento no es válido
            print('Error. Ingrese un departamento válido.')


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


# ESTABLECER DASHBOARD 

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


def grafico_dashboard1(departamentos_a_comparar):
    
    cant_departamentos = len(departamentos_a_comparar)
    #cant_departamentos = int(input('Ingrese la cantidad de departamentos a comparar: '))
    
    #departamentos_a_comparar = []
    #for i in range(cant_departamentos):
        #departamento = pedir_departamento()
        #departamentos_a_comparar.append(departamento)
    
    plt.figure(figsize=(20,22))
    
    grafico_ingreso(df_pbi_percapita,cant_departamentos,departamentos_a_comparar)
    
    grafico_gasto(df_gasto_edu,cant_departamentos,departamentos_a_comparar)

    grafico_relacion_ingreso_gasto(df_relacion_pbi_educacion,cant_departamentos,departamentos_a_comparar)
    
    grafico_analfabetismo(df_analfabetismo,cant_departamentos,departamentos_a_comparar)
    
    plt.show()


def normalizar(lista):
    min_val = min(lista)
    max_val = max(lista)
    
    num_normalizados = []
    for num in lista:
        num_normalizados.append((num - min_val) / (max_val - min_val))
    
    return num_normalizados   


def grafico_ingreso_gasto_relacion(df_pbi_percapita, df_gasto_edu, df_relacion_pbi_educacion,departamento):
    # Pedimos al usuario que ingrese el departamento a analizar
    #departamento = pedir_departamento()
    
    plt.subplot(1,2,1)
    
    # Obtenemos los ingresos per cápita del departamento seleccionado
    ingresos = df_pbi_percapita.loc[df_pbi_percapita['Departamento'] == departamento].values.tolist()[0][1:]
    
    # Obtenemos los años
    años = df_gasto_edu.columns.tolist()[1:]
    
    # Lista para almacenar los gastos promedio de educación por año
    gastos_promedio = []
    
    # Recorremos cada fila del DataFrame de gasto educativo para encontrar el departamento seleccionado
    for i in range(len(df_gasto_edu)):
        if df_gasto_edu['Departamento / Nivel educativo'][i] == departamento:
            # Filtramos las filas correspondientes a inicial, primaria y secundaria
            df_filtrada = df_gasto_edu.iloc[i+1:i+4].reset_index(drop=True)
            
            # Calculamos el promedio de gasto para cada año
            for año in años:
                prom_año = round(df_filtrada[año].mean(), 4)
                gastos_promedio.append(prom_año)
    
    # Lista para almacenar las relaciones promedio entre gasto e ingreso por año
    relaciones_promedio = []
    
    for i in range(len(df_relacion_pbi_educacion)):
        if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
            # Filtramos las filas correspondientes a inicial, primaria y secundaria
            df_filtrada = df_relacion_pbi_educacion.iloc[i+1:i+4].reset_index(drop=True)
            
            # Calculamos el promedio de la relación para cada año
            for año in años:
                prom_año = round(df_filtrada[año].mean(), 4)
                relaciones_promedio.append(prom_año)
         
    # Normalizamos los valores de ingresos, gastos y relaciones para comparación
    ingresos_normalizados = normalizar(ingresos)
    gastos_normalizados = normalizar(gastos_promedio)
    relaciones_normalizadas = normalizar(relaciones_promedio)

    # Colores para las líneas de los diferentes conjuntos de datos
    colores = ['blue', 'green', 'red']
    
    # Graficamos las líneas normalizadas para ingresos, gastos y relaciones
    plt.plot(años, ingresos_normalizados, label='Ingreso per cápita (Normalizado)', color=colores[0]) 
    plt.plot(años, gastos_normalizados, label='Gasto en educación por alumno (Normalizado)', color=colores[1])    
    plt.plot(años, relaciones_normalizadas, label='Relación entre el gasto e ingreso (Normalizado)', color=colores[2])     
    
    # Configuramos las etiquetas y título del gráfico
    plt.xticks(años, rotation=90)    
    plt.title(f'EVOLUCIÓN DEL INGRESO PER CÁPITA, GASTO EN EDUCACIÓN POR ALUMNO Y \nRELACIÓN ENTRE EL GASTO PÚBLICO POR ALUMNO Y PBI PER CÁPITA DE {departamento.upper()}')
    plt.xlabel('AÑOS')
    plt.ylabel('VALORES NORMALIZADOS')
    
    plt.grid(True)  # Añadimos cuadrícula al gráfico
    plt.legend()  # Mostramos la leyenda
    

def grafico_analfabetismo_relacion(df_analfabetismo, df_relacion_pbi_educacion, departamento):
    # Pedimos al usuario que ingrese el departamento a analizar
    #departamento = pedir_departamento()
    
    plt.subplot(1,2,2)
    
    # Obtenemos las tasas de analfabetismo del departamento seleccionado
    tasas_analfabetismo = df_analfabetismo.loc[df_analfabetismo['Departamento'] == departamento].values.tolist()[0][1:]
    
    # Obtenemos los años
    años = df_analfabetismo.columns.tolist()[1:]
    
    # Lista para almacenar las relaciones promedio entre gasto e ingreso por año
    relaciones_promedio = []
    
    for i in range(len(df_relacion_pbi_educacion)):
        if df_relacion_pbi_educacion['Departamento / Nivel educativo'][i] == departamento:
            # Filtramos las filas correspondientes a inicial, primaria y secundaria
            df_filtrada = df_relacion_pbi_educacion.iloc[i+1:i+4].reset_index(drop=True)
            
            # Calculamos el promedio de la relación para cada año
            for año in años:
                prom_año = round(df_filtrada[año].mean(), 4)
                relaciones_promedio.append(prom_año)
         
    # Normalizamos los valores de tasas y relaciones para comparación
    tasas_analfabetismo_normalizados = normalizar(tasas_analfabetismo)
    relaciones_normalizadas = normalizar(relaciones_promedio)


    # Colores para las líneas de los diferentes conjuntos de datos
    colores = ['blue', 'red']
    
    # Graficamos las líneas normalizadas para ingresos, gastos y relaciones
    plt.plot(años, tasas_analfabetismo_normalizados, label='Tasa de analfabetismo (Normalizado)', color=colores[0])     
    plt.plot(años, relaciones_normalizadas, label='Relación entre el gasto e ingreso (Normalizado)', color=colores[1])     
    
    # Configuramos las etiquetas y título del gráfico
    plt.xticks(años, rotation=90)    
    plt.title(f'EVOLUCIÓN DE LA TASA DE ANALFABETISMO Y RELACIÓN ENTRE EL GASTO PÚBLICO \nPOR ALUMNO Y PBI PER CÁPITA DE {departamento.upper()}')
    plt.xlabel('AÑOS')
    plt.ylabel('VALORES NORMALIZADOS')
    
    plt.grid(True)  # Añadimos cuadrícula al gráfico
    plt.legend()  # Mostramos la leyenda
    

def grafico_dashboard2(departamento):
    
    #departamento = pedir_departamento()
    
    plt.figure(figsize=(20,8))
    
    grafico_ingreso_gasto_relacion(df_pbi_percapita, df_gasto_edu, df_relacion_pbi_educacion, departamento)
    
    grafico_analfabetismo_relacion(df_analfabetismo, df_relacion_pbi_educacion, departamento)
    
    plt.show()


def departamentos_max_min_analfabetismo(df):
    #filtramos solo las columnas necesarias para graficar
    df = df[['Departamento','Tasa promedio']]
    
    #ordenamos la data de mayor a menor
    df = df.sort_values(by='Tasa promedio', ascending=False)
    
    lista_dep_mayores_tasas = df['Departamento'].iloc[:4].tolist()
    lista_dep_menores_tasas = df['Departamento'].iloc[-4:].tolist()
    
    dep_mayor_tasa = lista_dep_mayores_tasas[0]
    dep_menor_tasa = lista_dep_menores_tasas[-1]
    
    return lista_dep_mayores_tasas,lista_dep_menores_tasas,dep_mayor_tasa,dep_menor_tasa


# GRAFICOS A ANALIZAR

def grafico_comparacion_departamentos_tasas_altas(lista_dep_mayores_tasas):
    grafico_dashboard1(lista_dep_mayores_tasas)
    
def grafico_comparacion_departamentos_tasas_menos(lista_dep_menores_tasas):
    grafico_dashboard1(lista_dep_menores_tasas)

def grafico_comparacion_departamentos_tasa_mayor_menor(lista):
    grafico_dashboard1(lista)

def grafico_analisis_departamento_mayor_tasa(dep_mayor_tasa):
    grafico_dashboard2(dep_mayor_tasa)

def grafico_analisis_departamento_menor_tasa(dep_menor_tasa):
    grafico_dashboard2(dep_menor_tasa)
'----------------------------------------------------------------------------------------------'

df_pbi,df_pob = cargar_y_limpiar_DF_PBI_POB(ruta1, ruta2)
#print(df_pbi)
#print(df_pob)

df_gasto_edu = cargar_y_limpiar_DF_gasto_educacion(ruta3)
#print(df_gasto_edu)

df_analfabetismo = cargar_y_limpiar_DF_analfabetismo(ruta4)
#print(df_analfabetismo)

df_pbi_percapita = establecer_DF_PBIpercapita(df_pbi, df_pob)
#print(df_pbi_percapita)

df_relacion_pbi_educacion = establecer_DF_relacion_pbi_educacion(df_gasto_edu, df_pbi_percapita)
#print(df_relacion_pbi_educacion)

df_analfabetismo_promedio = establecer_DF_tasa_promedio_analfabetismo(df_analfabetismo)
#print(df_analfabetismo_promedio)

#grafico_analfabetismo_tasa_promedio_por_dpto(df_analfabetismo_promedio)

#grafico_dashboard1()

#grafico_ingreso_gasto_relacion(df_pbi_percapita, df_gasto_edu, df_relacion_pbi_educacion)

#grafico_analfabetismo_relacion(df_analfabetismo, df_relacion_pbi_educacion)

#grafico_dashboard2()

lista_mayores,lista_menores,dep_max,dep_min = departamentos_max_min_analfabetismo(df_analfabetismo_promedio)
#print(lista_menores)

#grafico_comparacion_departamentos_tasas_altas(lista_mayores)

#grafico_comparacion_departamentos_tasas_menos(lista_menores)

#grafico_comparacion_departamentos_tasa_mayor_menor([dep_max,dep_min])

#grafico_analisis_departamento_mayor_tasa(dep_max)

grafico_analisis_departamento_menor_tasa(dep_min)