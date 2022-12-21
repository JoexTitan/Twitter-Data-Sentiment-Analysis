import sys
import bz2
import random
import json
import os
import requests as req
import tweepy

args = sys.argv
source = os.path.abspath(args[1])
trgt_dir = os.path.abspath(args[2])

try:
    os.mkdir(trgt_dir)
except:
    pass

with open(source) as urls:
    hd = True
    for url in urls:
        if not hd:
            url = url.split(',')
            root = os.path.join(trgt_dir, url[1])
            url[2] = url[2].split("\n")[0]
            f_path = os.path.join(root, f"{url[2]}.txt") 
            try:
                os.mkdir(root)
            except:
                pass
            with open(f_path, 'a') as f:
                f.write(f"{url[0]}\n")
        else:
            hd = False

def randomSelector(fpath, sample_size = 200):
    tweets = []
    with open(fpath) as tweetspool:
        for tweet in tweetspool:
            js = json.loads(tweet)
            if "id_str" in js.keys(): tweets.append(js['id_str'])
    random.shuffle(tweets)
    tweets = random.sample(tweets, sample_size)
    return tweets

args = sys.argv
sample_size = int(args[3])
optf = os.path.abspath(args[2])
srcdir = os.path.abspath(args[1])

for tweetspool in os.listdir(srcdir):
    tweets = randomSelector(os.path.join(srcdir, tweetspool), sample_size)
    with open(optf, 'a') as opt:
        opt.write(str.join('\n', tweets))
        
def randomSelector(fpath, sample_size = 2):
    urls = []
    with open(fpath) as f:
        for url in f:
            urls.append(url.split('\n')[0])
    random.shuffle(urls)
    urls = random.sample(urls, sample_size)
    urls = str.join('\n', urls)
    return urls

args = sys.argv
root = os.path.abspath(args[1])
optf = os.path.abspath(args[2])
sample_size = int(args[3])

for sub_stream in os.listdir(root):
    fld = os.path.join(root, sub_stream)
    for f in os.listdir(fld):
        urls = randomSelector(os.path.join(fld, f), sample_size)
        with open(optf, 'a') as opf_obj:
            opf_obj.write(f"{urls}\n")