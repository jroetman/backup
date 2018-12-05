from . ModelBase import ModelBase
from . imports import *

class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__(model, dtg)

        print(model)
        self.field = "aod"
        self.urlbase = 'http://silam.fmi.fi/thredds/ncss/silam_glob_v5_5_1/runs/silam_glob_v5_5_1_RUN_'
        #self.urlvariable='?var=ocd_dust_w550&timeStride=6&accept=netcdf&time_start='
        self.urlvariable='?var=ocd_dust_w550,ocd_frp_w550,ocd_sslt_w550,ocd_part_w550,ocd_abf_w550&timeStride=6&accept=netcdf&time_start='
        self.file_out = "silam_aod.nc"

    def download(self):
        dtg = self.dtg
    
        dtg1 =  lt.newdtg(dtg, 0)   #first available forecast is at 06Z                
        startstr = strftime( "%Y-%m-%dT00:%M:%SZ", gmtime(lt.dtg2epoch(dtg)) )
        startstr1 = strftime("%Y-%m-%dT01", gmtime(lt.dtg2epoch(dtg1)) )+":00:00Z"
        dtgend = lt.newdtg(dtg, 114)
        endstr = strftime("%Y-%m-%dT01", gmtime(lt.dtg2epoch(dtgend)) )+":00:00Z"
        url = self.urlbase + startstr + self.urlvariable + startstr1 + "&time_end="+endstr + self.requestmark
     
        print(self.file_out)
        utils.http_silam(url, self.file_out)
    
        #_Write Successful download results in form of status file
        utils.statusfile(self.model, dtg, True )
        #update hours
        rootgrp = Dataset(self.file_out, "r+")
        times = len(rootgrp.variables['time'])
        newtimes = range(0, times * 6, 6 ) #6 is the stride
        rootgrp.variables['time'][:] = newtimes
        rootgrp.close()
    
       
               
        
    
    
    
