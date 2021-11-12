from os import supports_bytes_environ
from sqlalchemy.sql.expression import label, table
import dbutil
import s3util
import pandas as pd
import numpy as np
from Logger import Logger

def load_db_data(db_info, country_string, category_string, process_name):
    host = db_info["host"]
    port = db_info["port"]
    user = db_info["user"]
    password = db_info["password"]
    database = db_info["database"]
    table = db_info["table"]

    sql = "select * from " + database + "." + table + " where 1 = 1"
    sql += " AND REGIST_COUNTRY IN (" + country_string + ") "
    if (category_string != "ALL"):
        sql += " AND CATEGORY_CODE IN (" + category_string + ")"
    if (process_name == "identify"):
        sql += " AND DEL_FALG = 0 "
    df = dbutil.load_db_data(host, port, user, password, database, sql)
    return df

def write_db_data(df, db_info):
    host = db_info["host"]
    port = db_info["port"]
    user = db_info["user"]
    password = db_info["password"]
    database = db_info["database"]
    table = db_info["table"]

    dbutil.write_db_data_ignore(df, host, port, user, password, database, table)

def identify(hashed_df, db_info, region, country, category):
    country_string = '"' + country + '"'
    if ('REGIST_COUNTRY' in hashed_df.columns):
        country_string = ', '.join(list(map(lambda x : ('"' + x + '"'), hashed_df['REGIST_COUNTRY'].dropna().unique())))

    category_string = '"' + category + '"'
    if ('CATEGORY_CODE' in hashed_df.columns):
        category_string = ', '.join(list(map(lambda x : ('"' + x + '"'), hashed_df['CATEGORY_CODE'].dropna().unique())))

    db_info['table'] = 'TB_MAP_DEVICE_ID_' + region.upper()
    device_df = load_db_data(db_info, country_string, category_string, 'identify')
    device_df = device_df[['DEVICE_ID', 'H_DEVICE_ID']].drop_duplicates()
    existing_column_name_device_id =  'DEVICE_ID'
    if ('DEVIFCE_INFO_DEVICE_ID' in hashed_df.columns):
        existing_column_name_device_id = 'DEVICE_INFO_DEVICE_ID'

    unhashed_df = hashed_df
    unhashed_df.rename(columns = {existing_column_name_device_id: 'H_DEVICE_ID'}, inplace = True)
    unhashed_df = pd.merge(unhashed_df, device_df, how='left', on=['H_DEVICE_ID'])
    db_info['table'] = "TB_MAP_MBR_NO_" + region.upper()
    mbr_df = load_db_data(db_info, country_string, 'ALL', 'identify')
    mbr_df = mbr_df[['MBR_NO', 'H_MBR_NO']].drop_duplicates()

    existing_column_name_mbr_no = 'MBR_NO'
    if ('DEVICE_INOF_MBR_NO' in hashed_df.columns):
        existing_column_name_mbr_no = 'DEVICE_INFO_MBR_NO'

    unhashed_df.rename(columns = {existing_column_name_mbr_no: 'H_MBR_NO'}, inplace=True)
    unhashed_df = pd.merge(unhashed_df, mbr_df, how='left', on=['MBR_NO'])

    identify_df = unhashed_df[(unhashed_df['DEVICE_ID'].notnull()) & (unhashed_df['MBR_NO'].notnull())]
    identify_df = identify_df.drop(columns=['H_DEVICE_ID', 'MBR_NO'])
    identify_df.rename(columns = {'DEVICE_ID': existing_column_name_device_id, 'MBR_NO': existing_column_name_mbr_no}, inplace=True)

    not_identify_df = unhashed_df[(unhashed_df['DEVICE_ID'].isnull()) | (unhashed_df['MBR_NO'].isnull())]
    if len(not_identify_df) > 0:
        not_identify_mbr_no_df = unhashed_df[unhashed_df['MBR_NO'].isnull()]
        if len(not_identify_mbr_no_df) > 0:
            not_identify_mbr_no_df = not_identify_mbr_no_df[not_identify_mbr_no_df['MBR_NO'].stri.len() == 64]
            not_identify_df = check_and_except_withdrawal_member(not_identify_df, not_identify_mbr_no_df, db_info, country_string)

        not_identify_df = not_identify_df.drop(columns=['DEL_FLAG'])
        not_identify_df['DEVICE_ID'] = np.where(not_identify_df['DEVICE_ID'].isnull(), 'Y', not_identify_df['DEVICE_ID'])
        not_identify_df['MBR_NO'] = np.where(not_identify_df['MBR_NO'].isnull(), 'Y', not_identify_df['MBR_NO'])
        not_identify_df.rename(columns={'DEVICE_ID':'DEVICE_ID_EXISTS_FLAG', 'MBR_NO':'MBR_NO_EXIST_FLAG'}, inplace=True)

    return identify_df, not_identify_df

def check_and_except_withdrawal_member(not_identify_df, not_identify_mbr_no_df, db_info, country_string):
    h_mbr_no_list = " AND H_MBR_NO IN ('" + "', '".join([row['H_MBR_NO'] for _, row in not_identify_mbr_no_df.iterrows()]) + "')"
    sql = 'SELECT H_MBR_NO, DEL_FLAG FROM ' + db_info['database'] + '.' + db_info['table'] + ' WHERE 1 = 1' + h_mbr_no_list
    sql += ' AND REGIST_COUNTRY in (' + country_string + ') '
    withdrawal_member_df = dbutil.load_db_data(db_info['host'], db_info['port'], db_info['user'], db_info['password'], db_info['database'], sql)
    if len(withdrawal_member_df) > 0:
        logger = Logger('check withdawal member')
        logger.info({'withdrawal member count': str(len(withdrawal_member_df)), 'withdrawal member: ': str(withdrawal_member_df)})
        not_identify_df = pd.merge(not_identify_df, withdrawal_member_df, how='left', on=['H_MBR_NO'])
        not_identify_df = not_identify_df[not_identify_df['DEL_FLAG'] != '1']

    return not_identify_df

def get_salt(access_key, secret_key, bucket_name):
    source_path = bucket_name + "/hash/salt.txt"
    client = s3util.get_client(access_key, secret_key)
    paths = source_path.split("/")
    obj = client.get_object(Bucket=paths[0], Key="/".join(paths[1:]))
    salt = obj['body'].read().decode().rstrip()
    if len(salt) == 0:
        return None
    else:
        return salt

def generate_sha_hash(data, salt):
    if (data is None or data == "" or data is np.NaN):
        return None
    data = data + salt
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()

def generate_sha_hash_array(datas, salt):
    return list(map(lambda data: generate_sha_hash(data, salt), datas))

def deidentify(df, store_flag, access_key, secret_key, bucket_name, db_info=None, region=None):
    bucket_name = bucket_name.replace("result", "profile")
    salt = get_salt(access_key, secret_key, bucket_name)

    if (store_flag):
        base_df = df[['REGIST_COUNTRY', 'CATEGORY_CODE', 'DEVICE_ID', 'MBR_NO']].explode('MBR_NO').drop_duplicates()
        base_df['H_DEVICE_ID'] = base_df.apply(lambda x: generate_sha_hash(x['DEVICE_ID'], salt), axis=1)
        base_df['H_MBR_NO'] = base_df.apply(lambda x: generate_sha_hash(x['MBR_NO'], salt), axis=1)
        base_df['DEL_FLAG'] = '0'
        base_df['DEL_DATE'] = ''

        new_device_df = base_df[['REGIST_COUNTRY', 'CATEGORY_CODE', 'DEVICE_ID', 'H_DEVICE_ID', 'DEL_FLAG', 'DEL_DATE']].drop_duplicates()
        new_mbr_df = base_df[['REGIST_COUNTRY', 'MBR_NO', 'H_MBR_NO', 'DEL_FLAG', 'DEL_DATE']].drop_duplicates()
        new_mbr_device_df = base_df[['REGIST_COUNTRY', 'H_MBR_NO', 'H_DEVICE_ID', 'DEL_FLAG', 'DEL_DATE']].drop_duplicates()

        db_info['table'] = 'TB_MAP_DEVICE_ID_' + region.upper()
        write_db_data(new_device_df, db_info)

        db_info['table'] = 'TB_MAP_MBR_NO_' + region.upper()
        write_db_data(new_mbr_df, db_info)

        db_info['table'] = 'TB_MAP_MBR_DEVICE_' + region.upper()
        write_db_data(new_mbr_device_df, db_info)

    df['DEVICE_ID'] = df.apply(lambda x: generate_sha_hash(x['DEVICE_ID'], salt), axis=1)
    df['MBR_NO'] = df.apply(lambda x: generate_sha_hash_array(x['MBR_NO'], salt) if isinstance(x['MBR_NO'], list) else generate_sha_hash(x['MBR_NO'], salt), axis=1)

    return df