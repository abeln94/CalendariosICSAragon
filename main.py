import datetime
import os

import requests
from bs4 import BeautifulSoup

from ics import Calendar


def getCalendarFromHtml(html, label):
    """Returns a calendar whose url is extracted from a previously fetched page, or None if not found"""
    marker = html.find(string=label)
    if marker is None: return None
    req = requests.get(marker.next_element.next_element.find("a").get("href"))
    req.encoding = 'UTF-8'  # fix for wrong server encoding
    return Calendar(req.text)


current_year = datetime.date.today().year

# fetch pages
year_pages = []
for year in [current_year - 1, current_year, current_year + 1]:
    print("Requesting page for year", year)
    page = BeautifulSoup(requests.get(
        f"https://opendata.aragon.es/datos/catalogo/dataset/calendario-de-festivos-en-comunidad-de-aragon-{year}").text,
                         'html.parser')
    year_pages.append((year, page))

# generate base calendar
base_calendar = Calendar()
for year, page in year_pages:
    print("Requesting base calendar for year", year)
    calendar = getCalendarFromHtml(page, f"Calendario de festivos en Comunidad de Aragón {year}")
    if calendar is None: continue
    base_calendar.events.update(calendar.events)

# generate other events
other_events = set()
for year, page in year_pages:
    for location in ["Zaragoza", "Teruel", "Huesca"]:
        print("Requesting calendar for location", location, "and year", year)
        calendar = getCalendarFromHtml(page, f"Calendario de festivos en provincia de {location} {year}")
        if calendar is None: continue
        other_events.update(calendar.events)

# generate calendars
for location in set(event.location for event in other_events):
    print("Generating calendar for location", location)
    clone = base_calendar.clone()
    for event in other_events:
        if event.location == location:
            clone.events.add(event)

    # sort events by date
    clone.events = sorted(clone.events, key=lambda e: e.begin)

    # save as file
    file_name = f'ics/{location.replace("/", "_")}.ics'
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(clone.serialize().replace("\r\n", "\n"))
