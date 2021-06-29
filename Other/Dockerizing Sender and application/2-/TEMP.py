import  docker

#connect to docker daemon
client = docker.from_env()

if IMAGE_VERSION in client.images.list():
    client.images.remove(IMAGE_VERSION)
image, build_logs=client.images.build(path='./',
                                      tag=IMAGE_VERSION,
                                      quiet=False,
                                      nocache=True,
                                      rm=True)
get_buid_log(build_logs)


container_name = [x.name for x in client.containers.list()]
if CONTAINER_NAME in container_name:
    container=client.containers.get(CONTAINER_NAME)
    container.stop()
    container.remove()
container=client.containers.run(image,
                                detach=True,
                                name=CONTAINER_NAME,
                                ports=PORT
                                )
container.logs()