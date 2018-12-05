import sqlite3
from flask import Flask, jsonify, send_file, request
from flask import g
from  datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import gdal, ogr, os, osr

from metpy.calc import get_wind_components
from metpy.calc import reduce_point_density
#from metpy.plots import add_metpy_logo, current_weather, sky_cover, StationPlot, wx_code_map
from metpy.plots import (add_metpy_logo, current_weather, simple_layout, StationPlot, StationPlotLayout, wx_code_map)
from metpy.units import units
import pandas as pd
import math


DATABASE = './metar.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index(): 
    return 'Index'

@app.route('/metar/available')
def available():
    cur = get_db().cursor()
    ret = []
    cur.execute("""
       SELECT 
         distinct strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') as date, 
        count(*) cnt from metar 
       GROUP BY strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') 
	""")
    res = cur.fetchall()

    for r in res:
      ret.append({'geojson': 'http://localhost:5000/metar/date/%s' % r[0], 'url' : 'http://localhost:5000/metar/image/%s' % r[0], 'time': datetime.strptime(r[0], "%Y%m%d%H").isoformat(), 'cnt': r[1]})

    return jsonify({'options' : ('withmap', 'temp', 'presentweather', 'barbs'),'data': ret})

@app.route('/metar/date/<date>')
def metarByDate(date):
    cur = get_db().cursor()
    t = (date,)
    cur.execute("""
      SELECT m.date,
             cast(m.vsby as float) as vis,
	     cast(m.wspd as float) as wspd,
	     cast(m.wdir as float) as wdir,
	     cast(s.lat_prp as float) as lat,
	     cast(s.lon_prp as float) as lon,
	     m.sig_prst_wx,
	     m.c_stn_id as stid
	     FROM metar m, stations s 
             WHERE m.c_stn_id = s.icao 
             AND strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') = ?
             AND s.lon_prp != '' 
             AND s.lat_prp != '' 
      """, t)

    res = cur.fetchall()
    res = list(map(lambda r: {'time': datetime.strptime(r[0], "%Y%m%d%H%M%S").isoformat(),  'vsby' : r[1], 'wspd' : r[2], 'wdir' : r[3], 'lat' : r[4], 'lon': r[5], 'sig_prst_wx' : r[6]}, res))
    res = {'type' : "FeatureCollection", 'features' : list(map(lambda r : {"type" : "Feature", "geometry" : {"coordinates" : [r['lon'], r['lat']], "type" : "Point"}, "properties" : r}, res))}
    return jsonify(res)

@app.route('/metar/station/<station>')
def metar(station):
    cur = get_db().cursor()
    t = (station,)
    cur.execute("SELECT m.*, s.lat_prp, s.lon_prop FROM metar m, stations s WHERE m.c_stn_id = s.icao AND m.c_stn_id = ?", t)
    res = cur.fetchall()
    return jsonify({'data': res})
 
@app.route('/metar/image')
def metarImage():
    return 'try /metar/image/date'
    
@app.route('/metar/geojson/<dt>')
def metarGeojsonByDate(dt, *args):
    t = (dt,)
    df = pd.read_sql_query("""
      SELECT
             strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') as date, 
             cast(m.vsby as float) as vis,
	     cast(m.wspd as float) as wspd,
	     cast(m.wdir as float) as wdir,
	     cast(m.tmp as float) as tmp,
	     cast(m.dpd as float) as dpd,
	     cast(m.pres_msl as float) as pres_msl,
	     cast(m.lw_cl_am as float) as lw_cl_am,
	     cast(s.lat_prp as float) as lat,
	     cast(s.lon_prp as float) as lon,
	     m.sig_prst_wx,
	     m.c_stn_id as stid
	     FROM metar m, stations s 
	     WHERE m.c_stn_id = s.icao 
	     AND strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') = ?
	     AND s.lon_prp != '' 
	     AND s.lat_prp != '' AND sig_prst_wx not like '%?%' 
      """, get_db(), params=t)

    #res = list(filter(lambda r : '?' not in ''.join(str(i) for i in r), res));
    #res = list(map(lambda r: {'time': datetime.strptime(r[0], "%Y%m%d%H%M%S").isoformat(),  'vsby' : r[1], 'wspd' : r[2], 'wdir' : r[3], 'lat' : r[4], 'lon': r[5], 'sig_prst_wx' : r[6]}, res))
    #res = np.fromiter(res, count=numrows, dtype=('str, str'))
    #list(map(lambda r: ('time': datetime.strptime(r[0], "%Y%m%d%H%M%S").isoformat(),  'vsby' : r[1], 'wspd' : r[2], 'wdir' : r[3], 'lat' : r[4], 'lon': r[5], 'sig_prst_wx' : r[6]), res))
    return df.to_json(orient="records")
    
@app.route('/metar/image/<dt>')
def metarImageByDate(dt, *args):
    t = (dt,)
    df = pd.read_sql_query("""
      SELECT
             strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') as date, 
             cast(m.vsby as float) as vis,
	     cast(m.wspd as float) as wspd,
	     cast(m.wdir as float) as wdir,
	     cast(m.tmp as float) as tmp,
	     cast(m.dpd as float) as dpd,
	     cast(m.pres_msl as float) as pres_msl,
	     cast(m.lw_cl_am as float) as lw_cl_am,
	     cast(s.lat_prp as float) as lat,
	     cast(s.lon_prp as float) as lon,
	     m.sig_prst_wx,
	     m.c_stn_id as stid
	     FROM metar m, stations s 
	     WHERE m.c_stn_id = s.icao 
	     AND strftime('%Y%m%d%H' ,substr(date,0,5) || '-' || substr(date,5,2) || '-' || substr(date,7,2) ||' '|| substr(date, 9,2) || ':00:00') = ?
	     AND s.lon_prp != '' 
	     AND s.lat_prp != '' 
	     AND CAST(wspd as INTEGER) > 0 
	     AND sig_prst_wx not like '%?%' 
      """, get_db(), params=t)

    #res = list(filter(lambda r : '?' not in ''.join(str(i) for i in r), res));
    #res = list(map(lambda r: {'time': datetime.strptime(r[0], "%Y%m%d%H%M%S").isoformat(),  'vsby' : r[1], 'wspd' : r[2], 'wdir' : r[3], 'lat' : r[4], 'lon': r[5], 'sig_prst_wx' : r[6]}, res))
    #res = np.fromiter(res, count=numrows, dtype=('str, str'))
    #list(map(lambda r: ('time': datetime.strptime(r[0], "%Y%m%d%H%M%S").isoformat(),  'vsby' : r[1], 'wspd' : r[2], 'wdir' : r[3], 'lat' : r[4], 'lon': r[5], 'sig_prst_wx' : r[6]), res))
    filename = generateImage(df, request);

    return send_file(filename, mimetype='image/gif')

def generateImage(data_arr, request):
  extent = request.args.get('extent')
  extent = tuple(map(lambda x : float(x), extent.split(","))) if extent is not None else (-180, 180, -90, 90)
  
  print(extent)
  useMap = request.args.get('withmap')
  barbs  = request.args.get('barbs')
  temp  = request.args.get('temp')
  dewpoint = request.args.get('dewpoint')
  width= float(request.args.get('width'))
  height = float(request.args.get('height'))
  #width=720;
  #height=361;
  presentweather = request.args.get('presentweather')

  data = {}

  # Copy out to stage everything together. In an ideal world, this would happen on
  # the data reading side of things, but we're not there yet.
  data['longitude'] = data_arr['lon'].values
  data['latitude'] = data_arr['lat'].values
  data['stid'] = data_arr['stid'].values
  data['air_temperature'] = data_arr['tmp'].values * units.degC
  data['dew_point_temperature'] = data_arr['dpd'].values * units.degC
  data['air_pressure_at_sea_level'] = data_arr['pres_msl'].values * units('mbar')
  

  # Convert the fraction value into a code of 0-8, which can be used to pull out
  # the appropriate symbol
#  data['cloud_coverage'] = (8 * data_arr['lw_cl_am']).fillna(10).values.astype(int)

  # Map weather strings to WMO codes, which we can use to convert to symbols
  # Only use the first symbol if there are multiple

  data_arr['sig_prst_wx'] =  data_arr['sig_prst_wx'].apply(lambda i: i if i in  wx_code_map else '')
  wx_text = data_arr['sig_prst_wx']
  data['present_weather'] = [wx_code_map[s.split()[0] if ' ' in s else s] for s in wx_text]

  # Create the figure and an axes set to the projection
  proj = ccrs.PlateCarree() #LambertConformal(central_longitude=-95, central_latitude=35, standard_parallels=[35])

  # Create the figure and an axes set to the projection
  dpi = 96.

  fig = plt.figure(figsize=((width/dpi)  , (height/dpi)))
  #ax = fig.add_subplot(111, projection=proj, rect=[0,0,1,1])
  ax = fig.add_axes([0,0,1,1], projection=proj)
  ax.set_extent(extent, ccrs.PlateCarree())
  #ax.set_axis_off()

  ax.outline_patch.set_visible(False)
  ax.background_patch.set_visible(False)


  if(useMap is not None):
    #ax.add_feature(cfeature.LAND)
       ax.add_feature(cfeature.OCEAN, zorder=1)
  #    ax.add_feature(cfeature.LAKES)
       ax.add_feature(cfeature.COASTLINE, zorder=1, alpha=0.5)
  #    ax.add_feature(cfeature.BORDERS)

  stationplot = StationPlot(ax, data['longitude'], data['latitude'],
                              transform=ccrs.PlateCarree(), fontsize=15, clip_on=True)

  stationplot.plot_text((2, 0), data['stid'])
  # Plot the temperature and dew point to the upper and lower left, respectively, of
  # the center point. Each one uses a different color.

  if (temp is not None):
      stationplot.plot_parameter('NW', data['air_temperature'], color='red')

  if (dewpoint is not None):
      stationplot.plot_parameter('SW', data['dew_point_temperature'], color='darkgreen')

  # A more complex example uses a custom formatter to control how the sea-level pressure
  # values are plotted. This uses the standard trailing 3-digits of the pressure value
  # in tenths of millibars.
  #stationplot.plot_parameter('NE', data['slp'], formatter=lambda v: format(10 * v, '.0f')[-3:])

  # Plot the cloud cover symbols in the center location. This uses the codes made above and
  # uses the `sky_cover` mapper to convert these values to font codes for the
  # weather symbol font.
  #stationplot.plot_symbol('C', cloud_frac, sky_cover)
  
  # Same this time, but plot current weather to the left of center, using the
  # `current_weather` mapper to convert symbols to the right glyphs.
  if (presentweather is not None):
      stationplot.plot_symbol('W', data['present_weather']  , current_weather, backgroundcolor='w', fontsize=20, color='black')
  
  # Add wind barbs
  #stationplot.plot_barb(u, v, zorder=2)
  if (barbs is not None):
      u, v = get_wind_components(data_arr['wspd'].values * units('m/s'),
                                     data_arr['wdir'].values * units.degree)
      data['eastward_wind'], data['northward_wind'] = u, v
      stationplot.plot_barb(u,v, flagcolor='r', barbcolor=['b', 'g'], barb_increments=dict(half=10, full=20, flag=100), flip_barb=True , zorder=2 )

  plt.plot(data['longitude'], data['latitude'], marker='o', color='r', linestyle='none', markersize=6, alpha=0.5)
  

  filename = "test.png";
  plt.savefig(filename, dpi=dpi , transparent=True)
  plt.close()

  return filename;
    
def arrayToRaster(array,fileName,EPSGCode,origin,numBands):
    xPixels = array.shape[1]  # number of pixels in x
    yPixels = array.shape[0]  # number of pixels in y
    pixelXSize =origin[0]#//(xMax-xMin)/xPixels # size of the pixel in X direction     
    pixelYSize = origin[1]#-(yMax-yMin)/yPixels # size of the pixel in Y direction

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(fileName,xPixels,yPixels,numBands,gdal.GDT_Byte, options = [ 'PHOTOMETRIC=RGB' ])
    dataset.SetGeoTransform((xMin,pixelXSize,0,yMax,0,pixelYSize))  

    datasetSRS = osr.SpatialReference()
    datasetSRS.ImportFromEPSG(EPSGCode)
    dataset.SetProjection(datasetSRS.ExportToWkt())
    
    for i in range(0,numBands):
        dataset.GetRasterBand(i+1).WriteArray(array[:,:,i])

    dataset.FlushCache()  # Write to disk.


app.run(debug=True)
