import os, sys
from datetime import datetime, timedelta

sqs_suffix = "_dev"

replace_log_url_port = "init-an2-tc-dev-airflow-master-cd66f7ae76c14d94.elb.ap-northeast-2.amazonaws.com:180800"

DEFAULT_DAG_ARGS  = {
    'owner': 'PCC',
    'depends_on_past': False,
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=20),
    'provide_context': True,
    'start_date': (datetime.now() - timedelta(days=2)),
    'queue': "default"
}

EC2_CONFIG = {
    'ami': "ami-06d7916c6462189ee",
    'ec2_template': 'it-an2-thinqcare-airflow-worker-spot',
    'template_version': "7"
}