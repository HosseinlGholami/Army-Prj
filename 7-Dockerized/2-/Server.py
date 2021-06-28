import docker

def get_buid_log(build_logs):
    for chunk in build_logs:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                print(line)

def Run_Broker(client,path,ports):
    #local_param
    IMAGE_VERSION_RBMQ="rbmq_army:v.0"
    CONTAINER_NAME_RBMQ="QUEUE_SERVER"
    #connect to docker daemon
    #HIGH level API for build IMAGES
    try:
        image=client.images.get(IMAGE_VERSION_RBMQ)
        print('the image has build before')
    except docker.errors.ImageNotFound:
        image, build_logs=client.images.build(path=path,
                                              tag=IMAGE_VERSION_RBMQ,quiet=False,
                                              nocache=True,rm=True)
        get_buid_log(build_logs)
    
    #HIGH level API for Run container
    try: 
        container=client.containers.get(CONTAINER_NAME_RBMQ)
        print('the container has runs before')
    except docker.errors.NotFound:
        container=client.containers.run(image,
                                        detach=True,
                                        name=CONTAINER_NAME_RBMQ,
                                        ports=ports
                                        )
        container.logs()
    return container

def create_Sender_Image(client,path,IMAGE_name):
    if IMAGE_name in client.images.list():
        client.images.remove(IMAGE_name)
    image, build_logs=client.images.build(path=path,
                                          tag=IMAGE_name,
                                          quiet=False,
                                          nocache=True,
                                          rm=True)
    get_buid_log(build_logs)
    return image
    

def Run_sender(client,image,CONTAINER_NAME,network):
    container_name = [x.name for x in client.containers.list()]
    if CONTAINER_NAME in container_name:
        container=client.containers.get(CONTAINER_NAME)
        container.stop()
        container.remove()
    container=client.containers.run(image,
                                    detach=True,
                                    name=CONTAINER_NAME,
                                    network=network
                                    )
    container.logs()
    return container
