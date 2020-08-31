# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:09:42 2020

@author: Thillai Subramanian

"""
########################## TASK BLOCK #########################################
# The Exchange Rates for various Countries in the world against USA dollar USD 
# from the year 1950 to 2019 is available in the website (For few countries the
# data is not available fully for above mentioned years).
# By importing this data as CSV file and generating Curves and BarChart displays
# to understand the rise and fall of their countrie's currency against USD. 
# Additionally providing current exchange rates for their currency against USD.

########################## PROGRAM BLOCK ######################################

import csv
import sys
from matplotlib import pyplot as plt
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import pycountry
import locale
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from datetime import datetime
        
# Defining a Class to extract Country code
class Country_code():
    def __init__(self, user_input):   
        # Since the CSV file has only 3 Digit Country Data. From user_input the given 
        # Country Name converted in to 3 digit code by using PYCOUNTRY library.            
        mapping = {country.name: [country.alpha_3, country.alpha_2] for country in pycountry.countries}
        try:
            # To get 3 Digit Country Code.
            self.country_name = mapping.get(user_input)[0] 
            # To get 2 Digit Country Code.
            self.country_name_2 = mapping.get(user_input)[1] 
        except:
            self.country_name = None
            self.country_name_2 = None

# Accessing CSV file
def open_file(filename,country_name):
    with open(filename) as f:
        reader = csv.reader(f)
        rates, year = [], []
        for row in reader: 
            if row[0] == country_name:
                exchange_rate = float(row[6])        
                rates.append(round(exchange_rate, 2))
                year_total = int(row[5])
                year.append(year_total)
                # print(rates)
                # print(year) 
        return rates, year

# To get International Currency Code, by using LOCALE Library.     
def currency_code(country_name_2):            
    name = "en_" + country_name_2
    locale.setlocale(locale.LC_ALL, name)  
    db = locale.localeconv()    
    t = db['int_curr_symbol']
    # print(db)
    # print(t)
    return t

# To get Updated Exchange Rate for any currency against USD, by using FOREX-PYTHON Library.
# forex_dict contains the actual available exchamge rates in FOREX-PYTHON Library.
def forex_dict(t):    
    forex_dict = ['USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 
                  'ISK', 'NOK', 'HRK', 'RUB', 'TRY', 'AUD', 'BRL','CAD', 'SGD',
                  'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR', 'NZD',
                  'PHP','THB', 'ZAR']
    if t in forex_dict:
        c = CurrencyRates()        
        x_c = c.get_rate('USD', t)
        Todays_Rate = (round(x_c, 2))
    else:
        Todays_Rate = None
    return Todays_Rate

# To get International Currency Symbols, by using FOREX-PYTHON Library.
def currency_symbol(t):
    sym = CurrencyCodes()
    s = sym.get_symbol(t)
    #print(s) 
    return s 

# Executing the program and calling the Functions
def execution(user_input):  
    # File taken from the link: https://data.oecd.org/conversion/exchange-rates.htm
    filename = 'DP_LIVE_21072020092417677.csv' 
    
    # Calling Class within Function
    x = Country_code(user_input)
    
    # For invalid input the program will be terminated
    while x.country_name == None:
        print("Please check your input. Kindly type a valid name")
        sys.exit()
    
    # Calling Function open_file()
    rates, year = open_file(filename,x.country_name)
                
    # Calling Function currency_code()
    t = currency_code(x.country_name_2)
    
    # Calling Function forex_dict()
    Todays_Rate = forex_dict(t)
    
    # Calling Function currency_symbol()
    s = currency_symbol(t)
  
    # To get Updated Date and Time, by usimg DATETIME Library
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")  

    # Data Visualization Module
    if len(year) != 0:
        #Make Visualization in MATPLOTLIB   
        plt.figure(dpi=128, figsize=(10, 6))
        plt.plot(year, rates,c="red")
        title = (user_input + "-" + t + " against 1-USD {}-{}".format( year[0], year[-1]))
        plt.title(title, fontsize=20)
        plt.xlabel("YEAR", fontsize=14)
        ylabel = ("{}-{}({}) Value".format(user_input, t, s))
        plt.ylabel(ylabel, fontsize=14)
        plt.tick_params(axis="both", which ="major", labelsize=14)
        plt.grid()
                
        #Make Visualization in PYGAL    
        my_style = LS('#333366', base_style=LCS)  
        chart = pygal.Bar(style=my_style, x_label_rotation = 90, show_legend=False)
        title = user_input + "-" + t + "(" + s + ")" + " against 1-USD($) {}-{}".format(year[0], year[-1])
        chart.title = title
        # For countries has no exchange rates information at FOREX-PYTHON Library
        if Todays_Rate == None:
            chart.x_title = "YEAR \nNote: Current Exchange Rate not available for {}({})".format(t, s)
        # For countries has exchange rates information at FOREX-PYTHON Library
        else:
            chart.x_title ="YEAR \nNote: For now {} 1-USD($) = {} {}({})".format(dt, Todays_Rate,t, s)
        chart.y_title = ("{}-{}({}) Value".format(user_input, t, s))
        chart.x_labels = year
        chart.add('', rates)
        chart.render_to_file('USA to {} Exchange_Rate.svg'.format(user_input))
        chart.render_in_browser()
    
    else :
        print("Unfortunately Exchange Data for {} ({}) not available in the website".format(user_input, t))

#Starting the Program to run
print("Welcome to Exchange Market Data against US Dollar")
user_input = input("Please Enter Country's name (First letter CAPS): ")
execution(user_input) 
    

