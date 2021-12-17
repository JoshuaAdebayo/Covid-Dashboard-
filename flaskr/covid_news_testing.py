"""
In this module I test functions within covid_news_handling.py
"""
import sched
import time

from covid_news_handling import news_API_request
from covid_news_handling import schedule_news_updates

def test_news_API_requests():
	news = news_API_request("Covid Covid-19 coronavirus")
	assert len(news) > 1
    
def test_schedule_news_updates():
        s = sched.scheduler(time.time, time.sleep)
        assert len(s.queue) == 0 
        schedule_news_updates(5, "test")
        assert len(s.queue) == 1
        s.run(blocking = False)
        assert len(s.queue) == 1
        time.sleep(5)
        assert len(s.queue) == 0 
 
