import os, sys
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import ec2_util

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "pcc_summary_executor"))

from load_config import *

dag_args = DEFAULT_DAG_ARGS

def terminate_ec2(**kwargs):
    if (kwargs['dag_run'].conf is not None and kwargs['dag_run'].conf['instance_id'] is not None):
        instance_id = kwargs['dag_run'].conf['isntance_id']
        ec2_util.terminate_instance(instance_ids=[instance_id])
        print(f"Instance {instance_id} terminated")
    return

def main():

    this = sys.modules[__name__]

    dag_name = 'terminate_ec2'
    dag_args['queue'] = 'default'

    dag = DAG(
        dag_id = dag_name,
        default_args = dag_args,
        catchup = False,
        max_active_runs = 1,
        schedule_interval = None
    )

    terminate_ec2_task = PythonOperator(
        task_id = dag_name,
        python_callable = terminate_ec2,
        provide_context = True,
        dag = dag
    )

    terminate_ec2_task
    setattr(this, dag_name, dag)

main()