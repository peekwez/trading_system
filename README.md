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

* execute the following `celery` tasks using [`ipython notebook`](http://localhost:8002) with the `Django Shell-Plus` kernel

  ```python
  tasks.add_symbols.delay() # all symbols for S&P/TSX and S&P/TSXV Indices
  tasks.add_historical_data_all.delay() # add historical data 10 year
  ```

### Updating Tickers Manually
* add the ticker(s) information to the **Symbols table** using the [Admin Page](http://localhost:8000/admin)

* update the historical prices for the added tickers by executing the following commands inside a cell in the [`ipython notebook`](http://localhost:8002) using the `Django Shell-Plus` kernel
  ```python
  tasks.add_historical_data_ticker.delay(tickers=['BBD.B','AME',...])
  ```

### Daily Prices
* `tasks.update_daily_quotes` task is executed every 10 minutes between 9am-6pm during the weekdays using `celery-beat` as the scheduler and the `celery-worker` as the task queue.

## **After System Restart/Reboot**
`cd` into application directory and execute the following commands
```
$ make docker-services
$ make processes
```

## **Miscellaneous**
### Sample Python Script
The test script below uses [`ipython notebook`](http://localhost:8002) to generate a simple and/or exponential moving average for the lowest three tickers whose __close value__ is less or equal to __$2.5__ as of today. The second part of the script performs a backward and forward testing for the selected tickers using a __coin flip__ day trading strategy(__short__=1, __long__=1).
```python
    # -*- coding: utf-8 -*-
    from __future__ import absolute_import
    from datetime import date, timedelta


    # turn matplotlib inline and asave figs as pdfs or svg
    get_ipython().magic(u'matplotlib inline')
    get_ipython().magic(u"config InlineBackend.figure_format = 'svg'")


    # fetch daily prices for tickers of interest
    today = date.today().strftime('%Y-%m-%d')
    tickers = DailyPrice.objects.filter(
        close_price__lte=3.,
        price_date=today).order_by('close_price').values_list(
        'symbol__ticker',
        flat=True)[:3]


    # Plot Close Price and Moving Averages for Specific Tickers

    # initialize plot function
    te = plot.PlotSymbol(tickers)

    # set start and end dates
    start_date = '2015-01-01'
    end_date = today

    # plot data with simple moving averages
    ma_type = 'simple'
    te.plot(ma_type=ma_type, start_date=start_date, end_date=end_date)


    # Trading Strategy Simulations

    # import random
    import random

    # initialize simulations for tickers
    mcs = []

    # initiliaze strategy
    strategy = RandomStrategy()

    # start simulation
    ptr = 0
    for ticker in tickers:
        random.seed()
        mcs.append(MonteCarlo(strategy,ticker))

        # test strategy
        mcs[ptr].run_strategy()

        ptr += 1
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
├── nginx.conf
├── README.md
├── requirements.txt
├── setup.cfg
├── src
│   ├── data
│   │   ├── admin.py
│   │   ├── assets
│   │   │   ├── __init__.py
│   │   │   ├── other.csv
│   │   │   ├── sec.csv
│   │   │   ├── tsx.csv
│   │   │   └── tsxv.csv
│   │   ├── constants.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── misc.py
│   │   ├── models.py
│   │   ├── plots.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── utils.py
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
