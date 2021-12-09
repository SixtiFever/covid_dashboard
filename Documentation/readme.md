
<!-- Headings -->
<!-- Strong -->
<!-- Horizontal Rule -->
<!-- Link -->
<!-- Blockquote -->
# Introduction
This project uses python to populate an HTML dashboard with real time covid-19 metrics pulled from the Public Health England API.

### Built with

[Python 3.9.7](https://www.python.org/)

[Flask](https://flask.palletsprojects.com/en/2.0.x/)

# Pre-requesites

**News API key**
- An API key will be needed for pulling news articles from the news API. Go to [news API](https://newsapi.org/) and click **Get API Key**. This key needs to be **assigned to news_api_key in config.json**.

**Packages**

Install flask
  > ``$ pip3 install flask``

Install PHE covid-19 package
  > ``$ pip3 install uk_covid19``


# Installation

### Cloning repository locally
Create directory that will hold the project. Whilst in the directory, clone the project into it.

> ``$ git clone https://github.com/SixtiFever/covid_dashboard.git``



# How to use

**Note: The program is run from the covid_data_handler.py module**


### Running from terminal
1. Jump into the directory containing the package
2. Run **covid_data_handler.py** E.g python3 covid_data_handler.py
3. Go to [covid dashboard](http://127.0.0.1:5000/index)

### Running from environment
**In this example I use Visual Studio Code**
1. Open the package in VSC
2. Select covid_data_handler.py
3. Ensure that the correct interpreter is selected
    > ``Python 3.9.7 64-bit``
4. Run the file
5. Go to [covid dashboard](http://127.0.0.1:5000/index)


The dashboard should be running, showing
data from the default function arguments.

### Customising dashboard output

**Customising Covid data shown:**
- Go to the config.json module
- Set different values for the area_name and area_type keys
    - area_name -> Can be any city in the UK
    - area_nation -> region, nation, ltla, overview, nhsReghion, utla

**Custoising News feed:**
- Set a different value for the news_kw key in config.json

### Scheduling an event:
In order to change the dashboard output, an event must be scheduled. To schedule an event the from inputs on the dashboard intrface must be uses...
1. Enter a event name and time
2. Select one of the checkboxes -> covid data, news, repeat
3. Click submit

This event is now scheduled, and will update the dashboard at the input time


# Testing

Install and run pytest to iterate through the static test modules in the package. Make sure it is run from the root directory of the package.

> $ pip3 install pytest
> $ python3 pytest


