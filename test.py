import json
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from threading import Thread
import requests
count = -1
total_proxies = []
live_proxies = []
if not os.path.exists(os.path.join(os.getcwd(),'output')):
    os.makedirs(os.path.join(os.getcwd(),'output'))

class checkProxy(Thread):
    def __init__(self,index = 0):
        super(checkProxy, self).__init__()


    def run(self):
        global count
        global live_proxies
        self.count = 0
        while True:
            global total_proxies
            if count > len(total_proxies) - 1: break
            count += 1
            self.count = count

            try:
                proxies = {
                    'http': total_proxies[self.count].strip('\n'),
                    'https': total_proxies[self.count].strip('\n')
                }
                response = requests.get('https://api.ipify.org?format=json', proxies=proxies, timeout=5)
                print(response.text)
                live_proxies.append(total_proxies[self.count].strip('\n'))
                print(f'{len(live_proxies)} Live / {len(total_proxies)}/{count} Total Proxies')
                if 'http' in total_proxies[self.count]:
                    open('output/http.txt', 'a', encoding='utf8').write(total_proxies[self.count].strip('\n')+'\n')
                elif 'socks4' in total_proxies[self.count]:
                    open('output/socks4.txt', 'a', encoding='utf8').write(total_proxies[self.count].strip('\n')+'\n')
                elif 'output/socks5' in total_proxies[self.count]:
                    open('socks5.txt', 'a', encoding='utf8').write(total_proxies[self.count].strip('\n')+'\n')
            except:
                pass

            with open('output/total_proxies.txt', 'w', encoding='utf8') as wf:
                for item in live_proxies:
                    wf.write(item+'\n')






if __name__ == '__main__':

    title = """
    __________        .__        __       ___ /\/\___ ___         .__  .__         __      __            .__       .__/\/\ ___    
    \______   \_______|__| _____/  |_    /  / )/)/   |   \   ____ |  | |  |   ____/  \    /  \___________|  |    __| _)/)/ \  \   
     |     ___/\_  __ \  |/    \   __\  /  /    /    ~    \_/ __ \|  | |  |  /  _ \   \/\/   /  _ \_  __ \  |   / __ |      \  \  
     |    |     |  | \/  |   |  \  |   (  (     \    Y    /\  ___/|  |_|  |_(  <_> )        (  <_> )  | \/  |__/ /_/ |       )  ) 
     |____|     |__|  |__|___|  /__|    \  \     \___|_  /  \___  >____/____/\____/ \__/\  / \____/|__|  |____/\____ |      /  /  
                              \/         \__\          \/       \/                       \/                         \/     /__/   
     Download and check proxies 
     
     
     Press Enter To Download Proxies Proxy And Check Live
     

    """

    print(title)

    proxy_type = ''
    config_proxies = open('config.json','r',encoding='utf8').read()
    config_proxies = json.loads(config_proxies)
    proxy_providers = config_proxies['proxy-providers']
    i = 0
    for proxy_provider in proxy_providers:
        i+=1
        type = proxy_provider['type']
        url = proxy_provider['url']
        response = requests.get(url,timeout=5)
        for proxy in response.text.splitlines():
            if type == 1:
                proxy_type = 'http://'
            elif type == 4:
                proxy_type = 'socks4://'
            elif type == 5:
                proxy_type = 'socks5://'
            total_proxies.append(proxy_type +proxy.strip('\n'))
        print(f'Download {len(total_proxies)} Proxies from {len(proxy_providers)} Providers / {i}')
    childThread = {}
    for i in range(0,1000):
        childThread[i] = checkProxy(index=i)
        childThread[i].start()


