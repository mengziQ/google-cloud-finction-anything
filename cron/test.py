
import os
import zipfile
import json
import boto3
import re

from boto3.session import Session
session = boto3.Session(
  aws_access_key_id='AKIAJIDXWU7BVEEVOVKQ',
  aws_secret_access_key='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',
  region_name='ap-northeast-1',
)
ec2 = session.resource('ec2', region_name='ap-northeast-1', api_version='2016-04-01')


