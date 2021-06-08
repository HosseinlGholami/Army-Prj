
import requests,json

user='guest'
passwd='guest'
host='localhost'
port='15672'
  
exchange_name='hey1'

def create_exchange(user,passwd,host,port,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {"type":"direct"}
    
    # sending post request and saving response as response object
    r = requests.put(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        r.json()
        return False
    except :
        return True

def get_active_exchange(user,passwd,host,port):    
    a=list()
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]
    

x=create_exchange(user,passwd,host,port,exchange_name)

print(x)
print(get_active_exchange(user,passwd,host,port))
