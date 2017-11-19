# -*- coding: utf-8 -*-
# encoding=utf8

#import urllib2, simplejson, parse, cache, re, xbmcaddon, html, xbmc, datetime, time
#import urlparse

import xbmcaddon, xbmc
import urllib2, simplejson
import html
from BeautifulSoup import BeautifulSoup

BASE_HOST = 'videos.tva.ca'
BASE_URL = 'https://' + BASE_HOST

PROXY_URL = BASE_URL + '/proxy/page'
UUID = 'dead3540-701e-452f-b2d9-629c652f7038'
APPID = '5955fc5f23eec60006c951f1'
GENRES_URL = PROXY_URL + '/contenus?appId=' + APPID + '&uuid=' + UUID

VIDEOS_URL = 'https://edge.api.brightcove.com/playback/v1/accounts/5481942443001/videos/'


def get_json_data( url ):
    #todo cache
    opener = urllib2.build_opener()
    opener.addheaders = [('accept', 'application/json')]
    response = opener.open(url)
    data = simplejson.load(response)

    return data


def get_shows_data():
    return get_json_data(GENRES_URL)


def get_shows_by_id( shows_data ):
    shows_list = {}
    for show in shows_data['item']:
        attributes = {'id' : show['id']}
        for attr in show['attributes']:
            attributes.update({attr['key'] : attr['value']})
        shows_list.update({show['id'] : attributes})

    return shows_list


def get_genres( shows_data, shows_by_id ):
    genres_list = {}
    for genre in shows_data['container']:
        if 'title' in genre:
            items = genre['itemId']
            genres_list.update({genre['id']: {'id'    : genre['id'],
                                              'label' : u(genre['title']),
                                              'items' : items,
                                              'thumb' : shows_by_id[items[0]]['image-background']}})

    return genres_list


def get_show_sections( show ):
    url = PROXY_URL + '/' + show['pageAlias'] + '?appId=' + APPID + '&uuid=' + UUID
    data = get_json_data(url)

    videos_list = {}
    for video in data['item']:
        if video['typeId'] == 'go-item-video':
            attributes = {'id' : video['id']}
            for attr in video['attributes']:
                attributes.update({attr['key'] : attr['value']})
            videos_list.update({video['id'] : attributes})

    sections_list = {}
    for section in data['container']:
        if 'itemId' in section:
            items = {}
            for item_id in section['itemId']:
                if item_id in videos_list:
                    items.update({item_id : videos_list[item_id]})

            if items:
                first_video = videos_list[section['itemId'][0]]
                thumb = show['image-background']
                if 'image-background' in first_video:
                    thumb = first_video['image-background']
                elif 'image-landscape' in first_video:
                    thumb = first_video['image-landscape']
                sections_list.update({section['id']: {'id'    : section['id'],
                                                      'title' : u(section['title']),
                                                      'items' : items,
                                                      'thumb' : thumb}})

    return sections_list


def get_video_url( video_id ):
    #TODO text tracks
    xbmc.log(VIDEOS_URL + video_id);

    opener = urllib2.build_opener()
    opener.addheaders = [('Accept', 'application/json;pk=BCpkADawqM1hywVFkIaMkLk5QCmn-q5oGrQrwYRMPcl_yfP9blx9yhGiZtlI_V45Km8iey5HKLSiAuqpoa1aRjGw-VnDcrCVf86gFp2an1FmFzmGx-O-ed-Sig71IJMdGs8Wt9IyGrbnWNI9zNxYG_noFW5dLBdPV3hXo4wgTzvC2KvyP4uHiQxwyZw'),
                         ('Origin', 'https://videos.tva.ca'),
                         ('Referer', 'https://videos.tva.ca/')]
    response = opener.open(VIDEOS_URL + video_id)
    data = simplejson.load(response)

    bitrate = 0
    for source in data['sources']:
        if 'avg_bitrate' in source:
            if source['avg_bitrate'] > bitrate:
                bitrate = source['avg_bitrate']
                url = source['src']

    return url



#def get_videos(category):
#    """
#    Get the list of videofiles/streams.
#    Here you can insert some parsing code that retrieves
#    the list of video streams in the given category from some site or server.
#    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
#        instead of returning lists.
#    :param category: Category name
#    :type category: str
#    :return: the list of videos in the category
#    :rtype: list
#    """
#    return VIDEOS[category]


def u(data):
    return data.encode("utf-8")