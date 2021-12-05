# import sched, time, requests
# from logging import error
# from types import DynamicClassAttribute
# from uk_covid19 import Cov19API
# from flask import Flask, render_template, request
# from covid_news_handling import news_API_request, update_news, remove_article, news_list

# """ Covid_update puts data for interface into a global list. List is imported to app.py and used locally """
# app = Flask(__name__)
# s = sched.scheduler(time.time, time.sleep)


# data_dict = dict()
# sched_list = list()
# news_list.append(update_news())



# # @app.route('/index')
# # def update():
# #     covid_update()
# #     remove_article()
# #     if request.args.get('two'):
# #         update_name, update_interval = request.args.get('two'), request.args.get('update')
# #         if update_interval == None:
# #             raise ValueError

# #         schedule_covid_updates(update_name,update_interval, 'rugby' ,'Portsmouth','Wales')

# #     s.run(blocking=False)

# #     return render_template('index.html', hospital_cases = data_dict['hospital_cases'], 
# #     deaths_total = data_dict['total_deaths'], national_7day_infections = data_dict['national_7day_rate'], 
# #     local_7day_infections = data_dict['local_7day_rate'], nation_location = data_dict['nation_location'],
# #     location = data_dict['area_name'], updates = sched_list, news_articles = news_list)


# def schedule_covid_updates(update_name, update_interval, news_kw ,area_name='Exeter', nation='England'):
#     # Creating sched list
#     sched_item = {'title':f'{update_name}' , 'content':f'{update_interval}'}
#     secs_until = secs_to_wait(hh_mm(update_interval))
#     sched_list.append(sched_item)
#     # Schedule event
#     # If covid box checked
#     if request.args.get('covid-data'):
#         s.enter(secs_until, 1, covid_update, argument=(f'{area_name}', f'{nation}'))
#     if request.args.get('news'):
#         s.enter(secs_until, 1, update_news, kwargs={'keyword':f'{news_kw}'})
#         s.run(blocking=False)
#     # Pop scheduled event
#     s.enter(secs_until+1, 1, remove_sched_event)
#     return


# #################### Live Data Access ####################

# def covid_API_request(location = "Exeter", location_type = "ltla") -> dict:  # Parameters are set to defaults, # For city set Location type to region
#     filter_list = [f"areaType={location_type}", f"areaName={location}"] 
#     pulled_data = {
#     "date": "date",
#     "areaName": "areaName",
#     "areaCode": "areaCode",
#     "newCasesByPublishDate": "newCasesByPublishDate",
#     "cumCasesByPublishDate": "cumCasesByPublishDate",
#     "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
#     "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
#     "hospitalCases":"hospitalCases",
#     "totalDeaths":"newDailyNsoDeathsByDeathDate"
#     }
#     api = Cov19API(filters=filter_list,structure=pulled_data) # Set up api request specifications and put in var
#     pyth_obj = api.get_json()  # get data and place json object into python object. This will return the filtered, structured data
#     return pyth_obj


# """ Function that collates all data needed for interface """

# def covid_update(local_area = 'Exeter', nation = 'England'):
#     hospital_cases = 0
#     national_7day_cases = 0
#     local_7day_cases = 0
#     total_deaths = 0
#     # Current hospital cases and total deaths
#     local_data_dict = covid_API_request('England','nation')
#     for data_item in local_data_dict['data']:
#         if data_item['hospitalCases'] != None:
#             hospital_cases += data_item['hospitalCases']
#         if data_item['totalDeaths'] != None:
#             total_deaths += data_item['totalDeaths']
#     # 7 day cases
#     # National
#     sliced_list_for_national = covid_API_request(f'{nation}', 'nation')['data'][0:7]
#     for data_item in sliced_list_for_national:
#         if data_item['newCasesByPublishDate'] != None:
#             national_7day_cases += data_item['newCasesByPublishDate']
#             national_7day_rate = round(national_7day_cases / 7)
#     # Local
#     sliced_list_for_local = covid_API_request(f'{local_area}', 'ltla')['data'][0:7]
#     for data_item in sliced_list_for_local:
#         if data_item['newCasesByPublishDate'] != None:
#             local_7day_cases += data_item['newCasesByPublishDate']
#             local_7day_rate = round(local_7day_cases / 7)
#     local_dict = {'hospital_cases':f'{hospital_cases}', 'total_deaths':f'{total_deaths}', 
#     'national_7day_rate':f'{national_7day_rate}', 'local_7day_rate':f'{local_7day_rate}',
#     'area_name':f'{local_area}', 'nation_location':f'{nation}'}
#     data_dict.update(local_dict)
#     return

# # Input time from dashboard: Converting to seconds
# # Input format must be 24 hours and type str e.g '13:00'
# def hh_mm(str_number: str):
#     num = str_number.split(':')
#     int_list = list(map(int, num))
#     hours_to_secs = (int_list[0]) * (60**2)
#     mins_to_secs = (int_list[1]) * 60
#     total_secs = hours_to_secs + mins_to_secs
#     return total_secs

# # Function that calculates seconds to wait.
# # Input_time should be hh_mm
# def secs_to_wait(input_time):
#     local_time = time.localtime()
#     hours, mins, seconds = ((local_time[3])*(60**2)), (local_time[4]*60) , local_time[5]
#     current_time = hours + mins + seconds
#     time_to = input_time - current_time
#     return time_to


# # convert str lists elements to int
# def convert_list(input_list):
#     int_list = list(map(int, input_list))
#     return int_list

# def remove_sched_event():
#     sched_list.pop(0)
#     return

# def remove_article():
#     if request.args.get('notif'):
#         for article in news_list:
#             index = news_list.index(article)
#             if article != None:
#                 if article['title'] == request.args.get('notif'):
#                     news_list.pop(index)
#     return


# if __name__ == '__main__':
#     app.run(debug=True)


