#!/usr/bin/python

import tweepy
import time

# setting
twitter_conf = {
    'consumer' : {
        'key'    : "consumer_key",
        'secret' : "consumer_secret"
    },
    'access'   : {
        'key'    : "access_key",
        'secret' : "access_secret"
    }
}

# RateLimitError -> sleep 17sec
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("!except tweepy.RateLimitError!")
            print("5/17 min")
            time.sleep(5 * 60)
            print("10/17 min")
            time.sleep(5 * 60)
            print("15/17 min")
            time.sleep(5 * 60)
            print("17/17 min")
            time.sleep(2 * 60)
             
# get follow user-id list
def getFriends(id,name,friends_ids):
    print("getFriends ID=" + str(id) + ",NAME=" + name)
    for friend_id in limit_handled(tweepy.Cursor(api.friends_ids, user_id=id).items()):
        friends_ids.append(friend_id)

# write csv frind data
def writeFriends(friends_ids,source_id,source_name,f):
    for i in range(0, len(friends_ids), 100):
        for user in api.lookup_users(user_ids=friends_ids[i:i+100]):
            linestr = str(source_id) + ",\"" + source_name + "\"," + str(user.id) + ",\"" + user.name + "\""
            print(linestr)
            f.write(linestr+"\r\n")

# Twitter authentication
auth = tweepy.OAuthHandler(
    twitter_conf['consumer']['key'],
    twitter_conf['consumer']['secret'])
auth.set_access_token(
    twitter_conf['access']['key'],
    twitter_conf['access']['secret'])

# get tweepy api object
api = tweepy.API(auth)
my_info = api.me()

# open csv with write mode
f = open('twex.csv', 'w')

f.write("source_id,source_name,target_id,target_name"+"\r\n")

# my friends write csv
print("myinfo-start")
friends_ids = []
getFriends(my_info.id,my_info.name,friends_ids)
writeFriends(friends_ids,my_info.id,my_info.name,f)
print("myinfo-end")

# A friend of a friend
for friend_id in friends_ids:

    # get user info
    user_info = api.get_user(friend_id)
    print("friend_id="+str(friend_id)+",name="+user_info.name)
    
    # get friend of a friend
    friendsfriends_ids = []
    getFriends(friend_id,user_info.name,friendsfriends_ids)

    # write csv
    writeFriends(friendsfriends_ids,user_info.id,user_info.name,f)
    print("friend_id="+str(friend_id)+" end")

#close
f.close()

