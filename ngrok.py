#help manage a ngrok connection
import requests
import subprocess
from time import sleep


class ngrok():
    #Execute NGROK from bash "ngrok http 5000"
    def __init__(self,protocol="http",port="5000"):
        bashCmd = ["ngrok",protocol,port]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    
    #Get NGROK urls from localhost api
    def get_ngrok_urls(self):
        self.urls = []
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'
        tunnels = requests.get(self.ngrok_console).json()['tunnels']
        for tunnel in tunnels:
            self.urls.append(tunnel['public_url'])
        return self.urls

#Simple test app
if __name__ == '__main__':
    print("Starting NGROK",end="",flush=True)
    n = ngrok()
    done = False
    #Wait for 2 urls http and https
    while not done:
        sleep(1)
        urls = n.get_ngrok_urls()
        if len(urls) == 2: 
            print(".Done!")
            done = True
        else:
            print(".",end="",flush=True)
    #Print URLs to screen
    for url in urls:
        print(url)