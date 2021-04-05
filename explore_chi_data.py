#########################################################
#    Title: Explore Chicago Data                        #
#   Author: Lauren McNamara                             #
#  Created: 4/1/2021                                    #                       
# Modified: 4/1/2021                                    #
#  Purpose: Explore open data for city of Chicago       #
#########################################################


##############  Setup  ##############
# import packages
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np 
import freqit
from sodapy import Socrata

# set working directory
os.chdir("/Users/Lauren/Documents/Python/ChicagoData")
# os.getcwd()
# os.listdir('.')

# color palette
# source: https://learnui.design/tools/data-color-picker.html#palette
pdblue = '#003f5c'
plblue = '#444e86'
ppurple = '#955196'
ppink = '#dd5182'
porange = '#ff6e54'
pyellow = '#ffa600'
pgray = '#64666B'

##############  Get Data  ##############
# This dataset shows monthly averages, by day type (weekday, Saturday or Sunday/Holiday) 
# and monthly totals for all CTA bus routes, back to 2001.
# bus_monthly_avg = pd.read_json("https://data.cityofchicago.org/resource/bynn-gwxy.json")
# bus_monthly_avg.head()

# Current Employee Names, Salaries, and Position Titles
employee_salary = pd.read_json("https://data.cityofchicago.org/resource/xzkq-xp2w.json")
employee_salary.head()
# this method limits to 1000 rows

with Socrata("data.cityofchicago.org", None) as client:
    results = client.get("xzkq-xp2w", limit=2000)
    employee_salary = pd.DataFrame.from_records(results)
    # need to get an app_token or suffer strict throttling limits

##############  Clean Data  ##############
# count number of commas in name
employee_salary['n_comma'] = employee_salary.name.str.count(',')
freqit.oneway(employee_salary['n_comma']).freqtable()
# 2000 recs all have one comma per name

# split into first and last name
