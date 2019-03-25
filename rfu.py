#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests, json, datetime, os, sys, getopt, atexit, configparser, re

for var in ['quiet', 'nolog', 'cache', 'printtime', 'first']:
    exec("{} = False".format(var))
check_num, added, fails = 0, 0, 0

def fatal(error):
    global printtime
    printtime = False
    log(error + u"\n")
    sys.exit(2)

#%% Output files

def log(text):
    if printtime and text != "": pay = datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S] ") + text
    else: pay = text
    if not quiet: 
        try: print(pay)
        except: print(pay.encode(sys.getdefaultencoding(), errors = 'replace'))

def final():
    global printtime    
    printtime = False
    log(u"\n" + words[u'text'][u'bye'].format(added)) 
 
#%%  API Function

def api(com = "get", args = None ):
    global printtime
    """
    get & {} | lookup & {id:} | post & {**data}
    """

    url = radarr_url
    key = {"apikey": config[u'radarr'][u'api_key']}
    if com == "post":
        url += u"?apikey=" + config[u'radarr'][u'api_key']
        response = requests.post(url, data = args)
        return response.status_code
    elif com == "lookup":
        url += "/lookup/imdb"
        key.update({"imdbId" : str(args)})
    
    response = requests.get(url, params = key )
    response.content.decode("utf-8")
    return response.json()
    
#%% Configuration

start_time = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")    
    
words = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),allow_no_value=True)
words.read(u'words.conf')
config = configparser.ConfigParser(allow_no_value=True)
config.read(u'rfu.conf')

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hqd:",["help","quiet","data="])
    except getopt.GetoptError:
        print(u"\n" + u'Error in options\n')
        print(words[u'help'][u'text'])
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(words[u'help'][u'text'])
            sys.exit()
        elif opt in ("-q", "--quiet"): quiet = True
        elif opt in ("-d", "--data"): path = arg


#%% Data grab

exts = ["avi", "mkv", "mp4", "m4a", "mov", "wmv", "wma", "flv", "webm", "vob"]

if u'true' in config[u'radarr'][u'ssl'].lower(): radarr_url = u"https://"
else: radarr_url = u"http://"
radarr_url += u"{0}/api/movie".format(config[u'radarr'][u'server'])

log(words[u'text'][u'hello'] +  u"\n")
atexit.register(final)
printtime = True

#%% Begin

for root, dirs, files in os.walk(path):
    for name in files:
        if name[-3:] in exts:
            folder = root.replace(path,"")
            imdb = re.search(r"tt\d{7}", name)
            if imdb: imdb = imdb.group()
            else: break
            
            lookup_json = api(com = "lookup", args = imdb)
            payload = imdb, lookup_json['title'], lookup_json['year']
            log(words[u'text'][u'data'].format(*payload))  
            inpath = os.path.join(root,name)
            post_data = {u"qualityProfileId" : config[u'radarr'][u'quality'],
                     u"path": inpath,
                     u"monitored" : 'true'}
            for dictkey in [u"tmdbId",u"title",u"titleSlug",u"images",u"year"]: post_data.update({dictkey : lookup_json[dictkey]})
            if sys.version_info[0] == 2: data_payload = json.dumps(post_data)
            elif sys.version_info[0] == 3: data_payload = str(post_data).replace("'","\"")
            post = api(com = "post", args = data_payload)
            if post == 201: 
                log(words[u'text'][u'add_true'])
                added += 1
            else:
                log(words[u'text'][u'add_fail'].format(post))
                fails += 1
                if fails == 10:
                    printtime = False
                    fatal(words[u'text'][u'retry_err'])
