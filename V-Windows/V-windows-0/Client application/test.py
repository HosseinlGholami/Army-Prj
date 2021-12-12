def get_server_param():
    with open('Server.inf') as reader:
        return {x.split('=')[0]:x.split('=')[1] for x in reader.read().split('\n')}
    