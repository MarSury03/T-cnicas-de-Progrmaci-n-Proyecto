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


####---------------------------------FUNCIÓN ESTANDARIZADORA DE INPUTS
def pedir_departamento():
    dep = input('Ingrese el departamento a analizar: ').title()
    
    #nos cercioramos de que el departamento y nivel académico introducidos se encuentren escritos correctamente
    if ' De ' in dep:
        dep = dep.replace(' De ',' de ')
        
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
def graf_a():
    ###------------------pa todos los dptos, aÒo especÌfico y nivel acadÈmico
    año = pedir_año()
    nivel_acad = pedir_nivel_acad()

    #quitamos 'total' del df
    df_analisis = df_relacion_pbi_educacion[4:]
    df_analisis.reset_index(drop=True,inplace=True)

    #filtramos el nivel educativo de interÈs
    departamentos = df_pbi['Departamento'][:-1].tolist() #sacamos los dptos

    for i in range(len(df_analisis)):
        if df_analisis['Departamento / Nivel educativo'][i] != nivel_acad and df_analisis['Departamento / Nivel educativo'][i] not in departamentos:
            df_analisis.drop(i,inplace=True)

    df_analisis.reset_index(drop=True,inplace=True)

    #nos quedamos con el aÒo de interÈs
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

    df_analisis.plot(kind='bar',legend=False,xlabel='DEPARTAMENTOS',ylabel='GASTO(SOLES)/PBI PER C¡PITA')
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
    plt.title(f'EVOLUCION DE LA RELACION ENTRE EL GASTO PUBLICO EN \nEDUCACION {nivel_acad}/PBI PER CAPITA DE LAS REGIONES {regiones}')
    plt.xlabel('Años')
    plt.ylabel('GASTO(SOLES)/PBI PER CAPITA')
    
    plt.legend()
    plt.show()

def graf_g():
    """
    Comparación del Crecimiento del PIB per cápita y el Gasto en Educación por Departamento
    """
    # Solicitar el año de inicio y fin para la comparación
    año_inicio = int(input("Ingrese el año de inicio para la comparación (e.g., 2011): "))
    año_fin = int(input("Ingrese el año de fin para la comparación (e.g., 2021): "))

    # Filtrar los datos para el período seleccionado
    df_pbi_filtrado = df_pbi[[año_inicio, año_fin, 'Departamento']].copy()
    df_gasto_filtrado = df_gasto_edu[[año_inicio, año_fin, 'Departamento']].copy()

    # Calcular el crecimiento
    df_pbi_filtrado['Crecimiento_PBI'] = ((df_pbi_filtrado[año_fin] - df_pbi_filtrado[año_inicio]) / df_pbi_filtrado[año_inicio]) * 100
    df_gasto_filtrado['Crecimiento_Gasto'] = ((df_gasto_filtrado[año_fin] - df_gasto_filtrado[año_inicio]) / df_gasto_filtrado[año_inicio]) * 100

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(14, 8))
    ancho_barras = 0.4  # Ancho de las barras

    # Posiciones de las barras
    indices = range(len(df_pbi_filtrado))

    # Crear las barras para el PIB per cápita
    barras_pbi = ax.bar([i - ancho_barras / 2 for i in indices], df_pbi_filtrado['Crecimiento_PBI'], width=ancho_barras, label='Crecimiento PIB per cápita (%)')

    # Crear las barras para el gasto en educación
    barras_gasto = ax.bar([i + ancho_barras / 2 for i in indices], df_gasto_filtrado['Crecimiento_Gasto'], width=ancho_barras, label='Crecimiento Gasto en Educación (%)')

    # Etiquetas y títulos
    ax.set_xlabel('Departamentos')
    ax.set_ylabel('Crecimiento (%)')
    ax.set_title(f'Comparación del Crecimiento del PIB per cápita y el Gasto en Educación\npor Departamento del {año_inicio} al {año_fin}')
    ax.set_xticks(indices)
    ax.set_xticklabels(df_pbi_filtrado['Departamento'], rotation=90)
    ax.legend()

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()
        

'--------------------------------------------------------------------------------'
#ruta1 = "C:/Sebastian/UNIVERSIDAD DEL PACÕFICO/2024-1/TÈcnicas de ProgramaciÛn/Proyecto/Para crear Tabla PBI per c·pita/PBI POR DEPARTAMENTO 2007-2022.xlsx"
#ruta2 = "C:/Sebastian/UNIVERSIDAD DEL PACÕFICO/2024-1/TÈcnicas de ProgramaciÛn/Proyecto/Para crear Tabla PBI per c·pita/CRECIMIENTO POBLACIONAL 2007-2022.xlsx"
#ruta3 = "C:/Sebastian/UNIVERSIDAD DEL PACÕFICO/2024-1/TÈcnicas de ProgramaciÛn/Proyecto/Para crear Tabla PBI per c·pita/GASTO P⁄BLICO EDUCACI”N B¡SICA REGULAR.xlsx"
ruta1 = "C:/Users/USER/Downloads/PBI POR DEPARTAMENTO 2007-2022.xlsx"
ruta2 = "C:/Users/USER/Downloads/CRECIMIENTO POBLACIONAL 2007-2022.xlsx"
ruta3 = "C:/Users/USER/Downloads/GASTO PÚBLICO EDUCACIÓN BÁSICA REGULAR.xlsx"

df_pbi,df_pob = cargarDF_PBI_POB(ruta1, ruta2)

df_pbi = limpiarDF(df_pbi)
df_pob = limpiarDF(df_pob)
#print(df_pbi)
#print(df_pob)

df_pbi_percapita = estabelecerDF_PBIpercapita(df_pbi, df_pob)
#print(df_pbi_percapita)
df_gasto_edu = cargarDF_gasto_educacion(ruta3)
#print(df_gasto_edu)

df_relacion_pbi_educacion = establecer_relacion_pbi_educacion(df_gasto_edu, df_pbi_percapita)
#print(df_relacion_pbi_educacion)


print('''Opciones de graficos:

a) Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para el año de su elección, dentro del período 2011-2021

b) Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de los departamentos de su elección durante el periodo 2011-2021
    
c) Evolución de la relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita del departamento de su elección durante el periodo 2011-2021

d) Relación entre el gasto público en educación (inicial, primaria y secundaria) y el PIB per cápita de los departamentos de su elección para el año de su elección, dentro del período 2011-2021
    
e) Relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de cada departamento del Perú para los años de su elección, dentro del período 2011-2021
  
f) Evolución de la relación entre el gasto público en educación (inicial, primaria o secundaria) y el PIB per cápita de las regiones del Perú durante el periodo 2011-2021

    ''')
      
opcion = input('Ingrese la opcion de gráfico a utilizar: ')


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
    graf_f()
elif opcion == 'g':
    print('\nGrafico: Comparación del Crecimiento del PIB per cápita y el Gasto en Educación por Departamento\n')
    graf_g()