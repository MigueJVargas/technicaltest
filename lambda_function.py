import requests
import pymysql
import os
import sys
import logging

user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']
api_key = os.environ['api_key']  

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    # URL de la API de CoinMarketCap para obtener información de las criptomonedas
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

    # Parámetros de la solicitud
    parameters = {
        'start': '1',
        'limit': '2',
        'convert': 'USD',
        'symbol': 'BTC,ETH'
    }

    # Cabeceras de la solicitud con la clave de API
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # Configurar una sesión de requests
    with requests.Session() as session:
        # Configurar la clave de API como un encabezado en la sesión
        session.headers.update(headers)
        
        try:
            logging.info("Realizando la solicitud a la API...")
            # Realizar la solicitud a la API 
            respuesta = session.get(url, params=parameters)

            # Verificar si la solicitud a la API fue exitosa
            if respuesta.status_code == 200:
                datos = respuesta.json()
                logging.info("Solicitud a la API exitosa!")

                # Insertar información sobre las criptomonedas en la tabla de la base de datos
                for cripto in datos['data']:
                    nombre = cripto['name']
                    simbolo = cripto['symbol']
                    precio = cripto['quote']['USD']['price']
                    ultima_actualizacion = cripto['last_updated']

                    # Consulta SQL para insertar datos en la tabla
                    insert_query = "INSERT INTO criptoinfo (cripto, precio, datetime) VALUES (%s, %s, %s)"
                    insert_values = (simbolo, precio, ultima_actualizacion)

                    # Conectar a la base de datos RDS
                    try:
                        # Obtener el cursor
                        with conn.cursor() as cursor:
                            # Ejecutar la consulta
                            cursor.execute(insert_query, insert_values)

                        # Hacer commit de los cambios
                        conn.commit()

                        logging.info(f"Inserción en la base de datos exitosa para {nombre}")

                    except pymysql.Error as err:
                        logging.error(f"Error en la base de datos: {err}")

            else:
                logging.error(f"Error al hacer la solicitud a la API. Código de estado: {respuesta.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error al hacer la solicitud a la API: {e}")

        finally:
            # Cerrar la conexión fuera del bucle for para evitar cerrarla en cada iteración
            conn.close()
