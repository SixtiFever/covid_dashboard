# from flask import Flask, render_template, request
# import covid_data_handler, covid_news_handling, sched, time

# app = Flask(__name__)

# a = covid_data_handler
# b = covid_news_handling

# s = sched.scheduler(time.time, time.sleep)


# ##################### FLASK ###############################

# """ http://127.0.0.1:5000/index """

# @app.route('/index')
# def update():

#     """ Populating dashboard on start-up. Then ensuring it doesn't overwrite dict on every refresh.
#     It's always len 0 on start-up, but once populated, covid_update will keep replacing dict items """
#     if len(a.data_dict) == 0:
#         a.covid_update()
#     a.remove_article()
#     if request.args.get('two'):
#         update_name, update_interval = request.args.get('two'), request.args.get('update')

#         a.schedule_covid_updates(update_name, update_interval)

#     s.run(blocking=False)

#     return render_template('index.html', hospital_cases = a.data_dict['hospital_cases'], 
#     deaths_total = a.data_dict['total_deaths'], national_7day_infections = a.data_dict['national_7day_rate'], 
#     local_7day_infections = a.data_dict['local_7day_rate'], nation_location = a.data_dict['nation_location'],
#     location = a.data_dict['area_name'], updates = a.sched_list, news_articles = b.news_list,
#     image = 'covid_19.jpg' )

# if __name__ == '__main__':
#     app.run(debug=True)