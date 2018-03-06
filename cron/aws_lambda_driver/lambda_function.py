import requests
import os
SECRET = os.environ['SECRET']
def lambda_handler(event, context):
  res = requests.get('https://us-central1-machine-learning-173502.cloudfunctions.net/pycall_ec2_onoff?secret=' + SECRET)
  return res.status_code
