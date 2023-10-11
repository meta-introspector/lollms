import docker

def inspect():
    client = docker.from_env()
    data = {}
    for container in client.containers.list():
        data[container.name] = dict(
            attrs = str(container.attrs),
            logs = str(container.logs())
            )
        return data
