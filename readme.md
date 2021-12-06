
<!-- Headings -->
<!-- Strong -->
<!-- Horizontal Rule -->
<!-- Link -->
# How to use

# Users

## Running:
There are 2 ways to intiate the program. 
1. Run via the 'Run python file' button on the covid_data_handler.py module
2. Type 'python3 covid_data_handler.py'  into the terminal
- Once running, go to: [covid dashboard](http://127.0.0.1:5000/index) . Here the dashboard should be running, showing
data from the default function arguments.

## Customising dashboard output

**Customising Covid data shown:**
- Go to the config.json module
- Set different values for the area_name and area_type keys
    - area_name -> Can be any city in the UK
    - area_nation -> region, nation, ltla, overview, nhsReghion, utla

**Custoising News feed:**
- Set a different value for the news_kw key in config.json

## Scheduling an event:
- In order to change the dashboard output, an event must be scheduled
- To schedule an event the from inputs on the dashboard intrface must be uses...
    1. Enter a event name and time
    2. Select one of the checkboxed -> covid data, news, repeat
    3. Click submit
- This event is now scheduled, and will update the dashboard at the input time


# Developers

