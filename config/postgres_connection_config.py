import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from loguru import logger
from config.logging_config import script_filter

# Configure logger
db_logger = logger.bind(script="postgres_connection")
log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                             f'postgres_connection_{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
db_logger.add(log_file_path, filter=script_filter("postgres_connection"),  rotation="10 MB",enqueue=True)

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# Initialize the connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **POSTGRES_CONFIG)
    if connection_pool:
        db_logger.info(f"Connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    db_logger.error(f"Error while connecting to PostgresSQL: {error}")
    connection_pool = None


def get_db_connection():
    """
    Get a database connection from the connection pool.
    Returns Non if connection pool is not set up or an error occurred.
    :return:
    """
    try:
        if connection_pool:
            return connection_pool.getconn()
        else:
            db_logger.warning(f"Connection pool is not set up")
            return None
    except (Exception, psycopg2.DatabaseError) as error:
        db_logger.error(f"eEror while connecting to PostgresSQL: {error}")
        return None


def put_db_connection(connection):
    """
    Return the connection back to the connection pool
    :param connection:
    :return:
    """
    if connection:
        try:
            connection_pool.putconn(connection)
            db_logger.info(f"Returned connection pool has been made to PostgresSQL: {connection}")
        except (Exception, psycopg2.DatabaseError) as error:
            db_logger.error(f"Error while connecting to PostgresSQL: {error}")


def close_db_connection():
    """
    Close all database connections and connection pool
    :param:
    :return:
    """
    if connection_pool:
        try:
            connection_pool.closeall()
            db_logger.info(f"Connection has been closed")
        except (Exception, psycopg2.DatabaseError) as error:
            db_logger.error(f"Error while connecting to PostgresSQL: {error}")


def demonstrate_connection_capabilities():
    """
    Function to demonstrate the capabilities of the PostgresSQL connection configuration.
    :return:
    """
    # Test getting a connection
    conn = get_db_connection()
    if conn:
        db_logger.info(f"Successfully obtained a database connection to PostgresSQL")
        # You can add more operations here to demonstrate other functionalities

        put_db_connection(conn)
        db_logger.info(f"Successfully returned connection pool to the PostgresSQL database")

        close_db_connection()
        db_logger.info(f"Successfully closed a database connection to PostgresSQL")
    else:
        db_logger.error(f"Could not obtain a database connection to PostgresSQL")
