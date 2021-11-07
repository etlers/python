"""
    Create, Start and Stop AWS EC2 Instance
"""
import boto3
import os, time

def get_client():
    client = boto3.client('ec2')
    return client

def get_resource():
    ec2 = boto3.resource('ec2')
    return ec2

def create_instance(ami_id, instance_type, template_id, template_version, tags=[]):
    ec2 = get_resource()
    client = get_client()
    instance = ec2.create_instance(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        Instancetype=instance_type,
        LaunchTemplate={
            'LaunchTemplateName': template_id,
            'Version': template_version
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            },
        ]
    )
    waiter = client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance[0].id])
    return instance[0].id

def terminate_instance(instance_ids=[]):
    client = get_client()
    client.stop_instance(Instanceids=instance_ids)
    waiter = client.get_waiter('instance_stopped')
    waiter.wait(Instanceids=instance_ids)

def stop_instance(instance_ids=[]):
    client = get_client()
    client.stop_instance(Instanceids=instance_ids)
    waiter = client.get_waiter('instance_running')
    waiter.wait(Instanceids=instance_ids)

def start_instance(instance_ids=[]):
    client = get_client()
    client.start_instance(Instanceids=instance_ids)
    waiter = client.get_waiter('instance_running')
    waiter.wait(Instanceids=instance_ids)

def update_instance_type(instance_id, instance_type='m3.xlarge'):
    client = get_client()    
    return client.modify_instance_attribute(InstanceId=instance_id, Attribute='instance_type', Value=instance_type)

def create_tags(instance_ids=[], tags={}):
    ec2 = get_resource()
    return ec2.create_tags(Resources=instance_ids, Tags=[tags])
