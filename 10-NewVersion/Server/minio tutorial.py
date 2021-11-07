from minio import Minio
minioClient = Minio('localhost:9000', access_key='admin', secret_key='admin1234', secure=False)
buckets = minioClient.list_buckets()


# client.remove_bucket(buckets[1].name)

objects = minioClient.list_objects(buckets[1].name, 
                              recursive=True)

#for client applicatoin 
#reciceving data:
buckets = minioClient.list_buckets()

objects = minioClient.list_objects(buckets[1].name, 
                              recursive=True)

for obj in objects:
    print(obj.object_name)
    data = minioClient.get_object(obj.bucket_name, obj.object_name)
    with open('salam_'+obj.object_name, 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)

#for server application
#deleting data:
buckets = minioClient.list_buckets()

objects = minioClient.list_objects(buckets[1].name, 
                              recursive=True)
for obj in objects:
    print(obj.object_name)
    minioClient.remove_object(obj.bucket_name, obj.object_name)
    
minioClient.remove_bucket(buckets[1].name)

index=[ i for i,bname in enumerate(buckets) if bname.name=="jangal_c1"][0]
print(index)