# Никифорова Анастасия
# Лезжова Валерия
# Орлина Кристина

import vk_requests
import xml.etree.ElementTree as ET
import time
import re
import random
import operator


#application program interface

def create_api(vk_config, type):
    tree = ET.parse(vk_config)
    root = tree.getroot()

    data = []

    for child in root:
        data.append(child.text)

    return vk_requests.create_api(app_id = data[0], login = data[1], password = data[2], scope = type)

api = create_api('vk.xml', 'messages')
print(api.users.get())

# 1 считывание моих сообщений из вк
def get_all_texts():
    messages = []
    i = 0
    while True:
        tmp = api.messages.get(out = 1, count = 200, offset = 200*i)
        i += 1
        if len(tmp['items']) == 0:
            break
        for y in tmp['items']:
            messages.append(y['body'].lower())
        if i%3 == 0:    #let it rest
            time.sleep(1)
        if i >= 4:
            break
    return messages

messages = get_all_texts()
#print(messages)

# 2 добавление символа
def add_symb(messages):   #checked - must work
    symb_mes = []
    for i in messages:
        i = '#' + i + '&'
        symb_mes.append(i)
    return symb_mes

symb_mes = add_symb(messages)
#print(symb_mes)

def get_tokens(messages):  #works
    tokens = []
    for i in messages:
        mt = re.findall('\w+', i)
        tokens.extend(mt)
    return tokens
tokens = get_tokens(messages)
print(len(tokens))


#got this on stackoverflow
def get_ngrams(n):                      #works
    ngrams = [tokens[i:i+n] for i in range(len(tokens) - n+1)]
    return ngrams

bigrams = get_ngrams(2)
trigrams = get_ngrams(3)
#print(bigrams[:5], trigrams[:3])

#getting ngrams and frequencies with nltk here:
'''
def get_bi(tokens):
    bi = nltk.bigrams(tokens)
    return bi
bi = get_bi(tokens)
#print(bi)

def get_tri(tokens):
    tri = nltk.trigrams(tokens)
    return tri
tri = get_tri(tokens)
#print(tri)

def freq_dist(ng):
    fdist = nltk.FreqDist(ng)
    return fdist

bi_freq = freq_dist(bi)
tri_freq = freq_dist(tri)
print (bi_freq)
print (tri_freq)
'''

def freq_counter(ngram):                        #works
    count_freq = {}
    for i in ngram:
        if type(i) == str:
            if i not in count_freq.keys():
                count_freq[i] = 1
            else:
                count_freq[i] += 1
        else:
            if tuple(i) not in count_freq.keys():
                count_freq[tuple(i)] = 1
            else:
                count_freq[tuple(i)] += 1
    return count_freq
uni_freq = freq_counter(tokens)
bi_freq = freq_counter(bigrams)
tri_freq = freq_counter(trigrams)
#print(bi_freq)

'''
#если понадобится объединить n-граммы по строкам:

def join_to_string(function, n):
    [' '.join(x) for x in function(n)] # ['a b', 'b c', 'c d']


# 4 Maximum likelihood for bigrams
def mle_bi():
    mle_bi = nltk.ConditionalProbDist(???, nltk.MLEProbDist)
    return mle_bi

'''

# теперь самое муторное (пока) - посчитать вероятности.

def prob_bi(uni_freq, bi_freq):             #works
    prob_bi = {}
    values = {}
    for token in uni_freq.keys():
        for bigram in bi_freq.keys():
            if bigram[0] == token:
                values[bigram[1]] = bi_freq[bigram]/uni_freq[token]
            else:
                pass
        prob_bi[token] = values
        values = {}
    return prob_bi

bi_prob = prob_bi(uni_freq, bi_freq)
#print (bi_prob)

def prob_tri(bi_freq,tri_freq):     # {'кошка':{'спит':0.5,'ест':0.49,'прогает':0.01}}  #works
    prob_tri = {}
    values = {}
    for bigram in bi_freq.keys():
        for trigram in tri_freq.keys():
            if trigram[:-1] == bigram[0:]:
                values[trigram[2]] = tri_freq[trigram]/bi_freq[bigram]
            else:
                pass
        prob_tri[bigram[0:]] = values
        values = {}
    return prob_tri

tri_prob = prob_tri(bi_freq,tri_freq)
#print (tri_prob)

#уиии! после двух дней мучений и 100500 исправлений и переписываний кода все заработало, урааа!

# теперь перейдем собственно к генерации

def get_first_word(symb_mes):           # works
    first_words = []
    for i in symb_mes:
        fw = re.findall(r"#\w+", i)
        first_words.extend(fw)
    random_fw = random.choice(first_words)
    random_fw = re.sub('#', '', random_fw)
    return random_fw
first = get_first_word(symb_mes)
#print(first)

def generate_text(bigram_prob):     # {'кошка':{'спит':0.5,'ест':0.49,'прогает':0.01}, 'спит':{}}
          # p = 0,999   0,5 (+= s_p), new_words = '' , 0,49 (+=s_p 0.99)
    start = get_first_word(symb_mes)
    text = [start]
    while len(text) < 10:
        flag = False
        for k,v in bigram_prob.items(): # v - словарь
            s_p = 0.0
            p = random.random()
            if k == text[-1]:
                sorted_v = sorted(v.items(), key=operator.itemgetter(1), reverse=True)       #сортировка v
                for i in sorted_v:
                    s_p += i[1]
                    nw = i[0]
                    if s_p >= p:
                        text.append(nw)
                        flag = True
                        break
                    else:
                        pass
            elif len(text) > 10:
                break
            if flag:
                break
    return(text)

text = generate_text(bi_prob)
print(text)

def send_text(text):
    a = api.messages.send(user_id=27372476, message=text)
    return(a)

send = send_text(text)
send