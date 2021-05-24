
import requests,json

user='guest'
passwd='guest'
host='localhost'
port='15672'
  
exchange_name='hey'


https://funprojects.blog/2019/11/08/rabbitmq-rest-api/

url ='http://'+host+':'+'port'+'/api/exchanges/%2f/'+exchange_name
# r2 = requests.put(url,
#                   data ="{""type"":""direct"",""durable"":true}",
#                   auth=(user,passwd)
#                   )


# url = 'http://'+host+':'+port+'/api/exchanges'
# r = requests.get(url, auth=(user,passwd))

# if exchange_name in [x['name'] for x in r.json()]:
#     print('the exchange has exist change the exchange name')
# else:
#     print("salam")
    