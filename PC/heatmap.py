from functools import partial
from random import random,randint
import threading 
import time
from tornado import gen
from os.path import getmtime

from math import pi
import pandas as pd
from random import randint, random
from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.sampledata.unemployment1948 import data

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0], taps=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

class generator(threading.Thread):
    def __init__(self):
        super(generator, self).__init__()
        self.chart_coords = {'x':[],'y':[],'taps':[]}
        self.Pi_coords = {}  
        self.coord = 0
        self.pos = 0
        self.col = 0
        self.row = 0
        self.s = 0        
        
    def chart_dict_gen(self,row, col):
       self.col = col
       self.row = row
       self.chart_coords['x'] = [i for i in range(cla.row)]
       self.chart_coords['y'] = [i for i in range(cla.col, 0, -1)] #reversed list because chart requires that
       self.chart_coords['taps']= [0]*(row * col)
       self.taps = [[0 for y in range(col)] for x in range(row)]
     
    def Pi_dict_gen(self,row,col):
       key = 1
       for x in range(0,row):
           for y in range(0,col):
               self.Pi_coords[key] = (x,y)
               key = key + 1
               
    def Pi_to_chart(self,N):
       x,y = self.Pi_coords[N][0],  self.Pi_coords[N][1]
       return x,y
   
    def run(self):
      while True:
          
        time.sleep(0.1)
        
        h = getmtime("Server_dump.txt")
        if self.s != h:
             self.s = h
             with open('Server_dump.txt') as f:
                m = next(f)
                y,x = self.Pi_to_chart(int(m))
                self.taps[x][y] += 1 
                # but update the document from callback 
                doc.add_next_tick_callback(partial(update, x=x, y=y, taps=self.taps[x][y]))
             

cla = generator()
cla.chart_dict_gen(5,5)
cla.Pi_dict_gen(5, 5)

x = cla.chart_coords['x']
y = cla.chart_coords['y']
taps = cla.chart_coords['taps']

@gen.coroutine
def update(x, y, taps):
   taps += taps
   print(taps)
   source.stream(dict(x=[x], y=[y], taps=[taps]))

colors = ["#CCEBFF","#B2E0FF","#99D6FF","#80CCFF","#66c2FF","#4DB8FF","#33ADFF","#19A3FF", "#0099FF", "#008AE6", "#007ACC","#006BB2", "#005C99", "#004C80", "#003D66", "#002E4C", "#001F33", "#000F1A", "#000000"]
mapper = LinearColorMapper(palette=colors, low= 0, high= 15) #low = min(cla.chart_coords['taps']) high = max(cla.chart_coords['taps'])

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"


p = figure(title="Taps heatmap ({0} - {1})".format(x[0], x[-1]),
           x_range= list(map(str,x)),
           y_range= list(map(str,reversed(y))),
           x_axis_location="above",
           plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below',
           tooltips=[('date', '@y @x'), ('taps', '@taps%')])


p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="x", y="y",
       width=1, height=1,
       source=source,
       fill_color={'field': 'taps', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper,
                     major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))

p.add_layout(color_bar, 'right')

doc.add_root(p)

thread = cla
thread.start()

"""
def ch(row, col):
       chart_coords = {'x':[],'y':[],'taps':[]}
       col = col    
       for x in range(0,row):
           for mult in range(0,col):
               chart_coords['x'].append(x)
       for mult in range(0,row):
           for y in range(0,col):
               chart_coords['y'].append(y)
       chart_coords['taps']= [0]*(row * col)
       for i in range(row * col):
          chart_coords['taps'][i] = randint(1,20)
       return chart_coords
"""
