# Análisis del Analfabetismo en los Departamentos del Perú (2011-2021)

Este proyecto tiene como objetivo analizar la relación entre el PBI per cápita, el gasto público por alumno en educación y la tasa de analfabetismo en los departamentos del Perú desde 2011 hasta 2021. El análisis se enfoca en los departamentos con las tasas de analfabetismo más altas (Apurímac, Huánuco, Huancavelica y Cajamarca) y los departamentos con las tasas más bajas (Callao, Ica, Tumbes y Tacna).

## Estructura del Proyecto

### Archivos Principales

- `CODIGO_TP.txt`: Contiene el código principal para cargar, limpiar y analizar los datos, así como para generar gráficos.
- `PBI_POBLACION.xlsx`: Datos de PBI por departamento y crecimiento poblacional.
- `GASTO_EDUCACION.xlsx`: Datos del gasto público en educación básica regular.
- `ANALFABETISMO.xlsx`: Datos de la tasa de analfabetismo de la población de 15 y más años de edad.

### Funcionalidades del Código

#### Cargar y Limpiar Datos:

- `cargarDF_PBI_POB`: Carga y limpia los datos de PBI y población.
- `cargarDF_gasto_educacion`: Carga y limpia los datos de gasto en educación.
- `cargar_df_analfabetismo`: Carga y limpia los datos de analfabetismo.

#### Crear DataFrames:

- `estabelecerDF_PBIpercapita`: Calcula el PBI per cápita.
- `establecer_relacion_pbi_educacion`: Calcula la relación entre el PBI per cápita y el gasto en educación.
- `DF_con_tasa_promedio_analfabetismo`: Calcula la tasa promedio de analfabetismo.

#### Generar Gráficos:

- `grafico_dashboard`: Genera un dashboard con varios gráficos.
- `graf_a`, `graf_b`, `graf_c`, `graf_d`, `graf_e`, `graf_f`, `graf_g`: Generan gráficos específicos según las opciones del usuario.

## Instalación

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install pandas matplotlib numpy openpyxl
