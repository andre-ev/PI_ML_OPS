# Proyecto de Análisis de Datos y Recomendaciones de Juegos en Steam
El proyecto se enfoca en analizar patrones de juego y preferencias de los usuarios de Steam para ofrecer recomendaciones personalizadas de videojuegos. Se emplea FastAPI para la implementación de una API web que proporciona acceso a información variada y sugerencias de juegos adaptadas a los gustos de los usuarios.

## Datos Utilizados
El dataset utilizado se encuentra en: [Enlace al dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj).

# Trabajo Realizado
El proyecto aborda el análisis de diversas fuentes de datos de Steam para mejorar la interacción de los usuarios con la plataforma. Se procesaron datos JSON transformándolos en CSV, optimizando así su manejo. Este procesamiento incluyó la limpieza de datos irrelevantes, como entradas vacías. Posteriormente, se desarrollaron funciones específicas para la API que se valen de la similitud del coseno para crear matrices de correlaciones, tanto para usuarios como para ítems, que a su vez apoyan la construcción de funciones predictivas avanzadas.

## ¿Qué archivos se utilizan dentro de la API?

Se utilizan los siguientes archivos:

- `playtime_genre.parquet` : Contiene información sobre las horas jugadas por género de juego.
- `user_for_genre.parquet` : Contiene información sobre las horas jugadas por uusario y género de juego.
- `user_recommend.parquet` : Contiene datos de usuarios y la cantidad de juegos que han comprado o adquirido.
- `sentiment_year.parquet` : Contiene reseñas de juegos realizadas por los usuarios, incluyendo análisis de sentimientos.
- `df_id.parquet` : Se utiliza para extraer el id_item para la función de recomendación.
- `game_sim.parquet` : Contiene una matriz de juegos y sus similitudes con el resto de juegos. 
- `umatrix_norm.parquet` : Matriz que representar las preferencias o comportamientos de los usuarios de manera normalizada,
- `user_sim.parquet` : Contiene la similitud entre diferentes usuarios.

## Funciones de la API

El proyecto brinda diversas funcionalidades a través de su API, permitiendo a los usuarios acceder a información detallada y obtener recomendaciones personalizadas:

- **`/PlayTimeGenre/{genre}`**: Devuelve el año de lanzamiento con la mayor cantidad de horas jugadas para un género de juego específico.

- **`/UserForGenre/{genre}`**: Muestra el usuario con la mayor cantidad de horas jugadas en un género específico y proporciona una lista de horas jugadas por año para ese usuario.

- **`/UsersRecommend/{year}`**: Calcula los 3 juegos más recomendados en un año específico, basándose en las reseñas de los usuarios y la cantidad de recomendaciones positivas o neutrales.

- **`/UsersNotRecommend/{year}`**: Similar a `/UsersRecommend`, pero para reseñas negativas. Devuelve los 3 juegos menos recomendados en un año específico.

- **`/sentiment_analysis/{year}`**: Realiza un análisis de sentimiento de las reseñas de juegos para un año específico, contabilizando la cantidad de reseñas en cada categoría de sentimiento (negativo, positivo y neutral).

- **`/similar_user_recs/{user}`**: Genera una lista de juegos recomendados para un usuario específico, basada en las valoraciones de usuarios con comportamientos similares.

- **`/get_recommendations_by_id/{item_id}`**: Proporciona recomendaciones de juegos similares a uno dado, basado en su ID en la plataforma Steam.

Cada una de estas rutas de la API ofrece información valiosa y recomendaciones específicas basadas en los datos y preferencias de los usuarios en la plataforma Steam.
 
## ¿Qué hay en las carpetas?

El proyecto consta de tres carpetas principales. La primera, denominada "Data", alberga todos los archivos parquet empleados para el manejo de datos. En la segunda carpeta, "Models", se hallan los desarrollos realizados con los datos para adaptarlos al modelo, incluyendo archivos de NumPy esenciales para establecer las conexiones entre usuarios y elementos. Finalmente, la carpeta "ETL" contiene los scripts usados en el proceso ETL, aplicados a los archivos descritos en la sección "Datasets/Raw".

## ¿Y los archivos que no están en carpetas?

estos son los siguientes:

1. **README**: Este es el archivo que estás leyendo en este momento.
2. **main.py**: Aquí se encuentra desarrollada la API, por lo que las funciones de la API se toman de este archivo.
3. **api_funct.py**: Estas son las mismas funciones de la API, pero están diseñadas para ejecutarse de manera local sin la necesidad de la librería FastAPI.
4. **EDA.ipynb**: Es un pequeño EDA que ayuda a observar de mejor manera los csv principales
5. **requirements.txt**: Este archivo contiene la lista de dependencias que tu máquina necesita para ejecutar todos los archivos sin problemas. Para instalar estas dependencias, debes usar el siguiente comando:

```bash
pip install -r requirements.txt