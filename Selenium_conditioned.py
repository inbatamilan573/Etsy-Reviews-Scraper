# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:19:19 2023

@author: Inbatamilan
"""
import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import re


def is_v4_present():
    v_4_xpath1 = '//*[@id="same-listing-reviews-panel"]/div'
    v_4_xpath2 = '//*[@id="reviews"]/div[2]/div[2]'
    
    if browser.find_elements(By.XPATH, v_4_xpath1):
        return browser.find_element(By.XPATH, v_4_xpath1)
    else:
        return browser.find_element(By.XPATH, v_4_xpath2)
    

def review_scrapping(list_review):
    
    pattern = r'(.+) (\d+ [A-Za-z]+, \d+)'
    pattern_two = r'\bPurchased item\b'
    
    if len(list_review) == 8:
        r=0
        u=1
        print("_____________________Length__________________________")
        print(len(list_review))
        print("_____________________Samples__________________________")
        print("0 :",list_review[0].text.strip())
        print("1 :",list_review[1].text.strip())
        print("2 :",list_review[2].text.strip())
        print("3 :",list_review[3].text.strip())
        print("4 :",list_review[4].text.strip())
        print("5 :",list_review[5].text.strip())
        print("6 :",list_review[6 ].text.strip())
        print("________________________________________________")
        
        while r<len(list_review):

            if re.match(pattern,list_review[r].text.strip()):
                r=r+2
                u=u+2 
                continue
            elif re.match(pattern_two,list_review[r].text.strip()):
                r=r+2
                u=u+2
                continue
            else:
                review_list.append(list_review[r].text.strip())
            
            if re.match(pattern,list_review[r].text.strip()):
                user_date=list_review[r].text.strip()
                
            else:
                user_date=list_review[u].text.strip()
                
            match = re.match(pattern,user_date)
            name=''
            lastname=''
            d=''
            
            if match:
                name = match.group(1)
                d=match.group(2)
                
            user_list.append(name)
            date_list.append(d)
            
            r=r+2
            u=u+2
    
    if len(list_review) == 12:
        r=0
        u=2
        print("___________________Length____________________________")
        print(len(list_review))
        print("____________________Samples___________________________")
        print("0 :",list_review[0].text.strip())
        print("1 :",list_review[1].text.strip())
        print("2 :",list_review[2].text.strip())
        print("3 :",list_review[3].text.strip())
        print("4 :",list_review[4].text.strip())
        print("5 :",list_review[5].text.strip())
        print("6 :",list_review[6 ].text.strip())
        print("________________________________________________")
        
        while r<len(list_review):

            if re.match(pattern,list_review[r].text.strip()):
                r=r+3
                u=u+3 
                continue
            elif re.match(pattern_two,list_review[r].text.strip()):
                r=r+3
                u=u+3
                continue
            else:
                review_list.append(list_review[r].text.strip())
            
            if re.match(pattern,list_review[r].text.strip()):
                user_date=list_review[r].text.strip()
                
            else:
                user_date=list_review[u].text.strip()
                
            match = re.match(pattern,user_date)
            name=''
            lastname=''
            d=''
            
            if match:
                name = match.group(1)
                d=match.group(2)
                
            user_list.append(name)
            date_list.append(d)
            
            r=r+3
            u=u+3
            
    return True

def page_wise_list(crt): 
    
    print("____________________Total Product In That Page____________________________")
    print(len(crt))
    
    for i in range(len(crt)):
        i=i+1
        #selecting the product One by one
        values=f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[7]/div/div/div/ol/li[{i}]/div/div/a'
        link_data=browser.find_element(By.XPATH,values)
        browser.get(link_data.get_attribute('href'))
        print("____________________URL____________________________")
        print(browser.current_url)
        print("________________________________________________")

        try:
            #checking the valid Xpath in the product page
            crt_ano_ = is_v4_present()
            if crt_ano_:
                list_review = crt_ano_.find_elements(By.TAG_NAME, 'p')
                #Scrapping the review in the product page
                review_scrapping(list_review)
                browser.back()
        except selenium.common.exceptions.NoSuchElementException:
            browser.back()
        

review_list=[]
user_list=[]
date_list=[]

#Review Scrapping from page 1 to 252
for i in range(1,252):
          #https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page=252
    url=f'https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page={i}'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    browser=webdriver.Chrome(options=chrome_options)
    #browser.add_argument("--incognito")
    browser.get(url)
    #values selecting the correct list product
    values='//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[7]/div/div/div/ol/li'
    crt=browser.find_elements(By.XPATH,values)
    print("_________________Page Navigation_______________________________") 
    print("page_navigation_no:",i)
    page_wise_list(crt)

    

    
print("___________________Review_List_____________________________")  
print(review_list)
print("____________________User_List__________________________")
print(user_list)
print("__________________Date_List______________________________")
print(date_list)
print("________________________________________________")

import pandas as pd
df = pd.DataFrame(list(zip(date_list,user_list,review_list)), columns = ['Date', 'Users','Reviews'])
df.to_csv('Reviews',index=False)
