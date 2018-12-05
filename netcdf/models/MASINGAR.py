from . ModelBase import ModelBase
from . imports import *

class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__(model, dtg)

        self.field = "aod"
        self.file_out = 'aod_masingar.nc'

    def download(self):
        dtg = self.dtg
        dtg = lt.newdtg( dtg, -24 )
    
        #_Setup output file
        file_in = '/ftp/receive/aerosol/icap_jma/' + dtg + '_aod_masingar.nc' 
        #_Skip if file already downloaded
        if not os.path.exists( file_in ):
            utils.dbg( 'file not available yet '+ file, l=2 )
            sys.exit(1)
            
        #_if file present and proper size, begin copy
        shutil.move( file_in, self.file_out )
        os.chmod(self.file_out, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)

    def plot(self):
        plotUtils.netcdfPlot(self.model, self.dtg, self.field, self.file_out)
