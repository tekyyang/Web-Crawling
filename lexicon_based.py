from collections import OrderedDict, defaultdict, Counter
import re
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
from nltk import bigrams #pay attention to the 's' of bigrams
from nltk.tokenize import RegexpTokenizer



def get_features(dataset):
# input a list of sentence to be processed

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


#preprocessing--get features from tweets---get together the results from each sentence--exist duplicated elements----------
def pre_process(file_path): #upload data from file and get their features
    hcr = pd.read_csv(file_path,sep=',',error_bad_lines=False)
    hcr=hcr[(hcr['sentiment']=='positive')|(hcr['sentiment']=='negative')]#get only pos/neg label data
    hcr=hcr.reset_index(drop=True) #reindex the table


    dataset = hcr['content'] #get tweets
    #users = hcr['username'] #get usernames
    #users = list(users.values)
    #tweets = list(dataset.values)

    original_polarity=hcr['sentiment'].values.tolist()

    results=get_features(dataset) #调用上一个函数 #################

    #(1)unigram
    unigram_list=results[0]  #return a tuple, the first element is uni_list, the second is bi_list
    from nltk.corpus import stopwords
    all_unigram=[]
    for item in unigram_list: #select a sentence
        for i in item:        #select a word
            all_unigram.append(i) #integrate all the words into a list
    filter_unigram=[word for word in all_unigram if word not in stopwords.words('english')] #filter stopwords
    unigram=sorted(set(filter_unigram)) #drop the same words

    #(2)bigram
    bigram_list=results[1]
    all_bigram=[]
    for item in bigram_list:
        for i in item:
            all_bigram.append(i)
    bigram=sorted(set(all_bigram))

    #(3)hashtag
    hashtag_list=results[2]
    all_hashtag=[]
    for item in hashtag_list:
        for i in item:
            all_hashtag.append(i)
    hashtag=sorted(set(all_hashtag))

    #(4)emoticon
    emoticon=results[3]
    #print('original length is '+str(len(original_polarity))) #490

    return unigram_list,unigram,bigram,hashtag,emoticon,original_polarity



def lexicon_polarity():
    with open("/Users/yyb/Documents/LPtest/new_lexicon.txt",'r') as f:
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
                score_num_lexicon.append(1)
            elif i=='weakneg':
                score_num_lexicon.append(-1)
            elif i=='strongneg':
                score_num_lexicon.append(-2)
            else:
                score_num_lexicon.append(2)
        return word_lexicon,score_num_lexicon


def lexicon_accuracy():
    #input: dataset
    file_path='/Users/yyb/Documents/LPtest/updown_copy_3/updown/data/hcr/train/orig/hcr-train.csv'
    bigram_list=pre_process(file_path)[0] #################
    #print(len(bigram_list)) 490
    original_polarity=pre_process(file_path)[5] #################

    word_lexicon=lexicon_polarity()[0]  #################
    score_lexicon=lexicon_polarity()[1]  #################

    sentence_score_list=[]
    #no_list=['no','not','never','none','nobody','nothing','nowhere','neither','nor','but','without','unless','but','rather than']

    for sentence in bigram_list:
        sentence_score=0
        for word in sentence:
            if word in (word_lexicon):
                word_number=word_lexicon.index(word)
                word_score=int(score_lexicon[word_number])
                sentence_score+=word_score
            '''
            if word in no_list:
                sentence_score*=-1
            '''

        sentence_score_list.append(sentence_score)
    print(len(sentence_score_list))


    sentence_score_result=[]
    for i in sentence_score_list:
        if i>0:
            sentence_score_result.append('positive')
        if i<0:
            sentence_score_result.append('negative')
        if i==0:
            sentence_score_result.append('neutral')
    #print(len(sentence_score_result))

    correct_num=0
    for i in range(len(original_polarity)):
        if sentence_score_result[i] == original_polarity[i]:
            correct_num+=1

    accurancy=correct_num/len(original_polarity)
    #print(len(original_polarity))
    #print(len(sentence_score_result))
    print(accurancy)



def main():
    file_path='/Users/yyb/Documents/LPtest/updown_copy_3/updown/data/hcr/train/orig/hcr-train.csv'
    lexicon_accuracy()


main()