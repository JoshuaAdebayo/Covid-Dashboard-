"""
In this module I import json and requests and right a function,
news_API_request() which outputs a list of dictionaries related to covid-19
"""
import time 
import json
import sched 
import logging
import requests

with open("config.json") as config_json:
    config = json.load(config_json)
def news_API_request(covid_terms= config["Main details"]["terms"]):
    """
    This function searches for news articles related to covid-19 and returns a list
    of dictionaries that holds the information.

    Parameters:
    covid_terms  = 'Covid COVID-19 coronavirus' - string

    Returns:
    articles['articles'] - list
    """
    api_key = {'Authorization':config["Main details"]['Key']}

    all_news = config["Main details"]["Url"]
    covid_payload = {'q':covid_terms, 'language':config["Main details"]["Language"],
    'sortBy': config["Main details"]["Sort"]}
    try:
        response = requests.get(url = all_news,headers = api_key,params = covid_payload)
        raw_articles = json.dumps(response.json())
        articles = json.loads(raw_articles)
        logging.info("News articles related to the covid pandemic have been retreived")
    except requests.exceptions.ConnectionError as error:
        logging.error("Unable to retreive news articles, %s" ,error)
    return articles['articles']

def schedule_news_updates(update_interval, update_name):
    """
    This function schedules for new articles to be searched for
    Parameters:
    update_interval, update_name
    """
    s = sched.scheduler(time.time, time.sleep)
    s.enterabs(time.time() + update_interval, 1,news_API_request(),(update_name))
    
