import praw
import re
import os
import datetime

submissions = {}
searchresults = []
subs = "subreddit0+subreddit1"
ql = ["keywordA", "keywordB", "keywordC", "keywordD"]
f = open("res.mail", "w", encoding="utf-8")

def addurltags(r):
    redditurl = r'(\[(.+?)\]\((http[s]*:\/\/.+?)\))+?'
    resultredd = re.findall(redditurl, r)
    if len(resultredd) > 0:
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


## starts here ##

reddit = praw.Reddit(
    client_id="74sdNOT_REALg254",
    client_secret='Q_NOT_REAL_Qlkc',
    user_agent='blah blah')

for submission in reddit.subreddit(subs).new(limit=200):
    submissions[submission.id] = [submission.title, submission.permalink, submission.selftext]
    for comment in submission.comments.list():
        try:
            submissions[submission.id].append(comment.body)
        except:
            pass


for s in submissions:
    for post in submissions[s]:
        if any(keyword.upper() in post.upper() for keyword in ql):
            searchresults.append(s)

unqsets = list(set(searchresults))
m0 = """From: abraham.salloum@gmail.com
Subject:  """ + "fshn " + str(datetime.datetime.now())

m1 = """
MIME-Version: 1.0
Content-Type: text/html

"""
mime = m0+m1
email=mime
for s in unqsets:
    email = email + "<a href='https://www.reddit.com/" + submissions[s][1] +"'>"+submissions[s][0]+"</a>"
    email= email + "<table border='1' bgcolor='silver'>"
    for r in submissions[s][2:]:
        r = addurltags(r)
        r = addhighlights(r)
        email = email + "<tr><td>"+r+"</td></tr>"
    email= email + "</table><hr>"
f.write(email)
f.close()
cmd = "cat /home/pygar/res.mail | msmtp -a gmail abrahamsalloum@gmail.com"
os.system(cmd)

