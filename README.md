# Kapp Consult - Trading System [![Build Status](https://travis-ci.com/peekwez/trading_system.svg?token=BnDQr5dc9iRq4pSqsjvc&branch=master)](https://travis-ci.com/peekwez/trading_system)

## **System Dependencies (Ubuntu 14.04 LTS)**
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
* `tasks.update_daily_quotes` task is executed every __10 minutes__ between __9am-6pm__ during the weekdays using `celery-beat` as the scheduler and the `celery-worker` as the task queue.

## **After System Restart/Reboot**
`cd` into application directory and execute the following commands
```
$ make docker-services
$ make processes
```

## **Miscellaneous**
### Sample Python Script
The test script below uses the [`ipython notebook`](http://localhost:8002) launched to generate a simple moving average for companies whose latest __close value__ is greater or equal to __$0.5__ but less or equal to __$2.5__, and also with an average volume of __100000__ shares since listed on the __TSX__ exchange. The second part of the script performs a backward and forward test for a random (__coin flip__) trading strategy (__short__ = 1, __long__ = 0) using the tickers from the first part.

```python
    # -*- coding: utf-8 -*-

# turn matplotlib inline and save figs as pdfs or svg
get_ipython().magic(u"matplotlib inline")
get_ipython().magic(u"config InlineBackend.figure_format = 'svg'")

# get latest date in database
latest_price = DailyPrice.objects.latest('price_date')
latest_date  = latest_price.price_date.strftime('%Y-%m-%d')

# define constraints
lower = 0.5
upper = 2.5
volume = 100000
exchange = 'TSX'

# fetch tickers with daily bars
tickers = DailyPrice.objects.annotate(
    average_volume=Avg('volume')
).filter(
    close_price__lte=upper,
    close_price__gte=lower,
    average_volume__gte=volume,
    symbol__exchange__abbrev=exchange,
    price_date=latest_date
).order_by(
    'close_price'
).values_list(
    'symbol__ticker',
    flat=True
)


# Plot Close Price and Moving Averages for Specific Tickers

# plot constraints
start_date = '2015-01-01'
end_date = latest_date
ma_type = 'exponential' # options='simple' or 'exponential'

# get number of plots
end = min(len(tickers),20)

# initialize plot class and plot tickers
f = plots.PlotSymbol(tickers[:end])
f.plot(ma_type=ma_type, start_date=start_date, end_date=end_date)


# Trading Strategy Simulations

# initialize simulations for tickers
g = []

# get number of plots
end = min(len(tickers),3)

# initialize strategy class
strategy = strategies.RandomStrategy()

# start simulation
for k,ticker in enumerate(tickers[:end]):

    # initialize the basic random generator
    seed()

    # initialize simulation class and test strategy
    g.append(simulations.MonteCarlo(strategy,ticker))
    g[k].run_strategy()
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
