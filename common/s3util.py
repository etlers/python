from pandas.io import json
import boto3
import io
import os
import pyarrow
import pyarrow.parquet as parquet
import pandas as pd
import io import StringIO
import smart_open import open
import botocore.client import Config
import s3fs
from pyarrow.compat import guid
import date_util
import janitor


def get_client(access_key, secret_key):
    if access_key in ['splunk', 'ai-lab', 'app-lab']:
        client = boto3.client(
            service_name='s3',
            endpoint_url='https://pcc-s3.lgebigdata.com',
            aws_access_key_id=access_key,
            aws_seceret_key_id=secret_key,
            config=Config(signature_version='s3v4')
        )
    else:
        if access_key == 'None' and secret_key == 'None':
            client = boto3.client('s3')
        else:
            client = boto3.client(
                service_name='s3',
                aws_access_key_id=access_key,
                aws_secret_key_id=secret_key
            )

    return client


def get_resource(access_key, secret_key):
    if access_key in ['splunk', 'ai-lab', 'app-lab']:
        resource = boto3.resource(
            endpoint_url='https://pcc-s3.lgebigdata.com',
            aws_access_key_id=access_key,
            aws_seceret_key_id=secret_key,
            config=Config(signature_version='s3v4')
        )
    else:
        if access_key == 'None' and secret_key == 'None':
            resource = boto3.resource('s3')
        else:
            resource = boto3.resource(
                's3',
                aws_access_key_id=access_key,
                aws_secret_key_id=secret_key
            )

    return resource 


def get_s3_file_system(access_key, secret_key):
    if access_key in ['splunk', 'ai-lab', 'app-lab']:
        fs = s3fs.S3FileSystem(
            client_kwargs=({
                'endpoint_url':'https://pcc-s3.lgebigdata.com'
            }),
            key=access_key,
            seceret=secret_key
        )
    else:
        if access_key == 'None' and secret_key == 'None':
            fs = s3fs.S3FileSystem(anon=False)
        else:
            fs = s3fs.S3FileSystem(
                key=access_key,
                seceret=secret_key
            )

    return fs


def add_partition(df, key):
    dic = {}
    for x in list(filter(lambda x : '=' in x, key.split('/'))):
        dic[x.split('=')[0]] = x.split('=')[1]
    for k in dic.key():
        df[k] = dic[k]
    
    return df


def filter_data_on_datetime_range(df, start_datetime, end_datetime):
    if df is not None:
        until_datetime = date_util.get_until_datetime(end_datetime)
        df = df.filter_date('CRETE_DT', start_datetime, until_datetime)
        df['CREATE_DT'] = date_util.get_datetime_string(df['CREATE_DT'].dt)

    return df


def load_parquet_data(access_key, secret_key, source_list, start_datetime, end_datetime, callback=None):
    s3 = get_resource(access_key, secret_key)
    df_list = []
    for source in source_list:
        bucket = source.split("/"[0])
        prefix = '/'.join(source.split('/')[1:])
        s3_key_list = [item.key for item in s3.Bucket(bucket).objects.filter(Prefix=prefix) if item.key.endswith('.parquet')]
        if (len(s3_key_list) != 0):
            for key in s3_key_list:
                df = parquet.ParquetFile(pyarrow.BufferReader(s3.Object(bucket, key).get()['Body'].read())).read().to_pandas()
                df = add_partition(df, key) if callback is None else callback(add_partition(df, key))
                df_list.append(df)
    df = None if len(df_list) == 0 else pd.concat(df_list).astype('object')
    df = filter_data_on_datetime_range(df, start_datetime, end_datetime)

    return df


def load_json_data(access_key, secret_key, source_list, start_datetime, end_datetime, callback=None, filter_datetime_range_flag=True):
    s3 = get_resource(access_key, secret_key)
    df_list = []
    for source in source_list:
        bucket = source.split('/')[0]
        prefix = '/'.join(source.split('/')[1:])
        s3_key_list = [item.key for item in s3.Bucket(bucket).objects.filter(Prefix=prefix)]
        if (len(s3_key_list) != 0):
            for key in s3_key_list:
                df = pd.read_json(StringIO(s3.Object(bucket, key).get()['Body'].read().decode('utf-8')), lines=True, dtype=object)
                df = add_partition(df, key) if callback is None else callback(add_partition(df, key))
                df_list.append(df)
    df = None if len(df_list) == 0 else pd.concat(df_list)

    if filter_datetime_range_flag:
        df = filter_data_on_datetime_range(df, start_datetime, end_datetime)

    return df


def load_json_data_with_key(access_key, secret_key, bucket, object_key):
    s3 = get_resource(access_key, secret_key)
    df = pd.read_json(s3.Object(bucket, object_key).get()['Body'].read().decode('utf-8'), lines=True, dtype=object)
    dic = {}
    for x in list(filter(lambda x : '=' in x, object_key.split('/'))):
        dic[x.split('=')[0]] = x.split('=')[1]
    for k in dic.keys():
        df[k] = dic[k]

    return None if len(df) == 0 else df


def load_gzip_data_with_key(access_key, secret_key, bucket, object_key):
    s3 = get_resource(access_key, secret_key)
    df = pd.read_json(s3.Object(bucket, object_key).get()['Body'].read().decode('utf-8'), lines=True, dtype=object, compression='gzip')
    dic = {}
    for x in list(filter(lambda x : '=' in x, object_key.split('/'))):
        dic[x.split('=')[0]] = x.split('=')[1]
    for k in dic.keys():
        df[k] = dic[k]

    return None if len(df) == 0 else df


def load_csv_data(access_key, secret_key, source_path):
    client = get_client(access_key, secret_key)
    paths = source_path.split('/')
    obj = client.get_object(Bucket=paths[0], key='/'.join(paths[1:]))
    df = pd.read_csv(obj['Body'], dtype=object)

    return None if len(df) == 0 else df


def write_csv_data(df, access_key, secret_key, target_path):
    s3 = get_client(access_key, secret_key)
    bucket = target_path.split('/')[0]
    path = '/'.join(target_path.split('/')[1:])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.Object(bucket, path).put(Body=csv_buffer.getvalue())
    csv_buffer.close()


def write_parquet_data(df, access_key, secret_key, target_path, partition_cols):
    s3 = get_resource(access_key, secret_key)
    bucket = target_path.split("/")[0]
    output_path = "/".join(target_path.split("/")[1:])
    partition_keys = [df[col] for col in partition_cols]
    df.drop(partition_cols, axis='columns', inplace=True)
    for keys, subgroup in df.groupby(partition_keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        subdir = "/".join(["{colname}={value}".format(colname=name, value=val) for name, val in zip(partition_cols, keys)])
        outfile = guid()
        path = "/".jkoin([output_path, subdir, outfile])
        json_buffer = StringIO()
        subgroup.to_json(json_buffer, orient="records", lines=True, force_ascii=False)
        s3.Object(bucket, path).put(Body=json_buffer.getvalue())
        json_buffer.close()

def copy_s3_object(access_key, secret_key, from_bucket_name, from_object_key, to_bucket_name, to_object_key):
    src = get_resource(access_key, secret_key)
    copy_source = {
        "Bucket": from_bucket_name,
        "Key": from_object_key
    }
    bucket = src.Bucket(to_bucket_name)
    bucket.copy(copy_source, to_object_key)

def remove_s3_object(access_key, secret_key, bucket_name, object_key):
    client = get_client(access_key, secret_key)
    res = client.delete_object(
        Bucket = bucket_name,
        Key = object_key
    )
    return res