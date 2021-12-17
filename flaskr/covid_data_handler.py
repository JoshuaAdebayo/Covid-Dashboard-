"""
In this module I write functions that retrieve covid related data using the
uk_covid19 module. I also have functions the parse csv data and to extract certain
information that I looking for
Additionally, all scheduling related functions are written in this module, as well as
functions that remove scheduled news, data or presisting news articles.
"""

import csv
import time
import json
import sched
import logging
import datetime

from datetime import datetime
from uk_covid19 import Cov19API

import covid_news_handling

s = sched.scheduler(time.time, time.sleep)

with open("config.json") as config_json:
    config = json.load(config_json)

search_structures = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
 }

def parse_csv_data(csv_filename):
    """
This function takes a csv file and puts it into a list

Parameters:
csv_filename - csv

Returns:
covid_data - list
"""
    covid_data = []
    with open(csv_filename,'r') as filename:
        file = csv.reader(filename)
        heading = next(file)
        [covid_data.append(r_w) for r_w in filename]
        covid_data.insert(0, heading)
    return covid_data

def col_place(title):
    """
This function finds the column which had the inputed title
    """
    ta_l = 0
    for heading in search_structures:
        if title == heading:
            return ta_l
        ta_l += 1
    return -1

def row_finder(list_, column):
    """
In this function I find the first empty row of the chosen column
    """
    ta_l = 1
    while ta_l < len(list_):
        if list_[ta_l][column] != "":
            return ta_l
        ta_l += 1
    return -1
def process_covid_csv_data(covid_csv_data):
    """
In this function I take a list of dictionaries and extract information
on how many current hospital cases, total deaths and cases within the last
week of covid-19.

Parameters:
covid_csv_data - list
Returns:
final - list
 """
    deaths = 0
    weeks_cases = 0
    active_cases = 0
    col = col_place("cumDailyNsoDeathsByDeathDate")
    row = row_finder("cumDailyNsoDeathsByDeathDate" ,col)
    if row != -1 and col != -1:
        deaths = int(covid_csv_data[row][col])

    col = col_place("hospitalCases")
    row = row_finder("hospitalCases", col)
    if row != -1 and col != -1:
        active_cases = int(covid_csv_data[row][col])

    col = col_place("newCasesBySpecimenDate")
    row = row_finder(covid_csv_data, col)
    if row != -1 and col != -1:
        row += 1
        ta_l = 0
        while ta_l < 7 :
            weeks_cases += (covid_csv_data[row][col])
            row += 1
            ta_l += 1
    return deaths, active_cases, weeks_cases                      

def covid_API_request(location = 'Exeter', location_type = 'ltla'):
    """
This function takes a location and location type and uses it to search for covid
related data about the location.

Parameters:
location = 'Exeter'
location_type = 'ltla'

Returns:
data_ - list
"""
    try:
        location_filters = ['areaType='+location_type,
        'areaName='+location]
        api = Cov19API(filters = location_filters, structure = search_structures)
        data = api.get_json()
        data_ = data['data']
        return data_
    except FileNotFoundError as error:
        logging.info("Error in parsing data, %s", error)
def process_data():
    """
    In this function I run the covid_API_request function twice to get data about
    a local region and all of England. The number of cases, deaths in the post week,
    and infection rate locally and nationally are calculated.
    Returns:
    [deaths, active_cases, l_infectionr, n_infectionr] - list
    """
    local = covid_API_request(location = config['Main details']['Location'],
    location_type = config['Main details']['Location_type'])
    nation = covid_API_request(location = config['Main details']['Nation'],
    location_type = config['Main details']['Nation_type'])

    row = 1
    l_cases = 0
    n_cases = 0

    while row < 9:
        l_cases += local[row]["newCasesBySpecimenDate"]
        n_cases += nation[row]["newCasesBySpecimenDate"]
        row += 1
    deaths = 0
    for n_a in nation:
        if n_a["cumDailyNsoDeathsByDeathDate"] is None:
            pass
        else:
            deaths = n_a["cumDailyNsoDeathsByDeathDate"]
            l_infectionr = l_cases/7
            n_infectionr = n_cases/7
            active_cases = nation[1]["hospitalCases"]

    return [deaths, active_cases, l_infectionr, n_infectionr]

TALLY = 0
ALARMS =[]

def update_schedule(title, update_time, repeats, data, news):
    """
    This is the function that is activated once someone tries to schedule
    an operation on the user interface. It gets the current time and puts
    it into hours and minutes in string form then converts it make into
    a datetime object. Then the scheduled time is converted into a datetime object
    the 2 times are then subtracted and put through the schedule_covid_updates function
    """
    global TALLY
    TALLY += 1
    header = "Update" +str(TALLY) + " " + title

    try:
        include_updates(header, update_time, repeats, data, news)
    except FileNotFoundError as error:
        logging.info("Error in parsing data, %s", error)
        include_updates(header, update_time, repeats, data, news)

def include_updates(header, timing, repeats, data, news):
    """
    This function takes information from the user interface and puts it
    into a list that will be presented on the website.
    """

    if timing is not None:
        counter = timing
    else:
        counter = "No time input"

    ALARMS.append({'title' : header,
    'content' : 'Time till update ' + counter + '. Repeating: ' + str(repeats)
                   + '. Data: ' + str(data) + '. News: ' + str(news),
                   'repeats' : repeats})
    logging.info("New update: %s", header)


def update_deleter(name):
    """
    This function deletes a selected article that has been selected
    in the user interface
    """
    for a_s in ALARMS:
        if name == a_s["title"]:
            ALARMS.remove(a_s)

def update_picker(name):
    """
    This function selects the right update to be returned
    """

    for a_s in ALARMS:
        if name == a_s["title"]:
            return a_s
    return None

def update_remover(name):
    """
    This function deletes an update from the user interface and also cancels
    the scheduled update.
    """
    for a_s in ALARMS:
        if name == a_s["title"]:
            s.cancel(a_s["event"])
            logging.info("Scheduled event has been terminated")
