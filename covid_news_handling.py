import json, requests, sched, time, requests, logging
from typing import Dict, List
from flask import request

""" assigning config.json """
json_file = open('Documentation/config.json', 'r')
config = json.load(json_file)

""" logging setup """
log_format = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
logging.basicConfig(filename='sys.log' ,level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

""" global data structures """
news_list = []

""" function to pull data from the news api """
def news_API_request(covid_terms = "Covid coronavirus COVID-19") -> Dict:
    base_url = "https://newsapi.org/v2/everything?"
    api_key = config['news_API_key']
    complete_url = base_url + "q=" + covid_terms + "&apiKey=" + api_key
    logger.critical(' - Pulling news API')
    try:
        response = requests.get(complete_url)
    except Exception as error:
        logger.critical(error, 'Error calling news api')
    else:
        py_obj = response.json()
    return py_obj

""" func to update local data structure with relevant api data """
def update_news(keyword = 'covid') -> None:
    logger.debug(' - Calling news_API-request into local var')
    api_pull = news_API_request(f'{keyword}')
    logger.debug(' - Entering API list containing dict')
    all_articles = api_pull['articles']
    logger.debug(' - Iterating list & appending dict vals to news list')
    for article in all_articles:
        news_list.append({
            'title':article['title'],
            'content':article['content']
        })
    """ capping news feed list to 20 items """
    logger.debug(' - Deleting first 20 items of list. Moving next 20 to the front')
    if len(news_list) > 20:
            del news_list[0:21]
    return None


""" remove article when x is clicked on toast widget """
def remove_article() -> None:
    if request.args.get('notif'):
        for article in news_list:
            index = news_list.index(article)
            if article != None:
                if article['title'] == request.args.get('notif'):
                    try:
                        news_list.pop(index)
                    except IndexError as index_error:
                        logger.debug(index_error, 'Error popping index')
                    else:
                        news_list.pop(index)
    return None

