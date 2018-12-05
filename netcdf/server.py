import importlib, json , sqlite3
from  models import *
from  models import ModelBase
from models.imports import *
import models.PlotUtils as PlotUtils
import models.QueryUtils as  QueryUtils
from flask import Flask, jsonify, send_file, request, g
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index(): 
    return 'Index'

@app.route('/icap/plotNetcdf')
def plotNetcdf(*args):
    layers  = json.loads(request.args.get('layers'))
    mapName  = request.args.get('mapName')
    #field  = model['var']
    print(layers)
   # field  = request.args.get('field')
   # spec  = request.args.get('specie')

    dtg   = request.args.get('dtg')
    hour  = float(request.args.get('hour'))
    extent = request.args.get('extent')
    withMap = request.args.get('withMap')
    width=   request.args.get('width')
    height = request.args.get('height')
    region = request.args.get('region')
    #options  = model['options']

    if extent is None: 
       extent = "-180,90,180,-90"

    width = 800 if width is None else float(width)
    height = 600 if height is None else float(height)

    #modelInstances = [];
    #nm = QueryUtils.getModelInstance(model['model'], dtg, varname=field, level=options["level_id"])
    #nm['options'] = options

    filepath = PlotUtils.netcdfPlot(layers, dtg,  extent, hour, withMap, width, height, region, mapName)
    if(os.path.exists(filepath)):
        return send_file(filepath, mimetype='image/gif')
    else:
        return filepath


@app.route('/latest')
def getLatest(*args):
    model  = request.args.get('model')
    dtg   = request.args.get('dtg')
    field  = request.args.get('field')
    
    nw = QueryUtils.getModelInstance(model, dtg, field)
    PlotUtils.getLatest(nw)

    return jsonify("get latest")

@app.route('/available')
def getImagePaths(*args):
    modelName = request.args.get('model')
    dtg   = request.args.get('dtg')
    var   = request.args.get('field')
    nw    = QueryUtils.getModelInstance(modelName, dtg, var)

    return jsonify(PlotUtils.getImagePaths(nw, var))


@app.route('/discover')
def discover(*args):
    ignoreme = ["forecast_period", "lat", "hybrid", "time","latitude", "lon", "longitude"]
    #H08_20180813_0000_1DARP030_FLDK.02401_02401.nc
    model  = request.args.get('model')
    dtg    = request.args.get('dtg')
    res    = []

    try:
        nm = QueryUtils.getModelInstance(model, dtg)
        if 'ncfile' in nm:
             path = nm['ncfile']
             ncfile  = Dataset(path)
             nvars, dims = PlotUtils.getVars(ncfile)
             
             for idx, k in enumerate(nvars.keys()):
                if k.lower() not in ignoreme: 
                    vdims = nvars[k].dimensions
                    dimdict = {}
                    for dk in vdims:
                      if dk not in ignoreme and dk not in dimdict:
                          if dk in nvars: dimdict[dk] = nvars[dk][:].tolist()

                    #some vars aren't plottable .. electromagnetic_wavelength, forecast_period. 
                    if len(nvars[k].shape) > 0:
                        v  =  {"name" : k, "dims" : dimdict}
                        if 'wnd_ucmp_isobaric' in nvars: v['hasWind'] = True
                        #v['levels'] = plt_dict[nm.field]['levs']
                        res.append(v)

             ncfile.close()
    except:
      pass;

    return jsonify(res)

@app.route('/icap/getColors')
def getColors(): 
    return QueryUtils.getColors()

@app.route('/icap/getProducts')
def getProducts(): 
  return QueryUtils.getProducts()

@app.route('/icap/updateColor', methods=['POST'])
def updateColor(): 
  json = request.get_json()
  print(json)
  colorId  = json.get('colorId')
  domains = json.get('domains')
  palette  = json.get('palette')
  QueryUtils.updateColor(colorId, domains, palette)
  return QueryUtils.getColors()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
