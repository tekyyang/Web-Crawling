__author__ = 'yyb'

import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def follower_crawl(usernames):

    follower_dic={'info':[]}
    follower_len=len(usernames)
    success_num=0
    fail_num=0

    for username in usernames:
        username=str(username)
        browser=webdriver.Firefox()
        browser.implicitly_wait(10)
        try:
            #url="https://twitter.com/CU_FASS/followers"
            browser.get("https://twitter.com/"+username+"/followers")
            time.sleep(5)

            name=browser.find_element_by_css_selector('input.js-initial-focus')#div.LoginForm-input LoginForm-username #input.js-signin-email
            name.send_keys("telephone")

            password=browser.find_element_by_css_selector('input.js-password-field')
            password.send_keys("password")

            time.sleep(2)
            login_button=browser.find_element_by_xpath("//button[@type='submit']")#this place use xpath
            login_button.click()

            parameter_list=browser.find_elements_by_xpath("//span[@class='ProfileNav-value']")

            follower_num=parameter_list[2].text
            try:
                scroll_num=int(int(follower_num)/2+2)
                #lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                #print(lenOfPage)
            except:
                follower_num=re.sub(r',','',follower_num)
                scroll_num=int(float(follower_num)/2+2)

            load=browser.find_element_by_css_selector('body')#text-input email-input js-signin-email
            for i in range(scroll_num):
                load.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)

            follower_list_for_one_user=[]

            scrnames=browser.find_elements_by_css_selector('span.ProfileCard-screenname')#b.u-linkComplex-target
            for scrname in scrnames:#get followers for each username
                a=scrname.text
                a=a[1:]
                a=a.split(" ")[0]
                follower_list_for_one_user.append(a)

            follower_dic['info'].append({username:follower_list_for_one_user})
            browser.close()
            success_num+=1
        except:
            print(username+' follower failed!')
            browser.close()
            fail_num+=1
            continue
        print('this is the '+str(success_num+fail_num)+' user finished, since now success '+str(success_num)+', fail '+str(fail_num)+' total '+str(follower_len)+' users!')

        #save each result to file
        with open("/Users/yyb/Documents/python_crawl/"+str(username)+".json",'a') as f:
            json.dump(follower_dic,f)
            print('input successfully')

def following_crawl(usernames):

    following_dic={'info':[]}
    following_len=len(usernames)
    success_num=0
    fail_num=0

    for username in usernames:
        username=str(username)
        browser=webdriver.Firefox()
        browser.implicitly_wait(10)
        try:
            url="https://twitter.com/"+username+"/following"
            browser.get(url)
            time.sleep(5)

            name=browser.find_element_by_css_selector('input.js-initial-focus')#div.LoginForm-input LoginForm-username #input.js-signin-email
            name.send_keys("your phone number")

            password=browser.find_element_by_css_selector('input.js-password-field')
            password.send_keys("your password")

            time.sleep(2)
            login_button=browser.find_element_by_xpath("//button[@type='submit']")#this place use xpath
            login_button.click()

            parameter_list=browser.find_elements_by_xpath("//span[@class='ProfileNav-value']")
            following_num=parameter_list[1].text
            scroll_num=int(int(following_num)/2+2)

            #lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            #print(lenOfPage)

            load=browser.find_element_by_css_selector('body')#text-input email-input js-signin-email
            for i in range(scroll_num):
                load.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)

            following_list_for_one_user=[]

            scrnames=browser.find_elements_by_css_selector('span.ProfileCard-screenname')#b.u-linkComplex-target
            for scrname in scrnames:#get followers for each username
                a=scrname.text
                a=a[1:]
                a=a.split(" ")[0]
                following_list_for_one_user.append(a)

            following_dic['info'].append({username:following_list_for_one_user})
            browser.close()
            success_num+=1
        except:
            print(str(username)+' following failed!')
            fail_num+=1
            continue
        print('this is the '+str(success_num+fail_num)+' user finished, since now success '+str(success_num)+', fail '+str(fail_num)+' total '+str(following_len)+' users!')

        #save each user to file
        with open("/Users/yyb/Documents/python_crawl/"+username+".json",'a') as f:
            json.dump(following_dic,f)
            print('input successfully')


#follower_crawl("https://twitter.com/musicinthedarky/followers")
#following_crawl("https://twitter.com/musicinthedarky/following")


def main():
    hcr = pd.read_csv('/Users/yyb/Documents/LPtest/updown/data/hcr/train/orig/hcr-train.csv', sep=',',error_bad_lines=False)
    hcr=hcr[(hcr['sentiment']=='positive')|(hcr['sentiment']=='negative')]
    hcr=hcr.reset_index(drop=True)
    users = hcr['username']
    users = users.values

    filelist=os.listdir("/Users/yyb/Documents/python_crawl/")
    existing_names=[]
    for filename in filelist:
        name=filename.split('.')[0]
        if  name!='':
            existing_names.append(name)

    name_waiting_list=[]
    for i in users:
        if i in existing_names:
            pass
        else:
            name_waiting_list.append(i)

    follower_crawl(name_waiting_list)
    #following_crawl(users)

main()

