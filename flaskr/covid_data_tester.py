"""
In this module I test functions within covid_data_handler.py
"""
import csv
from covid_data_handler import parse_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_csv_data

def test_parse_csv_data():
    """
    Testing the parse_csv_data function
    """
    data = parse_csv_data( 'nation_2021-10-28.csv')
    assert len(data) == 639


def test_covid_API_request():
    """
    In this function I test the covid_API_request function
    """
    data = covid_API_request("Leeds", "ltla")
    assert len(data) > 1
    
def test_process_covid_csv_data():
    """
    Testing the process_covid_csv_data function
    """
    last7days_cases , current_hospital_cases , total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141544
