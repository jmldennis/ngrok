#help manage a ngrok connection
import requests

class Ngrok():
    def __init__(self):
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'
        

    def get_ngrok_urls(self):
        urls = []
        tunnels = requests.get(ngrok_console).json()['tunnels']
        for tunnel in tunnels:
            urls.append(tunnel['public_url'])
        return urls

if __name__ == '__main__':
    ngrok_urls = Ngrok().get_ngrok_urls()