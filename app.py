import numpy as np 
import pandas as pd 

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
)

app=Flask(__name__)

weatherdata=pd.read_csv('stations_data.csv')
weatherloc=pd.read_csv('stat_loc.csv')

@app.route('/')
def home():
    """Return the dashboard homepage."""
    return render_template('map.html')

@app.route('/dash')
def dash():
    return render_template('dash.html')

@app.route('/stations')
def stations():
    stations=list(weatherdata['name'].unique())
    stat_sort=sorted(stations)
    return jsonify(stat_sort)

@app.route('/dates')
def dates():
    dates=list(weatherdata['Date'].unique())
    dates_sort=sorted(dates)
    return jsonify(dates_sort)

@app.route('/data/<station>/<date>')
def meteodata(station,date):
    try: 
     mean_t=weatherdata[(weatherdata['name'] == station) & (weatherdata['Date']==date)]['MeanTemp'][0]
    except:
        mean_t='no data'
    # print(weatherdata[(weatherdata['name']==station)&(weatherdata['Date']==date)]['MeanTemp'])
    try:
        prec=weatherdata[(weatherdata['name']==station)&(weatherdata['Date']==date)]['Precip'][0]
    except:
        prec='no data'
    try:
        wind_s=weatherdata[(weatherdata['name']==station)&(weatherdata['Date']==date)]['WindGustSpd'][0]
    except:
        wind_s='no data'
    daydata={}
    daydata['Mean T']=mean_t
    daydata['Prcpt']=prec
    daydata['Wind Sp']=wind_s
    # print(daydata)
    return jsonify(daydata)
    # return str(list(weatherdata[(weatherdata['name'] == station) & (weatherdata['Date']==date)]['MeanTemp'])[0])
    # weatherdata[(weatherdata['name'] == station) & (weatherdata['Date']==date)]['MeanTemp']

@app.route('/location/<station>')
def location(station):
    stat_geo={}
    lat=str(weatherloc[weatherloc['name']==station]['lat'].item())
    lon=str(weatherloc[weatherloc['name']==station]['long'].item())
    stat_geo['name']=station
    stat_geo['lat']=lat
    stat_geo['long']=lon
    return jsonify(stat_geo)

if __name__ == "__main__":
    app.run(debug=True)
