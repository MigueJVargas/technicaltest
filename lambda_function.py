from request import Request, Session
import sys
import logging
import json
import os
import subprocess
import pymysql

user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(api_key):
     
    "This function creates a new RDS database table "
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # Parámetros de la solicitud
    parametros = {
        'start':'1',
        'limit':'2',
        'convert':'USD',  # Convertir los precios a dólares estadounidenses
        'symbol':'BTC,ETH'  # Símbolos de las criptomonedas (Bitcoin y Ethereum)
    }

    # Cabeceras de la solicitud con la clave de API
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    

    item_count = 0
    
    message = json.dumps(event['data']['1']['quote']['USD'])
    data = json.loads(message)
    Value = data['price']
    datetime = data['last_updated']
    cripto = 'BTC'
    
    sql_string = f"insert into criptoinfo (cripto, Value, datetime) values('{cripto}', '{Value}','{datetime}')"


    with conn.cursor() as cur:
        cur.execute("create table if not exists criptoinfo ( id int  NOT NULL AUTO_INCREMENT , cripto varchar(5) NOT NULL, Value varchar(255) NOT NULL, datetime varchar(255), PRIMARY KEY (id))")
        cur.execute(sql_string)
        conn.commit()
        cur.execute("select * from criptoinfo")
        logger.info("The following items have been added to the database:")
        for row in cur:
            item_count += 1
            logger.info(row)
    conn.commit()

    return "Added %d items to RDS for MySQL table" %(item_count)