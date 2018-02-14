from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time


def refresh_token():
    browser=webdriver.Firefox()
    browser.implicitly_wait(2)

    browser.get('https://developers.facebook.com/tools/explorer/145634995501895/')
    time.sleep(2)

    browser.implicitly_wait(2)

    login_button=browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div/div[3]/a')
    login_button.click()

    username=browser.find_element_by_xpath('//*[@id="email"]')
    username.send_keys("3437777135")

    password=browser.find_element_by_xpath('//*[@id="pass"]')
    password.send_keys("yyb901027")

    login_button_inner=browser.find_element_by_xpath('//*[@id="loginbutton"]')
    login_button_inner.click()

    get_token=browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div[2]/div/div[2]/a/span[2]')
    get_token.click()

    get_user_access_token=browser.find_element_by_xpath('/html/body/div[10]/div/div/div/ul/li[1]/a/span/span/span')
    get_user_access_token.click()

    time.sleep(2)

    create_access_token=browser.find_element_by_xpath('/html/body/div[11]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div/button[1]')
    create_access_token.click()

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(2)

    token_content = soup.find_all('div', attrs={'class': '_5wpg _5wph'})[0]
    token_we_want = re.search(r'type="text" value="(.*)"/></label>',str(token_content)).group(1)

    return token_we_want
