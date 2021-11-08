import os
import sys
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import yaml
import json
import pandas as pd
import fnmatch

from airflow.models import DAG

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "pcc_summary_executor"))

from diagnosis_process import generate_dag
import WRAPPER
import date_util
from Logger import Logger as Logger

from load_config import *
dag_args = DEFAULT_DAG_ARGS

cwd = os.getcwd()


def load_config_file(config_path):
    with open(config_path) as f:
        config_value = yaml.safe_load(f)
    return config_value


def diagnosis_summary(logic_name, base_conf_path, **kwargs):
    logic = logic_name.split(".")[0]
    config = logic_name.split(".")[1]

    logic_path = os.path.join(cwd, 'dags', 'proactive_logic')
    os.environ["BASE_CONF"] = base_conf_path
    os.environ["LOOKUP_DIR"] = os.path.join(logic_path, 'lookup')

    for (logic_path, dir, files) in os.walk(logic_path):
        for file_name in files:
            if fnmatch.fnmatch(file_name, logic + ".py"):
                script_path = os.path.join(logic_path, file_name)
            elif fnmatch.fnmatch(file_name, logic + ".yaml"):
                config_path = os.path.join(logic_path, file_name)

    config_value = load_config_file(config_path)

    logger = Logger(config)

    next_execution_date = kwargs['next_execution_date']
    normalized_now_time = date_util.get_normalized_datetime(next_execution_date, 60)
    diagnosis_date = date_util.get_before_datetime(date_util.get_datetime_string(normalized_now_time), hours=1 if 'hourly' in config_value['output_path'] else (2 if 'daily' in config_value['output_path'] else 3))

    logger.info({'next_execution_date': str(next_execution_date)})
    logger.info({'diagnosis_date': str(diagnosis_date)})

    WRAPPER.run(script_path=script_path, config_path=config_path, diagnosis_date_list=[diagnosis_date])


def load_ec2_config(df, logic_name):
    df = df[df.SUMMARY_CONFIG_NAME.eq(logic_name)]
    ec2_config = {
        'ami': EC2_CONFIG['ami'],
        'ec2_template': EC2_CONFIG['ec2_template'],
        'template_version': EC2_CONFIG['template_version'],
        'op_type': df["op_type"].values[0],
        'instance_id': df["instance_id"].values[0],
        'ec2_type': df["ec2_type"].values[0]
    }
    return ec2_config


def main():
    base_conf_path = os.path.join(cwd, 'dags', 'pcc_summary_executor', 'config', 'base_conf.yaml')
    base_conf = load_config_file(base_conf_path)

    region = base_conf['db_info']['database'].split("_")[2]

    config_file_name = os.path.join(cwd, 'dags', 'pcc_diagnosis_schedule', region.upper(), 'diagnosis_schedule_config_' + region + ".csv")
    df = pd.read_csv(config_file_name)
    df = df[(df['SUMMARY_TYPE'] != 'on-arrival-diagnosis')]

    df['SUMMARY_CONFIG_NAME'] = df['SUMMARY_NAME'] + "." + df['CONFIG_NAME']

    this = sys.modules[__name__]

    for (logic_name, schedule_time) in zip(df["SUMAMRY_CONFIG_NAME"], df['SCHEDULE_TIME']):
        dag_args['queue'] = logic_name
        if 'customer_report' in logic_name:
            dag_args['start_date'] = datetime.now() - relativedelta(month=2)
        dag_config = {
            'dag_id': logic_name,
            'dag_default_args': dag_args,
            'process_func': diagnosis_summary,
            'schedule_interval': schedule_time,
            'logic_name': logic_name,
            'base_conf_path': base_conf_path,
            'ec2_config': load_ec2_config(df, logic_name)
        }
        dag = generate_dag(**dag_config)
        setattr(this, logic_name, dag)


main()