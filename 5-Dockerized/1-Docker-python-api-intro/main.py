import docker


#Utils file
IMAGE_VERSION='sa:v.0'
CONTAINER_NAME="SERVER_APP"
PORT={5000:6000}
def get_buid_log(build_logs):
    for chunk in build_logs:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                print(line)


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