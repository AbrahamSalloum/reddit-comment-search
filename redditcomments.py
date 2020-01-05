#!/usr/bin/env python3

import praw
import re
import os
import datetime

submissions = {}
subreddits = ["subreddit1","subreddit2", "subreddit3"]
ql = ["keyword1", "keyword2", "keyword3","keyword4"]
num = 100 # number of comments per sub to extract

f = open("res.mail", "w", encoding="utf-8")


def addurltags(r):
    redditurl = r'(\[(.+?)\]\((http[s]*:\/\/.+?)\))+?'
    resultredd = re.findall(redditurl, r)
    for rr in resultredd:
        urllink = "<a href='"+rr[2]+"'>"+rr[1]+"</a>"
        r = r.replace(rr[0],urllink)
    return r

def addhighlights(r):
    for w in ql:
        result = re.search("\s"+w, r, re.IGNORECASE)
        if result:
            hl = '<span style="background-color:yellow;">'+result.group(0)+"</span>"
            r = r.replace(result.group(0),hl)
    return r

reddit = praw.Reddit(
    client_id="1_GET_YOUR_OWN_Q",
    client_secret='Q_GET_YOUR_OWN_c',
    user_agent='comments app')

for sub in subreddits:
    for submission in reddit.subreddit(sub).new(limit=num):
        submissions[submission.id] = [submission.title, submission.permalink, submission.selftext]
        for comment in submission.comments.list():
            try:
                submissions[submission.id].append(comment.body)
            except:
                pass

searchresults = []
for s in submissions:
    for post in submissions[s]:
        if any(keyword.upper() in post.upper() for keyword in ql):
            searchresults.append(s)

unqsets = list(set(searchresults))
m0 = """From: heycitizen.mail@gmail.com
Subject:  """ + "results " + str(datetime.datetime.now())

m1 = """
MIME-Version: 1.0
Content-Type: text/html

"""
mime = m0+m1
email=mime
for s in unqsets:
    email = email + "<h4><a href='https://www.reddit.com/" + submissions[s][1] +"'>"+submissions[s][0]+"</a></h4>"
    email= email + "<table border='1' bgcolor='silver'>"
    for r in submissions[s][2:]:
        r = addurltags(r)
        r = addhighlights(r)
        email = email + "<tr><td>"+r+"</td></tr>"
    email= email + "</table><hr>"
f.write(email)
f.close()
cmd = "cat res.mail | msmtp -a gmail recipient@gmail.com" 
os.system(cmd)
