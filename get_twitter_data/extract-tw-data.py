import sys
import bz2
import os
import requests as req
import tweepy

def getAPI(
    apikey,
    apikey_secret,
    accesstoken,
    accesstoken_secret
):
    auth = tweepy.OAuthHandler(apikey, apikey_secret)
    auth.set_access_token(accesstoken, accesstoken_secret)
    api = tweepy.API(auth)
    return api

def lookupStatuses(api, ids, path):
    tweets = api.statuses_lookup(ids)
    jstweets = [str(tw._json) for tw in tweets]
    data = str.join('\n', jstweets)
    with open(path,'a') as opt:
        opt.write(data)

args = sys.argv
srcf = os.path.abspath(args[1])
optf = os.path.abspath(args[2])
api = getAPI(
    args[3],
    args[4],
    args[5],
    args[6]
)

with open(srcf) as src:
    c = 0
    ids = []
    for tw in src:
        if tw != '\n':
            if c<100:
                ids.append(tw.split('\n')[0])
                c+=1
            else:
                lookupStatuses(api,ids,optf)
                c=0
                ids = []
    if len(ids) > 0:
        lookupStatuses(api,ids,optf)

args = sys.argv
srcdir = os.path.abspath(args[1])
optdir = os.path.abspath(args[2])

try:
    os.mkdir(optdir)
except:
    pass

err = os.path.abspath("decerr.txt")
dec = bz2.BZ2Decompressor()

for f in os.listdir(srcdir):
    try:
        with bz2.open(os.path.join(srcdir, f), 'rb') as bf:
            data = bf.read()
        with open(os.path.join(optdir, f"{f.split('.')[0]}.json"), 'wb') as opt:
            opt.write(dec.decompress(data.decode('unicode_escape')))
    except Exception as e:
        print(e)
        with open(err, 'a') as errf:
            errf.write(f"{f}\n")
        pass

args = sys.argv
src = os.path.abspath(args[1])
optdir = os.path.abspath(args[2])
errfile = os.path.abspath(args[3])

try:
    os.mkdir(optdir)
except:
    pass

with open(src) as srcf:
    count = 1
    for url in srcf:
        url = url.split('\n')[0][2:]
        try:
            r = req.get(f"https://{url}")
            with open(os.path.join(optdir, f"{count}.json.bz2"), 'wb') as opt:
                opt.write(r.content)
        except:
            with open(errfile, 'a') as err:
                err.write(f"{url}\n")
            pass
        count += 1