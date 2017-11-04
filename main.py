# -*- coding: utf-8 -*-

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import content


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


SHOWS_DATA = content.get_shows_data()
SHOWS_BY_ID = content.get_shows_by_id(SHOWS_DATA)
GENRES = content.get_genres(SHOWS_DATA, SHOWS_BY_ID)
SHOW_SECTIONS = {}


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.
    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_categories():
    """
    Create the list of show categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Tous les contenus par genre')
    # Set plugin content. It allows Kodi to select appropriate views for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

    categories = GENRES
    # Iterate through categories
    for key, category in categories.items():
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['label'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        list_item.setArt({'thumb': category['thumb'],
                          'icon': category['thumb'],
                          'fanart': category['thumb']})
        # Set additional info for the list item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category['label'], 'genre': category['label']})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=key)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_shows(category_id):
    """
    Create the list of shows for a specified category in the Kodi interface.
    """

    # Get category details
    category = GENRES[category_id]

    # Set plugin category. It is displayed in some skins as the name of the current section.
    xbmcplugin.setPluginCategory(_handle, category['label'])
    # Set plugin content. It allows Kodi to select appropriate views for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

    shows = category['items']
    # Iterate through shows
    for item_id in shows:
        item = SHOWS_BY_ID[item_id]
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item['title'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        list_item.setArt({'thumb': item['image-background'],
                          'icon': item['image-background'],
                          'fanart': item['image-background'],
                          'landscape': item['image-landscape']})
        # Set additional info for the list item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': item['title'],
                                    #'plot' : item['description'],
                                    'genre': category['label']})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='section-listing', show=item_id)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_sections(show_id):
    """
    Create the list of sections for a specified show in the Kodi interface.
    """

    # Get show sections
    if show_id in SHOW_SECTIONS:
        sections = SHOW_SECTIONS[show_id]
    else:
        SHOW_SECTIONS[show_id] = content.get_show_sections(SHOWS_BY_ID[show_id])
        sections = SHOW_SECTIONS[show_id]

    # Set plugin category. It is displayed in some skins as the name of the current section.
    xbmcplugin.setPluginCategory(_handle, SHOWS_BY_ID[show_id]['title'])
    # Set plugin content. It allows Kodi to select appropriate views for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

    # Iterate through sections
    for key, section in sections.items():
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=section['title'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        list_item.setArt({'thumb': section['thumb'],
                          'icon': section['thumb'],
                          'fanart': section['thumb']})
        # Set additional info for the list item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': section['title']})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='videos-listing', show=show_id, section=key)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(show_id, section_id):
    """
    Create the list of playable videos in the Kodi interface.
    """

    # Get show sections
    if show_id in SHOW_SECTIONS:
        sections = SHOW_SECTIONS[show_id]
    else:
        SHOW_SECTIONS[show_id] = content.get_show_sections(SHOWS_BY_ID[show_id])
        sections = SHOW_SECTIONS[show_id]

    section = sections[section_id]

    # Set plugin category. It is displayed in some skins as the name of the current section.
    xbmcplugin.setPluginCategory(_handle, section['title'])
    # Set plugin content. It allows Kodi to select appropriate views  for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

    videos = section['items']
    # Iterate through videos.
    for key, video in videos.items():
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['title']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        img_back = video['image-background']
        img_land = img_back
        if 'image-landscape' in video:
            img_land = video['image-landscape']
        list_item.setArt({'thumb': img_back,
                          'landscape': img_land,
                          'icon': img_back,
                          'fanart': img_back})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['id'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(video_id):
    """
    Play a video by the provided path.
    :param path: Fully-qualified video URL
    :type path: str
    """

    path = content.get_video_url(video_id.replace('_', ''))

    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of shows in a provided category.
            list_shows(params['category'])
        elif params['action'] == 'section-listing':
            # Display the list of videos in a provided show.
            list_sections(params['show'])
        elif params['action'] == 'videos-listing':
            # Display the list of videos in a provided show.
            list_videos(params['show'], params['section'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])