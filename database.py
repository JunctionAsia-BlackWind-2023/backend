from asyncio import constants
from infra.exception import EngineNoneTypeException

from sqlmodel import  SQLModel, create_engine, Session,select
from sqlalchemy.future import Engine

from secret import mysql_connection_string

print(mysql_connection_string)

engine = create_engine(mysql_connection_string,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db_engine()-> Engine:
    if engine == None:
        raise EngineNoneTypeException("The engine is None")
    return engine

def get_db_session():
    return Session(get_db_engine())

def get_by_id(table, id):
    with get_db_session() as session:
        statement = select(table).where(table.id ==id)
        return session.exec(statement).one_or_none()

'''
def get_rds_connection():
    try:
        rds_conn = pymysql.connect(
            host=rds_connection_host,
            user=rds_connection_username,
            passwd = rds_connection_password,
            db=rds_connection_database,
            port=rds_connection_port,
            use_unicode=True,
            charset ='utf8')
'''
    
