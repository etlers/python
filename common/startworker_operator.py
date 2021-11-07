from airflow.operators.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
import boto3
import os
import logging
import ec2_util

from load_config import *

class StartWorkerOperator(BaseOperator):

    @apply_defaults
    def __init__(self, ec2_config={}, task_que=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ami = ec2_config['ami']
        self.ec2_type = ec2_config['ec2_type']
        self.ec2_template = ec2_config['ec2_template']
        self.op_type = ec2_config['op_type']
        self.template_version = ec2_config['template_version']
        self.instance_id = ec2_config['instance_id']
        self.task_queue = ec2_config['task_queue']

    def execute(self, context):
        ti = context['task_instance']
        print(f"Requests ec2 resource for {self.task_queue} : {self.ec2_type}")

        try:
            if self.op_type is "C":
                self.instance_id = ec2_util.create_instance(
                    self.ami, self.ec2_type, self.ec2_template, self.template_version, tags=[
                        {
                            'key': 'airflow-task_queue',
                            'value': self.task_queue
                        }
                    ]
                )
                ti.xcom_push('instance_id', self.instance_id)
                print(f"Instance {self.instance_id} created")
            elif self.op_type is "S":
                ec2_util.start_instance(instance_ids=[self.instance_id])
                print(f"Instance {self.instance_id} started")
            else:
                logging.exception('Invalid operation type. Check the pcc_diagnosis_schedule value.')
        except Exception:
            logging.exception('Terminated ec2')
            if self.op_type is 'C':
                ec2_util.terminate_instance(instance_ids=[self.instance_id])
            elif self.op_type is 'S':
                ec2_util.start_instance(instance_ids=[self.instance_id])
            raise Exception('An error has occurred. Please check the log.')

        return self.instance_id