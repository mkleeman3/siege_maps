#!/usr/bin/env python
# coding: utf-8

# In[8]:


# https://towardsdatascience.com/creating-an-interactive-map-in-python-using-bokeh-and-pandas-f84414536a06

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import PRGn, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
import numpy as np
import pandas as pd


# In[9]:


sieges_df = pd.read_csv('data/sieges.csv', index_col=0, encoding='cp1252')


# In[10]:


sieges_df.head()


# In[11]:


# Define function to switch from lat/long to mercator coordinates

def x_coord(x, y):
    
    lat = x
    lon = y
    
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x/lon
    y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + 
        lat * (np.pi/180.0)/2.0)) * scale
    return (x, y)

# Define coord as tuple (lat,long)

sieges_df['coordinates'] = list(zip(sieges_df['lat'], sieges_df['lon']))

# Obtain list of mercator coordinates

mercators = [x_coord(x, y) for x, y in sieges_df['coordinates'] ]


# In[12]:


# Create mercator column in our df

sieges_df['mercator'] = mercators

# Split that column out into two separate columns - mercator_x and mercator_y

sieges_df[['mercator_x', 'mercator_y']] = sieges_df['mercator'].apply(pd.Series)


# In[13]:


sieges_df.head()


# In[24]:


# Select tile set to use

chosentile = get_provider(Vendors.STAMEN_TONER)


# In[25]:


# Choose palette

palette = RdYlGn[11]


# In[26]:


# Tell Bokeh to use df as the source of the data

source = ColumnDataSource(data=sieges_df)


# In[27]:


# Define color mapper - which column will define the colour of the data points

color_mapper = linear_cmap(field_name = 'Casualties', palette = palette, low = sieges_df['Casualties'].min(), high = sieges_df['Casualties'].max())


# In[43]:


# Set tooltips - these appear when we hover over a data point in our map, very nifty and very useful

tooltips = [('Casualties','@Casualties'), ('Siege','@Siege'), ('Year','@Year')]


# In[44]:


# Create figure

p = figure(title = 'Historical Battles & Sieges by Number of Casualties', x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude', tooltips = tooltips)


# In[45]:


# Add map tile

p.add_tile(chosentile)


# In[46]:


# Add points using mercator coordinates

p.circle(x = 'mercator_x', y = 'mercator_y', color = color_mapper, source=source, size=30, fill_alpha = 0.7)


# In[47]:


#Defines color bar

color_bar = ColorBar(color_mapper=color_mapper['transform'], 
                     formatter = NumeralTickFormatter(format='0.0[0000]'), 
                     label_standoff = 13, width=8, location=(0,0))

# Set color_bar location

p.add_layout(color_bar, 'right')

curdoc().add_root(column(p))


# In[48]:


# Display in notebook

# output_notebook()

# Save as HTML

# output_file('sieges.html', title='Historical Battles & Sieges by Number of Casualties')


# In[50]:


# Show map

# show(p)


# In[ ]:




