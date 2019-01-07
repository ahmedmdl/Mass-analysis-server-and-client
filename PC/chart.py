from functools import partial
from random import random
import threading 
import time

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen
from os.path import getmtime

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

class generator(threading.Thread):
    def __init__(self):
        super(generator, self).__init__()
        self.chart_coords = {'x':[],'y':[],'taps':[]}
        self.key = 0
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
       for y in range(0,col):
           for mult in range(0,row):
               self.chart_coords['y'].append(y)
       self.chart_coords['taps']= [0]*(row * col)
    
    def Pi_dict_gen(self,row,col):
       for y in range(0,col):
           for x in range(0,row):
               self.Pi_coords[self.key] = (x,y)
               self.key = self.key + 1
    def Pi_to_chart(self,N):
       self.coord = self.Pi_coords[N]
       self.pos = self.Pi_coords[N][0] * self.col + self.Pi_coords[N][1] 
       self.chart_coords['taps'][self.pos] += 1
       return self.pos
    def run(self):
      while True:
        # do some blocking computation
        time.sleep(0.1)
        h = getmtime("Server_dump.txt")
        #print(h,s)
        if self.s != h:
             self.s = h
             with open('Server_dump.txt') as f:
                m = next(f)
             print(m)
             if m[0] == 'r':
                x = self.Pi_to_chart(int(m[1])) 
             if m[0] == 'c' 
                y = self.Pi_to_chart(int(m[1]))
                # but update the document from callback 
                doc.add_next_tick_callback(partial(update, x=x, y=y))

cla = generator()
cla.chart_dict_gen(3,5)
cla.Pi_dict_gen(3, 5)

@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))

p = figure(x_range=[0, 15], y_range=[0,15])
l = p.circle(x='x', y='y', source=source)

doc.add_root(p)

thread = cla
thread.start()

