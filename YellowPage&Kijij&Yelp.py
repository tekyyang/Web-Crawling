__author__ = 'yyb'

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from bs4 import BeautifulSoup



class Web_scraper:

    def __init__(self,keyword,location,location_code):
        self.keyword=keyword
        self.location=location
        self.location_code=location_code



#here is the start of yellow page
class Yellow_page(Web_scraper):

    def __init__(self,keyword,location,location_code):
        super().__init__(keyword,location,location_code)

        kw_length=len(self.keyword.split(' '))#the length of keyword

        if kw_length==1:
            self.url="https://www.yellowpages.ca/search/si/1/"+self.keyword+"/"+self.location_code
        elif kw_length==2:
            one,two=self.keyword.split(' ')
            self.url="https://www.yellowpages.ca/search/si/1/"+one+"%20"+two+"/"+self.location_code
        elif kw_length==3:
            one,two,three=self.keyword.split(' ')
            self.url="https://www.yellowpages.ca/search/si/1/"+one+"%20"+two+"%20"+three+"/"+self.location_code
        elif kw_length==4:
            one,two,three,four=self.keyword.split(' ')
            self.url="https://www.yellowpages.ca/search/si/1/"+one+"%20"+two+"%20"+three+"%20"+four+"/"+self.location_code
        else:
            print("input keyword is too long!")


    def load_pages(self):

        browser=webdriver.Firefox()
        browser.implicitly_wait(10)
        browser.get(self.url)
        time.sleep(5)

        finding_content=browser.find_element_by_class_name('contentControls-head_total') #there are overall 8 ways to get elements from web, like by id, name, xpath, css selector
        finding_text=finding_content.text #last step we find the element and we need to take the text of it

        finding_num=re.search(r'[\d,]+',finding_text) #get the number in the webpage
        scroll_num=int(re.sub(r',','',finding_num.group(0)))
        print('The total number of result of '+self.keyword+' in '+ self.location+' is: '+str(scroll_num))
        #print(int(finding_num.group(0)))

        load=browser.find_element_by_css_selector('body')
        for i in range(scroll_num):
            load.send_keys(Keys.PAGE_DOWN) #scroll to the downside of the page
            time.sleep(0.2)
        #Till now we finish rolling the pages

        self.html=browser.page_source
        self.soup=BeautifulSoup(self.html,"html.parser")
        #print(self.soup.prettify())
        self.soup=self.soup.find("div",{"class":"page__content jsListingMerchantCards jsListContainer"})

        browser.close()


    def get_info(self,save_file_path):

        #self.business_names_list=self.soup.findAll("div",{"class":"listing__title--wrap"})
        #self.business_names=[re.sub(r'Opening Hours »','',i.text).strip() for i in self.business_names_list]

        html_text=str(self.soup) #get the string of the content
        self.websites_list=re.findall(r'<link href="(.+)" itemprop="url"/>',html_text) #use re to match the string; before write it, print the content to see

        self.websites=['https://www.yellowpages.ca'+str(i) for i in self.websites_list]

        count=0

        for web in self.websites:
            page=requests.get(web)
            page=page.text
            #print(page)

            soup=BeautifulSoup(page,'html.parser')

            #self.business_name=re.search(r'<span class="merchant-title__name jsShowCTA"  itemprop="name" >(.+?)</span>',page).group(1)
            try:
                self.business_name = soup.find('h1', attrs={'class': 'merchantInfo-title merchant__title'}).getText()
            except:
                self.business_name = ''

            try:
                self.phone_um=re.search(r'<span class="mlr__sub-text" >(.+)</span><span class="mlr__label">',page).group(1)
            except:
                self.phone_um=''

            try:
                self.address=soup.find('div',attrs={'class':'merchant__item merchant__address'}).getText()
            except:
                self.address=''

            try:
                self.postcode=re.search(r'itemprop="postalCode" >(.+)</span>',page).group(1)
            except:self.postcode=''

            try:
                in_website=re.findall('href="/gourl\?(.+)" rel="nofollow" target="_blank"',page)
                in_website_tran=list(set(in_website))
                in_website_tran.sort(key=in_website.index) #list
                self.in_website=in_website_tran
            except:
                self.in_website=''

            try:
                self.services=re.search(r'<div class="hidden"  itemprop="magnet:YPproductservices"  content="(.+)" ></div>',page).group(1)
            except:
                self.services=''

            with open(save_file_path+self.keyword+'_yellow_page.txt','a') as file:

                row = str(self.business_name+'^'+self.phone_um.strip()+'^'+self.services+'^'+'Yellow Page'+'^'+self.location.strip()+'^'+self.address.strip()+'^'+self.postcode+'^'+str(self.in_website)+'\n')
                print(row)
                file.write(row)

            count+=1
            #print('Now we are processing the '+str(count)+' item of yellow page for '+self.keyword)


#here is the start of kijiji
class Kijiji(Web_scraper):

    def __init__(self,keyword,location,location_code):
        super().__init__(keyword,location,location_code)

        kw_length=len(self.keyword.split(' ')) #the length of keyword

        if kw_length==1:
            self.url="https://www.kijiji.ca/b-ontario/"+keyword+"/k0l9004?dc=true""/"+self.location
        elif kw_length==2:
            one,two=self.keyword.split(' ')
            self.url="https://www.kijiji.ca/b-ontario/"+one+"-"+two+"/"+"/k0l9004?dc=true""/"+self.location
        elif kw_length==3:
            one,two,three=self.keyword.split(' ')
            self.url="https://www.kijiji.ca/b-ontario/"+one+"-"+two+"-"+three+"/"+"/k0l9004?dc=true""/"+self.location
        elif kw_length==4:
            one,two,three,four=self.keyword.split(' ')
            self.url="https://www.kijiji.ca/b-ontario/"+one+"-"+two+"-"+three+"-"+four+"/"+"/k0l9004?dc=true""/"+self.location
        else:
            print("input keyword is too long!")

    def load_pages(self):

        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.browser.get(self.url)
        time.sleep(5)

        finding_content=self.browser.find_element_by_class_name('showing') #there are overall 8 ways to get elements from web, like by id, name, xpath, css selector
        finding_text=finding_content.text #last step we find the element and we need to take the text of it

        finding_num=re.search(r'of (.+) Ads',finding_text).group(1) #get the number in the webpage
        scroll_num=int(re.sub(r',','',finding_num))

        print('The total number of result of '+self.keyword+' is: '+str(scroll_num))
        #print(int(finding_num.group(0)))

        load=self.browser.find_element_by_css_selector('body')
        for i in range(scroll_num):
            load.send_keys(Keys.PAGE_DOWN) #scroll to the downside of the page
            time.sleep(0.2)
        #Till now we finish rolling the pages

        self.html=self.browser.page_source
        self.soup=BeautifulSoup(self.html,"html.parser")
        #print(self.soup.prettify())
        #self.soup=self.soup.find("div",{"class":"page__content jsListingMerchantCards"})


    def get_info(self,save_file_path):
        links=[]
        count=0

        #get the result links list
        try:
            content=self.soup.find_all('div',{'class':re.compile('.*regular-ad.*')})
            for i in content:
                i=re.search(r'data-vip-url="(.+)"',str(i))
                link='https://www.kijiji.ca'+i.group(1)
                links.append(link)
        except:
            content=self.soup.find_all('div',{'class':re.compile('.*search-item.*')})
            for i in content:
                i=re.search(r'data-vip-url="(.+)"',str(i))
                link='https://www.kijiji.ca'+i.group(1)
                links.append(link)

        #get content from each link
        for link in links:
            print(link)

            inner_browser=webdriver.Firefox()
            inner_browser.implicitly_wait(5)
            inner_browser.get(link)
            time.sleep(2)

            try:
                #click anywhere to continue
                somewhere=inner_browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div/div[5]')
                somewhere.click()
                time.sleep(2)

                #inner_page
                login_in=inner_browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/header/div[3]/div[1]/div/div[2]/div[2]/div[2]/a[2]')
                login_in.click()
                time.sleep(2)#click the login in

                #login_page
                user_name=inner_browser.find_element_by_xpath('//*[@id="LoginEmailOrNickname"]')
                user_name.send_keys('email_address')

                password=inner_browser.find_element_by_xpath('//*[@id="login-password"]')
                password.send_keys(('password'))

                login_in_botton=inner_browser.find_element_by_xpath('//*[@id="SignInButton"]')
                login_in_botton.click() #finish input info
                time.sleep(3)

                #show more button in the description
                try:
                    read_more_botten=inner_browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[6]/div[4]/button')
                    read_more_botten.click()
                except:
                    read_more_botten = inner_browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div/div[6]/div[4]/button')
                    read_more_botten.click()


                #telephone
                try:
                #inner_page_loaded
                    tele_button=inner_browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[6]/div[6]/div[2]/div/div/div/div[2]/div/button')
                    tele_button.click()
                    time.sleep(2)
                    telephone_load_page=inner_browser.page_source
                    #print(telephone_load_page)
                    tele=re.search(r'aria-label="Phone number: (\d+)"><',telephone_load_page).group(1)
                except:
                    tele=''


                loaded_soup=inner_browser.page_source
                inner_soup=BeautifulSoup(loaded_soup,'html.parser')

                #business name
                try:
                    business_name = inner_soup.find('h1', {'class': 'title-3283765216'}).getText()
                except:
                    business_name = ''

                #location
                try:
                    location=inner_soup.find_all('div',{'class':'locationContainer-203058252'})[0]
                    location_text=location.text
                    location=re.search(r'(.*)\(',location_text).group(1)
                    #print(location)
                except:
                    location=''

                #post_code
                try:
                    post_code=re.search(r'ON [A-Z1-9]{3} [A-Z1-9]{3}',location).group(1)
                except:
                    post_code=''

                #description
                try:
                    description=inner_soup.find_all('div',{'class':'showMoreChild-512293512'})[0]
                    description=re.sub(r'<.*?>|\n','',str(description))
                except:
                    description=''

                #email
                try:
                    email=re.search(r'([a-zA-Z]+@(.+?).com)',description).group(0)
                except:
                    email=''

                #website
                try:
                    website=re.search(r'(www.[a-zA-Z]+.com)',description).group(0)
                except:
                    website=''


                with open(save_file_path+self.keyword+'_Kijiji.txt','a') as file:

                    row = str(business_name)+str(tele).strip()+'^'+email.strip()+'^'+str(link.strip()+'^'+description+'^'+location+'^'+post_code+'^'+website)
                    print(row)
                    file.write(row)

                count+=1
                print('Now we are processing the '+str(count)+' item of Kijiji for '+self.keyword)
                #website


                inner_browser.close()
            except:
                inner_browser.close()



#here is the start of yelp
class Yelp(Web_scraper):

    def __init__(self,keyword,location,location_code):
        super().__init__(keyword,location,location_code)

        kw_length=len(self.keyword.split(' '))#the length of keyword

        if kw_length==1:
            self.url="https://www.yelp.ca/search?find_desc="+self.keyword+"&find_loc="+self.location+",+Ontario"
        elif kw_length==2:
            one,two=self.keyword.split(' ')
            self.url="https://www.yelp.ca/search?find_desc="+one+"+"+two+"&find_loc="+self.location+",+Ontario"
        elif kw_length==3:
            one,two,three=self.keyword.split(' ')
            self.url="https://www.yelp.ca/search?find_desc="+one+"+"+two+"+"+three+"&find_loc="+self.location+",+Ontario"
        elif kw_length==4:
            one,two,three,four=self.keyword.split(' ')
            self.url="https://www.yelp.ca/search?find_desc="+one+"+"+two+"+"+three+"+"+four+"&find_loc="+self.location+",+Ontario"
        else:
            print("input keyword is too long!")


    def get_pages(self):

        r = requests.get(self.url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        finding_position = soup.find('span', 'pagination-results-window').getText().strip()
        total_number = int(re.split(r' ', finding_position)[-1])
        pages=int(total_number/10)+1
        print('The total number of result of ' + self.keyword + ' in ' + self.location + ' is: ' + str(total_number))

        url_list=[]
        for i in range(1,pages+1):
            if i == 1:
                url_list.append(self.url)
            else:
                url_list.append(self.url+'='+str(10*i))

        href_list = []

        # each result page
        for url in url_list:

            page = requests.get(url)
            html_page = page.text
            soup_search_results=BeautifulSoup(html_page,'html.parser')
            soup_search_results=soup_search_results.find('div','search-results-content')
            soup_search_results=soup_search_results.find_all('a','biz-name js-analytics-click')
            print('------------')

            #each shop page
            for i in soup_search_results:
                href = re.search(r'href="(.*?)"><span>',str(i)).group(1)
                if len(href)<250:
                    link='https://www.yelp.ca'+href
                    href_list.append(link)

                    each_page=requests.get(link).text
                    inner_soup=BeautifulSoup(each_page,'html.parser')
                    try:
                        title=inner_soup.find('h1','biz-page-title embossed-text-white shortenough').text.strip()
                    except:
                        title=''

                    try:
                        address=inner_soup.find('div','map-box-address u-space-l4').text.strip()
                    except:
                        address=''

                    try:
                        tele=inner_soup.find('span','biz-phone').text.strip()
                    except:
                        tele=''

                    try:
                        web=inner_soup.find('span','biz-website js-biz-website js-add-url-tagging').text.strip()
                    except:
                        web=''

                    print(title,address,tele,web,self.location)




##Start crawling

city_list=[

['Toronto','Scarborough','North York','East York','Richmond Hill',
'Vaughan','Markham','Brampton','Mississauga','Etobicoke','Oakville',
'Pickering','Oshawa','Newmarket'],

['Toronto%2C%20ON','Scarborough%2C%20ON','North%20York%2C%20ON',
'East%20York%2C%20ON','Richmond%20Hill%2C%20ON','Vaughan%2C%20ON',
'Markham%2C%20ON','Brampton%2C%20ON','Mississauga%2C%20ON',
'Etobicoke%2C%20ON','Oakville%2C%20ON','Pickering%2C%20ON',
'Oshawa%2C%20ON','Newmarket%2C%20ON'],
]

for i in range(len(city_list[0])):
    spider1=Yellow_page('Computer Repair',city_list[0][i],city_list[1][i])
    spider1.load_pages()
    spider1.get_info('/Users/yyb/PycharmProjects/Twitter/Twitter_crawl/')



'''
spider_kijiji=Kijiji('swimming pool cleaning','ontario')
spider_kijiji.load_pages()
spider_kijiji.get_info('/Users/yyb/PycharmProjects/Twitter/Twitter_crawl/')
'''


