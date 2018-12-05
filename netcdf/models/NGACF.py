#!/usr/bin/env python
from . import SILAM_AOD
from . imports import *

class Model(NGAC.Model):
    def __init__(self, model, dtg):
        super().__init__("NGACF", dtg) 
        self._dir_out  = self.dir_prod + '/' + 'NGACF' + '/' + self.dtg[:6]
        #call the setter to pudate the path to the new model name
        self.file_out = 'aod_550_ngac.nc.ngacf'

    def download(self):
       #super().download()
       #this was already downloaded from NGAC
       file_tmp = self.dir_prod + '/NGAC/' + self.dtg[:6] + '/' + 'ngac.'+ self.dtg+'.aod_550nm'

       try:
           shutil.move(file_tmp, self.dir_out + '/ngac.'+ self.dtg+'.aod_550nm') 
           os.chmod(file_tmp, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)

       except: 
           print("File doesn't exist, or already moved")

       file_tmp = self.dir_out + '/ngac.'+ self.dtg+'.aod_550nm' 

       file_conv_ngacf = utils.convert_grib2ncdf_ngacf(file_tmp,  self.dtg )
       shutil.move(file_conv_ngacf, self.file_out )
       os.chmod(self.file_out, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)

       #print(li.read_ngacffcst(self.dtg))
       os.unlink( file_tmp )

