from functools import partial
from random import random
import threading 
import time
from tornado import gen
from os.path import getmtime

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure



# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

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
       for x in range(0,row):
           for mult in range(0,col):
               self.chart_coords['x'].append(x)
       for mult in range(0,row):
           for y in range(0,col):
               self.chart_coords['y'].append(y)
       self.chart_coords['taps']= [0]*(row * col)
       #return pd.DataFrame.from_dict(chart_coords)
    
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
                # but update the document from callback 
                doc.add_next_tick_callback(partial(update, x=x, y=y))

cla = generator()
cla.chart_dict_gen(3,3)
cla.Pi_dict_gen(3, 3)

@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))

p = figure(x_range=[0, 15], y_range=[0,15])
l = p.circle(x='x', y='y', source=source)

doc.add_root(p)

thread = cla
thread.start()

