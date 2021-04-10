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
from pandas_profiling import ProfileReport

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
# Current Employee Names, Salaries, and Position Titles
# employee_salary = pd.read_json("https://data.cityofchicago.org/resource/xzkq-xp2w.json")
# employee_salary.head()
# this method limits to 1000 rows

# this method allows more data to be pulled
with Socrata("data.cityofchicago.org", None) as client:
    results = client.get("xzkq-xp2w", limit=2000)
    employee_salary = pd.DataFrame.from_records(results)
    # need to get an app_token or suffer strict throttling limits

##############  Clean Employee Salary Data  ##############
#####  examine and clean name
# count number of commas in name
employee_salary['n_comma'] = employee_salary.name.str.count(',')
freqit.oneway(employee_salary['n_comma']).freqtable()
# 2000 recs all have one comma per name

# split into first and last name
esalary = employee_salary.merge(
                    employee_salary.name.str.split(',',n=1, expand=True)
                    ,left_index=True
                    ,right_index=True
                    ,how='outer')   \
                    .rename(columns={0:'name_last'
                                    ,1:'name_first'})

# remove leading and trailing spaces from first name
esalary['name_first'] = esalary.name_first.str.strip()

# split out middle initial
esalary = esalary.merge(
                    esalary.name_first.str.split(' ',n=1, expand=True)
                    ,left_index=True
                    ,right_index=True
                    ,how='outer')   \
                    .drop(columns=['name_first'])   \
                    .rename(columns={0:'name_first'
                                    ,1:'name_mid'})

# count non-alpha characters
not_alpha_name = esalary.loc[~(esalary.name_first.str.isalpha())
                                    ,'name_first']
not_alpha_name
# have one name with a hyphen


#####  examine and clean salary
# why is typical hours an object
freqit.oneway(esalary['typical_hours']).freqtable()

# convert numeric variables from object to float
esalary['typical_hours'] = pd.to_numeric(esalary['typical_hours'], errors='coerce')
esalary['hourly_rate'] = pd.to_numeric(esalary['hourly_rate'], errors='coerce')
esalary['annual_salary'] = pd.to_numeric(esalary['annual_salary'], errors='coerce')

# are salary vs hourly full or part time
esalary.groupby(['full_or_part_time','salary_or_hourly']).size()
# in sample set, salary is always full time and hourly can be
# either full or part time

# if hourly full time, is typical hours always 40
esalary.loc[(esalary.full_or_part_time == 'F') & 
            (esalary.salary_or_hourly == 'Hourly'),'typical_hours'].describe()
# hours are generally 40 but not always

# typical_hours are either 10, 20, 35, or 40 which per data documentation these
#   are more categories than an actual number of hours, and employment may
#   be seasonal and not year-round.  Better to convert annual to an 
#   hourly estimate than calc an annual salary from hourly.

# set hourly salary as annual salary / 2080 (2080 = 40 hrs x 52 wks)
#   if annual salary not missing, otherwise use hourly_rate
esalary['hourly_salary'] = esalary['hourly_rate']
esalary.loc[~(esalary.annual_salary.isnull()),'hourly_salary'] = esalary['annual_salary']/2080

esalary.info()
esalary.head()

##############  Exploratory Data Analysis  ##############
# fields of interest:
# controls: 
#   job_titles
#   department
#   full_or_part_time
#   salary_or_hourly
# key fields:
#   name_first - use to predict gender
#   hourly_salary

profile = ProfileReport(esalary, title="Pandas Profiling Report")
profile