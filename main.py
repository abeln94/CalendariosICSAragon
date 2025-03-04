import datetime
import os

import requests
from bs4 import BeautifulSoup

from ics import Calendar

FROM_YEAR = 2018  # first year with full ICS calendars


def get_calendar_from_main_page(html, label):
    """Returns a calendar whose url is extracted from a previously fetched page, or None if not found"""
    # find label
    marker = html.find(string=label)
    if marker is None:
        print(f"Calendar with label '{label}' was not found")
        return None

    # search link
    href = None
    for sibling in marker.parent.next_siblings:
        if sibling == '\n':
            continue
        if 'title' in sibling['class']:
            # not found
            print(f"Next title found before ICS link for calendar with label '{label}'")
            return None
        a = sibling.find("a")
        if a == -1:
            continue
        ahref = a['href']
        if ahref.endswith(".ics"):
            href = ahref
            break
    if href is None:
        print(f"ICS link was not found for calendar with label '{label}'")
        return None

    # download
    print("->", href)
    req = requests.get(href)
    req.encoding = 'UTF-8'  # fix for wrong server encoding
    return Calendar(req.text)


# fetch pages
year_pages = []
for year in range(FROM_YEAR, datetime.date.today().year + 1 + 1):
    print("Requesting page for year", year)
    page = BeautifulSoup(requests.get(
        f"https://opendata.aragon.es/datos/catalogo/dataset/calendario-de-festivos-en-comunidad-de-aragon-{year}").text,
                         'html.parser')
    year_pages.append((year, page))

# generate base calendar
base_calendar = Calendar()
for year, page in year_pages:
    print("Requesting base calendar for year", year)
    calendar = get_calendar_from_main_page(page, f"Calendario de festivos en Comunidad de Aragón {year}")
    if calendar is None:
        print("Removed calendar for year", year)
        year_pages.remove((year, page))
        continue
    base_calendar.events.update(calendar.events)

# generate other events
other_events = set()
for year, page in year_pages:
    for location in ["Zaragoza", "Teruel", "Huesca"]:
        print("Requesting calendar for location", location, "and year", year)
        calendar = get_calendar_from_main_page(page, f"Calendario de festivos en provincia de {location} {year}")
        if calendar is None: continue
        other_events.update(calendar.events)

# generate calendars
# locations are normalized as lowercase, since github doesn't support two files with the same name
for location in set(event.location.lower() for event in other_events):
    print("Generating calendar for location", location)
    clone = base_calendar.clone()
    for event in other_events:
        if event.location.lower() == location.lower():
            clone.events.add(event)

    # sort events by date
    clone.events = sorted(clone.events, key=lambda e: e.begin)

    # save as file
    file_name = f'ics/{location.replace("/", "_")}.ics'
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(clone.serialize().replace("\r\n", "\n"))
