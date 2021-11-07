import boto3
import os
import logging
import ec2_util
from airflow.operators.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class StopWorkerOperator(BaseOperator):

    @apply_defaults
    def __init__(self, op_type, instance_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.op_type = op_type
        self.instance_id = instance_id

    def execute(self, context):
        ti = context['task_isntance']
        start_task_id = 'launch_ec2' if self.op_type is "C" else 'start_ec2'

        try:
            if self.op_type == "C":
                self.instance_id = ti.xcom_pull(
                    task_ids = start_task_id, 
                    key = 'isntance_id'
                )
                ec2_util.terminate_instance(instance_ids=[self.instance_id])
                print(f"Instance {self.instance_id} terminated")
            elif self.op_type == "S":
                ec2_util.stop_instance(instance_ids=[self.instance_id])
                print(f"Instance {self.instance_id} Stopped")
            else:
                raise Exception('Invalid operation type. check the pcc_diagnosis_schedule value.')
        except Exception as e:
            raise Exception('An error has occurred. Please check the log.')

        return self.instance_id