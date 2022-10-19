#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from bokeh.palettes import Spectral5
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc


# 

# Purpose: Output a table displaying the top and bottom five perfoming ETFs given an input of the top 100 ETFs based on market cap and a given data range. Will also output an interactive HTML plot of the top five ETFs. 
# 
# Metrics: "Performance" refers to normalized adjusted closing prices over a given timeframe.
# 
# Data Source: Yahoo Finance
# 
# Requisites: A CSV file containing a list of the top 100 ETFs with a single row of ticker symbols and a column name "Symbol"
# 
# Alternative Uses: Any input file can be utilized so long as it follows the proper formatting and the column header is named "Symbol", though this can easily be altered in the code. 

# 

# In[4]:


#Top 100 ETFs based on market cap (2022-10-16)
ETFs = pd.read_csv("ETFList.csv") #Reads in your input list into "ETFs"


# In[5]:


ETFs_List = ETFs['Symbol'].tolist() #Creates a list from your data to iterate through 


# 

# In[6]:


def adjClose_Grouped():
    '''Returns ONLY Adjusted Closing Historical values for input tickers and Groups them into a single table'''
    Tickers = ETFs_List
    
    SD = input("Enter the Start Date YYYY-MM-DD: ")
    ED = input("Enter the End Date YYYY-MM-DD: ")
    
    #pulls data from yahoo finance and makes a table with ALL ticker data for your specified dates
    data = yf.download(Tickers, start = SD, end = ED)
    
    #Removes all columns aside from the Adjusted Close data
    data = data[["Adj Close"]]
    
    #Returns the data for future use
    return(data)


# 

# In[7]:


def normalize_data(df):
    '''Normalizes datasets by dividing all values by the first'''
    return df/df.iloc[0, :]


# 

# In[8]:


def norm_Grouped_Data():
    '''
    Utilizes adjClose_Grouped function to retrieve grouped adj closed data, then normalizes that data with the 
    normalize_data function
    '''
    data = adjClose_Grouped()
    data_n = normalize_data(data)
    return(data_n)
    type(data_n)


# 

# In[10]:


def plot_data2():
    '''Plots Grouped Normalized Stock Adjusted Close data from yahoo finance.'''
    ETFNormed = norm_Grouped_Data()
    
    #Sorts the values from least to Greatest
    ETFNormed_s = ETFNormed.sort_values(ETFNormed.last_valid_index(), axis=1)
    
    #Drop columns with ALL NaN values
    ETFNormed_s2 = ETFNormed_s.dropna(axis='columns', how ='all')
    
    #Renames columns to JUST the ticker (WAS a tuple -- (Adj Close, TickerName))
    ETFNormed_s2.columns = ['{}'.format(x[1]) for x in ETFNormed_s2.columns]
    
    #BOTTOM 5 performers
    first_n_column  = ETFNormed_s2.iloc[: , :5] #Takes a slice (First 5, thus lowest 5) 
    print("\nBottom 5 Performers: ")
    print(first_n_column.tail(1))
    
    #TOP 5 performers
    Last_5_column  = ETFNormed_s2.iloc[: , -5:] #Takes a slice (Last 5, thus highest 5)
    print("\n \n \nTop 5 Performers: ")
    print(Last_5_column.tail(1), '\n \n \n')
    
    curdoc().theme = 'dark_minimal' #Sets a theme for the plot
    p = figure(width=1600, height=500, x_axis_type="datetime") #Creates an empty figure
    p.title.text = 'Click on legend entries to hide the corresponding lines' #Adds Title
    p.xaxis.axis_label = 'Time' #x-axis label
    p.yaxis.axis_label = 'Normalized Performance' #y-axis label
    df = pd.DataFrame(Last_5_column) #Stores the top 5 (last 5 columns) data as a dataframe named df
    
    #Creates lines, colors the lines, creates a legend, ...
    for x, color in zip(df.columns, Spectral5):
        p.line(df.index, df[x], line_width=2, alpha=0.8, color = color, muted_color = color, legend_label= str('{}'.format(x)))

    p.legend.location = "top_left" 
    p.legend.click_policy="mute" #Mutes colors when selecting an ETF from the interactive legend

    output_file("TopFive.html", title="Top Five Performers") #outputs (and downloads) the plot as an HTML file

    show(p)


# In[11]:


plot_data2()

