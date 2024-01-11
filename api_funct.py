# Importaciones
import pandas as pd
import operator
import warnings
warnings.filterwarnings("ignore")


#Load data

df_playtime_genre = pd.read_parquet('Data/parquet/playtime_genre.parquet')
df_user_for_genre = pd.read_parquet('Data/parquet/user_for_genre.parquet')
df_user_recommend = pd.read_parquet('Data/parquet/user_recommend.parquet')
df_sentiment_year = pd.read_parquet('Data/parquet/sentiment_year.parquet')
df_id = pd.read_parquet('Data/parquet/df_id.parquet')
df_games = pd.read_parquet('Data/parquet/game_sim.parquet.gz')
umatrix_norm = pd.read_parquet('Data/parquet/umatrix_norm.parquet')
user_sim_df = pd.read_parquet('Data/parquet/user_sim.parquet.gz')


def Intro():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Steam</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
                text-align: center;
            }

            h1 {
                color: #333;
                margin-bottom: 10px;
            }

            p {
                color: #666;
                font-size: 18px;
                margin-top: 10px;
            }

            a {
                color: #007bff;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }

            img {
                width: 50px;
                height: 20px;
                vertical-align: middle;
                margin-left: 5px;
            }

            .github-badge {
                display: inline-block;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>André Escobar. PI1, Machine Learning Operations (MLOps)</h1>
        <h1>PROYECTO INDIVIDUAL Nº1</h1>
        <h1>API de consulta de videojuegos de la plataforma Steam</h1>
        <p>Para interactuar con los puntos finales disponibles, explore la documentación de la API <b>haciendo clic en la imagen</b>.</p>
        <a href="/docs"><img src="https://store.cloudflare.steamstatic.com/public/shared/images/header/logo_steam.svg" alt="Steam Logo" style="width: 500px; height: auto; margin-top: 20px;"></a>
    
        <p>Para obtener detalles del proyecto, consulte el <a href="https://github.com/andre-ev/PI_ML_OPS" target="_blank" rel="noopener noreferrer" class="github-badge">repositorio de GitHub <img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
    </body>
    </html>
        '''

def PlayTimeGenre(genre: str):
    """
    Devuelve el año de lanzamiento con más horas reproducidas para el género determinado.

     Parámetros:
     - género (str): Género del que se desea obtener el año de lanzamiento con más horas reproducidas.

     Devoluciones:
     - dict: Diccionario con el año de lanzamiento con más horas reproducidas para el género especificado.
    """
    genre_lower = genre.lower() if isinstance(genre, str) else None
    genre_df = df_playtime_genre[df_playtime_genre['genres'].str.lower() == genre_lower]

    if genre_df.empty:
        return {f"No hay datos disponibles para el género. {genre}": None}

    # Verifique los datos antes de intentar obtener el índice del valor máximo
    if not genre_df['playtime_forever'].empty:
        # Obtener el año con más horas jugadas
        max_playtime_year = genre_df.loc[genre_df['playtime_forever'].idxmax(), 'release_year']
        return {f"Año de lanzamiento con más horas reproducidas para el género. {genre}": max_playtime_year}
    else:
        return {f"No hay datos disponibles para el género {genre}": None}
    

    
def UserForGenre(genre: str):
    """
    Devuelve el usuario con más horas reproducidas para el género determinado y una lista de horas reproducidas por año para ese usuario.

     Parámetros:
     - género (str): Género del que se quiere obtener el usuario y la acumulación de horas reproducidas.

     Devoluciones:
     - dict: Diccionario con el usuario con más horas jugadas y el listado de horas jugadas al año de ese usuario.
    """
    genre_lower = genre.lower() if isinstance(genre, str) else None
    genre_df = df_user_for_genre[df_user_for_genre['genres'].str.lower() == genre_lower]
    if genre_df.empty:
        return {"Usuario con más horas reproducidas para el género": None, "Horas reproducidas por año": {}}
    user_playtime_sum = genre_df.groupby('user_id')['playtime_hours'].sum()
    max_playtime_user = user_playtime_sum.idxmax()
    user_df = genre_df[genre_df['user_id'] == max_playtime_user]
    playtime_by_year = dict(zip(user_df['release_year'], user_df['playtime_hours']))

    return {f"Usuario con más horas reproducidas para el género {genre}": max_playtime_user, "Horas reproducidas por año": playtime_by_year}


def UsersRecommend(year):
    '''
    Esta función toma un año como entrada y filtra las reseñas de los usuarios para ese año, considerando solo las reseñas recomendadas.
     Luego selecciona reseñas positivas/neutrales (sentiment_analysis 1 o 2) y cuenta las recomendaciones para cada juego.
     La función devuelve los 3 mejores juegos con el mayor número de recomendaciones en el año especificado.

     Parámetros:
     - año (int): el año objetivo para filtrar reseñas.

     Devoluciones:
     Lista de diccionarios, donde cada diccionario representa un juego superior y su recuento de recomendaciones.
    '''
    filtered_reviews = df_user_recommend[(df_user_recommend['posted'] == year) & (df_user_recommend['recommend'] == True)]
    
    positive_reviews = filtered_reviews[filtered_reviews['sentiment_analysis'].isin([1, 2])]
    recommendations_count = positive_reviews['item_name'].value_counts().reset_index()
    recommendations_count.columns = ['item_name', 'recommendations_count']
    top3_recommendations = recommendations_count.head(3)
    result = [{"Posición {}: {}".format(i+1, row['item_name']): row['recommendations_count']} for i, row in top3_recommendations.iterrows()]
    
    return result

def UsersNotRecommend(year):
    '''
    Esta función toma un año como entrada y filtra las reseñas de los usuarios para ese año, considerando solo las reseñas recomendadas.
    Luego selecciona reseñas negativas (sentiment_analysis 0) y cuenta las recomendaciones para cada juego.
    La función devuelve los 3 mejores juegos con el menor número de recomendaciones en el año especificado.

    Parámetros:
    - año (int): el año objetivo para filtrar reseñas.

    Devoluciones:
    Lista de diccionarios, donde cada diccionario representa los elementos más bajos y su recuento de recomendaciones.
    '''
    filtered_reviews = df_user_recommend[(df_user_recommend['posted'] == year) & (df_user_recommend['recommend'] == False)]
    negative_reviews = filtered_reviews[filtered_reviews['sentiment_analysis'] == 0]
    not_recommendations_count = negative_reviews['item_name'].value_counts().reset_index()
    not_recommendations_count.columns = ['item_name', 'not_recommendations_count']
    top3_not_recommendations = not_recommendations_count.head(3)
    result = [{"Position {}: {}".format(i+1, row['item_name']): row['not_recommendations_count']} for i, row in top3_not_recommendations.iterrows()]
    
    return result


def sentiment_analysis(year):
    '''
    Esta función realiza un análisis de opinión sobre las reseñas de juegos de un año específico. Filtra reseñas según el año de lanzamiento.
    y cuenta la cantidad de reseñas para cada categoría de sentimiento (Negativa, Neutral, Positiva).

    Parámetros:
    - año (int): el año objetivo para filtrar reseñas.

    Devoluciones:
    Diccionario que contiene el recuento de reseñas para cada categoría de sentimiento.
    Ejemplo:
    {'Negativo': 10, 'Neutral': 20, 'Positivo': 30}
    '''
    filtered_reviews = df_sentiment_year[df_sentiment_year['release_year'] == year]
    sentiment_counts = filtered_reviews['sentiment_analysis'].value_counts().to_dict()
    result = {
        'Negative': sentiment_counts.get(0, 0),
        'Neutral': sentiment_counts.get(1, 0),
        'Positive': sentiment_counts.get(2, 0)
    }
    
    return result


def user_similarity(user: str):
    '''
    Genera una lista de los elementos más recomendados para un usuario, basada en calificaciones de usuarios similares.

    Argumentos:
        usuario (cadena): El nombre o identificador del usuario para quien desea generar recomendaciones.

    Devoluciones:
        lista: una lista de los elementos más recomendados para el usuario según la calificación de usuarios similares.
    '''
    if user not in umatrix_norm.columns:
        return 'No hay datos disponibles sobre el usuario {}'.format(user)
    sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
    best = []  
    most_common = {}  
    
    for i in sim_users:
        max_score = umatrix_norm.loc[:, i].max()
        best.extend(umatrix_norm[umatrix_norm.loc[:, i] == max_score].index.tolist())      
    
    for j in best:
        most_common[j] = most_common.get(j, 0) + 1
    
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)

    return 'Usuarios similares a {}: también les gustó'.format(user), sorted_list[:5]



def item_similarity(item_id: int):
    '''
    Genera recomendaciones para un juego dada su ID.
    Parámetros:
    - item_id (int): El ID del juego para el que deseas obtener recomendaciones.

    Devoluciones:
    - recomendaciones (lista): una lista de nombres de juegos recomendados para el juego determinado.
    - mensaje (str): Un mensaje que indica si el ID ingresado no tiene datos disponibles.
    '''
    game_name = df_id.loc[df_id['item_id'] == item_id, 'item_name'].iloc[0]
    if game_name not in df_games.index:
        return [], f"ID {item_id} no tiene datos disponibles."

    game_row = df_games.loc[game_name]
    similar_games = df_games.dot(game_row).sort_values(ascending=False)
    similar_games = similar_games.drop(game_name)
    recommendations = similar_games.nlargest(5).index.tolist()

    return 'Recomendar artículos similares al artículo {}'.format(item_id), recommendations