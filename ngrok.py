#help manage a ngrok connection
import requests
import subprocess
from time import sleep


class ngrok():
    #Execute NGROK from bash "ngrok http 5000"
    def __init__(self,protocol="http",port="5000"):
        self.protocol = protocol
        self.port = port
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'

    def start_ngrok(self):
        bashCmd = ["ngrok",self.protocol,self.port]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    
    #Get NGROK urls from localhost api
    def get_ngrok_urls(self):
        self.urls = []
        print("Getting tunnel urls",end="",flush=True)
        done = False
        
        #Wait for 2 urls http and https if running immediately after starting ngrok
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

    def kill_ngrok(self):
        #Issuing this command 
        #kill $(ps | grep '[n]grok http 5000' | awk '{print $1}')
        bashCmd = f"kill $(ps | grep '[n]grok {self.protocol} {self.port}' | awk "+"'{print $1}')"
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE, shell=True)
      
        print("Kill NGROK",end="",flush=True)
        done = False

        #Get Tunnel URL's until it fails, then NGROK is really dead
        while not done:
            try:
                tunnels = requests.get(self.ngrok_console).json()['tunnels']
                print(".",end="",flush=True)
                sleep(1)
            except Exception:
                print(".Done!")
                done = True

#Simple test app
if __name__ == '__main__':
    print("Starting NGROK")
    n = ngrok()
    n.start_ngrok()
    urls = n.get_ngrok_urls()

    #Print URLs to screen
    for url in urls:
        print(url)