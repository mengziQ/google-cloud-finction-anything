import os
import zipfile
import json
import bs4
import boto3
import re
from boto3.session import Session
import requests

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './machine-learning-04e9c583b5dd.json'

args = json.loads(input())

key = args.get('key')
sec  = args.get('secret')
region = args.get('region')
name = args.get('name')

imgs = ['"https://ja.gravatar.com/userimage/9847738/e0cfe4c445d28598ffc3d0a4fd235fa5.jpg?size=200"', \
  '"https://ja.gravatar.com/userimage/9847738/647f7900b8912b0669a1da2edc352b5e.jpg?size=200"',
  '"https://ja.gravatar.com/userimage/9847738/44b7b8d6b72f2dce6609be9e059c3920.jpg?size=200"']
html = '''
<head>
<title>EC2 Control</title>
<link rel="icon" href={img}/>
<link rel="apple-touch-icon" href={img}/>
</head>
<body>
<p>
{body}
</p>
</body>
'''

def ec2_stop():
  session = boto3.Session(
      aws_access_key_id=key,
      aws_secret_access_key=sec,
      region_name=region
  )  
 
  ec2 = session.resource('ec2', region_name=region)

  try:
    r = requests.get('http://www.ugtop.com/spill.shtml')
    r.encoding = r.apparent_encoding  
    soup = bs4.BeautifulSoup(r.text)
    ipaddr = soup.find('font', {'color':'blue', 'size':'+2'})
    ec2_info = session.client('ec2').describe_instances()
  except Exception as e:
    print(html.format(body='{}\n{}'.format(e,ipaddr.text)))

  logs = []

  for reserv in ec2_info["Reservations"]:
    instances = reserv.get('Instances')
    for instance in instances:
      if instance.get('Tags') is None:
        continue
      else:
        for tag in instance.get('Tags'): 
          if tag.get('Key') == 'Name':
            names = instance.get('Tags').pop().get('Value')
            instance_id = instance.get('InstanceId')
            # if re.search(r'^ml-', name) is not None:
            if name in names:
              response = session.client('ec2').stop_instances(
                InstanceIds=[
                  instance_id
                ] 
              )          

  print(html.format(body='shutted down ' + name,img=imgs[0]))

def ec2_start():
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
            names = instance.get('Tags').pop().get('Value')
            instance_id = instance.get('InstanceId')
            # if re.search(r'^ml-', name) is not None:
            if name in names:
              response = session.client('ec2').start_instances(
                InstanceIds=[
                  instance_id
                ]    
              )    

  print(html.format(body='started ' + name,img=imgs[1]))

if args.get('ops') == 'start':
  ec2_start()
elif args.get('ops') == 'stop':
  ec2_stop()
else:
  print('no operation specified.')
