import redis
import json 

REDIS_IP='localhost'
REDIS_PORT=6379

def update_alg(redis_cli,came_name,alg,active,lvl):
    current_json=redis_cli.hget(came_name,"alg")
    if current_json ==None:
        current_json ="{}"
    current_dict=json.loads(current_json)
    if active !=-1:
        current_dict[alg]=(active,lvl)
    else:
        if alg in current_dict:
            del current_dict[alg]
    updated_json=json.dumps(current_dict)
    redis_cli.hset(came_name,"alg",updated_json)
    
Redis_client = redis.Redis(host=REDIS_IP, port=REDIS_PORT)


print(Redis_client.hgetall("DEF_MINIO"))

# update_alg(Redis_client,"c4","eye",-1,1)
# update_alg(Redis_client,"c4","face",-1,10)

# a=dict()
# a={"1":10,"2":9,"3":8}
# aa=json.dumps(a)
# Redis_client.hset("gholi","alg",aa)


# bb=Redis_client.hget("gholi","alg")

# b=json.loads(bb)

# print(b)
# print(type(b))

