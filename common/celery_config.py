# -*- coding: utf-8 -*-

"""
    Additional celery configuration.
"""

from airflow.config_templates.default_celery import DEFAULT_CELERY_CONFIG

CELERY_CONFIG = dict(DEFAULT_CELERY_CONFIG, **{
    "worker_max_tasks_per_child": 1000,
    "worker_poll_restarts": "True"
})