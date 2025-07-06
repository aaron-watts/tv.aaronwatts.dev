#!/usr/bin/env python3

import requests
from datetime import date
from shows import shows
import json

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

    return episodes

def main():
    schedule = {"schedule": get_episodes(shows)}
    with open("schedule.json", "w") as fp:
        json.dump(schedule, fp, indent=4)

if __name__ == "__main__":
    main()