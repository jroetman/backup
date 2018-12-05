#!/software/depot/anaconda-3-5.1.0/bin/python
import sys, os, time, stat, shutil, re
import logging
from datetime import datetime 
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')    
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from netCDF4 import Dataset, num2date
import numpy as np
#import ICAPDownloadUtils as utils
from time import gmtime, strftime, strptime

#logging
dir_out = '/logs'

if not os.path.exists(dir_out):
     os.mkdir(dir_out)
logging.basicConfig(filename=dir_out + '/ICAPlog',level=logging.DEBUG)


__all__ = [ 'datetime', 'sys', 'os', 'time',  \
            'gmtime', 'strftime', \
            'strptime', 'datetime', 'timedelta', 'Dataset', \
            'plt', 'shutil', 'stat', 'ccrs','cfeature', 'LONGITUDE_FORMATTER', \
            'LATITUDE_FORMATTER', 'np',  're', 'logging']
