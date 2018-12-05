from . ModelBase import ModelBase
from . imports import *

class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__(model, dtg)
        self.field = "aod"
        self.file_out = 'aod_MOCAGE.nc'

    def download(self):
        dtg = self.dtg
        lt.mkdir_p(self.dir_out)

        fs = 44000000    
    
        #_Setup output file
        yyyymmdd = dtg[:8]
        file = 'regrid1dg_Mocage_4D_'+yyyymmdd+'_AOD.nc'
        file_in = '/ftp/receive/aerosol/mocage/' + file
    
        #_copy from push
        if not os.path.exists( file_in ):
           logging.error( 'file not available yet '+ file, l=2 )
           #sys.exit(1)
    
        elif utils.file_size( file_in ) > fs:
           shutil.move( file_in, self.file_out )
           os.chmod( filePath, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)
         
