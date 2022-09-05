import pandas as pd
import pymysql
import os
import logging

logger = logging.getLogger(__name__)

CONNECTION_STRING = {
    'host':        os.getenv('MYSQL_HOST'),
    'database':    os.getenv('MYSQL_DATABASE'),
    'user':        os.getenv('MYSQL_USER'),
    'password':    os.getenv('MYSQL_PWD'),
    'cursorclass': pymysql.cursors.DictCursor
}

class BaseTable:
    TABLE_NAME = 'test_table'
    CREATE_SQL = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        datetime_col   TIMESTAMP,
                        text_col       TEXT,
                        float_col      DECIMAL(12,2),
                        int_col        INTEGER
                    )'''
    
    @classmethod
    def get_total_cols(cls):
        return int(
            len(
                cls.CREATE_SQL[cls.CREATE_SQL.find('(') + 1: cls.CREATE_SQL.rfind(')')].split()
            )
            /2
        )
           
    @classmethod
    def create_connection(cls):
        return pymysql.connect(**CONNECTION_STRING)
    
    @classmethod
    def prepare_data_to_insert(cls, df):
        # zoradi stplce podla db
        cols = cls.get_data_from_query(f'SELECT * FROM {cls.TABLE_NAME} LIMIT 1').columns
        df.columns = [col.lower() for col in df.columns]
        df_to_db = df[cols]
        
        return cls.df2ListOfTuples(df_to_db)
    
    @staticmethod
    def df2ListOfTuples(df):
        return list(df.astype(object).where(pd.notnull(df), None).itertuples(index=False))
    
    @classmethod
    def execute_query(cls, SQL, message=None):
        try:
            with cls.create_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(SQL)
                    conn.commit()
            
                    if message:
                        logger.info(message)
                    else:
                        logger.info(f"Query '{SQL}' executed sucesfully!!!")
        
        except Exception as e:
            logger.info(f"Query '{SQL}' failed!!!")
            logger.exception('Exception occured')
            
    @classmethod
    def get_data_from_query(cls, query):
        try:
            with cls.create_connection() as con:
                return pd.read_sql(query, con)
        
        except Exception as e:
            logger.info(f"Query '{query}' failed!!!")
            logger.exception('Exception occured')
        
        return pd.DataFrame()
            
    @classmethod  
    def get_all_data(cls):
        SQL = f"SELECT * FROM {cls.TABLE_NAME}"
        
        return cls.get_data_from_query(SQL)
    
    @classmethod
    def delete_all_rows(cls, message=None):
        if not message:
            message = f'All rows from {cls.TABLE_NAME} deleted!!!'
            
        SQL = f"DELETE FROM {cls.TABLE_NAME}"

        cls.execute_query(SQL, message)
        
    @classmethod
    def create(cls, message=None):
        if not message:
            message = f'{cls.TABLE_NAME} table created!!!'

        cls.execute_query(cls.CREATE_SQL, message)
        
    @classmethod
    def drop(cls, message=None):
        if not message:
            message = f'{cls.TABLE_NAME} table droped!!!'
            
        SQL = f"DROP TABLE {cls.TABLE_NAME}"

        cls.execute_query(SQL, message)
    
    @classmethod
    def insert_many(cls,df):            
        SQL = f"""INSERT INTO {cls.TABLE_NAME} VALUES ({','.join(['%s']*cls.get_total_cols())})"""
        
        values = cls.prepare_data_to_insert(df)
            
        try:
            with cls.create_connection() as conn:
                with conn.cursor() as cur:
                    cur.executemany(SQL, values)
                    conn.commit()
                    logger.info(f'{len(values)} rows inserted succesfully')  
            
        except Exception as e:
            logger.info(f"Query '{SQL}' failed!!!")
            logger.exception('Exception occured')
            

class CarsTable(BaseTable):
    TABLE_NAME = 'cars'
    CREATE_SQL = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        id              VARCHAR(48),
                        url             VARCHAR(256),
                        make            VARCHAR(128),
                        model           VARCHAR(128),
                        color           VARCHAR(128),
                        interior_colour VARCHAR(128),
                        body            VARCHAR(128),
                        power           INTEGER,
                        drive_type      VARCHAR(32),
                        transmission    VARCHAR(32),
                        mileage         INTEGER,
                        registration    TIMESTAMP
                    )'''
    
    @classmethod
    def delete_by_id(cls, id_):
        SQL = f"DELETE FROM {cls.TABLE_NAME} WHERE id = '{id_}'"
        cls.execute_query(SQL)


class PriceHistoryTable(BaseTable):
    TABLE_NAME = 'price_history'
    CREATE_SQL = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        id          VARCHAR(48),
                        datetime    TIMESTAMP,
                        price       DECIMAL(12,2)
                    )'''
    
    @classmethod
    def delete_by_id(cls, id_):
        SQL = f"DELETE FROM {cls.TABLE_NAME} WHERE id = '{id_}'"
        cls.execute_query(SQL)
        

class FeaturesTable(BaseTable):
    TABLE_NAME = 'features'
    CREATE_SQL = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        id          VARCHAR(48),
                        feature     TEXT
                    )'''
    
    @classmethod
    def delete_by_id(cls, id_):
        SQL = f"DELETE FROM {cls.TABLE_NAME} WHERE id = '{id_}'"
        cls.execute_query(SQL)


class PhotosTable(BaseTable):
    TABLE_NAME = 'photos'
    CREATE_SQL = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        id          VARCHAR(48),
                        url         TEXT
                    )'''
    
    @classmethod
    def delete_by_id(cls, id_):
        SQL = f"DELETE FROM {cls.TABLE_NAME} WHERE id = '{id_}'"
        cls.execute_query(SQL)