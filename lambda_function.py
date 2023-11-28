import sys
import logging
import json
import os
import subprocess
import pymysql

# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    raise Exception("Error connecting to the database.")

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    "This function creates a new RDS database table "
    
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS criptoinfo (id INT NOT NULL AUTO_INCREMENT, cripto VARCHAR(5) NOT NULL, Value VARCHAR(255) NOT NULL, datetime VARCHAR(255), PRIMARY KEY (id)")
    except pymysql.MySQLError as e:
        logger.error("Error creating table:")
        logger.error(e)
        raise Exception("Error creating table.")

    return "Table criptoinfo created successfully"
