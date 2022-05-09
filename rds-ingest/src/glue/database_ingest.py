# Import all the python mumbo jumbo
from datetime import datetime
import awswrangler as wr
import logging
import sys

# Import getResolvedOptions if on Glue environment
try:
    from awsglue.utils import getResolvedOptions
except ImportError:
    print("Local run...")


execution_time = int(datetime.now().timestamp())

# Set execution details constants # TODO/FEAT/Configuration.
ZONE = 'intake'
TIER = 'raw'
PROCESS = 'database'


def get_logger():
    """
    Get the right logger configuration (thanks to https://stackoverflow.com/a/63361324)

    TODO/FEAT/GenericWHL: This is a generic function and should be moved into a custom WHL
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger()

def main(event):

    data_bucket = event['s3_data_bucket']
    code_bucket = event['s3_code_bucket']
    glue_connection_name = event['glue_connection_name']
    glue_database_name = event['glue_database_name']
    database_name = event['database_name']

    try:

        con = wr.mysql.connect(glue_connection_name)

        sql_query = f"SHOW TABLES IN {database_name}"
        df = wr.mysql.read_sql_query(sql=sql_query, con=con)

        for index, row in df.iterrows():
            table_name = row[f'Tables_in_{database_name}']

            sql_query_table = f"SELECT * FROM {database_name}.{table_name}"
            df_table = wr.mysql.read_sql_query(sql=sql_query_table, con=con)

            if df_table.empty:
                continue

            df_table['dumpdate'] = execution_time

            # Convert all columns to string
            df_table = df_table.astype(str)

            extraction = f'{database_name}_{table_name}'

            print(f"\n> Extraction is: {extraction}, size is:")
            print(df_table.size)

            wr.s3.to_parquet(
                df=df_table,
                path=f's3://{data_bucket}/{ZONE}/{TIER}/{PROCESS}/{extraction}/',
                dataset=True,
                database=glue_database_name,
                table=f't_{extraction}_v1', # TODO/FEAT/Configuration - Move version to conf
                partition_cols=['dumpdate'],
                mode='append',
                schema_evolution=True,
            )


        logger.info("I'm done")

    except Exception as e:
        # TODO/FEAT/FlowControl: Maybe handle errors on S3 or elsewhere
        logger.error(e)
        raise e


if __name__ == "__main__":
    try:
        event = getResolvedOptions(sys.argv, [
            's3_data_bucket',
            's3_code_bucket',
            'glue_connection_name',
            'glue_database_name',
            'database_name'
        ])
    except NameError:
        # Fallback event for local development (outside Glue environment)
        event = {
            # * -> HERE YOU CAN CHANGE THE DATE FOR TESTING
            's3_data_bucket': 'your-datalake',
            's3_code_bucket': 'your-datalake-code',
            'glue_connection_name': 'test-connection',
            'glue_database_name': 'athena_db',
            'database_name': 'input_db_name'
        }

    logger.info(f'#: Event: {event}')
    main(event)
