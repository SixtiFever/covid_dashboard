import os
import sched, time, json, logging
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from covid_news_handling import update_news, remove_article, news_list
from uk_covid19 import Cov19API
from types import DynamicClassAttribute

""" importing and locally assigning config.json """
jsonfile = open('Documentation/config.json', 'r')
config = json.load(jsonfile)

""" setting up logging """
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
logging.basicConfig(filename='sys.log' ,level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

""" calling sched and flask object, assigning to variable """
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

""" global data structs to place pulled data in, which will then be returned via render_template """
data_dict = dict()
sched_list = list()

""" to populate an initial news feed upon first load """
news_list.append(update_news())




##################### FLASK ###############################

""" http://127.0.0.1:5000/index """

@app.route('/index')
def update():

    """ Populating dashboard on start-up. Then ensuring it doesn't overwrite dict on every refresh.
    It's always len 0 on start-up, but once populated, covid_update will keep replacing dict items """
    if len(data_dict) == 0:
        covid_update()
    remove_article()
    if request.args.get('two'):
        update_name, update_interval = request.args.get('two'), request.args.get('update')

        schedule_covid_updates(update_name, update_interval)

    s.run(blocking=False)

    return render_template('index.html', hospital_cases = data_dict['hospital_cases'], 
    deaths_total = data_dict['total_deaths'], national_7day_infections = data_dict['national_7day_rate'], 
    local_7day_infections = data_dict['local_7day_rate'], nation_location = data_dict['nation_location'],
    location = data_dict['area_name'], updates = sched_list, news_articles = news_list,
    image = 'covid_19.jpg' )


""" 

READ FROM DATA FILE
extract required data from nation_2021 csv

"""

def parse_csv_data(csv_filename: str):
    logger.debug('- Opening and reading .csv file')
    """ try-except to catch any errors when openine file """
    try:
        covid_data = open(csv_filename)
    except FileNotFoundError as err:
        logger.error(err, 'File not found in package')
    else:
        covid_data_list = []
        covid_data_csv = covid_data.readlines()
        """ remove title row """
        covid_data_csv.pop(0)
        logger.debug('- Iterating, stripping and appending .csv data to new list')
        for data_item in covid_data_csv:
            data_item = data_item.strip().lower()
            covid_data_list.append(data_item)
    return covid_data_list


""" 

DATA PROCESSING
function to format and iterate through data in the .csv file. Extracting specified data

"""

def process_covid_csv_data(covid_csv_data):
    all_cases_by_specimen = []
    alph_numbers_list_deaths = []
    hospital_cases = []

    logger.info('- for loop pulling covid metrics')
    try:
        for data_row in covid_csv_data:
            data_row = data_row.split(',')
            """ calculting the cumulative deaths """
            if data_row[4] == '':
                data_row[4] = 0
            alph_numbers_list_deaths.append(data_row[4])

            """ filtering hospital cases and appending to new list for easier manipulation """
            if data_row[5] == '':
                data_row[5] = 0
            hospital_cases.append(data_row[5])

            """ cases for last 7 days """
            all_cases_by_specimen.append(data_row[6])
    except IndexError as index_err:
        logger.error(index_err, 'Error iterating through .csv data')
    except Exception as error:
        logger.error(error)
    
    else:
        cases_last_7_days = all_cases_by_specimen[2:9]
        """ formatting for output  """
        logger.debug('- Converting to int lists')
        int_numbers_list_deaths = convert_list(alph_numbers_list_deaths)
        current_hospital_cases = convert_list(hospital_cases)
        int_cases_last_7_days = convert_list(cases_last_7_days)
        sum_of_cases_7_days = sum(int_cases_last_7_days)
        """ [13] since i popped the title row in parse function """
        return int_numbers_list_deaths[13], current_hospital_cases[0], sum_of_cases_7_days




""" 

LIVE DATA ACCESS
requesting and assigning the PHE covid data api

"""
def covid_API_request(location = 'Exeter', location_type = 'ltla') -> dict:
    filter_list = [f'areaType={location_type}', f'areaName={location}'] 
    pulled_data = {
    'date': 'date',
    'areaName': 'areaName',
    'areaCode': 'areaCode',
    'newCasesByPublishDate': 'newCasesByPublishDate',
    'hospitalCases':'hospitalCases',
    'totalDeaths':'newDailyNsoDeathsByDeathDate'
    }
    logger.critical('- Pulling PHE API and placing in py variable')
    try:
        api = Cov19API(filters=filter_list,structure=pulled_data)
        pyth_obj = api.get_json()
    except Exception:
        logger.critical('Error pulling PHE API')
    finally:
        return pyth_obj



"""

SCHEDULE COVID UPDATES
function to create schedules. Takes name and update time. 
Data and news to be shown in the interface are customised via config.json.

"""

def schedule_covid_updates(update_name: str, update_interval: str) -> None:

    covid_arg = request.args.get('covid-data')
    news_arg = request.args.get('news')
    repeat = request.args.get('repeat')

    """ creating and appending new sched list item """
    sched_item = {'title':f'{update_name}' , 'content':f'{update_interval}'}

    """ defining time interval based on form input """
    logger.debug('- Converting form input to secs to wait')
    secs_until = secs_to_wait(hh_mm(update_interval))
    sched_list.append(sched_item)

    """ creating sched event based on which interface checkbox is ticked """
    logger.info('- Covid-data checked')
    if covid_arg:
        s.enter(secs_until, 1, covid_update, argument=(config['interface_data']['area_name'], config['interface_data']['nation']))
        s.run(blocking=False)
    logger.info('- news checked')
    if news_arg:
        s.enter(secs_until, 1, update_news, kwargs={'keyword':config['interface_data']['news_kw']})
        s.run(blocking=False)
    if repeat and news_arg:
        s.enter(secs_until, 1, update_news, kwargs={'keyword':config['interface_data']['news_kw']})
        s.enter(86400, 1, update_news, kwargs={'keyword':config['interface_data']['news_kw']})
        s.run(blocking=False)
    if repeat and covid_arg:
        s.enter(secs_until, 1, covid_update, argument=(config['interface_data']['area_name'], config['interface_data']['nation']))
        s.enter(86400, 1, covid_update, argument=(config['interface_data']['area_name'], config['interface_data']['nation']))
        s.run(blocking=False)

    """ removing sched item at index 0 after the event has been executed """
    if repeat is None:
        logger.debug('- Remove sched item')
        s.enter(secs_until+1, 1, remove_sched_event, argument=(sched_item,))
    return None




""" 

Extra functions

"""


""" Function that collates all data needed for interface """
def covid_update(local_area = 'Exeter', nation = 'England'):
    """ set empty data structs for appending to """
    total_deaths = 0

    """ setting national data for hospital cases and total deaths """
    logger.info('- Call API for hospitl cases and total deaths')
    try:
        local_data_dict = covid_API_request('England','nation')
        hospital_cases = local_data_dict['data'][0]['hospitalCases']
    except Exception:
        logger.error('Error assigning covid API call to local_data_dict')
    else:
        for data_item in local_data_dict['data']:
            if data_item['totalDeaths'] is not None:
                total_deaths += data_item['totalDeaths']
    
    """ specifying data for a selected nation in the last 7 days """
    logger.info('- Call API and slicing list for last 7 days (national)')
    try:
        sliced_list_for_national = covid_API_request(f'{nation}', 'nation')['data'][0:7]
    except Exception:
        logger.error('Error assigning sliced list for nation')
    else:
        last_7_days_national = list()
        for data_item in sliced_list_for_national:
            daily_national_cases = data_item['newCasesByPublishDate']
            if daily_national_cases is not None:
                last_7_days_national.append(daily_national_cases)
        national_rate = sum(last_7_days_national)

    """ specifying data for a selected city in the last 7 days """
    logger.info('- Call API and slicing list for last 7 days (local)')
    try:
        sliced_list_for_local = covid_API_request(f'{local_area}', 'ltla')['data'][0:7]
    except Exception:
        logger.error('Error assigning sliced list for local')
    else:
        last_7_days_local = list()
        for data_item in sliced_list_for_local:
            daily_local_cases = data_item['newCasesByPublishDate']
            if daily_local_cases is not None:
                last_7_days_local.append(daily_local_cases)
        local_rate = sum(last_7_days_local)

    """ assigning data to dict. All data here is what's needed for the interface """
    logger.info('- Assigning to metrics to corresponding interface units')
    local_dict = {'hospital_cases':f'{hospital_cases}', 'total_deaths':f'{total_deaths}', 
    'national_7day_rate':f'{national_rate}', 'local_7day_rate':f'{local_rate}',
    'area_name':f'{local_area}', 'nation_location':f'{nation}'}

    """ updating global dict with local dict data """
    logger.debug('- Update global dict with local dict')
    data_dict.update(local_dict)
    return None


""" Function to convert hours and minutes into seconds since 00:00. 
Input format must be 24 hours and type str e.g '13:00' """
def hh_mm(str_number: str):
    num = str_number.split(':')
    int_list = list(map(int, num))

    """ try-except to catch any errors with converting the str list to int list """
    try:
        hours_to_secs = (int_list[0]) * (60**2)
        mins_to_secs = (int_list[1]) * 60
    except TypeError as err:
        logger.debug(f'{err} - Check for issues with conversion from str to int')
    else:
        total_secs = hours_to_secs + mins_to_secs

    return total_secs

""" takes hh_mm as argument, returns the time to wait until the original input time (arg passed into hh_mm) """
def secs_to_wait(input_time: int):
    local_time = time.localtime()
    logger.debug('- Converting local time to secsons since previous midnight (00:00)')
    hours, mins, seconds = ((local_time[3])*(60**2)), (local_time[4]*60) , local_time[5]
    current_time = hours + mins + seconds
    logger.debug('- Calculate seconds until event')
    time_to = input_time - current_time
    return time_to


""" Function to convert lists with str type items to int """
def convert_list(input_list: list):
    int_list = list(map(int, input_list))
    return int_list

""" function to automate the removal of the recently executed sched event from sched_list """
def remove_sched_event(list_item):
    sched_list.remove(list_item)
    return None


if __name__ == '__main__':
    app.run(debug=True)