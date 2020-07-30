#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
import json
import pandas as pd
import numpy as np
import math
import time
import pprint
from datetime import date, datetime, timedelta

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, Label
from bokeh.palettes import brewer
from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select, Button, Text
from bokeh.layouts import widgetbox, row, column

#SHAPEFILE --> https://www.arcgis.com/home/item.html?id=dcbcdf86939548af81efbd2d732336db
shapefile = 'data/1m_admin_canada/Canada.shp'
sf = gpd.read_file(shapefile)[['NAME', 'geometry']]
sf.columns = ['province', 'geometry'] 
sf.loc[sf['province'] == 'Yukon Territory', 'province'] = 'Yukon' #Replace Yukon Territory by Yukon 

#CANADA-COVID
datafile = 'https://health-infobase.canada.ca/src/data/covidLive/covid19.csv'
df = pd.read_csv(datafile, skipinitialspace=True, usecols=['prname', 'date', 'numdeaths', 'numtotal', 'numrecover']) #selec columns

# This dictionary contains the formatting for the data in the plots (by category)
format_data = [('numtotal', 0, 50000,'0,0', 'Total Cases'),
            ('numdeaths', 0, 5000,'0,0', 'Deaths'),
            ('numrecover', 0, 50000, '0,0', 'Recovered')]

#Create a DataFrame object from the dictionary 
format_df = pd.DataFrame(format_data, columns = ['field' , 'min_range', 'max_range' , 'format', 'case_category'])

def json_data(selectedDate):
    
    date_from_slider = selectedDate
    merged_by_date = df[df['date'] == date_from_slider]
    
    if not merged_by_date.empty: # if dataframe is empty take the previous values

        #Select Total
        global cases_canada
        cases_canada = merged_by_date[merged_by_date['prname'] =='Canada']
        
        ##GeneralData
        merged_by_date = df[df['date'] == date_from_slider]  
        merged = sf.merge(merged_by_date, left_on = 'province', right_on = 'prname', how='left')
        merged.fillna('No data', inplace = True) ##Replace null values

        #JSON
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data
    else:
        print('EMPTY DATAFRAME: DATE Without CASES') ##NEED TO BE FIX

def make_plot(field_name, field_date):    
        
    # format of the colorbar
    min_range = format_df.loc[format_df['field'] == field_name, 'min_range'].iloc[0]
    max_range = format_df.loc[format_df['field'] == field_name, 'max_range'].iloc[0]
    field_format = format_df.loc[format_df['field'] == field_name, 'format'].iloc[0] #format integers

    # LinearColorMapper that maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, 
                                     low = min_range, 
                                     high = max_range,
                                     nan_color = '#d9d9d9' #GRAY
                                    )
    
    if max_range == 5000:
        tick_labels = {
                '0': '>0', 
                '100':'>100', 
                '500':'>500', 
                '1000':'>1000', 
                '2500':'>2500', 
                '5000':'>5000'
            }
    else:
        tick_labels = {
                '0': '>0', 
                '1000':'>1000', 
                '5000':'>5000', 
                '10000':'>10000', 
                '30000':'>30000', 
                '50000':'>50000'
            } 
    
    # Create color bar.
    format_tick = NumeralTickFormatter(format=field_format)
    
    color_bar = ColorBar(color_mapper=color_mapper,
                         label_standoff=10, 
                         #formatter=format_tick,
                         border_line_color=None,
                         location = (0, 0), 
                         major_label_overrides = tick_labels
                         )
    
    # Create figure object.
    #case_category = format_df.loc[format_df['field'] == field_name, 'case_category'].iloc[0]
    
    p = figure(title = ('Covid-19 Canada : ' + str(field_date)), # update date
                        plot_width = 850,
                        plot_height = 700, 
                        toolbar_location = None)
    
    p.background_fill_color = "whitesmoke"
    p.background_fill_alpha = 0.5
    
    # Create banner with total cases
    case_category = format_df.loc[format_df['field'] == field_name, 'case_category'].iloc[0]
    
    if case_category=='Total Cases':
        valor_total = cases_canada['numtotal'].values[0]
    if case_category=='Deaths':
        valor_total = cases_canada['numdeaths'].values[0]
    if case_category=='Recovered':
        valor_total = cases_canada['numrecover'].values[0]
    
    if np.isnan(valor_total): #NaN to 0
        valor_total=0

    total_text = case_category +" : "+ str(int(valor_total))

    citation = Label(x=60, y=50, 
                    x_units='screen', y_units='screen',
                    text=total_text, 
                    render_mode='css',
                    #border_line_color='red',
                    border_line_alpha=1.0,
                    background_fill_color='white', 
                    background_fill_alpha=1.0)
    p.add_layout(citation)

    #Layout conf
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    
    # Add patch renderer to figure. 
    p.patches('xs','ys', 
              source = geosource, 
              fill_color = {'field' : field_name, 'transform' : color_mapper},
              line_color = 'black', 
              line_width = 0.25, 
              fill_alpha = 1)

    # Specify color bar layout.
    p.add_layout(color_bar, 'right')

    # Add the hover tool to the graph
    p.add_tools(hover)
    return p 

def update_plot(attr, old, new):
    
    # The input is the date selected from the slider
    rest = (total_days - int(slider.value))
    last_date = datetime.strptime(yesterday, '%d-%m-%Y')
    selected_date = (last_date - timedelta(days=rest)) #Ex. 2020-06-17 07:04:02.936282
    date_from_slider = selected_date.strftime('%d-%m-%Y')
    new_data = json_data(date_from_slider)

    # The input cr is the criteria selected from the select box
    cr = select.value
    input_field = format_df.loc[format_df['case_category'] == cr, 'field'].iloc[0]
    
    # Update the plot based on the changed inputs
    p = make_plot(input_field, date_from_slider)
    
    # Update the layout, clear the old document and display the new document
    layout = column(p, column(slider), column(select), column(button))
    curdoc().clear()
    curdoc().add_root(layout)
    
    geosource.geojson = new_data # Update the data

def animate_update():
    ant_date = slider.value + 10
    if ant_date > total_days:
        button.label = '► Play'
        ant_date = 0
        return None
    else:
        button.label = '❚❚ Pause' 

    slider.value = ant_date

def animate():
    global callback_id
    if button.label == '► Play':
        slider.value = 0
        button.label = '❚❚ Pause' #PLAY ANIMATION
        callback_id = curdoc().add_periodic_callback(animate_update, 100) #miliseconds
    else:
        button.label = '► Play' #PAUSE ANIMATION
        curdoc().remove_periodic_callback(callback_id)

#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

first_case = date(2020, 1, 31) #date of first case reported
today_date = date.today() # update date
today_date = (today_date - timedelta(days=1)) # works with dates of yesterday (last cases)

yesterday = today_date.strftime('%d-%m-%Y')
total_days = ((today_date - first_case).days)

geosource = GeoJSONDataSource(geojson = json_data(yesterday)) # first plot
input_field = 'numtotal' #first category

pallete_color = 'OrRd'
palette = brewer[pallete_color][5]
palette = palette[::-1] # Reverse color order

#--------------------------------------------------------------#
# Add hover tool
hover = HoverTool(tooltips = [ ('Provinces/territorie','@province'),
                               ('Total Cases', '@numtotal'),
                               ('Deaths', '@numdeaths'),
                               ('Recovered', '@numrecover')
                               ])

# Call the plotting function
p = make_plot(input_field, yesterday)
#--------------------------------------------------------------#
select = Select(title='Select Criteria', 
                value='Total Cases', 
                options=['Total Cases', 'Deaths', 'Recovered'],  
                width=300)
select.on_change('value', update_plot)
#--------------------------------------------------------------#

#--------------------------------------------------------------#
slider = Slider(title=None, 
                start=0, 
                end=total_days, 
                value=total_days, 
                step=7, 
                width=800)
slider.on_change('value', update_plot)
#--------------------------------------------------------------#

callback_id = None
button = Button(label='► Play')
button.on_click(animate)

# Display the current document
layout = column(p, column(slider), column(select), column(button))

curdoc().add_root(layout)
curdoc().title = "Covid-19 Canada"

#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#