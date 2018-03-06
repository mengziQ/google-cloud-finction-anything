import os
import zipfile
import json
import boto3
import re
from boto3.session import Session

ins = json.loads(input())

sec1, sec2 = ins.get('secret').split(',')

# apply, ml
for key, sec in [('Access Key1', sec1),('Access Key2', sec2)]: 
  for region in ['ap-northeast-1', 'us-east-1']:
    session = boto3.Session(
      aws_access_key_id=key,
      aws_secret_access_key=sec,
      region_name=region
    ) 
    ec2 = session.resource('ec2', region_name=region)

    ec2_info = session.client('ec2').describe_instances()
    logs = []

    for reserv in ec2_info["Reservations"]:
      instances = reserv.get('Instances')
      for instance in instances:
        if instance.get('Tags') is None:
          continue
        else:
          for tag in instance.get('Tags'): 
            if tag.get('Key') == 'Name':
              name = instance.get('Tags').pop().get('Value')
              instance_id = instance.get('InstanceId')
              if re.search(r'^ml-', name) is not None:
              #if 'ml-asano' in name:
                response = session.client('ec2').stop_instances(
                  InstanceIds=[
                    instance_id
                  ] 
                )        

print('OK!')
