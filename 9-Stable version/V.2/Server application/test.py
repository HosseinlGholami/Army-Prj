#https://www.rabbitmq.com/amqp-0-9-1-reference.html
#http://localhost:15672/api/index.html
import requests ,json
host='localhost'
port=15672
user='guest'
passwd='guest'
exchange_name='c1'

def check_binded_exchange(host, port, user, passwd,exchange_name):
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}/bindings/source"
    # your source code here
    # sending post request and saving response as response object
    r = requests.get(url = API_ENDPOINT ,auth=(user, passwd),)
    return [person['destination'] for person in r.json()]
    

def delete_exchange(host, port, user, passwd,exchange_name):
    active_person=check_binded_exchange(host, port, user, passwd,exchange_name)
    if len(active_person)==0:
        API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
        # your source code here
        headers = {'content-type': 'application/json'}
        # data to be sent to api
        pdata = {'type':'fanout','if-unused':True}
        # sending post request and saving response as response object
        r = requests.delete(url = API_ENDPOINT ,auth=(user, passwd),
                          json = pdata,
                          headers=headers)
        try:
            r.json()
            return False
        except:
            return True
    else:
        return active_person
        
print(delete_exchange(host, port, user, passwd,exchange_name))
