"""  Testing module for covid_news_handler functions  """

import covid_news_handling

""" Every dict from newsapi has 3 items, I know if the length of return is 3, 
the api has been pulled """
def test_news_API_request():
    assert len(covid_news_handling.news_API_request()) == 3

a = covid_news_handling.news_API_request()

""" Proving the eky a['article'] stores a list of values of len > 0 let's us know that 
we have a populated list of articles """
def test_update_news():
    assert len(a['articles']) > 0