from numpy.core.fromnumeric import partition
from pandas.core.indexes import category
from pandas.io import sql
from pandas.tseries.offsets import Hour
import yaml, os, sys, pymysql
import pandas as pd
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import pcc_summary_executor.deidentification as deidentification
from pcc_summary_executor.Logger import Logger as Logger

import date_util
import s3util

# load default dag arguments
from pcc_airflow_dag_config import *
dag_args = DEFAULT_DAG_ARGS

SELECT_KEY = {
    'diagnosis':'CRT_DATE', 'app_push':'CRT_DATE', 'email':'TRANSFER_DATE'
}
PARTITION_KEY = [
    'diagnosis':'DIAGNOSIS_DATE', 'app_push':'TRANSFER_DATE', 'HISTORY':'EMAIL_SEND_DATE', 'SURVEY':'SURVEY_SEND_DATE'
]

def add_date_partition_key(df, table_type, table):
    key = PARTITION_KEY[table.split("_")[-3]] if (table_type == 'email') else PARTITION_KEY[table_type]

    df['datetime'] = pd.to_datetime(df[key])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month.apply(lambda x: "{:0>2d}".format(x))
    df['day'] = df['datetime'].dt.day.apply(lambda x: "{:0>2d}".format(x))
    df['date'] = df[['year', 'month', 'day']].applymap(str).apply(lambda x: '-'.join(x), axis=1)
    df.drop(['datetime', 'year', 'month', 'day'], axis='columns', inplace=True)

    return df


def convert_datetime(df):
    for col in df.columns:
        if (col.find("DATE") != -1):
            df[col] = df[col].astype(str)
    
    return df


def load_yaml(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)


def connect_db(base_conf):
    return pymysql.connect(
        host=base_conf['db_info']['host'],
        port=base_conf['db_info']['port'],
        user=base_conf['db_info']['user'],
        password=base_conf['db_info']['password'],
        db=base_conf['db_info']['database'],
        charset='utf-8',
        local_infile=1
    )


def load_db_data(conn, base_conf, start_datetime, end_datetime, table, table_type):
    sql = f"SELECT * FROM {base_conf['db_info']['database']}.{table} WHERE {SELECT_KEY[table_type]} >= '{start_datetime}' AND {SELECT_KEY[table_type]} < '{end_datetime}'"
    return pd.read_sql(sql, conn)


def add_partiton_key(df, table, table_type, category_map):
    table_split = table.split('_')
    df = add_date_partition_key(df, table_type, table)

    if (table_type == 'diagnosis'):
        partition_cols = ['server', 'region', 'country', 'category', 'date']
        df['server'] = df['DEVICE_INFO_SERVER_NAME']
        df['region'] = table_split[-2]
        df['country'] = table_split[-1]
        df['category'] = category_map['_'.join(table_split[2:-2])]
    elif (table_type == 'app_push'):
        partition_cols = ['server', 'region', 'country', 'category', 'date']
        df['server'] = df['DEVICE_INFO_SERVER_NAME']                
        df['country'] = df['REGIST_COUNTRY']
        df['category'] = df['CATEGORY_CODE']
        df['region'] = table_split[-1]
    elif (table_type == 'email'):
        partition_cols = ['date']

    return df, partition_cols


def deidentify(df, access_key, secret_key, bucket_name):
    bucket_name = bucket_name.replace('result', 'profile')
    salt = deidentification.get_salt(access_key, secret_key, bucket_name)

    if 'DEVICE_INFO_DEVICE_ID' in df.columns:
        df['DEVICE_INFO_DEVICE_ID'] = df.apply(lambda x: x['DEVICE_INFO_DEVICE_ID'] if len(x['DEVICE_INFO_DEVICE_ID']) >= 64 else deidentification.generate_sha_hash(x['DEVICE_INFO_DEVICE_ID'], salt), axis=1)
    if 'DEVICE_INFO_MBR_NO' in df.columns:
        df['DEVICE_INFO_MBR_NO'] = df.apply(lambda x: x['DEVICE_INFO_MBR_NO'] if isinstance(x['DEVICE_INFO_MBR_NO'],list) and len(x['DEVICE_INFO_MBR_NO'][0]) >= 64 else deidentification.generate_sha_hash_array(x['DEVICE_INFO_MBR_NO'], salt) if isinstance(x['DEVICE_INFO_MBR_NO'],list) else x['DEVICE_INFO_MBR_NO'] if len(x['DEVICE_INFO_MBR_NO'][0]) >= 64 else deidentification.generate_sha_hash(x['DEVICE_INFO_MBR_NO'], salt), axis=1)

    return df


def deidentify_datetime(df, col_list):
    for col in col_list:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:00:00')

    return df


def sync_data(base_conf, start_datetime, end_datetime, table, table_type, logger, category_map):
    conn = connect_db(base_conf)

    logger.info({'DB to S3 Sync Load DB Data:': table})
    df = load_db_data(conn, base_conf, start_datetime, end_datetime, table, table_type)
    logger.info({'DB to S3 Sync Deidentify Data:': table})

    if (base_conf['stage_env'].lower() == 'prod'):
        deidentified_df = deidentify(df, base_conf['access_key'], base_conf['secret_key'], base_conf['source_base_path'].split("/")[0])
    else:
        deidentified_df = df

    logger.info({'DB to S3 Sync Datatime PreProcessing': table})
    datetime_df = convert_datetime(deidentified_df)

    logger.info({'DB to S3 Sync Add Partition Key': table})
    result_df, partition_cols = add_date_partition_key(datetime_df, table, table_type, category_map)

    logger.info({'DB to S3 Sync Write Data': table})
    bucket_name = base_conf['source_base_path'].split("/")[0]
    db_sync_path = os.path.join(bucket_name, base_conf['source_base_path'])
    if (table_type == "email"):
        target_path = os.path.join(db_sync_path, table_type, table.split("_")[-3].lower())
        if (table.split("_")[3] == "SURVEY"):
            result_df = deidentify_datetime(result_df, ['SURVEY_SEBD_DATE'])
    else:
        target_path = os.path.join(db_sync_path, table_type)
    s3util.erite_json_data(result_df, base_conf['access_key'], base_conf['secret_key'], target_path, partition_cols)

    conn.close()

    return

def db_to_s3_sync(**kwargs):
    base_conf = kwargs['base_conf']
    config = kwargs['config']
    category_map = kwargs['category_map']
    logger = Logger('sync_db_to_s3')
    now_datetime = kwargs['next_execution_date'].replace(hour=0, minute=0, second=0, microsecond=0)

    if (kwargs['dag_run'].conf is not None and kwargs['dag_run'].conf['start_datetime'] is not None and kwargs['dag_run'].conf['end_datetime'] is not None and kwargs['dag_run'].conf['table_type'] is not None kwargs['dag_run'].conf['table'] is not None):
        start_datetime = kwargs['dag_run'].conf['start_datetime']
        end_datetime = kwargs['dag_run'].conf['end_datetime']
        logger.info({'DB to S3 Sync Trigger': 'Manual'})
        sync_data(base_conf, start_datetime, end_datetime, kwargs['dag_run'].conf['table'], kwargs['dag_run'].conf['table_type'], logger, category_map)
    else:
        end_datetime = date_util.get_datetime_string(now_datetime)
        start_datetime = date_util.get_datetime_string(now_datetime = timedelta(days=1))
        logger.info({'DB to S3 Sync Trigger': 'Schedule'})
        for sync_table in config['sync_table_list']:
            for table in sync_table['table_list']:
                sync_data(base_conf, start_datetime, end_datetime, table, sync_table['table_type'], logger, category_map)
    
    logger.info({'DB to S3 Sync Start Datetime :': start_datetime, 'End Datetime': end_datetime})

    return


def main():
    dag_name = 'sync_db_to_s3'
    this = sys.modules[__name__]
    base_conf_path = '/opt/airflow/dags/pcc_summary_executor/config/base_conf.yaml'
    region = os.environ['AWS_DEFAULT_REGION']
    config_base_path = os.path.join('/opt/airflow/dags/pcc_airflow_dag_config', region)
    config_path = os.path.join(config_base_path,'sync_config/db_to_s3sync_config.yaml')
    category_map_path = os.path.join('/opt/airflow/dags/pcc-airflow_dag_config', 'category_map.yaml')

    base_conf = load_yaml(base_conf_path)
    config = load_yaml(config_path)
    category_map = load_yaml(category_map_path)

    dag_args['queue'] = 'default'
    dag = DAG(
        dag_id = dag_name,
        default_args = dag_args,
        catchup = False,
        schedule_interval = config['schedule']
    )

    sync_db_to_s3_task = PythonOperator(
        task_id = dag_name,
        python_callable = db_to_s3_sync,
        op_kwargs = {'base_conf': base_conf, 'config': config, 'category_map': category_map},
        dag = dag
    )

    sync_db_to_s3_task
    setattr(this, dag_name, dag)

main()