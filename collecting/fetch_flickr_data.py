"""
Example:

{'constented': True,
 'event': 'prehope_test',
 'img': 'http://www.flickr.com/photos/friskolator/7510210418/',
 'metadata': {'date_posted': '1341519946',
              'date_taken': '2012-07-05 13:25:39',
              'date_updated': '1341587580',
              'location': 'PHL',
              'photo_id': '7510210418',
              'photo_owner_nsid': '81953314@N02',
              'photo_title': 'IMAG0350',
              'realname': 'Frisk Olator',
              'username': 'friskolator'},
 'name': 'Frisk Olator',
 'version': '0.5'}
"""

import flickrapi
import json
import os
import sys
from pprint import pprint

sys.path.insert(0, "..") #add our parent dir for secret.py and stream.py

import secret # import local secret.py file containing keys.
              # we expect 2 values in secret.py
              # api_key = "XXXX" #< your flickr api key
              # api_secret = "YYYY" #< your flickr api secret

import stream # we expect 2 id's 'user_id' and event tag
              # user_id = "USER_ID_ON_FLICKR"
              # event_tag = "tag to seach flickr for.

flickr = flickrapi.FlickrAPI(secret.api_key)

filter_tags = [stream.event_tag, "friskolator"] # so we don't get general event tags

for photo in flickr.walk(tag_mode="and",tags=filter_tags):
    #print dir(photo)
    #print photo.__dict__
    info = stream.template_frisk.copy()
    photo_id = photo.get("id")
    photo_url = "http://www.flickr.com/photos/friskolator/{0}/".format(photo_id)
    info["img"] = photo_url
    info["metadata"]["photo_title"] = photo.get("title")
    info["metadata"]["photo_id"] = photo.get("id")
    info["metadata"]["photo_owner_nsid"] = photo.get("owner")

    #xmlnode = flickr.photos_getInfo(photo_id=photo_id, format="xmlnode")
    etree = flickr.photos_getInfo(photo_id=photo.get("id"))
    for node in etree.iter():
        #print node.tag, node.attrib

        if node.tag == "owner":
            info["name"] = node.attrib["realname"]
            info["metadata"]["username"] = node.attrib.get("username")
            info["metadata"]["realname"] = node.attrib.get("realname")
            info["metadata"]["location"] = node.attrib.get("location")
        elif node.tag == "title":
            pass
        elif node.tag == "description":
            pass
        elif node.tag == "comments":
            pass
        elif node.tag == "dates":
            info["metadata"]["date_taken"] = node.attrib.get("taken")
            info["metadata"]["date_updated"] = node.attrib.get("lastupdate")
            info["metadata"]["date_posted"] = node.attrib.get("posted")
        elif node.tag == "note":
            pass
            #print node.attrib
            #note_id = node.attrib.get("id")
            #text = node.text
            #x, y = node.attrib["x"], node.attrib["y"]
            #w, h = node.attrib["w"], node.attrib["h"]
            #print "note %s at %s %s %s %s " % ( text, x, y, w, h)
            #print photo_id, note_id

    pprint(info)
    filename = "{0}.json".format(photo_id)
    with open(os.path.join(stream.event_data_dir, filename), "w") as f:
        f.write(json.dumps(info, indent=4))
