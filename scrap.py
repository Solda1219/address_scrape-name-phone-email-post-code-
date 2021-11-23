import pandas as pd
import requests
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import json

def listToString(s):    
    # initialize an empty string 
    str1 = ""     
    # traverse in the string  
    index = 0 
    for ele in s:
        if index != 0:
            str1 += "; "
        str1 += ele
        index +=1  
    # return string   
    return str1 
def saveInJson(data):
    print(data)
    toJson=[]
    toJson.append(data)
    f= open('address.json', 'w')
    f.write(json.dumps(toJson, indent= 2))
    f.close()
    print('Saved successfully!')
def getSoupWithout403(url):
    try:
        req= Request(url, headers= {'User-Agent': 'Mozilla/5.0'})
        webPage= urlopen(req).read()
        page_soup= BeautifulSoup(webPage, 'html.parser')
        return page_soup
    except:
        print('Such url does not exist')
class AddressScraper():
    def scrape(self):
        url= "https://www.idealista.com/alquiler-viviendas/madrid-madrid/"
        page_soup= getSoupWithout403(url)
        email= self.findEmail(page_soup)
        phone= self.findPhone(page_soup)
        postCode= self.findPostCode(page_soup)
        address= {}
        address['url']= url
        address['email']= email
        address['phone']= phone
        address['postCode']= postCode
        saveInJson(address)
    def findEmail(self, soup):
        res = ''
        EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        if soup != None:
            list = []
            for re_match in re.finditer(EMAIL_REGEX, soup.text):
                list.append(re_match.group())
            res = listToString(list)
        return res
    def findPhone(self, soup):
        try:
            phone = soup.select("a[href*=callto]")[0].text
            return phone
        except:
            pass
        try:
            phones = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', soup.text)
            phone= listToString(phones)
            if phone!='':
                return phone
        except:
            pass
        try:
            phones = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', soup.text)
            phone= listToString(phones)
            if phone!= '':
                return phone
        except:
            pass
        try:
            phones = re.findall(r'[+][0-9]{3}[ ]?[0-9]{7,9}', soup.text)
            phone= listToString(phones)
            if phone!= '':
                return phone
        except:
            print ('Phone number not found')
            phone = ''
            return phone
    def findPostCode(self, soup):
        try:
            postCodes = re.findall(r'[A-Z][A-Z][0-9][ ]?[0-9][A-Z][A-Z][ ][A-Z][A-Za-z]*[ ,]*[A-Z][A-Za-z]*[ ,]*[A-Za-z]*[ ,]*[A-Za-z]*[ ,]*[A-Za-z]*[ ,]*[A-Za-z]*[ ,]*[A-Za-z]*', soup.text)
            postCode= listToString(postCodes)
            if postCode!= '':
                return postCode
        except:
            pass
        try:
            postCodes = re.findall(r'[A-Z][A-Za-z]*[ ,]?[A-Za-z, ]*[A-Z][A-Z][0-9][ ,]*[0-9][A-Z][A-Z][ ,]*[A-Za-z]*', soup.text)
            postCode= listToString(postCodes)
            if postCode!= '':
                return postCode
        except:
            pass
        
        try:
            postCodes= re.findall(r'[0-9]{3,7}[-]?[0-9]*', soup.text)
            postCode= listToString(postCodes)
            if postCode!= '':
                return postCode
        except:
            print("postCode not find")
            return ' '
if __name__ == '__main__':
    scraper = AddressScraper()
    scraper.scrape()
