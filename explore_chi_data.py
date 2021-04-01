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
bus_monthly_avg = pd.read_json("https://data.cityofchicago.org/resource/bynn-gwxy.json")
bus_monthly_avg.head()