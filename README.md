# Kapp Consulting - Trading System [![Build Status](https://travis-ci.com/peekwez/trading_system.svg?token=BnDQr5dc9iRq4pSqsjvc&branch=master)](https://travis-ci.com/peekwez/trading_system)
---
## **System Dependencies (Ubuntu 14.04)**
Install the following system dependencies

* [pip](https://pip.pypa.io/en/stable/installing/)
* [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
* [Node.js](https://nodejs.org/en/)
* [docker](https://docs.docker.com/engine/installation/)
* [docker-compose](https://docs.docker.com/compose/install/)

## **Installation**

### Clone Repository.
```
$ git clone git@github.com:<peekwez>/trading_system.git
$ cd trading_system
```

### Install Application Dependencies
Copy and paste the lines below to install the following dependencies
```
$ sudo apt-get install -y build-essential gfortran gcc libatlas-base-dev  curl git python-dev libpq-dev libssl-dev postgresql-client libxml2-dev libxsltl-dev libgraphviz-dev libopenblas-dev liblapack-dev
$ sudo apt-get build-dep python-matplotlib
$ pip install -r requirements.txt
$ npm install -g redis-commander
```

## **Setup Instructions**

### Initial Setup
```
$ make setup
```

the command chains several commands to

* start a `postgres` and `redis` docker containers using `postgres:9.4.1` and `redis:2.8` images respectively. `docker-compose` is used to start the services. `postgres'` port `5432/tcp` is linked to port `5431` on the local machine, while `redis'` port `6379/tcp` is linked to port `6378` on the local machine. `redis` is started to serve as a broker for `celery`

* create a database called `securities_master` and a `Django` **admin** superuser for the application. The shell will prompt you to create the superuser login credentials

* create a `logs` directory in `trading_system/src/` and log files for all the supervisor processes inside the `logs` directory

### Supervisor Processes
```
$ make processes
$ make status  # (Check if processes are up and running)
```
the first command starts the following processes as a daemon

* `celery worker` - a task queue for real-time processing
* `celery beat` -  a task scheduler
* `Django development server`  - the **admin** page is at [http://localhost:8000/admin](http://localhost:8000/admin)
* `celery flower` - web client for monitoring `celery-worker`[http://localhost:8001](http://localhost:8001)
* `ipython notebook` - for python scripting; modules are imported using the `Django Shell-Plus` kernel [http://localhost:8002](http://localhost:8002)
* `redis-commander` web client for `redis` [http://localhost:8003](http://localhost:8003)


### Populating Database
* log in to the [Admin Page](http://localhost:8000/admin) and add the following information for **Yahoo** to the **Data Vendor table**
  ```
  Name = Yahoo Finance
  Historical url = http://ichart.finance.yahoo.com/table.csv
  Quotes url = http://download.finance.yahoo.com/d/quotes.csv
  Support email = support@yahoo.com
  ```

* execute the `celery` tasks inside an [`ipython notebook`](http://localhost:8002) cell using the `Django Shell-Plus` kernel
  ```python
  create_exchanges.delay() # adds TSX, TSXV, NASDAQ and NYSE exchanges to database
  update_securities_symbols.delay() # adds S&P500 and S&P/TSX tickers to database
  add_historical_prices.delay() # adds daily prices from Jan 01, 10 years ago to today
  ```

### Updating Tickers Manually
* add the ticker(s) information to the **Symbols table** using the [Admin Page](http://localhost:8000/admin)

* update the historical prices for the added tickers by executing the following commands inside a cell in the [`ipython notebook`](http://localhost:8002) using the `Django Shell-Plus` kernel
  ```python
  add_prices_for_tickers.delay(tickers=['AAPL','BBD-B.TO,'...'])
  ```

### Daily Prices
* `update_prices` task is executed every 10 minutes between 9am-6pm during the weekdays using `celery-beat` as the scheduler and the `celery-worker` as the task queue.

## **After System Restart/Reboot**
`cd` into application directory and execute the following commands
```
$ make docker-services
$ make processes
```

## **Miscellaneous**
### Sample Python Script
Open this script using [`ipython notebook`](http://localhost:8002) to generate a simple and/or exponential moving average for all tickers whose __close value__ is less or equal to __$2.5__ on date specified

```python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import date, timedelta


# turn on matplotlib inline and save figs as pdfs or svg
get_ipython().magic(u'matplotlib inline')
get_ipython().magic(u"config InlineBackend.figure_format = 'svg'")

# fetch daily prices for ticker(s)
today = '2016-01-29' # date.today()
tickers = DailyPrice.objects.filter(close_price__lte=2.5, price_date=today).values_list('symbol__ticker', flat=True)


# set start and end dates
start_date = '2015-01-01'
end_date = today

# initialize plot class
p = plot.PlotSymbol(tickers)

# plot a simple moving average using pandas
ma_type = 'simple' # 'exponential' is another option
p.plot(ma_type=ma_type, start_date=start_date, end_date=end_date)
```

### Makefile Help
Use the command below to see the options available for Makefile
```
$ make help
```

### File Structure
```
├── docker-compose.yml
├── fabfile.py
├── Makefile
├── Makefile.in
├── monaco.ttf
├── README.md
├── requirements.txt
├── setup.cfg
├── src
│   ├── data
│   │   ├── admin.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py├── nginx.conf
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── utils
│   │   │   ├── exchanges.py
│   │   │   ├── __init__.py
│   │   │   ├── misc.py
│   │   │   ├── plot.py
│   │   │   ├── prices.py
│   │   │   └── symbols.py
│   │   └── views.py
│   ├── db
│   │   ├── celery.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── systems
│       ├── bitops.py
│       ├── __init__.py
│       ├── simulations.py
│       ├── strategies.py
│       └── tests
│           ├── __init__.py
│           └── test_bitops.py
└── supervisord.conf
```
