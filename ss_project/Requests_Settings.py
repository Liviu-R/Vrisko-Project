from requests import request
from bs4 import BeautifulSoup
import random as rnd
import time
from fp.fp import FreeProxy

#HTTP header used for custom requests
UserAgents=["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
   ]

proxies=[]

#Getting free proxies for freeproxy.world throught HTTP request and scrapping the IP from the HTML
def getting_proxies()->None:

    headers_in_proxies={"User-Agent":rnd.choice(UserAgents)}
    
    freeworld=request(url="https://www.freeproxy.world/?type=http&anonymity=4&country=&speed=300&port=&page=1",headers=headers_in_proxies,method="GET").text
  
    soup=BeautifulSoup(freeworld,"html.parser")
    layu=soup.find("table",class_="layui-table")
    td=layu.find("tbody")
    ips=td.find_all("td",class_="show-ip-div")
    for ip in ips:
        http="http://" + ip.text.replace("\n","") + ":" + ip.find_next_sibling().text.replace("\n","") 
        if http not in proxies: 
            proxies.append(http)
    
    

