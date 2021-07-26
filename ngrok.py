#help manage a ngrok connection
import requests
import subprocess
from time import sleep


class ngrok():
    #Execute NGROK from bash "ngrok http 5000"
    def __init__(self,protocol="http",port="5000",region="us"):
        self.protocol = protocol
        self.port = port
        self.region = region
        self.ngrok_console = 'http://127.0.0.1:4040/api/tunnels'
        self.url = {}

    def start_ngrok(self):
        bashCmd = ["ngrok",self.protocol,self.port,"--region="+self.region]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    
    #Get NGROK urls from localhost api
    #url is a dictionary with the urls assigned by type ex. http or https
    #urls is a list of urls
    def get_ngrok_urls(self):
        print("Getting tunnel urls",end="",flush=True)
        done = False
        
        #Wait for 2 urls http and https if running immediately after starting ngrok
        while not done:
            try:
                self.urls = []
                tunnels = requests.get(self.ngrok_console).json()['tunnels']
                for tunnel in tunnels:
                    self.urls.append(tunnel['public_url'])
                if len(self.urls) == 2: 
                    print(".Done!")
                    done = True
                else:
                    print(".",end="",flush=True)
                    sleep(1)
            except Exception:
                sleep(1)

        for item in self.urls:
            if "https" in item:
                self.url["https"] = item
            elif "http" in item:
                self.url["http"] = item
            
        return self.urls

    def kill_ngrok(self):
        #Issuing this command 
        #kill $(ps aux | grep '[n]grok http 5000' | awk '{print $2}')
        bashCmd = "kill $(ps aux | grep '[n]grok "+self.protocol+ " "+str(self.port)+"' | awk "+"'{print $2}')"
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
    print(n.url["https"])
    print(n.url["http"])

    sleep(5)
    n.kill_ngrok()
    sleep(5)
    n.start_ngrok()
    urls = n.get_ngrok_urls()

    #Print URLs to screen
    for url in urls:
        print(url)
    sleep(5)
    n.kill_ngrok()