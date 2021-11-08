import redis

REDIS_IP='localhost'
REDIS_PORT=6379

Redis_client = redis.Redis(host=REDIS_IP, port=REDIS_PORT)

Redis_client.acl_setuser("person1", enabled=True, nopass=False, passwords="+salam",
                           commands=["+HGETALL","+ACL"],categories=['+@hash'],
                           keys=["*"])

print(Redis_client.acl_users())


Redis_client_p1 = redis.Redis(host=REDIS_IP, port=REDIS_PORT,
                              username="person1",password="salam")

print(Redis_client_p1.acl_whoami())
print(Redis_client_p1.hgetall("c1"))