from models.imports import *
from multiprocessing import Pool
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import glob, math, re, hashlib,time, traceback
import matplotlib.colors as colors
import matplotlib.ticker as mticker
import models.ColorUtils as ColorUtils
from collections import OrderedDict
from netCDF4 import  num2date
import models.QueryUtils as QueryUtils
import math, base64
import uwsgi


plot_dir = "/plots"
plot_out_dir = ""
dpi = 96 
ncfileDict = {}

def getMidpoint(lon1,lon2,lat1,lat2):
    Bx = math.cos(lat2) * math.cos(lon2-lon1);
    By = math.cos(lat2) * math.sin(lon2-lon1);
    latMid = math.atan2(math.sin(lat1) + math.sin(lat2),
                   math.sqrt( (math.cos(lat1)+Bx)*(math.cos(lat1)+Bx) + By*By ) );
    lonMid = lon1 + math.atan2(By, math.cos(lat1) + Bx);
    return lonMid

def getOptsStr(layers):
    m = hashlib.md5()
 
    for l in layers: 
        opts = l['options']
        optsStr = opts['level'] +  \
                  str(opts['alpha'] if 'alpa' in opts else 1) + \
                  opts['Contour Type'] if 'Contour Type' in opts else 'filled'

        m.update(base64.b64encode(bytes(optsStr, 'utf-8')))
    return m.digest()


def getFoot(dtg, model):
    return 'Plots Generated ' + getDisplayDate(dtg) + ' NRL/Monterey'

def to180(d):
    return (((d + 180) % 360) -180)

def getHead(analysisTime, vt,  tau, model, var, title):
    timeStr = getDisplayDate(analysisTime)
    vtime   = getDisplayDate(vt)

    title = "%s  %s t+%s \n%s Valid Time\n%s %s" %  \
             (timeStr, model, str(tau).zfill(3), vtime, var.upper(), title)
    title = title.replace('NMMB-','NMMB/')
    #if is_ens: title = ' '.join(( title, '(', 'nMEM', '=', str(nens), ')' ))
    return title

def getDisplayDate(dtg):
    return datetime.strftime(dtg, "%A %d %B %Y %H") + " UTC"

def processTimeDim(ncfile, model, dtg, file):
    print("ptimedim",model['name'] )
    variables = ncfile.variables
    time = variables['time']
    atime = datetime.strptime(dtg,"%Y%m%d%H")

    #if this can't convert to times, the times might be simply ints,.. 0,6,12,18...
    try:
        #times = num2date(time[:], time.units, time.calendar)
   
        attrs = time.ncattrs()
        if 'units' not in attrs:
            units = 'seconds since 1970-1-1'
        else:
           units = time.units
 
        times = num2date(time[:], units)

    except:

        units = "hours"
        attrs = time.ncattrs()

        if 'units' in attrs:
            if "seconds" in time.units:
                  units = "seconds"

        if units == "seconds":
            times = list(map(lambda t : (atime + timedelta(seconds=int(t))), time[:]))

        else:
            times = list(map(lambda t : (atime + timedelta(hours=int(t))), time[:]))


    modelName = model['name']
    result = []
    atime = times[0] 
    vtime = None;

    for i in range(0, time.size):
         vtime = times[i] 
         diff = abs(vtime - atime)
         days =  diff.days 
         hours = (diff.seconds) / 3600
         tau = days * 24 + hours

         res = {'time' : vtime.isoformat(),
                'file' : file,
                'timestr' : datetime.strftime(vtime, "%Y%m%d%H"),
                'url'  : 'http://docker.nrlmry.navy.mil:5000/icap/plotNetcdf?model=%s&dtg=%s&hour=%s' % (modelName, model['dtg'], tau)}

         result.append(res)

    return result

def getVars(ncfile, field="", var=""):
    nvars = ncfile.variables
    dims  = ncfile.dimensions
    return (nvars, dims)
    
    
def getImagePath(filepath, model, dtg, var):
    res = []
    try:
        ncfile  = Dataset(filepath, "r")
        if 'time' in ncfile.dimensions:
            res = processTimeDim(ncfile, model, dtg, filepath) 
    
        else: 

            timestr = re.search(model['time_regex'],filepath).group(1)
            dtime   = datetime.strptime(timestr, model['time_format'])
            timestr = datetime.strftime(dtime, "%Y%m%d%H")
            print("getImgPath",filepath, timestr)

            res = [{'time' : dtime.isoformat(),
                   'timestr' : timestr,
                   'var' : var,
                   'file' : filepath,
                   'url'  : 'http://docker.nrlmry.navy.mil:5000/icap/plotNetcdf?model=%s&var=%s&dtg=%s' %                   (model['name'],var, model['dtg'] )}]
        
        ncfile.close()
    
    except Exception as e:
        logging.exception("ncfile not found for %s %s" % (model['name'], model['dtg']))
        print("ncfile not found for %s %s" % (model['name'], model['dtg']))
        pass

    return res


#This is making assumptions that the model netcdf file has the same times for every species
def getImagePaths(model, var=""):
    result = []
    ncfile = None;

    if 'name' in model:
        modelName = model['name']
        filepath  = model['path']
        dtg = model['dtg']

        #identify files with time dim or time as part of filename 
        if('isdaily' in model and  model['isdaily'] == True):
            dir_out = filepath.replace('dtg', dtg[:6])
            dir_out += dtg[6:8] + "/"
            print(dir_out)

        else:
            dir_out = filepath.replace('dtg', dtg[:6])

        filename = getProductFile(dir_out, dtg)
        filep = dir_out + filename 
        result = getImagePath(filep, model, dtg, var)

        if len(result) == 0:
          daysBack = 0;
          prevday = datetime.strptime(model['dtg'],"%Y%m%d%H")
          while daysBack < 100: 
              prevday = prevday - timedelta(days=1)
              prevdaystr = datetime.strftime(prevday, "%Y%m%d%H")
              dir_out = model['path'].replace('dtg', prevdaystr[:6])
              filename = getProductFile(dir_out, prevdaystr)
              daysBack += 1

              if filename != "":
                filepath  = dir_out + filename 
                res = getImagePath(filepath, model, prevdaystr, var)
                if res is not None and len(res) > 0:
                    result += [{"latest" : res[0]['time']}]
                break;
       
    return result

#duplicated in QueryUtils
def getProductFile(dir_out, dtg):
    ncfile = "" 
    try:
       for file in os.listdir(dir_out):
           if dtg[:8] in file:
              if file.endswith(".nc") and dtg[:8] in file:
                  ncfile = file
                  break;
    except Exception as e:
        #print("File Not Found %s %s" % (dir_out, dtg[:8])) 
        pass

    return ncfile;
            
    
def getLatLonIdx(lats, lons, extent):

    ext = extent.copy()
    llonidx  =    np.argmin(np.abs(lons - ext[0])) 
    ulonidx  =    np.argmin(np.abs(lons - ext[1])) 
    llatidx  =    np.argmin(np.abs(lats - ext[2])) 
    ulatidx  =    np.argmin(np.abs(lats - ext[3]))

    if(llatidx > ulatidx): 
      t = llatidx
      llatidx  =  ulatidx
      ulatidx = t

    if(llonidx > ulonidx): 
      t = llonidx 
      llondix  =  ulonidx
      ulonidx = t

    print("Lat lon indicies (llon, ulon, llat, ulat): %s %s %s %s" % (llonidx, ulonidx, llatidx, ulatidx))
    return {'llonidx' : llonidx, 
            'ulonidx' : ulonidx, 
            'llatidx' : llatidx, 
            'ulatidx' : ulatidx
           }
 
def getLatLons(m, imagePaths):
    filePath = m['ncfile']
    ncfile  = Dataset(filePath, "r")
    variables = ncfile.variables
    lats  = variables["lat"][:] if 'lat' in variables else variables["latitude"][:]
    lons  = variables["lon"][:] if 'lon' in variables else variables["longitude"][:]
    roll = None
    
    #If we're not going to -180, then this is a 0-360 grid
    if np.min(lons) == 0:
        roll = 360 
        lons = lons[:]-179.5

    ncfile.close()
    return {'lats': lats, 'lons': lons, 'roll' : roll }


def makePlotDir(region, dtg):
    #ngac doesn't have taus, and has full timestamps to time dim
    plot_out_dir =  plot_dir + "/" + region  + "/" + dtg

    if not os.path.isdir(plot_dir):
            os.mkdir(plot_dir)

    if not os.path.isdir(plot_dir + "/" + region):
            os.mkdir(plot_dir + "/" + region)

    if not os.path.isdir(plot_out_dir):
            os.mkdir(plot_out_dir)

    return plot_out_dir

def getvtime(atime,  tau):
    delta =  timedelta(hours=int(tau)) 
    vtime = atime + delta
    return vtime



def getVals(model, props):
    vals = None;
    nvar = props['nvar'];
    variables = props['vars']
    extent = props['extent']

    if nvar in  variables:
        dims = list(variables[nvar].dimensions)

        #don't want lat/lon. this is fragile. not sure dims are always ordered with lat/lon at end
        dims = dims[:-2]
#        latrange = slice(llatidx, ulatidx)
#        lonrange = slice(llonidx, ulonidx)

       # if "lat" in dims: dims[dims.index("lat")] = latrange
       # if "latitude" in dims: dims[dims.index("latitude")] = latrange
       # if "lon" in dims: dims[dims.index("lon")] = lonrange 
       # if "longitude" in dims: dims[dims.index("longitude")] = lonrange 
        if "hybrid" in dims: dims[dims.index("hybrid")] = 0

        if 'options' in model:
           for opt in model['options'].keys():
              val = model['options'][opt]

              #temp for now until setup in db
              if opt.lower() == 'level':
                if  'isobaric' in dims: opt = 'isobaric'
                if  'level'    in dims: opt = 'level'

              if opt in dims: 
                  vallist = variables[opt][:].tolist()
                  dims[dims.index(opt)] = vallist.index(float(val))
                

        #some products are daily, and don't have a time dim
        if 'time' in dims:
            times = list(props['times'])
            tau   = props['tau']

            tidx = times.index(tau)
            if "time" in dims: dims[dims.index("time")] = tidx
            #vals = variables[nvar][tidx, llatidx:ulatidx, llonidx:ulonidx]


        vals = variables[nvar]
        dims = list(map(lambda d : d if type(d) is not str else 0 , dims))
        if len(dims) > 0:
          vals = vals[dims[0]]

        if len(dims) == 2:
            vals = vals[dims[1]]

        if props['roll'] is not None:
            print("rolling vals due to adjusting from 360 to 180")
            vals = np.roll(vals, props['roll'])
            

        #default to first index of nothing selected
        #if 'units' in model:
            #if model['units'].lower() == 'k':
               #vals = vals[:]   273.15;
        llat = props['llatidx'] 
        ulat = props['ulatidx'] 
        llon = props['llonidx'] 
        ulon = props['ulonidx'] 
        lons = props['lons']

        #shift if grid is not -180 to 180 by roll amount. 360 is typical 
        if extent[0] < 180 and extent[1] > 180:
           print("rolling vals for dateline", int(len(lons)/2))
           vals = np.roll(vals,int(props['lonsCount']/2),1)

        vals = vals[llat:ulat, llon:ulon]
        
    return vals

def genLevelCmap(domains, palette):
    levs = domains.split(",")
    palette = palette.split(",")

    levs = list(map(lambda s: float(s),levs))
    levs = list(OrderedDict.fromkeys(list(levs)))
    cmap = colors.ListedColormap(palette)

    if len(levs) == 2:
        diff = abs(levs[-1] - levs[0]) 
        levs = np.arange(levs[0], levs[-1], diff * .10)
        cmap = colors.LinearSegmentedColormap.from_list('cmap', palette, N=100)

    print(levs)
    return levs, cmap

def plotWorker(plotout, fig, dtg, layers, extent,times, tau, atime, vtime=""):
    axes = []
    fileName = "Idon'texists"
    centralLon = False
    proj = ccrs.PlateCarree()
    alpha = 1;
    vtimestr = datetime.strftime(vtime, "%Y%m%d%H")
    #used to shift variabled x amount in case grid is not -180 to 180
    roll = None
    vals = []

    ax = plt.subplot2grid((100,1),(0,0), rowspan=70, projection=proj)
    for l in layers:
       
        if 'isVisible' not in  l['options'] or l['options']['isVisible'] != False:
            try:
                layerModel = QueryUtils.getModelInstance(l['model'], dtg, varname=l['field']['varname'], level=l['options']["level_id"])
                layerModel['options'] = l['options']

                #add dataset to dict, so we can close later
                npath             = layerModel['ncfile']
                
                ncfileDict[npath] = Dataset(npath, "r")
                nvar = l['field']['varname']

                imagePaths =getImagePaths(layerModel, nvar)

                ll  = getLatLons(layerModel, imagePaths)
                lats = ll['lats'][:]
                lons = ll['lons'][:]
                lonsCount = len(lons)
                roll = ll['roll']

                extent, proj, centralLon, lons = adjustForDateline(extent, proj, lons)
                ax.projection=proj

                llIdxs = getLatLonIdx(lats, lons, extent)
                ulatidx = llIdxs['ulatidx'] + 10 
                llatidx = llIdxs['llatidx'] 
                ulonidx = llIdxs['ulonidx'] + 10 
                llonidx = llIdxs['llonidx']
                llonidx = llonidx - 10 if llonidx >= 10 else 0
                llatidx = llatidx - 10 if llatidx >= 10 else 0
                lons    = lons[llonidx:ulonidx]
                lats    = lats[llatidx:ulatidx]


                levs, cmap = genLevelCmap(layerModel['domains'], layerModel['palette'])
                norm   = colors.BoundaryNorm(levs, cmap.N) #BoundaryNorm(levs, cmap.N)
                 
                if 'color' in layerModel['options']: 
                    if 'type' in layerModel['options']['color']:
                      ntype = layerModel['options']['color']['type']
                      if ntype.lower() == "log": 
                          norm = colors.SymLogNorm(vmin=levs[0], vmax=levs[-1], linthresh=0.1)

                #option for a filled contour
                cfill = 'filled' 
                if 'Contour Type' in layerModel['options']: 
                 cfill = layerModel['options']['Contour Type']

                lprops = {
                  'alpha'   : 1,
                  'levs'    :levs ,
                  'roll'    : roll,
                  'cfill'   : cfill,
                  'extent'  : extent,
                  'proj'    : proj,  
                  'centralLon' : centralLon,
                  'cmap'    : cmap,
                  'norm'    : norm,
                  'nvar'    : nvar,
                  'tau'      : tau,
                  'times'   : times,
                  'vars' :  ncfileDict[npath].variables,
                  'lons' : lons,
                  'lonsCount' : lonsCount,
                  'lats' : lats,
                  'llonidx' : llonidx, 
                  'llatidx' : llatidx,
                  'ulatidx' : ulatidx,
                  'ulonidx' : ulonidx
                } 

                if 'alpha' in l['options']:
                   lprops['alpha'] = l['options']['alpha'] / 100

                if lprops['nvar']  == 'wnd_spd':
                    #wnd_spd is a derived field 
                    lprops['nvar'] = 'wnd_spd'
                    plotVector(l, fig, ax, lprops) 

                else:
                    vals = getVals(layerModel, lprops)
                    plotContour(fig, ax, vals, lprops, axes)

            except Exception as e:
                print(traceback.format_exc())
                #ax("No data fell within given domains. Check the Colorbar", (0,-40), xycoords='axes points', color="red")
                pass;

        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
        ax.add_feature(cfeature.BORDERS)
        
        if len(axes) == 1:
            gl = None;
            cs = ccrs.PlateCarree()

            if type(proj).__name__ != 'PlateCarree':
                gl = ax.gridlines(crs=cs, linestyle='--', color="black")

            else:
                if (centralLon == True): 
                    locs = np.arange(extent[0], extent[1] , 20)
                    locs = np.append(locs, 179)
                    #ax.gridlines(crs=cs, color="black", xlocs=locs,
                    #     linewidth=0.5, linestyle='--', draw_labels=False)

                    locslabel = locs.copy()
                    locslabel[locs > 180] -= 360 

                    gl = ax.gridlines(color="black", linestyle="--", crs=cs, draw_labels=True)
                    gl.xlocator = mticker.FixedLocator(locslabel)
                else: 
                    gl = ax.gridlines(crs=cs, color="black", draw_labels=True, linestyle='--')

            gl.xlabels_top=False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
     
    f_title = ""#plt_dict[m.field]['title']
    #head = getHead(atime, vtime, tau, modelName, m['varname'], f_title)
    head = getHead(atime, vtime, tau, "", "", f_title)
    ax.set_title(head, loc='left')

    #cs2 = ax.imshow(vals, extent=extent)
    #plt.rc('axes', titlesize=10)     # fontsize of the axes title

    #DATA plots
    #add Colorbars
    addColorbars(fig, axes)
    print("finished plot: %s %s %s" % (f_title, atime, tau))
    fig.savefig(plotout, dpi=dpi, bbox_inches="tight", transparent=False)

    for nk in ncfileDict.keys():
        try:
           ncfileDict[nk].close()
        except Exception as e:
           pass

    axes = []

def addColorbars(fig, axes):
    
   idx = 0.2 - (0.05 * len(axes))
   idx = 1
   for (nvar, cs) in axes:
      print(idx)
      cbaxes = plt.subplot2grid((100,1),(77 + idx,0), rowspan=2) # (add_axes([0.2, idx, 0.7, 0.02]) 
      cb = fig.colorbar(cs, cax=cbaxes, orientation="horizontal")
      cb.ax.minorticks_on()
      cb.ax.set_title(nvar, x=.5 )
      idx += 10#0.09

   axes = []

def plotHist(fig,ax,vals, props):
    #vals = vals[~np.isnan(vals)]
    data_ax = plt.subplot2grid((6,1),(5,0))
    title = "Min: %s Max: %s" % (vals.min(), vals.max())
    data_ax.set_title(title)
 
    y,x = np.histogram(vals, bins=20)
    data_ax.bar(x[:-1],y)
    plt.ylabel('Grid Points')
    plt.xlabel(props['nvar'])

def plotContour(fig, ax, vals, props, axes):
        lons = props['lons']
        lats = props['lats']
        levs = props['levs']
        proj = props['proj']
        norm = props['norm']
        cmap = props['cmap']
        cfill = props['cfill']
        alpha = props['alpha']
        
        vals[vals == 0] = 'nan'
        alpha = 1 if alpha is None else alpha;
        cs = None;
       

        #cmap.set_over(color='white')
        vals = np.nan_to_num(vals)

        print(vals)
        if vals.size < 300000 :
            if cfill.lower() == 'filled' or cfill is None:
                cs = ax.contourf(lons, lats, vals, alpha=alpha, levels=levs, norm=norm, transform=ccrs.PlateCarree(), cmap=cmap, extend='max')
            else:
                cs = ax.contour(lons, lats, vals, alpha=alpha, levels=levs, norm=norm, transform=ccrs.PlateCarree(), cmap=cmap)
                ax.clabel(cs)
              
        else:
            cs = ax.pcolormesh(lons, lats, vals, alpha=alpha, norm=norm, transform=ccrs.PlateCarree(), cmap=cmap)
            #cs2 = ax.contourf(lons, lats, vals, levels=levs, norm=norm, cmap=cmap, transform=ccrs.PlateCarree())

        axes.append((props['nvar'], cs))

def plotVector(m, fig, ax,props):
    plons = props['lons']
    plats = props['lats']
    norm = props['norm']
    cmap = props['cmap']
    proj = props['proj']
    variables = props['vars']
    plotType = 'Streamlines'

    if props['nvar'] == 'wnd_spd':
         xlim = np.max(plons) - np.min(plons)
         ylim = np.max(plats) - np.min(plats)
         a =xlim * ylim
         d = a / (180 * 90) 
         print("Density: %s " % d)
        
         if 'plotType' in m['options']:
            plotType = m['options']['plotType']

         print("PLOT TYPE %s" % plotType)

         if 'wnd_ucmp_isobaric' in variables:
             print("ploting wind ")

             props['nvar'] = 'wnd_ucmp_isobaric'
             puvals  = getVals(m, props)

             props['nvar'] = 'wnd_vcmp_isobaric'
             pvvals  =  getVals(m, props)

             start_time = time.time()

             lonslice = slice(0,-1,int(1 + (d * 20)))
             latslice = slice(0,-1,int(1 + (d * 20)))
             lons = plons[lonslice]
             lats = plats[latslice] 
             uvals = puvals[latslice, lonslice] 
             vvals = pvvals[latslice, lonslice] 
             C = np.sqrt(uvals**2 + vvals**2)

             if plotType == 'Barbs':

                 ax.barbs( lons, lats, uvals, vvals, C, cmap=cmap,norm=norm, transform=proj)

             elif plotType == 'Quiver':

                 ax.quiver( lons, lats, uvals, vvals, C, edgecolors='black', linewidth=.5,  norm=norm, cmap=cmap, transform=proj)

             else:
                 d = 1 +  (abs(math.log(1/d))) 
                 print("new d", d)
                 lonslice = slice(0,-1,int(d ))
                 latslice = slice(0,-1,int(d ))
                 lons = plons[lonslice]
                 lats = plats[latslice] 
                 uvals = puvals[latslice, lonslice] 
                 vvals = pvvals[latslice, lonslice] 

                 ax.streamplot( lons, lats, uvals, vvals, linewidth=1, density=d ,norm=norm, cmap=cmap, transform=proj)

             #histvals = np.square(np.add(np.power(uvals, 2), np.power(vvals, 2)))

             print("plotted %s" % str(time.time() - start_time))
             props['nvar'] = 'wnd_spd'
             #plotHist(fig, ax, histvals, props)


def plot(plotout, layers, dtg, atime, tau, times, extent):
    tidx = None;
    cm = getMidpoint(extent[0],extent[1],extent[2], extent[3] )
    vtime    = getvtime(atime, tau)

    fig = plt.figure(figsize=(12, 9))
    plotWorker(plotout, fig, dtg,  layers, extent,times, tau,atime, vtime)
    plt.close()
    

def netcdfPlotC(props): 
   #check to see if we're no longer needed

   netcdfPlot(*props)

def netcdfPlot(layers, dtg, extent, hour, withMap, width, height, region, mapName=None):

    extent = extent.split(",")
    extent = list(map(lambda e : round(float(e), 2), extent))
    strExtent = list(map(lambda e : str(round(float(e))), extent))
    plotExt = ",".join(strExtent)
    oe = [extent[0], extent[2], extent[3] , extent[1]]

    plot_out_dir = makePlotDir(plotExt, dtg)
    atime   = datetime.strptime(dtg,"%Y%m%d%H")
    #varlist = layers['varname']
    mapName = mapName if mapName is not None else "" 
    layerNames = "".join(list(map(lambda l: l['model'] + l['field']['varname'] , layers)))

    #create hash to detect changes in optoins
    optionsStr = getOptsStr(layers)
    times = np.arange(0,120,6)

    requestedTime = getvtime(atime, hour)
    filename = "%s_%s_%s_%s.jpg" % \
      (datetime.strftime(atime,"%Y%m%d%H" ), datetime.strftime(requestedTime, "%Y%m%d%H"), layerNames, optionsStr)

    plotout = plot_out_dir + "/" + filename

    #used to find previous plots if options chnage
    oldPlotsPattern = "%s_%s_%s_.*" % \
      (datetime.strftime(atime,"%Y%m%d%H" ), datetime.strftime(requestedTime, "%Y%m%d%H"), layerNames)
      #(plot_out_dir, datetime.strftime(atime,"%Y%m%d%H" ), datetime.strftime(requestedTime, "%Y%m%d%H"), ("-").join(varlist))

    try:
        #remove old plots
        for f in os.listdir(plot_out_dir):
          if re.search(oldPlotsPattern, f):
              fsplit = f.split("_")
              if fsplit[len(fsplit) - 1] != str(optionsStr) + ".jpg":
                  print("REMOVING Plot: %s " % f)
                  os.remove(os.path.join(plot_out_dir, f))

        if(os.path.exists(plotout)):
            plot(plotout, layers, dtg, atime, hour, times, oe)
            #return plotout

        else:
            print("NEW PLOT ", plotout)
            plot(plotout, layers, dtg, atime, hour, times, oe)
                
    except Exception as e:
        print(traceback.format_exc())
        logging.exception("Failed to plot")
        plt.close()


    return plotout

def getLatest(model):
    parentDir = model.dir_out[:model.dir_out.index(model.model) + len(model.model)]
    res = []

    for path in os.listdir(parentDir):
       for dtgpath in os.listdir(os.path.join(parentDir, path)):
           dtg = re.search(model['timeRegex'],dtgpath)
           res.append(dtg[1])


def  adjustForDateline(extent, proj, lons):
    #adjust extent to always be within range when crossing date line
    centralLon = False
    if extent[0] < -180:
        while (extent[0] < 0):
            extent[0] += 360
            extent[1] += 360

    #adjust extent to never go out of lat bounds
    if extent[3] > 90:
        proj = ccrs.NorthPolarStereo(central_longitude=0)
        extent[3] = 90
        extent[0] = -180
        extent[1] = 180

    if extent[2] < -90:
        proj = ccrs.SouthPolarStereo(central_longitude=0)
        extent[0] = -180
        extent[1] = 180
        extent[2] = -90

    if extent[0] < 180 and extent[1] > 180:
        centralLon = True
        proj = ccrs.PlateCarree(central_longitude=180)
        lons[lons < 0] = lons[lons< 0]+360
        lons = np.roll(lons, int(len(lons) /2))

    return (extent, proj, centralLon, lons)

def savePlot(props):
   print("save plot")
