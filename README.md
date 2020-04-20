# wizzScrap

Wizzair Airline Flights Price Scraper

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Download and install ```chromedriver``` compatibile with your machine
* [chromedriver](https://chromedriver.chromium.org/) download here

The requirements are in the ```requirements.txt``` file

### Installation
Clone the repository and install the requirements in a virtual environment
```bash
$ git clone https://github.com/johnnybigH/WizzScrap.git
$ cd wizzScraping
$ pipenv shell
$ pipenv install -r requirements.txt 
```
#### Before you run the project
Open wizzScraping.py in your text editor and change... <br />
that line of code :
```bash
self.driver = webdriver.Chrome("/Users/adamke/Downloads/chromedriver", options=options)
```
to:
```bash 
self.driver = webdriver.Chrome("/direction which store your chromedriver", options=options)
```

## Running

#### Bash run:
```bash
$ python3 wizzScraping.py 
```
#### with argparse arguments:

to find available destinations from your city
```bash
--origin 'city name' --list list
```

to search your flight
```bash
--origin 'city name' --add 'arrival' --date 'date' # date format 2020-04-10

--add     # add destination
--date    # search until date
```
optionaly you can add more destinations like:
```bash
--add 'arrival1' 'arrival2' 'arrival3'
```
or to search for all available destinations from your city
```bash
--origin 'city name' --all dest --date 'date' # date format 2020-04-10
```

For list of available arguments
```bash
--help
```

## Contributions
This project was developed in my free time. However, contributions from everybody in the community are welcome. If you think there should be a particular feature, you find a bag or you can just make it work better, feel free to open up a new issue or pull request.

## Roadmap
At the moment the program only finds one way flights. <br />
The next steps:
* adding the option of searching for return flights. <br />
* pricing comparison feature

## Scraping Resources
### Tools
### Build With
* [Selenium](https://selenium-python.readthedocs.io/) The selenium package is used to automate web browser interaction from Python.
* [Requests](https://requests.readthedocs.io/en/master/) Requests is an elegant and simple HTTP library for Python.
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) Beautiful Soup is a Python library for pulling data out of HTML and XML files.
* [Argparse](https://docs.python.org/3.3/library/argparse.html#module-argparse) The argparse module makes it easy to write user-friendly command-line interfaces.

# wizzScrap
