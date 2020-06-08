from flask import Flask, render_template, request, redirect

import requests

from io import StringIO

import csv

import pandas as pd

import numpy as np
from math import pi

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, DatetimeTickFormatter  
from bokeh.models.tools import HoverTool
from bokeh.embed import file_html, components
from bokeh.resources import CDN 

app = Flask(__name__)


#@app.route('/', methods = ['GET', 'POST'])
@app.route('/send', methods = ['GET', 'POST'])
def send():
  if request.method == 'POST':
    ticker = request.form['ticker']

    url = "https://www.alphavantage.co/query?"

    payload = {"function":"TIME_SERIES_DAILY","symbol":ticker,"outputsize":"compact", "datatype":"csv", "apikey": "Q5SR5ZD47LDY44VJ"}

    response = requests.get(url, params=payload)

    response_text = response.text

    temp = StringIO(response_text)

    df = pd.read_csv(temp)

    df['date'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d')

    #output_file('stock_chart.html')

    source = ColumnDataSource(df)

    p = figure()
    p.circle(x='date', y='close',
             source=source,
             size=5, color='green')

    p.title.text = 'Stock Price - 6 Months Period'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'

    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = pi/4

    hover = HoverTool()
    hover.tooltips=[
        ('TIME', '@timestamp'),
        ('PRICE', '@close'),
    ]

    p.add_tools(hover)

    script, div = components(p)

    return render_template("stock_chart.html", script=script, div=div, ticker = ticker)

  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=5000, debug=True)