from fastapi import FastAPI, Query # Importa las bibliotecas necesarias
from fastapi.responses import HTMLResponse # Importa las bibliotecas necesarias
import api_funct as ft # Importa módulos específicos

import importlib # Importa módulos específicos
importlib.reload(ft) # Importa módulos específicos

import uvicorn

app = FastAPI() # Crea una instancia de la aplicación FastAPI


@app.get(path="/",  # Define una ruta GET para la aplicación
         response_class=HTMLResponse,
         tags=["Home"])
def home(): # Define una función
    ''' Home page '''
    return ft.Intro() # Devuelve el resultado de la función


@app.get(path = '/PlayTimeGenre', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el género en el cuadro a continuación.<br>
                        3. Desplázate hasta "Responses body" para ver el año de lanzamiento con más horas reproducidas para el género especificado.
                        </font>
                        """,
         tags=["Queries"])

def PlayTimeGenre(genre: str = Query(...,  # Define una función
                                description="Genre", 
                                example="Adventure")):
        
       return ft.PlayTimeGenre(genre) # Devuelve el resultado de la función



@app.get(path = '/UserForGenre', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el género en el cuadro a continuación.<br>
                        3. Desplácese hasta "Responses body" para ver el usuario con más horas jugadas y la lista de horas jugadas por año para ese usuario.
                        </font>
                        """,
         tags=["Queries"])
def UserForGenre(genre: str = Query(...,  # Define una función
                                description="Genre", 
                                example='Action')):                
    return ft.UserForGenre(genre) # Devuelve el resultado de la función



@app.get(path = '/UsersRecommend', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el año en el cuadro a continuación.<br>
                        3. Desplázate hasta "Responses body" para ver un juego destacado y su recuento de recomendaciones.
                        </font>
                        """,
         tags=["Queries"])

def UsersRecommend(year: int = Query(...,  # Define una función
                                description="The target year for filtering reviews", 
                                example='2014')):                
    return ft.UsersRecommend(year) # Devuelve el resultado de la función



@app.get(path = '/UsersNotRecommend', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el año en el cuadro a continuación.<br>
                        3. Desplázate hasta "Responses body" para ver un juego destacado y su recuento de recomendaciones.
                        </font>
                        """,
         tags=["Queries"])

def UsersNotRecommend(year: int = Query(...,  # Define una función
                                description="The target year for filtering reviews", 
                                example='2014')):                
    return ft.UsersNotRecommend(year) # Devuelve el resultado de la función



@app.get(path = '/sentiment_analysis', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el año en el cuadro a continuación.<br>
                        3. Desplácese hasta "Cuerpo de las respuestas" para ver el recuento de reseñas para cada categoría de sentimiento.
                        </font>
                        """,
         tags=["Queries"])
def sentiment_analysis(year: int = Query(...,  # Define una función
                                description="The target year for filtering reviews", 
                                example='2014')):
    return ft.sentiment_analysis(year) # Devuelve el resultado de la función



@app.get(path = '/similar_user_recs', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese el usuario en el cuadro a continuación.<br>
                        3. Desplácese hasta "Cuerpo de las respuestas" para ver una lista de los elementos más recomendados para el usuario según la calificación de usuarios similares.
                        </font>
                        """,
         tags=["Queries"])
def similar_user_recs(user: str = Query(...,  # Define una función
                                description="User id in the Steam Platform", 
                                example='Urotsuki')):
    return ft.user_similarity(user) # Devuelve el resultado de la función



@app.get(path = '/get_recommendations_by_id', # Define una ruta GET para la aplicación
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clic en "Try it out".<br>
                        2. Ingrese la identificación del artículo en el cuadro a continuación.<br>
                        3. Desplácese hasta "Cuerpo de las respuestas" para ver una lista de los elementos de similitud más recomendados.
                        </font>
                        """,
         tags=["Queries"])
def get_recommendations_by_id(item_id: int = Query(...,  # Define una función
                                description="Item id in the Steam Platform", 
                                example='322920')):
    return ft.item_similarity(item_id) # Devuelve el resultado de la función

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)