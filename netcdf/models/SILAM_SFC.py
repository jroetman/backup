from . import SILAM_AOD

#This is almost identical to SILAM_AOD, so lets use that model, and modify some params
class Model(SILAM_AOD.Model):
    def __init__(self, model, dtg):
        super().__init__(model, dtg) 

        #the parent class has using just SILAM, I need this silam_sfc for now
        self.file_out    = "silam_sfc.nc"
        self.field       = "sfc"
        self.urlbase     = 'http://silam.fmi.fi/thredds/ncss/silam_glob_v5_5_1/runs/silam_glob_v5_5_1_RUN_'
        self.urlvariable ='?var=cnc_PM10,cnc_PM2_5,cnc_PM_FRP,cnc_dust,cnc_sslt&vertCoord=10&timeStride=6&accept=netcdf&time_start='
