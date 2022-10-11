#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:05:37 2022

@author: liyan
"""
from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request
import requests



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import re


#Q1/1
seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
half_press='https://www.federalreserve.gov/newsevents/pressreleases/'
path='/Users/liyan/chromedriver'
driver = webdriver.Chrome(executable_path=path)

seen=[]##the urls of articles

page=1
maxVisit=200

#gain the list of urls of articles
try:
    driver.get(seed_url)
    while page<maxVisit:
        print(page)
        html=driver.page_source
        soup = BeautifulSoup(html,features="lxml")
        for tag in soup.find('div',attrs={'id':"article",'class':"col-xs-12 col-sm-8 col-md-8"}).find_all('a', href = True): 
            childUrl = tag['href'] #extract just the link
            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url, childUrl)
            #print("seed_url=" + seed_url)
           # print("original childurl=" + o_childurl)
           # print("childurl=" + childUrl)
           # print("half press url in childUrl=" + str(half_press in childUrl))
           # print("Have we seen this childUrl=" + str(childUrl in seen))
            rematch=re.findall('[0-9]{8}',childUrl)
            #print('This url is an article:'+str(len(rematch) ==1))
            if half_press in childUrl and childUrl not in seen and len(rematch) ==1:
                #print("***seen.append***")
                seen.append(childUrl)
            else:
                #print("######")
                nothing=0
        if page>8:
            next_page_button=driver.find_element(By.XPATH,'//*[@id="article"]/ul[1]/li[12]/a')##click next page
        else:
            next_page_button=driver.find_element(By.XPATH,'//*[@id="article"]/ul[1]/li[11]/a')
        next_page_button.click()
        wait = WebDriverWait(driver, 200)  
        page+=1
except:
    print('There is something wrong')
   
  
count=0
covid_urls=[]
for curr_url in seen:
        print(len(covid_urls))
        print(count)
        count+=1
        if len(covid_urls)<=10:
            try:
                print("Trying to access= "+curr_url)
                req = requests.get(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
                text=req.text
                if 'covid' in text.lower():
                    covid_urls.append(curr_url)
                else:
                    continue
        
            except Exception as ex:
                print("Unable to access= "+curr_url)
                print(ex)
                continue 
        else:
            break
print(covid_urls)
#Answer:
    #['https://www.federalreserve.gov/newsevents/pressreleases/monetary20220615a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/other20220523a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20220504a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/enforcement20220405a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/other20220225a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/bcreg20220214a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20220126a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/other20220114a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/other20211222a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20211215a.htm', 'https://www.federalreserve.gov/newsevents/pressreleases/other20211122b.htm']


#Q1/2
seed_url2='https://www.sec.gov/news/pressreleases'
path='/Users/liyan/chromedriver'
driver2 = webdriver.Chrome(executable_path=path)
seen2=[]
page_sec=1
maxVisit2=40

try:
    driver2.get(seed_url2)
    while page_sec<maxVisit2:
        print(page_sec)
        html2=driver2.page_source
        soup2 = BeautifulSoup(html2,features="lxml")
        for tag in soup2.find('table').find_all('a', href = True): 
            childUrl = tag['href'] #extract just the link
            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url2, childUrl)
            #print("seed_url=" + seed_url)
           # print("original childurl=" + o_childurl)
           # print("childurl=" + childUrl)
           # print("half press url in childUrl=" + str(half_press in childUrl))
           # print("Have we seen this childUrl=" + str(childUrl in seen))
            
            #print('This url is an article:'+str(len(rematch) ==1))
            if childUrl not in seen2:
                #print("***seen.append***")
                seen2.append(childUrl)
            else:
                #print("######")
                nothing=0
        next_page_button2=driver2.find_element(By.XPATH,'//*[@id="DataTables_Table_0_next"]')##click next page
        next_page_button2.click()
        wait = WebDriverWait(driver2, 200)  
        page_sec+=1
except:
    print('There is something wrong')


  
count2=0
charges_urls=[]

for curr_url in seen2:
        print(len(charges_urls))
        print(count2)
        count2+=1
        if len(charges_urls)<=19:
            try:
                print("Trying to access= "+curr_url)
                req = requests.get(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
                text=req.text
                if 'charges' in text.lower():
                    charges_urls.append(curr_url)
                else:
                    continue
        
            except Exception as ex:
                print("Unable to access= "+curr_url)
                print(ex)
                continue 
        else:
            break
print(charges_urls)

countf=1
for url in charges_urls:

    print('Url'+str(countf)+':',url)
    request = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(webpage)
    title=soup.find_all('h1',{'class':'article-title'})
    if len(title)==1:
        t=title[0].text
        print('Title'+str(countf)+':',t)
    else:
        continue
    textwords=soup.find_all('div',{'class':'article-body'})
    wholetext=''
    for p in textwords:
        wholetext=wholetext+p.text
    print('Text'+str(countf)+':')
    print(wholetext)
    countf+=1