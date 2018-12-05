from datetime import datetime
import sys, os, time
import libs.libtools as lt
import libs.libmeta as lm
import libs.libicap as li
import ICAPDownloadUtils as utils

from time import gmtime, strftime, strptime
from datetime import datetime 
from datetime import timedelta
from netCDF4 import Dataset

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np

class ModelBase:
    def __init__(self,**kwds):
        for k,v in kwds.items():
           setattr(self, k, v)
           self.dir_prod = lm.dir_prod 
           self.mod_dict = lm.models()

    @property
    def name(self):
        return self._name_

    @name.setter
    def name(self, name):
        self._name = name 

    def download(self, dtg):
        print("Download not implemented for the %s model" % (self._name) )

    def plot(self):
        print("Download not implemented for the %s model" % (self._name) )
