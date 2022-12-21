import json
import random
import datetime
import re
import csv
import os
import sys
import codecs
import concurrent.futures
from TweetProcessor import TweetProcesor
from UserProcessor import UserProcessor
from RandomTweetMetricsEstimator import RandomTweetMetricsEstimator
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language
from google.oauth2 import service_account

usrsdict = {}
args = sys.argv
srcf = os.path.abspath(args[1])
optd = os.path.abspath(args[2])

def loadto(data, outf):
    with open(outf, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(data)

def load_all_meta_data(twopt,usopt):
    twittos_meta = "us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category"
    tweets_meta = "tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month,is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,has_user_mentions, has_symbols, media_type"
    loadto(twittos_meta.split(','), usopt)
    loadto(tweets_meta.split(','), twopt)

def prepareTweet(optfile, tw):
    csvtw = tp.process(tw)
    loadto(csvtw,optfile)

def prepareUser(optfile, tw):
    csvus = up.process(tw)
    loadto(csvus,optfile)

if __name__ == '__main__':
    args = sys.argv
    srcdir = os.path.abspath(args[1])
    twopt = os.path.abspath(args[2])
    usopt = os.path.abspath(args[3])
    errf = os.path.abspath(args[4])
    up = UserProcessor()
    tp = TweetProcesor(RandomTweetMetricsEstimator().process)

    load_all_meta_data(twopt,usopt)

    for tweetspool in os.listdir(srcdir):
        with open(os.path.join(srcdir,tweetspool)) as src:
            print(tweetspool)
            for js in src:
                try:
                    tw = json.loads(js)
                except Exception as e:
                    with open(errf, 'a') as err:
                        err.write(f"{tweetspool},{e}\n")
                try:
                    if 'id_str' in tw.keys():
                        prepareTweet(twopt, tw)
                        prepareUser(usopt, tw)
                except Exception as e:
                    with open(errf, 'a') as err:
                        err.write(f"{tw['id']},{e}\n")

with open(srcf, newline='') as usrsfile:
    usrs = csv.reader(usrsfile, delimiter=',')
    c = 1
    for usr in usrs:
        d = [c, sum([int(i) for i in usr[5:10]])]
        if usr[0] in usrsdict.keys():
            usrsdict[usr[0]].append(d)
        else:
            usrsdict[usr[0]] = [d]
        c+=1

chosenusrs = [
    max(instances, key = lambda usr: usr[1])[0]
    for uid, instances
    in usrsdict.items()]

def process(f, usr):
    with open(f, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(usr)

try:
    os.mkdir(os.path.abspath(optd))
except:
    pass

with concurrent.futures.ThreadPoolExecutor(20) as ex:
    with open(srcf, newline='') as usrsfile:
        usrs = csv.reader(usrsfile, delimiter=',')
        c = 1
        f = 0
        for usr in usrs:
            if f == 10:
                f = 0
            if c in chosenusrs:
                ex.submit(lambda args:process(*args), [os.path.join(optd, f"{f}.csv"),usr])
                f += 1
            c+=1
            
class RandomTweetMetricsEstimator:
    def randCoeff(self):
        return 1 - random.random()*0.5

    def noise(self,x):
        return random.randint(0,int(x))

    def estimateTweetMetrics(self,X):
        w = [0.49,0.24,0.29]
        fmx = 280000
        wsmx = 21526374/1000000
        ws = 0
        for i in range(3): ws += w[i]*X[i]
        fv = fmx * (1/(1 + wsmx - ws/1000000))
        fv = fv*self.randCoeff()
        fv = self.noise(fv)
        rt = fv*(1/3)*self.randCoeff()
        rt = self.noise(rt)
        rp = rt*(1/3)*self.randCoeff()
        rp = self.noise(rp)
        return [ int(i) for i in [fv,rt,rp]]

    def process(self, tw):
        X = [int(tw['user']['followers_count']), int(tw['user']['statuses_count']), int(tw['user']['listed_count'])]
        Y = self.estimateTweetMetrics(X)
        return Y