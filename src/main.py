#!/usr/bin/env python3

from time import sleep
from datetime import date
import os.path
import requests
import xml.etree.ElementTree as ET
from shows import shows

def get_episodes(shows):
    episodes = {}

    def api_call(url):
        status_code = 0
        while status_code != 200:
            response = requests.get(url)
            status_code = response.status_code
            if status_code != 200:
                sleep(2)
        return response.json()

    for show_id in shows:
        show_data = api_call(f'https://api.tvmaze.com/shows/{show_id}?embed=nextepisode')

        if '_embedded' in show_data and 'nextepisode' in show_data['_embedded']:
            episodes[show_id] = show_data['_embedded']['nextepisode']

            air_date = date.fromisoformat(episodes[show_id]['airdate'])
            hh, mm = episodes[show_id]['airtime'].split(":") if len(episodes[show_id]['airtime']) > 0 else ['00', '00']
            episodes[show_id]['formatted_date'] = air_date.strftime(f"%a, %d %b %Y {hh}:{mm}:%S GMT")
            
            if 'medium' in show_data['image']:
                episodes[show_id]['image'] = show_data['image']['medium']

    return episodes

def build_item(el_parent, key, episode):
    rss_item = ET.SubElement(el_parent, 'item')
    item_guid = ET.SubElement(rss_item, 'guid')
    item_guid.text = f"{key}-{episode['id']}"
    item_title = ET.SubElement(rss_item, 'title')
    item_title.text = episode['_links']['show']['name']
    item_description = ET.SubElement(rss_item, 'description')
    item_description.text = f"""<h1>{episode['name']}</h1>
<p><b>Season {episode['season']} Epsiode {episode['number']}</b></p>
<p><i>{episode['formatted_date']}</i></p>
{episode['summary']}"""
    item_pubDate = ET.SubElement(rss_item, 'pubDate')
    item_pubDate.text = episode['formatted_date']
    if 'image' in episode:
        item_enclosure = ET.SubElement(rss_item, 'enclosure')
        item_enclosure.set('url', episode['image'])
        item_enclosure.set('length', '0')
        item_enclosure.set('type', 'image/jpeg')

def write_rss(path, episodes):
    # Declare namespaces
    ET.register_namespace('', 'http://www.w3.org/2005/Atom')
    # create root element and set attributes
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

    # add child elements to root
    rss_channel = ET.SubElement(rss, 'channel')
    
    atom_link = ET.SubElement(rss_channel, 'atom:link')
    atom_link.set('href', 'https://tv.aaronwatts.dev/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'applications/rss+xml')

    rss_title = ET.SubElement(rss_channel, 'title')
    rss_title.text = 'TV Shows'
    rss_link = ET.SubElement(rss_channel, 'link')
    rss_link.text = 'https://tv.aaronwatts.dev'
    rss_description = ET.SubElement(rss_channel, 'description')
    rss_description.text = 'Updates of new episodes of TV shows on my list of favourites'

    # create item per episode
    for key in episodes:
        episode = episodes[key]
        build_item(rss_channel, key, episode)

    tree = ET.ElementTree(rss)
    ET.indent(tree)
    tree.write(f'docs/{path}.xml', xml_declaration='version', encoding='UTF-8')

def update_rss(path, episodes):
    tree = ET.parse(f"docs/{path}.xml")
    root = tree.getroot()
    rss_channel = root[0]

    for item in root.iter('item'):
        show_id, episode_id = item[0].text.split('-')

        # update show item if out of date
        if show_id in episodes:
            episode = episodes[show_id]
            if not str(episode_id) == str(episode['id']):
                for element in item:
                    if element.tag == 'guid':
                        element.text = f"{show_id}-{episode['id']}"
                    elif element.tag == 'title':
                        element.text = episode['name']
                    elif element.tag == 'description':
                        element.text = f"Season {episode['season']} Epsiode {episode['number']}"
                    elif element.tag == 'pubDate':
                        element.text = episode['airstamp']
                if 'enclosure' not in item:
                    enclosure = ET.SubElement(item, "enclosure")
                    enclosure.set("url", episode["image"])
                    enclosure.set("length", "0")
                    enclosure.set("type", "image/jpeg")

            del episodes[show_id]
    
    # add missing shows
    for show in episodes:
        build_item(rss_channel, show, episodes[show])

    ET.indent(tree)
    tree.write(f"docs/{path}.xml")

def main():
    path = "feed"
    episodes = get_episodes(shows)
    
    if not os.path.isfile(f'docs/{path}.xml'):
        write_rss(path, episodes)
    else:
        update_rss(path, episodes)

if __name__ == "__main__":
    main()