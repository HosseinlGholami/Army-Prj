import docker
import json

#Utils file
IMAGE_VERSION='sa:v.0'
CONTAINER_NAME="SERVER_APP"
PORT={5000:8080}
def get_buid_log(build_logs):
    for chunk in build_logs:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                print(line)


#connect to docker daemon
client = docker.from_env()

client.networks.create("network1", driver="bridge")

#HIGH level API for build IMAGES
try:
    image=client.images.get(IMAGE_VERSION)
    print('the image has build before')
except docker.errors.ImageNotFound:
    image, build_logs=client.images.build(path='./',tag=IMAGE_VERSION,quiet=False)#,nocache=True,rm=True)
    get_buid_log(build_logs)

print(f"show the image id{image.id}")

#HIGH level API for Run container
try: 
    container=client.containers.get(CONTAINER_NAME)
except docker.errors.ImageNotFound:
    container=client.containers.run(image,
                                    detach=True,
                                    name=CONTAINER_NAME,
                                    port=PORT
                                    )
    container.logs()
