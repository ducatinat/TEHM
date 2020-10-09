#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 200121216
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
from geopy.geocoders import Nominatim
import sys
import argparse
import datetime
from collections import OrderedDict


parser = argparse.ArgumentParser()
parser.add_argument('id', type=str, # var = id
                    help='ID')
args = parser.parse_args()
InstagramAPI = InstagramAPI("CHANGEIT", "CHANGEIT")

InstagramAPI.login() # login
geolocator = Nominatim()
# media_id = InstagramAPI.LastJson # last response JSON
# InstagramAPI.like(media_id["ranked_items"][0]["pk"]) # like first media
# InstagramAPI.getUserFollowers(media_id["ranked_items"][0]["user"]["pk"])



########################Gets exact locatino with timestamp###############################

def CheckIfExist(id): #Could not catch 400 error, so checking for JSON response
    try:
        InstagramAPI.getUserFeed(id)
        a = InstagramAPI.LastJson['items']
    except KeyError:
        print "User with id: "+ id + " does not exist"
        sys.exit()
    print "Checking.. It may take a while if user has many photos"

def GetAdressesTimes(id):
    only_id = {} #var only for max_next_id parameter | pagination
    photos = [] # only photos
    hashtags = []
    a = None #helper
    while True:
        if (a == None):
            InstagramAPI.getUserFeed(id)
            a = InstagramAPI.LastJson['items']#photos 00, 01, 02...
            only_id = InstagramAPI.LastJson #all LastJson with max_id param
        else:
            InstagramAPI.getUserFeed(id, only_id['next_max_id']) #passing parameter max_id
            only_id = InstagramAPI.LastJson
            a = InstagramAPI.LastJson['items']

        photos.append(a)

        if not 'next_max_id' in only_id:
            break


    locations = {}

    for i in photos: #extract location from photos, related
        for j in i:
            if 'lat' in j.keys():
                lat = j.get('lat')
                lng = j.get('lng')

                locations[str(lat) + ', ' + str(lng)] = j.get('taken_at')

    address = {}
    for k,v in locations.iteritems():
        details = geolocator.reverse(k) #locate for key
        unix_timestamp = datetime.datetime.fromtimestamp(v) # read timestamp as a value
        address[details.address] = unix_timestamp.strftime('%Y-%m-%d %H:%M:%S')


    sort_addresses = sorted(address.items(), key=lambda p: p[1], reverse=True)  #sorting

#printing
    i = 1
    for address, time in sort_addresses:
        print str(i) + ' ' + address, time
        i = i+1
################################################################################################


def GetHashtags(id):
    text = []
    only_id = {}
    a = None #helper
    hashtags = []
    counter = 1
    while True:
        if (a == None):
            InstagramAPI.getUserFeed(id)
            a = InstagramAPI.LastJson['items']#photos 00, 01, 02...
            only_id = InstagramAPI.LastJson #all LastJson with max_id param
        else:
            InstagramAPI.getUserFeed(id, only_id['next_max_id']) #passing parameter max_id
            only_id = InstagramAPI.LastJson
            a = InstagramAPI.LastJson['items']


            try:
                for i in a:
                    c = i.get('caption', {}).get('text')
                    text.append(c)
                    #print str(counter) + ' ' + c
                    counter = counter +1
            except AttributeError:
                pass

        if not 'next_max_id' in only_id:
            break

    hashtag_counter = {}

    for i in text:
        for j in i.split():
            if j.startswith('#'):
                hashtags.append(j.encode('UTF-8'))

    for i in hashtags:
        if i in hashtag_counter:
            hashtag_counter[i] += 1
        else:
            hashtag_counter[i] = 1

    sortE = sorted(hashtag_counter.items(), key=lambda value: value[1], reverse=True)

    for k,v in sortE:
        print str(v) + ". " + str(k)
    print "Done with hashtags"
    # for k,v in ):Q
    #     print str(v) + ' ' + k

CheckIfExist(args.id)
GetHashtags(args.id)
GetAdressesTimes(args.id)
