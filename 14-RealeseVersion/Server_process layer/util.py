import  requests
from PyQt5.QtCore import QProcess
import cv2 as cv
import pickle
import json

def update_redis_alg(redis_cli,came_name,alg,exchange_name,active,lvl):
    current_json=redis_cli.hget(came_name,"alg")
    if current_json ==None:
        current_json ="{}"
    current_dict=json.loads(current_json)
    
    if active !=-1:
        current_dict[alg]=(exchange_name,active,lvl)
    else:
        if alg in current_dict:
            del current_dict[alg]
    updated_json=json.dumps(current_dict)
    redis_cli.hset(came_name,"alg",updated_json)
    
#=================================================================
#dummy class for developing , to test and debuge each function :)
#=================================================================
class a():
    def send_log(a,b):
        pass
self=a()
#==================================================================
#rabbit related function:
def get_active_exchange(user,passwd,host,port):    
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]
#=================
def call_rabbitmq_api_validation(host, port, user, passwd):
  url = f"http://{host}:1{port}/api/whoami"
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())

def check_binded_exchange(host, port, user, passwd,exchange_name):
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}/bindings/source"
    # your source code here
    # sending post request and saving response as response object
    r = requests.get(url = API_ENDPOINT ,auth=(user, passwd),)
    return [person['destination'] for person in r.json()]
    

def delete_exchange(host, port, user, passwd,exchange_name):
    API_ENDPOINT = f"http://{host}:1{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {'type':'fanout','if-unused':False}
    # sending post request and saving response as response object
    r = requests.delete(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        err=r.json()
        if err['error']=='Object Not Found':
            return True
        else:
            return False
    except:
        return True

def delete_queue(host, port, user, passwd,queue_name):
    API_ENDPOINT = f"http://{host}:1{port}/api/queues/%2f/{queue_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    
    # data to be sent to api
    pdata = {'if-unused':False,'if-empty':False}
    # sending post request and saving response as response object
    r = requests.delete(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        err=r.json()
        if err['error']=='Object Not Found':
            return True
        else:
            return False
    except:
        return True