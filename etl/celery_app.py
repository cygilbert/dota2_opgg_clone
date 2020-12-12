#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Init and config Celery app"""
from celery import Celery


celery = Celery()
celery.config_from_object('celeryconfig')
