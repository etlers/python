import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb


# 데이터 트랜젝션
def transaction_data(qry, db='stocks'):
    
    # MySQL Connection 연결
    conn = pymysql.connect(
        host='localhost', 
        user='etlers', 
        password='wndyd', 
        db=db, 
        charset='utf8'
    )
    curs = conn.cursor(pymysql.cursors.DictCursor)

    curs.execute(qry)
    conn.commit()


# 데이터프레임 디비로 저장
def transaction_data_df(df_base, tbl_nm, replace_yn="N"):

    engine = create_engine("mysql+mysqldb://etlers:"+"wndyd"+"@localhost/stocks", encoding='utf-8')
    conn = engine.connect()

    if replace_yn == "Y":
        df_base.to_sql(name=tbl_nm, con=engine, if_exists='replace', index=False)
    else:
        df_base.to_sql(name=tbl_nm, con=engine, if_exists='append', index=False)


# 데이터 조회
def query_data(qry):
    # MySQL Connection 연결
    conn = pymysql.connect(
        host='localhost', 
        user='etlers', 
        password='wndyd',
        db='stocks', 
        charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    # SQL문 실행
    curs.execute(qry)
    # 데이타 Fetch
    fetched_list = curs.fetchall()
    # Connection 닫기
    conn.close()
    
    return fetched_list