#### Creamos nuestro script de selenium
import random
import selenium                                       
import os                                             
import time                                           
import re                                             
                                                      
from selenium import webdriver                        
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from sqlalchemy import func, text


# Traemos la clase para poder crear los registros y la base de datos
import db
from db import sa_engine
from models import Category, QuestionsAnswers


# ------------------- CONFIGURACIÓN INICIAL DEL DRIVER  ------------------------------- #  
# 0. URL desde la que vamos a extraer la información                                       
URL = "https://youengage.me/blog/trivia-questions/"                                        
#URL = "https://google.com/"


# 1. Llamamos a la ruta del webdriver en nuestro entorno local                                          
PATH_DRIVER = "/Applications/driver_sel/chromedriver-mac-arm64/chromedriver"                            
CHROME_SERVICE = Service( executable_path = PATH_DRIVER )                                               
options = Options()                                                                                     
options.add_argument("--incognito") # Abre la ventana del webdriver en incógnito                        
# options.add_argument("--headless") # Ejecuta el scrapeo de la web sin abrir ventana del driver          
                                                                                                        
                                                                                                        
# 2. Creamos la instancia de nuestro driver y ajustamos el tamaño de la ventana                         
driver = webdriver.Chrome(service=CHROME_SERVICE, options=options)                                      
driver.set_window_size( 550, 950 )


# 3. Podemos comenzar el scrappeo -------------------------------  
def scrappeCategories():
    driver.get(URL)                                                                                                     
    time.sleep(3)                                                                                                       

    # Primero aceptamos las cookies                                                                                                             
    try:                                                                                                                
        cookies_site = driver.find_element(By.XPATH, value="/html/body/section/div/div[1]/div[2]/button[1]")            
        cookies_site.click()                                                                                            
        print("Aceptamos la política de cookies.")                                                                      
    except Exception as e:                                                                                              
        print("Algo salió mal")                                                                                         
        print(e, type(e).__name__)                                                                                      
                                                                                                                        
    time.sleep(3)


    # Hacemos scrapping de las categorías y creamos las instancias en la BBDD
    # Tenemos que considerar la casuística de que las categorías ya estén en la BBDD
    try:                                                                                                                                          
        category_list = []                                                                                                                        
        categories = driver.find_elements(By.XPATH, value="/html/body/div[1]/section[2]/div/div/div/div[1]/ol[1]/li")                             
        print("Estas son las categorias que tenemos que registrar en la BBDD:")                                                                   
        for index, category in enumerate(categories):
            if index <= 12:
                category_edit = re.sub(r'\s*Trivia\s*Questions$', '', category.text)
                category_instance = Category(name=category_edit)                                                                  
                category_list.append(category_instance)
                
            else:
                continue
        
        print("Mi lista de categorías para incluir en la BBDD: ", category_list)
        db.session.add_all(category_list)
        db.session.commit()
        db.session.close()
        print("-------------- CATEGORÍAS AGREGADAS A LA BBDD --------------")

    except Exception as e:                               
        print("Algo no ha ido bien", e, type(e).__name__)



# FUNCIÓN PARA HACER SCRAPPING DE LAS PREGUNTAS
def scrappeQuestionsAndAnswers():
    driver.get(URL)                                                                                                     
    time.sleep(3)  

    # 0 -> Primero aceptamos las cookies                                                                                                             
    try:                                                                                                                
        cookies_site = driver.find_element(By.XPATH, value="/html/body/section/div/div[1]/div[2]/button[1]")            
        cookies_site.click()                                                                                            
        print("Aceptamos la política de cookies.")                                                                      
    except Exception as e:                                                                                              
        print("Algo salió mal")                                                                                         
        print(e, type(e).__name__)                                                                                      
                                                                                                                        
    time.sleep(3)

    
    # 1 -> Recuperamos las preguntas y respuestas haciendo scrapping
    try:
        questions_and_answers_list = []
        for category in range(2,15):
            beta_results = driver.find_elements(By.XPATH, value="/html/body/div[1]/section[2]/div/div/div/div[1]/ol[{}]/li".format(category))
            for result in beta_results:
                # print(result.text)
                questions_and_answers_list.append(result.text)

    except Exception as e:
        print("Algo ha salido mal al recuperar las preguntas")
        print(e, type(e).__name__)

    #print("\n\nEste es mi listado de preguntas:", questions_and_answers_list)
    print("\n\nEl número total de preguntas que tengo que manejar son: ", len(questions_and_answers_list))

    # 2 -> Tenemos que formatear los resultados obtenidos.
    # Por cada registro del array, lo subdividimos
    array_first_edit = []
    for register in questions_and_answers_list:
        result = register.split(sep="\n")
        array_first_edit.append(result)
    
    time.sleep(3)
    for register in array_first_edit:
        # Verificamos y modificamos el string, generando uno nuevo
        if register[1].startswith("Answer"):
            register[1] = register[1][7:].strip()
        else:
            continue
        
        ##### TENEMOS QUE MANEJAR LAS RESPUESTAS ERRÓNEAS, LOS WRONGS 1 Y 2
        if len(register) > 2:
            register[2] = register[2].split(sep=",")

            # Aquí dentro tenemos que manejar un string que se convierta en dos substrings, divididos por la coma

        else:
            continue

    print("Este es mi array de resultados: ", array_first_edit)



    # 3 -> CREAMOS LAS INSTANCIAS EN LA BASE DE DATOS
    final_results = []
    for array_of_data in array_first_edit:

        question_text = array_of_data[0]
        right_answer = array_of_data[1]

        # Verificamos si existe un tercer elemento en array_of_data antes de intentar acceder a array_of_data[2]
        if len(array_of_data) > 2:
            # Verificamos que existan dos elementos dentro del array de errores:
            if len(array_of_data[2]) > 1:
                wrong_1 = array_of_data[2][0][7:].strip() 
                wrong_2 = array_of_data[2][1].strip()
            else:
                wrong_1 = array_of_data[2][0][7:].strip()
                wrong_2 = None
        else:
            wrong_1 = None
            wrong_2 = None


        # Creamos las instancias:
        question_instance = QuestionsAnswers(
            question=question_text, 
            right_answer=right_answer, 
            wrong_1=wrong_1, 
            wrong_2=wrong_2)
        
        final_results.append(question_instance)

    print("\n\nMi lista de preguntas para añadir en la bbdd:", final_results)
    db.session.add_all(final_results)
    db.session.commit()
    db.session.close()


#### FUNCIÓN PARA ASIGNAR A CADA PREGUNTA SU CORRESPONDIENTE CATEGORÍA
def categorizingQuestions():
    all_questions_list = db.session.query(QuestionsAnswers).all()

    """Categorias en total son 13:
    # 0 - 10: 1
    # 11 - 20: 2
    # 21 - 30: 3
    # 31 - 40: 4
    # 41 - 49: 5
    # 50 - 58: 6
    # 59 - 68: 7
    # 69 - 78: 8
    # 79 - 88: 9
    # 89 - 98: 10
    # 99 - 108: 11
    # 109 - 118: 12
    # 119 - 127: 13

    
    print("\n\nNuestro listado de preguntas:")
    for index, q in enumerate(questions):
        print("{} -> {}".format(index, q))
    """
    print(type(all_questions_list))

    for question in all_questions_list:
        print(question.id)
        if (question.id >= 1) and (question.id < 11):
            question.category_id = 1
        elif (question.id >= 11) and (question.id < 21):
            question.category_id = 2
        elif (question.id >= 21) and (question.id < 31):
            question.category_id = 3
        
        elif (question.id >= 31) and (question.id < 41):
            question.category_id = 4
        elif (question.id >= 41) and (question.id < 50):
            question.category_id = 5
        elif (question.id >= 50) and (question.id < 59):
            question.category_id = 6
        
        elif (question.id >= 59) and (question.id < 69):
            question.category_id = 7
        elif (question.id >= 69) and (question.id < 79):
            question.category_id = 8
        elif (question.id >= 79) and (question.id < 89):
            question.category_id = 9
        
        elif (question.id >= 89) and (question.id < 99):
            question.category_id = 10
        elif (question.id >= 99) and (question.id < 109):
            question.category_id = 11
        elif (question.id >= 109) and (question.id < 119):
            question.category_id = 12
        elif (question.id >= 119) and (question.id < 128):
            question.category_id = 13
        else: 
            print("Revisa los ids de las preguntas. Algo fue mal")
        
    db.session.commit()
    db.session.close()



# FUNCIÓN QUE NOS DEVUELVE 10 PREGUNTAS AL AZAR. 10 REGISTROS DE NUESTRA BBDD.
def randomTriviaTest():
    # Creamos un conjunto para los ids de las preguntas seleccionadas
    selected_question_ids = set()
    random_test = []
    for x in range(10):
        # Consulta aleatoria excluyendo las preguntas ya seleccionadas
        question = db.session.query(QuestionsAnswers).filter(~QuestionsAnswers.id.in_(selected_question_ids)).order_by(func.random()).first()

        if question:
            selected_question_ids.add(question.id)
            pregunta = question.question
            random_test.append(pregunta) 
        else:
            print("No hay más preguntas disponibles en la base de datos.")

    print("\nSe ha generado un test con las siguientes preguntas:")
    for pregunta in random_test:
        print("\t{}".format(pregunta))
    
    return random_test


# FUNCIÓN PARA GENERAR UN TEST BASADO EN SOLO ALGUNAS CATEGORÍAS
def categorizedTriviaTest(*category_ids: int):
    """
    En este caso vamos a seleccionar de manera aleatoría solo
    preguntas que entren dentro de las categorías que nos pasan por parámetros.
    
    Las categorías que va a poder recibir serán de tipo int
    """

    selected_questions_ids = set()
    categorized_questions= [] # Guardaremos un array de tuplas. Sobre este array recopilaremos 10 preguntas random

    # En esta primera variable, formateamos los ids: int que nos llegan por params
    category_ids_str = ",".join(map(str, category_ids))

    # Construimos la query y la llamamos desde el módulo de text()
    query_str = "SELECT * FROM questions_answers WHERE category_id IN ({})".format(category_ids_str)
    query = text(query_str)

    with sa_engine.connect() as connection:
        results = connection.execute(query, {"category_ids": category_ids})

        for row in results:
            question_id = row[0]
            categorized_questions.append(row) # Guardamos en el array todas los posibles resultados
    #print(categorized_questions) 
    
    # Finalmente, Barajamos con .shuffle() y cogemos los primeros 10 resultados:
    random.shuffle(categorized_questions)
    random_cat_test = categorized_questions[0:10]

    print("\nEnviamos nuestro test categorizado con 10 preguntas:\n", random_cat_test, len(random_cat_test))
    return random_cat_test









    