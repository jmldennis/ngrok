#help manage a ngrok connection
import requests
import subprocess
from time import sleep


class ngrok():
    def __init__(self,protocol="http",port="5000"):
        bashCmd = ["ngrok",protocol,port]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        
    def get_ngrok_urls(self):
        self.urls = []
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'
        tunnels = requests.get(self.ngrok_console).json()['tunnels']
        for tunnel in tunnels:
            self.urls.append(tunnel['public_url'])
        return self.urls

if __name__ == '__main__':
    print("Starting NGROK",end="",flush=True)
    n = ngrok()
    done = False
    while not done:
        sleep(1)
        urls = n.get_ngrok_urls()
        if len(urls) == 2: 
            print(".Done!")
            done = True
        else:
            print(".",end="",flush=True)
    for url in urls:
        print(url)