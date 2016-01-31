# Kapp Consulting - Trading System
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
* `$ git clone git@github.com:<peekwez>/trading_system.git`

* `$ cd trading_system`

### Install Application Dependencies
copy and paste the lines below to install the following dependencies

* `$ sudo apt-get install -y build-essential gfortran gcc libatlas-base-dev  curl git python-dev libpq-dev libssl-dev postgresql-client libxml2-dev libxsltl-dev libgraphviz-dev libopenblas-dev liblapack-dev`

* `$ sudo apt-get build-dep python-matplotlib`

* `$ pip install -r requirements.txt`

* `$ npm install -g redis-commander`


## **Setup Instructions**

### Initial Setup
* `$ make setup`

The above command performs the following tasks

* starts `postgres:9.4.1` and `redis:2.8` services using `docker-compose`. The `postgres` container's port `5432/tcp` is linked to port `5431` on the local machine while the `redis` container's port `6379/tcp` is linked to port `6378` on the local machine

* creates a database called `securities_master` and a Django admin superuser for the application. The superuser is created through a shell prompt

* creates log files in `trading_system/db/logs/` for all the supervisor processes

### Supervisor Processes
* `$ make processes`

* `$ make status` -- check if processes are up and running

The following process are started in the background by supervisor
* `celery worker`
* `celery beat`
* `django development server`  - the `admin` page is at [http://localhost:8000/admin](http://localhost:8000/admin)
* `celery flower` at [http://localhost:8001](http://localhost:8001)
* `ipython notebook` at [http://localhost:8002](http://localhost:8002) with a `Django Shell-Plus` kernel
* `redis-commander` at [http://localhost:8003](http://localhost:8003)


### Populating Database
* log in to the [Admin Page](http://localhost:8000/admin) and add the following information for **Yahoo** to the **Data Vendor table**
  ```
  Name = Yahoo Finance
  Historical url = http://ichart.finance.yahoo.com/table.csv
  Quotes url = http://download.finance.yahoo.com/d/quotes.csv
  Support email = support@yahoo.com
  ```

* execute the _celery_ tasks inside an [`ipython notebook`](http://localhost:8002) cell using the `Django Shell-Plus` kernel
  ```python
  create_exchanges.delay() # adds TSX, TSXV, NASDAQ and NYSE exchanges to database
  update_securities_symbols.delay() # adds S&P500 and S&P/TSX tickers to database
  add_historical_prices.delay() # adds daily prices from Jan 01, 10 years ago to today
  ```

### Updating Tickers Manually
* add the ticker(s) information to the **Symbols table** using the [Admin Page](http://localhost:8000/admin)

* update the historical prices for the added tickers by executing the following commands inside a cell in the [`ipython notebook`](http://localhost:8002) using the `Django Shell-Plus` kernel
  ```python
  add_prices_for_tickers.delay(tickers=['tk1','tk2','...'])
  ```

### Daily Prices
* `update_prices` _celery_ task is executed every 10 minutes between 9am-6pm during the weekdays using `celery-beat` as the scheduler and the `celery-worker` as the task queue. _Redis_ is used as the _celery_ broker.

## **After System Restart/Reboot**
`cd` into application directory and execute the following commands
* `$ make docker-services`

* `$ make processes`

## **Miscellaneous**
### Sample Python Script
This script can be run in [`ipython notebook`](http://localhost:8002) to generate a
simple and/or exponential moving average for all tickers whose value is less
or equal to **$2.5** on the specified date

```python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import date, timedelta


# turn matplotlib inline and save figs as pdfs or svg
get_ipython().magic(u'matplotlib inline')
get_ipython().magic(u"config InlineBackend.figure_format = 'svg'")

# fetch daily prices for tickers
today = '2016-01-29' # date.today()
tickers = DailyPrice.objects.filter(close_price__lte=2.5, price_date=today).values_list('symbol__ticker', flat=True)


# set start and end dates
start_date = '2015-01-01'
end_date = today

# initialized plot class
p = plot.PlotSymbol(tickers)

# plot a simple moving average using pandas
ma_type = 'simple' # 'exponential' is another option
p.plot(ma_type=ma_type, start_date=start_date, end_date=end_date)
```

### Makefile Help
Use the command below to see the options available for Makefile
* `$ make help`

### File Structure
```
├── db
│   ├── data
│   │   ├── admin.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
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
│   └── manage.py
├── docker-compose.yml
├── Makefile
├── Makefile.in
├── monaco.ttf
├── README.md
├── requirements.txt
├── supervisord.conf
└── testplots.ipynb
```
