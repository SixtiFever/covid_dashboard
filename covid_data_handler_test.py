"""  Testing module for covid_data_handler functions  """

from covid_data_handler import covid_API_request, parse_csv_data, process_covid_csv_data
import json

""" I am expecting 638 since I popped the title row in the function """
def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 638

def test_process_csv_data():
    data = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    cases_7_days, current_hospital_cases, total_deaths = data[2], data[1], data[0]
    assert total_deaths == 141544
    assert current_hospital_cases == 7019
    assert cases_7_days == 240299

""" Asserting the correct number of metrics have been pulled by the api """
def test_covid_API_request():
    api_pull = covid_API_request('London', 'region')
    for i in api_pull['data']:
            assert len(i) == 6


