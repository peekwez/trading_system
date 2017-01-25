# -*- coding: utf-8 -*-
from __future__ import absolute_import

import csv
import os
import numpy as np

from datetime import date



def Mat12(n):
    tmp = np.zeros([n,n])
    tmp[0,0] = -1.5
    tmp[0,1] =  2.
    tmp[0,2] = -0.5

    tmp[-1,-1] =  1.5
    tmp[-1,-2] = -2.;
    tmp[-1,-3] =  0.5

    for k in range(1,n-1):
        tmp[k,k-1] = -0.5;
        tmp[k,k+1] =  0.5;
    return tmp

def yahoo_date_fmt():
    end_date = date.today().timetuple()
    a = '00'; b = '01'; c = str(end_date[0]-10)
    d = str(end_date[1]-1).zfill(2); e = str(end_date[2]).zfill(2)
    f = str(end_date[0])
    return 'a=%s&b=%s&c=%s&d=%s&e=%s&f=%s'%(a,b,c,d,e,f)

def csv_to_sectors(sector_files):
    data = {}
    for key,location in sector_files:
        with open(location,'r') as csvfile:
            tmp_1 = csv.reader(csvfile)
            if key == 0:
                sym = 2; sec = 5
            else:
                sym = 0; sec = 2
            tmp_2 = {line[sym].strip():line[sec].strip() for line in tmp_1}
        if tmp_2 is not None: data.update(tmp_2)
    return data

def update_other_sectors():
    sector_wildcards = (
        ('Real Estate','Real Estate'),
        ('Real Estate','Property'),
        ('Real Estate','Residences'),
        ('Mining','Mining'),
        ('Mining','Zinc'),
        ('Mining','Gold'),
        ('Mining','Uranium'),
        ('Mining','Resources'),
        ('Mining','Exploration'),
        ('Mining','Minerals'),
        ('Financial Services','Fund'),
        ('Financial Services','Capital'),
        ('Financial Services','Asset'),
        ('Life Sciences','Health'),
        ('Life Sciences','Therapeutics'),
        ('Oil & Gas', 'Energy'),
        ('Oil & Gas', 'Oil'),
        ('Oil & Gas', 'Gas'),
        ('Diversified Industries', 'Industries'),
        ('Diversified Industries', 'Bombardier'),
        ('Comm & Media', 'Communications'),
        ('Comm & Media', 'Media'),
        ('Comm & Media', 'Entertainment'),
    )

    from data.models import Symbol
    import pdb

    pdb.set_trace()
    tmp = Symbol.objects.filter(sector=None).values_list('ticker',flat=True)
    tickers = [ticker for ticker in tmp]
    filepath = os.path.join(os.path.dirname(__file__)) + "/assets/other.csv"

    for sector,wildcard in sector_wildcards:
        Symbol.objects.filter(name__icontains=wildcard,sector=None).update(sector=sector)

    data = Symbol.objects.filter(ticker__in=tickers).values_list('ticker','name','sector')
    pdb.set_trace()
    with open(filepath,'w') as csvfile:
        writer = csv.writer(csvfile, delimiter= ',', quotechar="'")
        for row in data:
            writer.writerow(row)

    # reset those entries back
    data = Symbol.objects.filter(ticker__in=tickers).update(sector=None)

    return data


class colors:
    # hex color codes for plots
    SYMB  = '#003166' #'#004c99'
    FILL  = '#e6f2ff'  #'#e5f2ff'
    VLINE = '#003166'  #'#004c99'
    MA    = {'MA_5': '#ff3333',
             'MA_10': '#3fc03f',
             'MA_20': '#009933', #'#8533ff',
             'MA_60': '#b3b300', #'#ff1ab1',
             'MA_100': '#00cbcc',
             'MA_200': '#b300b3', #'#ff751a',
         }

class info:
    # colors for info, warning and fail outputs
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
