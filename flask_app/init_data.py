from typing import NamedTuple, List, Type, Iterable
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
            f"    timestamp TIMESTAMPTZ NOT NULL\n"
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

        for definition in table.definitions:
            if definition.db_column not in column_names:
                sql = f'ALTER TABLE {quote_ident(table.name, curs)} ADD COLUMN {quote_ident(definition.db_column, curs)} {definition.column_type} NULL'
                logger.debug(f"Executing: {sql}")
                curs.execute(sql)


def create_tables(conn, tables: List[Table]):
    logger.info("Creating tables (if needed)")
    for table in tables:
        create_table(conn, table)
        
is_success = False
with open("./pg_config.yaml") as txt:
    tables = read_definitions(txt)
    with psycopg2.connect(f"postgresql://zalando:{config2.psql_pw}@192.168.1.151:30001/movies") as conn:
        conn.autocommit = True
        logger.debug(f"Connected to Postgres")
        create_tables(conn, tables)
        conn.commit()
        is_success = True