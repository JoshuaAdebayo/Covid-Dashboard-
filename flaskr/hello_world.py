"""
This module is what some may call the central hub of the covid dashboard
as it calls functions from several other modules and does all the rendering
of data onto the web app. Additionally, logging is set up within this module
so that logging can be done in all the other modules.
"""

import sched
import json
import time
import logging

from flask import Flask
from flask import render_template
from flask import request

import covid_data_handler
import covid_news_handling

with open("config.json") as config_json:
    config = json.load(config_json)

news = covid_news_handling.news_API_request()
final_updates_ = covid_data_handler.ALARMS
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__, instance_relative_config = True)


logging.basicConfig(filename = config["Logging"]["file"],
format = config["Logging"]["format"],
level = config["Logging"]["level"],
filemode = config["Logging"]["filemode"],
force = True,
style = "{")

logging.info("App is operational")
@app.route('/')
@app.route('/index')

def index():
    """
    Within this function I render all the necessary information into the
    web app and use 'request.args.get(...)' to do thing upon the user interface
    such as deleting articles and scheduled requests.
    """
    deleted_alarm = request.args.get("update_item")
    news_title = request.args.get("notif")
    scheduled_update_title = request.args.get("alarm_item")
    update_title = request.args.get("two")

    if scheduled_update_title is not None:
        logging.info("Get request for 'alarm_item'")
        covid_data_handler.update_deleter(scheduled_update_title)
        covid_data_handler.update_remover(scheduled_update_title)
    if deleted_alarm is not None:
        logging.info("Get request for 'update_item'")
        for update in final_updates_:
            if update["title"] == deleted_alarm:
                final_updates_.remove(update)
            else:
                pass
    if news_title is not None:
        logging.info("Get request for 'notif'")
        for article in news:
            if article["title"] == news_title:
                news.remove(article)
            else:
                pass
    if update_title is not None:
        logging.info("Get request for 'two'")
        update_time = request.args.get("alarm")
        repeating = request.args.get("repeat")
        new_data = request.args.get("covid-data")
        new_news = request.args.get("news")
        covid_data_handler.update_schedule(update_title, update_time,
        repeating, new_data, new_news)

    logging.info("Scheduler events running")
    s.run(blocking = False)

    local_national = covid_data_handler.process_data()
    deaths = local_national[0]
    active_cases = local_national[1]
    l_infectionr = round(local_national[2])
    n_infectionr = round(local_national[3])


    return render_template(config['Main details']['Template_path'], news_articles = news,
    hospital_cases = active_cases, death_total = deaths,local_7day_infections = l_infectionr,
    nation_location = config['Main details']['Nation'],
                           location = config['Main details']['Location'],
    updates = final_updates_,national_7day_infections = n_infectionr,
    image = config['Main details']['Image'], title = config['Main details']['Title'])
if __name__ == '__main__':
    app.run(debug = True)
