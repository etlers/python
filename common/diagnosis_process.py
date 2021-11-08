import os, sys
from functools import partial
from urllib.parse import unquote
from datetime import timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from startworker_operator import StartWorkerOperator
from stopworker_operator import StopWorkerOperator


def generate_tasks(dag,
                   process_func,
                   logic_name,
                   base_conf_path,
                   ec2_config):
    start_worker = StartWorkerOperator(
        ec2_config = ec2_config,
        task_id = f'{"launch" if str(ec2_config["op_type"]) == "C" else "start"}_ec2',
        task_queue = logic_name,
        queue = 'default',
        dag = dag,
        retries = 2,
        retry_dealy = timedelta(seconds=5)
    )
    process_task = PythonOperator(
        task_id = f'{logic_name}',
        python_callable = process_func,
        op_kwargs = {'logic_name': logic_name, 'base_conf_path': base_conf_path},
        provide_context = True,
        dag = dag,
        retries = 2,
        retry_delay = timedelta(seconds=5)
    )
    stop_worker = StopWorkerOperator(
        dag = dag,
        op_type = ec2_config['op_type'],
        instance_id = ec2_config['instance_id'],
        task_id = f'{"terminate" if str(ec2_config["op_type"]) == "C" else "stop"}_ec2',
        trigger_rule = 'all_done',
        queue = 'default',        
        retries = 2,
        retry_dealy = timedelta(seconds=5)
    )
    start_worker >> process_task >> stop_worker

def generate_dag(dag_id,
                 dag_default_args,
                 process_func,
                 schedule_interval,
                 logic_name,
                 base_conf_path,
                 ec2_config):
    dag = DAG(
        dag_id = dag_id,
        default_args = dag_default_args,
        catchup = False,
        schedule_interval = schedule_interval
    )
    generate_tasks(
        dag = dag,
        process_func = process_func,
        logic_name = logic_name,
        base_conf_path = base_conf_path,
        ec2_config = ec2_config
    )
    return dag