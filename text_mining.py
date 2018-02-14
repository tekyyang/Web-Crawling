__author__ = 'yyb'

import re
from nltk import bigrams #pay attention to the 's' of bigrams
from nltk.tokenize import RegexpTokenizer
import json
import pandas as pd
import numpy as np


# labeled features extraction
class get_nodes_from_existing_resource():

    def __init__(self):
        pass

    def get_lexicon_nodes(self):
        with open("/Users/yyb/PycharmProjects/Twitter/data/lexicon/new_lexicon.txt",'r') as f:
            word_lexicon=[]
            score_lexicon=[]

            for line in f.readlines():
                word=re.search(r"word1=[\w]+", line).group(0)
                word=re.split(r'word1=',word)[1]

                polarity=re.search(r"mpqapolarity=[\w]+", line).group(0)
                polarity=re.split(r'=',polarity)[1]

                word_lexicon.append(word) #a list of word
                score_lexicon.append(polarity) #a list of polarity #weakpos #weakneg #strongneg #strongpos

            score_num_lexicon=[]
            for i in score_lexicon:
                if i=='weakpos':
                    score_num_lexicon.append(0.8)
                elif i=='weakneg':
                    score_num_lexicon.append(-0.8)
                elif i=='strongneg':
                    score_num_lexicon.append(-0.9)
                elif i=='strongpos':
                    score_num_lexicon.append(0.9)
                else:
                    score_num_lexicon.append(0)
            return word_lexicon,score_num_lexicon


    def get_emoticon_nodes(self): #output the emoticon list
        posi_emoticon=[':)',':D','=D','=)',':]','=]',':-)',':-D',':-]',';)',';D',';-)',';-D',';-]']
        nega_emoticon=[':(','=(',':[','=[',':-(',':-[',':\'(',':\'[','D:']
        posi=[]
        for i in posi_emoticon:
            posi.append(0.9)
        nega=[]
        for i in nega_emoticon:
            nega.append(-0.9)
        emoticon_list=posi_emoticon+nega_emoticon
        emo_score=posi+nega

        return emoticon_list,emo_score


#unlabeled features extraction
class get_nodes_from_tweets():
    def __init__(self,file_type,data_path):
        self.file_type=file_type
        self.data_path=data_path

    def read_csv(self):
        hcr = pd.read_csv(self.data_path,sep=',',error_bad_lines=False)
        hcr=hcr[(hcr['sentiment']=='positive')|(hcr['sentiment']=='negative')]#get only pos/neg label data
        hcr=hcr.reset_index(drop=True) #reindex the table

        dataset = hcr['content'].values.tolist() #get tweets
        users = hcr['username'] #get usernames
        original_polarity=hcr['sentiment'].values.tolist()

        return dataset,users,original_polarity

    def read_json(self):
        content=[]
        with open('/Users/yyb/PycharmProjects/Twitter/data/dataset/tweets_iphonex.json', 'r') as f:
            lines = f.readlines()
            for line in lines:
                tweet = json.loads(line) # load it as Python dict
                try:
                    tweet=tweet['text']
                    content.append(tweet)
                except:
                    continue

        return content

    def get_features(self):
    # input a list of sentence to be processed
        if self.file_type=='csv':
            dataset=self.read_csv()[0]
        else:
            dataset=self.read_json()

        tokenizer = RegexpTokenizer(r"[#@A-Za-z0-9']+")
        hashtag_token = RegexpTokenizer(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)")
        emo_zer = RegexpTokenizer(r"[:=;]+[-']*[D)(\]\[]+")

        uni_list=[]
        bi_list=[]
        hashtag_list=[]
        emoticon_list=[]

        for sentence in dataset:
            sentence=sentence.lower() #lowercase

            unigram = tokenizer.tokenize(sentence)
            bigram = bigrams(unigram)
            hashtag = hashtag_token.tokenize(sentence)
            emoticon = emo_zer.tokenize(sentence)

            uni_list.append(unigram)
            bi_list.append(bigram)
            hashtag_list.append(hashtag)
            emoticon_list.append(emoticon)

        return uni_list,bi_list,hashtag_list,emoticon_list


    def get_unigrams(self):
        results=self.get_features() #get the result from the last function
        unigram_list=results[0]  #return a tuple, the first element is uni_list, the second is bi_list

        from nltk.corpus import stopwords

        all_unigram=[]
        for item in unigram_list: #select a sentence
            for i in item:        #select a word
                all_unigram.append(i) #integrate all the words into a list
        filter_unigram=[word for word in all_unigram if word not in stopwords.words('english')] #filter stopwords
        unigram=sorted(set(filter_unigram)) #drop the same words

        return unigram

    def get_bigrams(self):
        results=self.get_features() #调用上一个函数 #################
        bigram_list=results[1]
        all_bigram=[]
        for item in bigram_list:
            for i in item:
                all_bigram.append(i)
        bigram=sorted(set(all_bigram))

        return bigram

    def get_hashtag(self):
        results=self.get_features() #调用上一个函数 #################
        hashtag_list=results[2]
        all_hashtag=[]
        for item in hashtag_list:
            for i in item:
                all_hashtag.append(i)
        hashtag=sorted(set(all_hashtag))

        return hashtag



class edges_weight():

    def __init__(self,file_type,feature_type,data_path):
        self.file_type=file_type
        self.feature_type=feature_type
        self.data_path=data_path

    def get_feature_edges(self): #input features(hashtags,ngrams),output features and corresponding weights #use the iphonex as baseline
        if self.feature_type=='unigram':
            feature_all_list=get_nodes_from_tweets(self.file_type,self.data_path).get_features()[0] #unigram
        elif self.feature_type=='bigram':
            feature_all_list=get_nodes_from_tweets(self.file_type,self.data_path).get_features()[1] #bigram
        else:
            feature_all_list=get_nodes_from_tweets(self.file_type,self.data_path).get_features()[2] #hashtag

        all_word_list=[]
        for sentence in feature_all_list:
            for word in sentence:
                all_word_list.append(word)
        all_word_num=len(all_word_list)#all words

        feature_norepeat_list=get_nodes_from_tweets(self.file_type,self.data_path).get_unigrams()
        word_frequency_list=[]
        for word in feature_norepeat_list:
            word_count=all_word_list.count(word)
            word_frequency_list.append(word_count)#frequency

        word_fre_ratio_list=[]
        for i in word_frequency_list:
            word_fre_ratio=float(i/all_word_num)
            word_fre_ratio_list.append(word_fre_ratio)#feequency rate

        return word_fre_ratio_list


#obj11=edges_weight('csv','unigram')
#print(obj11.get_feature_edges())

#------build graph file---------#
#----node A, node B, linkweight----#
start1=time.time()

graph_list=[]

#original words from twitter
obj1=get_nodes_from_tweets('csv',"/Users/yyb/PycharmProjects/Twitter/data/hcr/hcr-combine.csv")
tweets=obj1.read_csv()[0]

unigram_list=obj1.get_features()[0]
bigram_list=obj1.get_features()[1]
hashtag_list=obj1.get_features()[2]
emoticon_list=obj1.get_features()[3]

unigram=obj1.get_unigrams()
bigram=obj1.get_bigrams()
hashtag=obj1.get_hashtag()


obj2=get_nodes_from_existing_resource()

lexicon_words=obj2.get_lexicon_nodes()[0]
emoticons=obj2.get_emoticon_nodes()[1]


#weight words
obj_w=get_nodes_from_tweets('json','/Users/yyb/PycharmProjects/Twitter/data/dataset/tweets_iphonex.json')
json_tweets=obj1.read_json()

json_unigram=obj_w.get_unigrams()
json_bigram=obj_w.get_bigrams()
json_hashtag=obj_w.get_hashtag()
print(json_unigram)

#weight scores
csv_unigram_w=edges_weight('csv','unigram',"/Users/yyb/PycharmProjects/Twitter/data/hcr/hcr-combine.csv").get_feature_edges()
json_unigram_w=edges_weight('json','unigram','/Users/yyb/PycharmProjects/Twitter/data/dataset/tweets_iphonex.json').get_feature_edges()

csv_bigram_w=edges_weight('csv','bigram',"/Users/yyb/PycharmProjects/Twitter/data/hcr/hcr-combine.csv").get_feature_edges()
json_bigram_w=edges_weight('json','bigram','/Users/yyb/PycharmProjects/Twitter/data/dataset/tweets_iphonex.json').get_feature_edges()

csv_hashtag_w=edges_weight('csv','hashtag',"/Users/yyb/PycharmProjects/Twitter/data/hcr/hcr-combine.csv").get_feature_edges()
json_hashtag_w=edges_weight('json','hashtag','/Users/yyb/PycharmProjects/Twitter/data/dataset/tweets_iphonex.json').get_feature_edges()

end1=time.time()
print('loading complete, duration is: '+str(end1-start1))


#--tweets--lexicon--#
start2=time.time()
tweet_lexicon_edges=[]
tweet_num=0
for tweet in unigram_list:
    for word in tweet:
        if word in lexicon_words:
            lexicon_index=lexicon_words.index(word)+len(unigram_list)
            tweet_lexicon_edges.append((tweet_num,lexicon_index,1))
    tweet_num+=1


#--tweets--emoticon--#
tweet_emoticon_edges=[]
tweet_num=0
for tweet in emoticon_list:
    for emoji in tweet:
        if emoji in emoticons:
            emoji_index=emoticons.index(emoji)+len(unigram_list)+len(lexicon_words)
            tweet_emoticon_edges.append((tweet_num,emoji_index,1))
    tweet_num+=1


#--tweets--unigram--#
import math
tweet_unigram_edges=[]
tweet_num=0
for tweet in unigram_list:
    for uni in tweet:
        if uni in unigram:
            uni_index=unigram.index(uni)+len(unigram_list)+len(lexicon_words)+len(emoticons)
            #weight calculate
            try:
                if csv_unigram_w[unigram.index(uni)]>json_unigram_w[json_unigram.index(uni)]:
                    weight_uni=math.log(csv_unigram_w[unigram.index(uni)]/json_unigram_w[json_unigram.index(uni)])
                else:
                    weight_uni=0
            except:
                weight_uni=0
                continue
            tweet_unigram_edges.append((tweet_num,uni_index,weight_uni))
    tweet_num+=1


#--tweets--bigram--#
tweet_bigram_edges=[]
tweet_num=0
for tweet in bigram_list:
    for bi in tweet:
        if bi in bigram:
            bi_index=bigram.index(bi)+len(unigram_list)+len(lexicon_words)+len(emoticons)+len(unigram)
            #weight calculate
            try:
                if csv_bigram_w[bigram.index(bi)]>json_bigram_w[json_bigram.index(bi)]:
                    weight_bi=math.log(csv_bigram_w[bigram.index(bi)]/json_bigram_w[json_bigram.index(bi)])
                else:
                    weight_bi=0
            except:
                weight_bi=0
                continue
            tweet_bigram_edges.append((tweet_num,bi_index,weight_bi))
    tweet_num+=1

#--tweets--hashtag--#

tweet_hashtag_edges=[]
tweet_num=0
for tweet in hashtag_list:
    for hash in tweet:
        if hash in hashtag:
            hash_index=hashtag.index(hash)+len(unigram_list)+len(lexicon_words)+len(emoticons)+len(unigram)+len(bigram)
            #weight calculate
            try:
                if csv_hashtag_w[hashtag.index(hash)]>json_hashtag_w[json_hashtag.index(uni)]:
                    weight_hash=math.log(csv_hashtag_w[hashtag.index(hash)]/json_hashtag_w[json_hashtag.index(uni)])
                else:
                    weight_hash=0
            except:
                weight_hash=0
                continue
            tweet_hashtag_edges.append((tweet_num,hash_index,weight_hash))
    tweet_num+=1


nodes=[]
for a in tweet_lexicon_edges:
    nodes.append(a)
for b in tweet_emoticon_edges:
    nodes.append(b)
for c in tweet_unigram_edges:
    nodes.append(c)
for d in tweet_bigram_edges:
    nodes.append(d)
for e in tweet_hashtag_edges:
    nodes.append(e)
end2=time.time()
print('nodes complete, duration is: '+str(end2-start2))
#print(nodes)

column_vid1=[]
column_vid2=[]
column_w=[]

for point in nodes:
    column_vid1.append(point[0])
    column_vid2.append(point[1])
    column_w.append(point[2])

save=pd.DataFrame({"Vid1":column_vid1,"Vid2":column_vid2,"weight":column_w})
save.to_csv('/Users/yyb/PycharmProjects/Twitter/data/processing_data/edges.csv',index=True,sep='^')


#building the adjacency matrix
#1.tweets rows(the first row of the six)
for i in range(0,len(tweets)):

    ###user-tweet matrix
    for j in range(0,len(users)):
        user=users[j] #the user column
        if hcr.loc[[i]]['username'].values[0]==user: #pick each tweet's author, compare it with user
            matrix_adj[i][j+len(tweets)]=1

    ###unigram-tweet matrix
    for j in range(0,len(unigram)):
        uni=unigram[j] #the unigram column
        if uni in unigram_list[i]: #pick each tweet's unigram list element, compare it with uni
            matrix_adj[i][j+len(tweets)+len(users)]=1

    ###bigram-tweet matrix
    for j in range(0,len(bigram)):
        bi=bigram[j] #the bigram column
        if bi in bigram_list[i]: #pick each tweets's bigram list element, compare it with bi
            matrix_adj[i][j+len(tweets)+len(users)+len(unigram)]=1

    ###hashtag-tweet matrix
    for j in range(0,len(hashtag)):
        hasht=hashtag[j]
        if hasht in hashtag_list[i]:
            matrix_adj[i][j+len(tweets)+len(users)+len(unigram)+len(bigram)]=1

    ###dic-tweet matrix
    for j in range(0,len(dic)):
        word=dic[j]
        if word in unigram_list[i]:
            matrix_adj[i][j+len(tweets)+len(users)+len(unigram)+len(bigram)+len(hashtag)]=1


#2.user rows(the second row of the six)
for i in range(0,len(users)):
    user=users[i]
    try:
        with open("/Users/yyb/Documents/python_following/"+user+".json",'r') as f:
            con=json.load(f)
            following_list=con['info'][0][user]  #get the user of the first row's following list
        for j in range(0,len(users)):
            if users[j] in following_list:
                matrix[i+len(tweets)][j+len(tweets)]=1 ## finish building the adjacency_matrix
    except:
        continue




matrix_adj_2=np.array([[r[col] for r in matrix_adj] for col in range(len(matrix_adj[0]))])
matrix=matrix_adj+matrix_adj_2


node_names=np.arange(length).tolist()
a = pd.DataFrame(matrix, index=node_names, columns=node_names)

# Get the values as np.array, it's more convenenient.
A = a.values

# Create graph, A.astype(bool).tolist() or (A / A).tolist() can also be used.
g = igraph.Graph.Adjacency((A > 0).tolist())

# Add edge weights and node labels.
g.es['weight'] = A[A.nonzero()]
g.vs['label'] = node_names  # or a.index/a.columns

g.summary()

print(g.community_label_propagation(initial=label_list))