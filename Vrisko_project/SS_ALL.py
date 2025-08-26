from requests import session,request
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import random as rnd
import pandas as pd 
import sys
import os
import Requests_Settings as set

#Class that is used to store information about sites and other information like headers, proxy servers, and file name
class scrapper:
    def __init__(self,file,region=None) -> None:
        self.headers={'User-Agent': None}
        self.proxies={"http": None,"https":None}
        self.fine_name = file

        self.regions=region
        self.regional_categories=[]

        self.comp_emails=[]
        self.comp_names=[]
        self.comp_stafero=[]
        self.comp_site=[]
        self.comp_location=[]
        self.comp_urls=[]
        
        self.pagination=[]
        self.categories=[]
        
    #Function that is getting all the categories from the main page and conconcatenate with the regions selected and stores it in the class scrapper in categories property
    def get_all_categories(self)->None:

        print("START GETTING ALL CATEGORIES")

        url="https://www.vrisko.gr/"

        while True:

            delay=rnd.randint(15,25)
            time.sleep(delay) 

            self.headers["User-Agent"]=rnd.choice(set.UserAgents)
            self.proxies["http"]=rnd.choice(set.proxies)
            print(self.proxies," AND ",self.headers)

            try:
                html_page=request(url=url,headers=self.headers,proxies=self.proxies,method="GET").text
            except:
                print(f"ERROR IN REQUESTS {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue
            

            soup=BeautifulSoup(html_page,"html.parser")

            if soup.find("div",id="captchaText"):
                print(f"ERROR IN CAPTCHA {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            if soup.find("title").text == "Access Denied":
                print(f"ERROR IN ACCESS DENIED {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            container_of_categories=soup.find("div",id="tagContainer")
            if container_of_categories == None:
                continue
            for categories in container_of_categories.find_all("a",href=True):
                    self.categories.append(categories["href"])
            
            break

        if self.regions:
            for r_categories in self.regions:
                for category in self.categories:
                    self.regional_categories.append(category+r_categories)

            self.categories.clear()
            self.categories.extend(self.regional_categories)
           
        

    #Creating the csv file with the file name we input in class scrapper and store it in the program location 
    def preparing_csv(self)->None:
        path=(sys.argv[0].replace("SS_ALL.exe",""))+ self.fine_name + ".csv"
        info_dict = {'HOMESITE':self.comp_urls, 'NAME':self.comp_names,'LOCATION':self.comp_location, 'MAIL':self.comp_emails,'PHONE':self.comp_stafero, 'SITE':self.comp_site} 
        df = pd.DataFrame(info_dict) 
        df.to_csv(path, index=False)

        print("FINISH")
            
            
    #Getting all the urls for each categories page in the pagination of the category with BeautifulSoup
    def get_pagination(self)->None:

        counter = 1
        index = 0
        pagination = len(self.categories)

        print("START GETTING PAGINATION")

        while True:
            if index == pagination:
                break

            delay=rnd.randint(15,25)
            time.sleep(delay) 

            if not self.pagination:
                self.pagination.append(self.categories[index])
            elif self.categories[index] not in self.pagination:
                self.pagination.append(self.categories[index])

            self.headers["User-Agent"]=rnd.choice(set.UserAgents)
            self.proxies["http"]=rnd.choice(set.proxies)
            print(self.proxies," AND ",self.headers)

            try:
                html_page=request(url=self.categories[index],headers=self.headers,proxies=self.proxies,method="GET").text
            except:
                print(f"ERROR IN REQUESTS {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            soup=BeautifulSoup(html_page,"html.parser")

            if soup.find("div",id="captchaText"):
                print(f"ERROR IN CAPTCHA {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            if soup.find("title").text == "Access Denied":
                print(f"ERROR IN ACCESS DENIED {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            pagerclass=soup.find(class_="pagerWrapper")
            if pagerclass == None:
                continue
        
            for ur in pagerclass.find_all("a",href=True):
                self.pagination.append(ur["href"])

            print(counter)
            index+=1
            counter+=1
        
        

    #Getting the urls of companies' pages in the pagination of the categories with BeautifulSoup
    def get_single_page_url(self)->None:

        counter = 1
        index = 0
        pagination = len(self.pagination)

        print("START GETTING SINGLE PAGE URLS")
        
        while True:
            if index == pagination:
                break
             
            delay=rnd.randint(15,25)
            time.sleep(delay) 

            self.headers["User-Agent"]=rnd.choice(set.UserAgents)
            self.proxies["http"]=rnd.choice(set.proxies)
            print(self.proxies," AND ",self.headers)

            try:
                html_page=request(url=self.pagination[index],headers=self.headers,proxies=self.proxies,method="GET").text
            except:
                print(f"ERROR IN REQUESTS {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            soup=BeautifulSoup(html_page,"html.parser")

            if soup.find("div",id="captchaText"):
                print(f"ERROR IN CAPTCHA {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            if soup.find("title").text == "Access Denied":
                print(f"ERROR IN ACCESS DENIED {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            advnameheader=soup.find(id="SearchResults")

            if advnameheader:
                advnameheader=advnameheader.find_all("h2",class_="CompanyName")
                for ur in advnameheader:
                    page_url_comp=ur.find("a",href=True)
                    self.comp_urls.append(page_url_comp["href"])
            else:
                continue
            
            print(counter)
            index+=1
            counter+=1
               

    #Getting the data from each company url that was specified by the employer with BeautifulSoup
    def get_information(self)->None:
        retry_counter=0
        counter=1
        index = 0
        pagination = len(self.comp_urls)

        print("START GETTING INFORMATION")
        
        while True:
            if index == pagination:
                break
            
            delay=rnd.randint(15,25)
            time.sleep(delay)

            self.headers["User-Agent"]=rnd.choice(set.UserAgents)
            self.proxies["http"]=rnd.choice(set.proxies)
            print(self.proxies," AND ",self.headers)

            try:
                html_page=request(url=self.comp_urls[index],headers=self.headers,proxies=self.proxies,method="GET").text
            except:
                print(f"ERROR IN REQUESTS {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            soup=BeautifulSoup(html_page,"html.parser")

            if soup.find("div",id="captchaText"):
                print(f"ERROR IN CAPTCHA {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            if soup.find("title").text == "Access Denied":
                print(f"ERROR IN ACCESSS DENIED {self.proxies}")
                set.proxies.remove(self.proxies["http"])
                if not set.proxies:
                    set.getting_proxies()
                continue

            record_middle=soup.find("section",class_="record_middle")
            if record_middle:
                class_name=record_middle.find("div",class_="companyName_class")
            elif retry_counter == 10:
                index+=1
                self.comp_names.append("none")
                self.comp_location.append("none") 
                self.comp_stafero.append("none")
                self.comp_site.append("none")
                self.comp_emails.append("none")
                retry_counter=0
                continue
            else:
                retry_counter+=1
                continue
            
            #1:GETTING THE COMPANY NAMES 
            try:
                self.comp_names.append(class_name.find("span").get_text())
            except:
                self.comp_names.append("none")
    
            #2:GETTING LOCATION
            try:
                self.comp_location.append(record_middle.find("label",id="AddressLbl").get_text().replace("Δες στον χάρτη","").strip())
            except:
                self.comp_location.append("none")   
            
            #3:GETTING STAFERO
            try:
                self.comp_stafero.append(record_middle.find("label",class_="rc_firstphone").get_text().strip())
            except:
                self.comp_stafero.append("none")

            #4:GETTING SITE
            try:
                label_site=record_middle.find("div",class_="details_list_content_class websiteMarker")
                site=label_site.find("a",class_="rc_Detaillink")
                self.comp_site.append(site["href"])
            except:
                self.comp_site.append("none")

            #5:GETTING EMAIL
            try:
                email_site=record_middle.find("label",id="EmailContLbl")
                email=email_site.find("a",class_="rc_Detaillink")
                self.comp_emails.append(email["href"].replace("mailTo:",""))
            except:
                self.comp_emails.append("none")

            print(counter)
            index+=1
            counter+=1
            
            
                
def main():
 
    fileName:str=input("ENTER FILE NAME: ")
    region_name:str=input("ENTER REGION WITH / AT THE END AND SPACE BETWEEN IF MULTYPLY REGIONS: ")
    
    if region_name:
        region_list:list=region_name.split()
        scrap:object=scrapper(file=fileName,region=region_list)
    else:
        scrap=scrapper(fileName)

    set.getting_proxies()

    scrap.get_all_categories()
    scrap.get_pagination()
    scrap.get_single_page_url()
    scrap.get_information()
    scrap.preparing_csv()

if __name__ == "__main__": 
    main()