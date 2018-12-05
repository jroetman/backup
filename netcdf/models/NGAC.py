from . ModelBase import ModelBase
from . imports import *

class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__("NGAC", dtg)
        self.field = "aod"
        self.file_out = 'aod_550_ngac.nc'

    def download(self, auto=False ):
        dtg = self.dtg
        lt.mkdir_p(self.dir_out)
        
        #    'ngac/prod/ngac.' + dtg[:8] 
        url = 'ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/ngac/prod/ngac.'+dtg[:8]
        #_Setup tmporary local files and output file
        file_grb2 = 'ngac.t' + dtg[-2:] + 'z.aod_550nm.grib2'
        fs = 12e6
    
        #_Download intermediate file
        url = url + '/' +  file_grb2
    
        #_If final file present, get out of loop
        try: 
             utils.ftpurl( url, self.dir_out + "/" + file_grb2 )
    
        except Exception  as e: 
            print(e)
            utils.dbg(( 'failed to download', file_grb2 ))
            sys.exit(1)
    
        #_Temporary file to pass to conversion module
        file_tmp = self.dir_out + '/ngac.'+dtg+'.aod_550nm'
        shutil.move(self.dir_out + "/" +  file_grb2, file_tmp )
    
        #_Convert to ncdf
        match = ' -match ":aerosol=Dust Dry:" -set_ext_name l -netcdf '
        file_conv = utils.convert_grib2ncdf( file_tmp,  match)
        shutil.move( file_conv, self.file_out )

        os.chmod(self.file_out, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)
        os.chmod(file_tmp, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)

    
    def plot(self):
        plotUtils.netcdfPlot(self.model, self.dtg, self.field, self.file_out)
    
