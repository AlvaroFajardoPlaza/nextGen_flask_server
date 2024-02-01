#### Dentro de este archivo configuramos la BBDD con SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#### Variables de entorno
__USER = "root"
__PASSWORD = ""
__HOST = "localhost"

# url = 'mysql://username:password@14.41.50.12/dbname'

# Mis datos de usuario para la bbdd: root, "", localhost, 3306
#connection_string = "mysql://{}:{}@{}/database/scrapper_test.db".format(__USER, __PASSWORD, __HOST)

connection_string = "sqlite:///database/scrapper_test_01_02.db"
sa_engine = create_engine(connection_string, echo=True) # la variable echo nos permite ver las requests a la BBDD

# Creamos el objeto session que se encargará de las gestiones con la BBDD
Session = sessionmaker(bind = sa_engine)
session = Session()

# Desde models.py creamos las clases que después transformaremos en tablas
Base = declarative_base()