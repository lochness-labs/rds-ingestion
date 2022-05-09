#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging

# Environment variables
GLUE_CONNECTION_NAME = os.getenv('glue_connection_name')
GLUE_DATABASE_NAME = os.getenv('glue_database_name')
DATABASE_NAMES = os.getenv('database_names')
JOB_NAME = os.getenv('job_name')
S3_DATA_BUCKET = os.getenv('s3_data_bucket')
S3_CODE_BUCKET = os.getenv('s3_code_bucket')


def get_logger():
    """
    Get logger suppressing some boto info.

    TODO/FEAT/GenericLayer: This is a generic function and should be moved into a custom layer
    """
    logger = logging.getLogger()
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.getLogger('boto3').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)

    return logger


logger = get_logger()


def handler(event=None, context=None):

    try:
        out_event = []

        for DATABASE_NAME in DATABASE_NAMES.split(', '):

            logger.info(f'Adding {DATABASE_NAME}')

            out_event.append({
                's3_data_bucket': S3_DATA_BUCKET,
                's3_code_bucket': S3_CODE_BUCKET,
                'resource_name': JOB_NAME,
                'glue_connection_name': GLUE_CONNECTION_NAME,
                'glue_database_name': GLUE_DATABASE_NAME,
                'database_name': DATABASE_NAME.strip()
            })

        return out_event

    except Exception as e:
        logger.error('#: %s' % e, exc_info=True)
        raise e


if __name__ == "__main__":
    handler(event=None, context=None)
