import requests
from bs4 import BeautifulSoup
import re
import json

class Twitter_crawler():

    def __init__(self,keyword,save_path):
        self.keyword=keyword
        self.url="https://twitter.com/" + keyword + '?lang=en'
        self.path=save_path

    def get_pages(self):

        r = requests.get(self.url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        #Tweet number
        tweet_num_find = soup.find_all('a', attrs={'class': 'ProfileNav-stat ProfileNav-stat--link u-borderUserColor u-textCenter js-tooltip js-nav'})[0]
        tweet_num_find = tweet_num_find.find_all('span', attrs={'class': 'ProfileNav-value'})[0]
        self.tweet_num=tweet_num_find['data-count']

        #Tweet followers
        tweet_follower_find = soup.find_all('li', attrs={'class': 'ProfileNav-item ProfileNav-item--followers'})[0]
        tweet_follower_find = tweet_follower_find.find_all('span', attrs={'class': 'ProfileNav-value'})[0]
        self.tweet_follower=tweet_follower_find['data-count']

        #Tweet likes
        tweet_likes_find = soup.find_all('li', attrs={'class': 'ProfileNav-item ProfileNav-item--favorites'})[0]
        tweet_likes_find = tweet_likes_find.find_all('span', attrs={'class': 'ProfileNav-value'})[0]
        self.tweet_likes=tweet_likes_find['data-count']

    def save_as_json(self):
        data={}
        data['Twitter'] = []
        data['Twitter'].append({
            'user_name': self.keyword,
            'tweet_num': self.tweet_num,
            'tweet_followers': self.tweet_follower,
            'tweet_likes': self.tweet_likes
        })
        with open(self.path, 'a+') as outfile:
            json.dump(data, outfile)

    def main(self):
        self.get_pages()
        self.save_as_json()



class Instagram_crawler():

    def __init__(self,keyword,save_path):
        self.keyword=keyword
        self.url='https://www.instagram.com/' + keyword +'/'
        self.path=save_path

    def get_pages(self):
        r = requests.get(self.url)
        html = r.text
        self.ins_posts=re.search(r'Following, (.*) Posts - See Instagram', html).group(1)
        self.ins_follower=re.search(r'<meta content="(.+) Followers,', html).group(1)

    def change_number_format(self,number):
        #test if there is letters
        letter_count=0
        for i in number:
            if i.isalpha():
                letter_count+=1

        if letter_count>0:
            unit=number[-1]
            if unit=='m':
                mutiple_number=1000000
            else:
                mutiple_number=1000

            #test if there is a float with a dot
            try:
                float_num=number.split('.')
                first=float_num[0]
                last=float_num[-1]
                first=int(first)*mutiple_number
                last=int(last[:-1])*mutiple_number/10
                integrate_num=first+last
            except:
                ins_follower_int=int(number[:-1])
                integrate_num=ins_follower_int*mutiple_number
        else:
            integrate_num=int(number)
        return integrate_num

    def save_as_json(self,posts,follower):
        data = {}
        data['Instagram'] = []
        data['Instagram'].append({
            'user_name': self.keyword,
            'ins_num': posts,
            'ins_followers_num': follower,
        })
        with open(self.path, 'a+') as outfile:
            json.dump(data, outfile)

    def main(self):
        self.get_pages()
        ins_posts=self.change_number_format(self.ins_posts)
        followers=self.change_number_format(self.ins_follower)
        self.save_as_json(ins_posts,followers)



# example:
# twitter_name_list=['TajinUSA','lifehacker','corninggorilla','MotorolaUS','realDonaldTrump']
# twitter_path='/Users/yibingyang/Documents/data_store/twitter_data.json'
# for i in twitter_name_list:
#     Twitter_crawler(i,twitter_path).main()


# ins_name_list=['dimaaliev','muji_global','fashionnova']
# ins_path ='/Users/yibingyang/Documents/data_store/ins_data.json'
# for i in ins_name_list:
#      Instagram_crawler(i,ins_path).main()

#'dimaaliev'   #18.3k followers
#'muji_global' #1m followers
#'fashionnova' 35,460 posts 12m followers
