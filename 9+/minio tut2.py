from minio import Minio
minioClient = Minio('localhost:9000', access_key='admin', secret_key='admin1234', secure=False)
buckets = minioClient.list_buckets()

INPUT_EXCHANGE_NAME = 'ex_c1'

# download file form minio so clean
# minio_buckets=[buckets.name.split('jangal_')[1] for buckets in minioClient.list_buckets()]
# if INPUT_EXCHANGE_NAME in minio_buckets:
#     bucket_index=minio_buckets.index(INPUT_EXCHANGE_NAME)
#     objects = minioClient.list_objects(buckets[bucket_index].name, 
#                                   recursive=True)
#     minio_objects=[obj.object_name for obj in objects]
#     if "ex_c1.face.txt" in minio_objects:
#         data = minioClient.get_object(buckets[bucket_index].name, "ex_c1.face.txt")
#         with open("ex_c1.face.txt", 'wb') as file_data:
#             for d in data.stream(32*1024):
#                 file_data.write(d)

#write file on minio
# minioClient.fput_object(
#     bucket_name=OUTPUT_BUCKET_NAME, object_name=TEST_DOC_NAME, file_path="./%s" % TEST_DOC_NAME
# )
minioClient.fput_object(
    bucket_name='jangal_'+INPUT_EXCHANGE_NAME , object_name="ex_c1.face.txt", file_path="./ex_c1.face.txt")    