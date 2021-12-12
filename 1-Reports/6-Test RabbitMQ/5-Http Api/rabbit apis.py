import  requests

RABBIT_PORT=15672
RABBIT_SERVER_IP='localhost'
RABBIT_SERVER_LOCAL_HOST='/'


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

    
a=delete_queue(RABBIT_SERVER_IP,RABBIT_PORT,"guest","guest","pr_ex_c1")

print(a)