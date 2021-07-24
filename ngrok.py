#help manage a ngrok connection
import requests
import subprocess
from time import sleep


class ngrok():
    #Execute NGROK from bash "ngrok http 5000"
    def __init__(self,protocol="http",port="5000"):
        bashCmd = ["ngrok",protocol,port]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        self.first_run = True
    
    #Get NGROK urls from localhost api
    def get_ngrok_urls(self):
        self.urls = []
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'
        print("Getting tunnels urls",end="",flush=True)
        done = False
        
        #Wait for 2 urls http and https if running immediately
        while not done:
            try:
                tunnels = requests.get(self.ngrok_console).json()['tunnels']
                for tunnel in tunnels:
                    self.urls.append(tunnel['public_url'])
                if len(self.urls) >= 2: 
                    print(".Done!")
                    done = True
                else:
                    print(".",end="",flush=True)
                    sleep(1)
            except Exception:
                sleep(1)
            
        return self.urls

#Simple test app
if __name__ == '__main__':
    print("Starting NGROK")
    n = ngrok()
    urls = n.get_ngrok_urls()
       
    #Print URLs to screen
    for url in urls:
        print(url)