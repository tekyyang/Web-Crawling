import requests
from bs4 import BeautifulSoup
import re



class Twitter_crawler():

    def __init__(self,twitter_url):
        self.url=twitter_url

    def clean_the_path(self):
        self.path=re.search(r'https?://[w]*.?twitter.com/[a-zA-Z0-9_-]*', self.url).group(0)
        self.user_name=re.search(r'https?://[w]*.?twitter.com/([a-zA-Z0-9_-]*)', self.path).group(1)
        #print(self.path)

    def get_pages(self):

        r = requests.get(self.path)
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

    def generate_json(self):
        data={}
        data['Twitter'] = []
        data['Twitter'].append({
            'user_name': self.user_name,
            'tweet_num': self.tweet_num,
            'tweet_followers': self.tweet_follower,
            'tweet_likes': self.tweet_likes
        })
        print(data)
        return data

    def main(self):
        self.clean_the_path()
        try:
            self.get_pages()
            self.generate_json()
        except:
            pass




class Instagram_crawler():

    def __init__(self,url):
        self.url=url

    def clean_the_path(self):
        self.path = re.search(r'https?://[w]*.?instagram.com/[a-zA-Z0-9_-]*', self.url).group(0)
        self.user_name = re.search(r'https?://[w]*.?instagram.com/([a-zA-Z0-9_-]*)', self.path).group(1)

    def get_pages(self):

        r = requests.get(self.path)
        html = r.text
        self.ins_posts=re.search(r'Following, (.*) Posts - See Instagram', html).group(1)
        self.ins_follower=re.search(r'<meta content="(.+) Followers,', html).group(1)

    def generate_json(self):
        data = {}
        data['Instagram'] = []
        data['Instagram'].append({
            'user_name': self.user_name,
            'ins_num': self.ins_posts,
            'ins_followers_num': self.ins_follower,
        })
        return data

    def main(self):
        self.clean_the_path()
        self.get_pages()
        self.generate_json()


        
#----Test Twitter----##    
# path_list=[
# 'https://www.twitter.com/coindesk',
# 'http://www.twitter.com/coindesk',
# 'http://twitter.com/coindesk',
# 'https://twitter.com/kyledcheney/status/1007317351031861248',
# 'https://twitter.com/WKYT/lists/wkytweather',
# 'https://twitter.com/ArkSurgical',
# 'https://www.twitter.com/spinehealth',
# 'https://twitter.com/NASpine'
# ]
#
# for i in path_list:
#     Twitter_crawler(i).main()


#----Test Instagram----##    
# path_list=[
# 'https://www.instagram.com/upworkinc/upworkinc/',
# 'http://www.instagram.com/upworkinc/',
# 'http://instagram.com/upworkinc/',
# 'http://instagram.com/indystar/'
# ]

# for i in path_list:
#     Instagram_crawler(i).main()
