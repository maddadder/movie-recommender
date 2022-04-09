from cmath import pi
from typing import NamedTuple, List, Type, Iterable
from sqlalchemy import create_engine
import pandas as pd
import logging

try:
    from yaml import load, FullLoader
except ImportError:
    raise ImportError("To use this command you must install the pyyaml package")
try:
    import psycopg2
    from psycopg2.extensions import quote_ident
except ImportError:
    raise ImportError("To use this command you must install the psycopg2-binary (or psycopg2) package")
import flask_app.config2 as config2

logger = logging.getLogger('my_logger')

class Table(NamedTuple):
    name: str
    definitions: List["Definition"]


class Definition(NamedTuple):
    column_type: str
    db_column: str
    isnull: str

def read_definitions(f) -> List[Table]:
    logger.info(f"Reading field definitions")
    in_yaml = load(f, Loader=FullLoader)
    tables = []

    for table_name, in_definitions in in_yaml.get('tables', {}).items():
        definitions = []
        for in_definition in in_definitions:
            # Get the block class
            definitions.append(Definition(
                column_type=in_definition['column_type'],
                db_column=in_definition['db_column'],
                isnull=in_definition['isnull'],
            ))

        tables.append(
            Table(table_name, definitions)
        )

    logger.debug(f"Found definitions: {tables}")
    return tables


def create_table(conn, table: Table):
    with conn.cursor() as curs:
        # Create the table in case it does not already exist
        sql = (
            f"CREATE TABLE IF NOT EXISTS {quote_ident(table.name, curs)} (\n"
            f"    \n"
            f")"
        )
        logger.info(f"Executing: {sql}")
        curs.execute(sql)

        # Get existing columns
        sql = (
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = 'public' "
            "AND table_name = %s"
        )
        curs.execute(sql, [table.name])
        column_names = {row[0] for row in curs.fetchall()}
        print(column_names)
        needed_columns = False
        set_primary_key = ""
        for definition in table.definitions:
            if definition.db_column not in column_names:
                if definition.column_type == "primary":
                    set_primary_key = f'ALTER TABLE {quote_ident(table.name, curs)} ADD PRIMARY KEY {definition.db_column} '
                else:
                    needed_columns = True
                    sql = f'ALTER TABLE {quote_ident(table.name, curs)} ADD COLUMN {quote_ident(definition.db_column, curs)} {definition.column_type} {definition.isnull}'
                    print(sql)
                    curs.execute(sql)
                    conn.commit()
        if needed_columns:
            print(set_primary_key)
            curs.execute(set_primary_key)
            conn.commit()
            

def create_tables(conn, tables: List[Table]):
    logger.info("Creating tables (if needed)")
    for table in tables:
        create_table(conn, table)

def import_data():

    
    conn = psycopg2.connect(database="movies",
                            user='zalando', password=config2.psql_pw, 
                            host='192.168.1.151', port='30001'
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    #movieId,title,genres
    
    sql2 = '''COPY movies(movieId,title,genres)
    FROM '../data/movies.csv'
    DELIMITER ','
    CSV HEADER;'''
    
    cursor.execute(sql2)
    
    sql3 = '''select * from movies;'''
    cursor.execute(sql3)
    for i in cursor.fetchall():
        print(i)
    
    conn.commit()
    conn.close()

is_success = False
with open("./pg_config.yaml") as txt:
    tables = read_definitions(txt)
    with psycopg2.connect(f"postgresql://zalando:{config2.psql_pw}@192.168.1.151:30001/movies") as conn:
        conn.autocommit = True
        logger.debug(f"Connected to Postgres")
        create_tables(conn, tables)
        conn.commit()
    
        engine = create_engine(f"postgresql://zalando:{config2.psql_pw}@192.168.1.151:30001/movies")

        with open('./data/movies.csv', 'r') as file:
            #movieId,title,genres
            df = pd.read_csv(file, index_col='movieId')
            df.to_sql(name = 'movies', con = engine, if_exists = 'replace', index_label = 'movieId')
            with open('./data/ratings.csv', 'r') as file:
                #userId,movieId,rating,timestamp
                df = pd.read_csv(file, index_col='userId')
                df.to_sql(name = 'movie_ratings', con = engine, if_exists = 'replace', index_label = 'userId')
                with open('./data/links.csv', 'r') as file:
                    #movieId,imdbId,tmdbId
                    df = pd.read_csv(file, index_col='movieId')
                    df.to_sql(name = 'link', con = engine, if_exists = 'replace', index_label = 'movieId')
                    is_success = True