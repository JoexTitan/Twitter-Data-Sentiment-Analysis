import os
import sys
import concurrent.futures
import csv

args = sys.argv
optd = os.path.abspath(args[2])
srcd = os.path.abspath(args[1])
usr_batch_size = int(args[4])
tw_batch_size = int(args[3])

try:
    os.mkdir(optd)
except:
    pass

for fn in os.listdir(srcd):
    fp = os.path.join(srcd,fn)
    if os.path.isdir(fp): continue
    op = os.path.join(optd, fn)
    c = 0
    with open(fp) as srcf:
        for l in srcf:
            if ('tw' in fn and c == tw_batch_size) or ('us' in fn and c == usr_batch_size):
                break
            with open(op, 'a') as optf:
                optf.write(l)
            c += 1

def loadto(data, srcf):
    with open(srcf, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)

def processTwittos(usr, counter, outd):
    usr[11] = usr[11].replace(',',' ')
    date_table = usr[12:15] + usr[18:20]
    timestamp_table = usr[15:18]
    location_table = usr[10:12]
    twitto_md = usr[4:5] + usr[20:22]
    twitto = usr[0:1] + usr[2:4] + usr[5:10]

    loadto([counter] + twitto, os.path.join(outd, 'tw_data1_sample'))
    loadto([counter] + twitto_md, os.path.join(outd, 'tw_data2_sample'))
    loadto([counter] + date_table, os.path.join(outd, 'tw_data3_sample'))
    loadto([counter] + timestamp_table, os.path.join(outd, 'tw_data4_sample'))
    loadto([counter] + location_table, os.path.join(outd, 'tw_data5_sample'))

def normalizeTwittos(srcf, outd):
    counter = 2061787
    with open(srcf, newline='') as f:
        usrs = csv.reader(f, delimiter=',')
        
        with concurrent.futures.ThreadPoolExecutor(10) as ex:
            for usr in usrs:
                ex.submit(lambda args:processTwittos(*args), [usr,counter if counter != 0 else 'id',outd])
                counter += 1

    return counter

def processTweets(tw,counter,outd):
    strs = [7] + list(range(17,22))
    for s in strs:
        tw[s] = tw[s].replace(',',' ')
    tweet = tw[0:5]
    tweet_md = tw[0:1] + tw[5:8] + tw[16:17] + tw[22:]
    date = tw[8:11] + tw[14:16]
    timestamp = tw[11:14]
    location = tw[17:22]

def normalizeTweets(srcf, outd, startid):
    counter = startid
    with open(srcf, newline='') as f:
        tweets = csv.reader(f, delimiter=',')
        with concurrent.futures.ThreadPoolExecutor(10) as ex:
            for tw in tweets:
                ex.submit(lambda args:processTweets(*args), [tw,counter if counter != startid else 'id',outd])
                counter += 1

if __name__ == '__main__':
    args = sys.argv
    outd = os.path.abspath(args[3])
    twf = os.path.abspath(args[2])
    usf = os.path.abspath(args[1])
    try:
        os.mkdir(outd)
    except:
        pass
    lastid = normalizeTwittos(usf, outd)

    loadto([counter] + tweet, os.path.join(outd, 'tw_data1_sample.csv'))
    loadto([counter] + tweet_md, os.path.join(outd, 'tw_data2_sample.csv'))
    loadto([counter] + date, os.path.join(outd, 'tw_data3_sample.csv'))
    loadto([counter] + timestamp, os.path.join(outd, 'tw_data4_sample.csv'))
    loadto([counter] + location, os.path.join(outd, 'tw_data5_sample.csv'))

