import pymysql
import pandas as pd
from sqlalchemy import create_engine, engine
import urllib.parse

from pandas.io import sql
from Logger import Logger

def load_db_data(host, port, user, password, db, sql, table):
    con = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8', autocommit=True)
    df = pd.read_sql(sql, con)
    return df

def write_db_data(df, host, port, user, password, db, table):
    logger = Logger('write_db_data')
    encode_pw = urllib.parse.quote_plus(password)
    db_info = "mysql+pymysql://" + user + ":" + encode_pw + "@" + host + ":" + str(port) + "/" + db + "?charset=utf8"
    engine = create_engine(db_info, encoding='utf-8')
    logger.info({'db':db, 'table': table})
    df.to_sql(name=table, con=engine, if_exists='append', index=False)

def write_sql(host, port, user, password, db, sql):
    con = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8', autocommit=True)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()

"""
    Only works for pandas 1.0.3
    monkey patched method
    'sql.SQLTable._execute_insert'
"""
def write_db_data_ignore(df, host, port, user, password, db, table):
    support_vers = [
        "1.0.3", "1.1.3"
    ]

    assert pd.__version__ in support_vers

    def moneky_patch_execute_insert(self, conn, keys, data_iter):
        data = [dict(zip(keys, row)) for row in data_iter]
        conn.execute(self.table.insert().prefix_wirh("IGNORE"), data)

    orig_execute_insert = sql.SQLTable._execute_insert
    sql.SQLTable._execute_insert = moneky_patch_execute_insert
    write_db_data(df, host, port, user, password, db, table)
    sql.SQLTable._execute_insert = orig_execute_insert