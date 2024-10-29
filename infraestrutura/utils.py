import requests

class DockerMonitor:
    ENDPOINT = ''
    HOSTS = {
        'VMDocker': {
            'host': '10.235.30.8',
            'port': '2376',
            'protocol': 'http'
        }
    }

    def __init__(self, params):
        self.host = params.get('host')
        self.port = params.get('port')
        self.protocol = params.get('protocol')
    
    def get_endpoint(self):
        return '{}://{}:{}/{}'.format(
            self.protocol,
            self.host,
            self.port,
            self.ENDPOINT
        )
    
    def list(self):
        url = self.get_endpoint()
        url = '{}/json'.format(url)
        return requests.get(url, params={'filters':'{\"status\":[\"created\",\"restarting\",\"running\",\"removing\",\"paused\",\"exited\",\"dead\"]}'})
    
    def get(self, id):
        url = self.get_endpoint()
        url = '{}/{}/json'.format(url,id)
        return requests.get(url)
    
    def delete(self, id):
        url = self.get_endpoint()
        url = '{}/{}'.format(url,id)
        return requests.delete(url)


class DockerImages(DockerMonitor):

    def __init__(self, params):
        super().__init__(params)
        self.ENDPOINT = 'images'


class DockerContainers(DockerMonitor):

    def __init__(self, params):
        super().__init__(params)
        self.ENDPOINT = 'containers'
    
    def start(self, id):
        url = self.get_endpoint()
        url = '{}/{}/start'.format(url,id)
        return requests.post(url)
    
    def stop(self, id):
        url = self.get_endpoint()
        url = '{}/{}/stop'.format(url,id)
        return requests.post(url)

