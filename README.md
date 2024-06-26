# Análisis del Analfabetismo en los Departamentos del Perú (2011-2021)

Este proyecto tiene como objetivo analizar la relación entre el PBI per cápita, el gasto público por alumno en educación y la tasa de analfabetismo en los departamentos del Perú desde 2011 hasta 2021. El estudio se enfoca en identificar las disparidades regionales y las tendencias temporales que afectan el desarrollo socioeconómico, con un énfasis particular en los departamentos con las tasas de analfabetismo más altas (Apurímac, Huánuco, Huancavelica y Cajamarca) y los departamentos con las tasas más bajas (Callao, Ica, Tumbes y Tacna).

## Estructura del Proyecto

### Archivos Principales

- `PROYECTO_TP_VF.txt`: Contiene el código principal para cargar, limpiar y analizar los datos, así como para generar gráficos.
- `PBI_POBLACION.xlsx`: Datos de PBI por departamento y crecimiento poblacional.
- `GASTO_EDUCACION.xlsx`: Datos del gasto público en educación básica regular.
- `ANALFABETISMO.xlsx`: Datos de la tasa de analfabetismo de la población de 15 y más años de edad.

## Procedimiento

El procedimiento consta de los pasos que se muestran a continuación:

#### Importación de las librerías

Se importan las librerías pandas y matplotlib para el tratamiento y preparación de los datos, y para la generación de los gráficos.

#### Carga y preparación de los datos de los archivos antes mencionados

Se define una función llamada `cargar_y_limpiar_DF_PBI_POB` que realiza las siguientes acciones:
- Usando la biblioteca pandas, se leen los archivos Excel que contienen los datos del Producto Bruto Interno (PBI) por departamento y los de la población.
- Se convierten los archivos leídos en DataFrames de pandas.
- Se asigna como encabezados de columnas a la fila correcta, se eliminan las filas que no se necesitan y se resetea el índice para mantener la consistencia en las filas.
- Se eliminan las columnas correspondientes a los años que no se trabajarán (2007, 2008, 2009, 2010, 2022).

#### Carga y preparación de los datos de gasto en educación pública

Se define una función llamada `cargar_y_limpiar_DF_gasto_educacion` que realiza las siguientes acciones:
- Usando pandas, se leen los datos desde un archivo Excel.
- Se establece la primera fila de los datos como nombres de las columnas y se eliminan las filas adicionales que no son necesarias.
- Se resetean los índices del DataFrame y se eliminan las filas con valores nulos en la columna de “Año”.
- Se ajusta el tipo de dato de la columna “Año”, convirtiéndola a entero para facilitar operaciones aritméticas y comparaciones.

#### Carga y preparación de datos de analfabetismo

Se define una función llamada `cargar_y_limpiar_DF_analfabetismo` que realiza las siguientes acciones:
- Se lee un archivo Excel que contiene la tasa de analfabetismo de la población de 15 años y más, organizada por departamentos y años específicos.
- Se extraen los departamentos desde la columna adecuada, se eliminan columnas y filas innecesarias y se resetea el índice para mantener la consistencia en los datos.
- Se ajustan los nombres de las columnas y se eliminan los años que no se utilizarán (2008, 2009, 2010, 2022).

#### Cálculo del PBI per cápita

Se establece una función titulada `establecer_DF_PBIpercapita` que realiza las siguientes acciones:
- Calcula el PBI per cápita para cada departamento y año.
- Organiza los datos en un nuevo DataFrame para facilitar el análisis posterior.
- Reorganiza las filas para poner 'Total' al principio.

#### Establecer la relación entre el PBI per cápita y el gasto en educación

Se define una función llamada `establecer_DF_relacion_pbi_educacion` que realiza las siguientes acciones:
- Selecciona las columnas relevantes del DataFrame de gasto en educación.
- Crea un DataFrame vacío para almacenar la relación de PBI per cápita y gasto en educación.
- Itera sobre cada año en las columnas del DataFrame de PBI per cápita, filtrando los datos de gasto en educación y PBI per cápita para cada año.
- Une los DataFrames de PBI per cápita y gasto en educación, utilizando la columna “Departamento” como clave de unión.
- Concatena los datos combinados de cada año al DataFrame final.

#### Conversión a tasas promedio de analfabetismo

Se define una función llamada `establecer_DF_tasa_promedio_analfabetismo` que toma un DataFrame de tasas de analfabetismo y calcula la tasa promedio para cada departamento.

#### Generación de gráfico de analfabetismo promedio por departamento

Se define una función llamada `grafico_analfabetismo_tasa_promedio_por_dpto` que toma un DataFrame como argumento y genera un gráfico de barras que muestra la tasa promedio de analfabetismo por departamento en Perú.

#### Estandarización de inputs

Se definen tres funciones para estandarizar las entradas del usuario:
- `pedir_departamento`: Solicita al usuario que ingrese un nombre de departamento y normaliza la entrada para asegurar la capitalización y el formato correctos. Verifica que el departamento ingresado esté en una lista predefinida.
- `pedir_nivel_acad`: Solicita al usuario que ingrese un nivel académico (Inicial, Primaria o Secundaria) y verifica que el nivel ingresado esté en la lista predefinida.
- `pedir_año`: Solicita al usuario que ingrese un año y verifica que el año ingresado esté dentro del rango de 2011 a 2021.

#### Normalización de datos

Se define una función llamada `normalizar` que toma una lista de valores y devuelve una lista con los valores normalizados entre 0 y 1. Esta función es utilizada para comparar diferentes conjuntos de datos en una misma escala.

#### Generación de gráficos y dashboards

Se definen varias funciones para generar gráficos y dashboards que permiten visualizar la evolución de los indicadores clave:
- `grafico_ingreso`: Genera un gráfico de líneas que muestra la evolución del ingreso per cápita de los departamentos seleccionados.
- `grafico_gasto`: Genera un gráfico de líneas que muestra la evolución del gasto en educación por alumno en los departamentos seleccionados.
- `grafico_analfabetismo`: Genera un gráfico de líneas que muestra la evolución de la tasa de analfabetismo en los departamentos seleccionados.
- `grafico_relacion_ingreso_gasto`: Genera un gráfico de líneas que muestra la relación entre el gasto en educación por alumno y el ingreso per cápita en los departamentos seleccionados.
- `grafico_dashboard1`: Integra varios gráficos en un solo dashboard para comparar la evolución de los indicadores en múltiples departamentos.
- `grafico_dashboard2`: Integra varios gráficos en un solo dashboard para analizar la evolución de los indicadores en un solo departamento.

## Instalación

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install pandas matplotlib numpy openpyxl
