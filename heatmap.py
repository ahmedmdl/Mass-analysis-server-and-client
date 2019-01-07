from math import pi
import pandas as pd
from random import randint
from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.sampledata.unemployment1948 import data

def cj(row, col):
       chart_coords = {'x':[],'y':[],'taps':[]}
       for x in range(0,row):
           for mult in range(0,col):
               chart_coords['x'].append(x)
       for mult in range(0,row):
           for y in range(0,col):
               chart_coords['y'].append(y)
       chart_coords['taps']= [0]*(row * col)
       return pd.DataFrame.from_dict(chart_coords)

if __name__ == '__main__':
   data = cj(20,30)
  # print(data)
   for i in range(0,600):
       data['taps'][i] = randint(0,30)
   data['x'] = data['x'].astype(str)
   data['y'] = data['y'].astype(str)
   #data = data.set_index('x')
   #data.columns.name = 'x'

   df = data
   print(df)
   y = sorted(set(df.y),key=int)
   x = sorted(set(df.x),key=int)
   print(x,y)
   
   #df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
   colors = ["#CCEBFF","#B2E0FF","#99D6FF","#80CCFF","#66c2FF","#4DB8FF","#33ADFF","#19A3FF", "#0099FF", "#008AE6", "#007ACC","#006BB2 ", "#005C99", "#004C80", "#003D66", "#002E4C", "#001F33", "#000F1A", "#000000"]
   mapper = LinearColorMapper(palette=colors, low=df.taps.min(), high=df.taps.max())

   TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

   p = figure(title="Taps heatmap ({0} - {1})".format(x[0], x[-1]),x_range=x, y_range=list(reversed(y)), x_axis_location="above", plot_width=900, plot_height=400, tools=TOOLS, toolbar_location='below', tooltips=[('date', '@y @x'), ('taps', '@taps%')])

   p.grid.grid_line_color = None
   p.axis.axis_line_color = None
   p.axis.major_tick_line_color = None
   p.axis.major_label_text_font_size = "5pt"
   p.axis.major_label_standoff = 0
   p.xaxis.major_label_orientation = pi / 3

   p.rect(x="x", y="y", width=1, height=1,source=df,fill_color={'field': 'taps', 'transform': mapper}, line_color=None)

   color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt", ticker=BasicTicker(desired_num_ticks=len(colors)),formatter=PrintfTickFormatter(format="%d%%"),label_standoff=6, border_line_color=None, location=(0, 0))
   p.add_layout(color_bar, 'right')
   show(p)

