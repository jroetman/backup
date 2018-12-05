from ModelBase import ModelBase
from imports import *

class Model(ModelBase):

    def __init__(self, model, dtg):
        ndtg = datetime.strptime(dtg, "%Y%m%d%H") - timedelta(days=1)
        ndtg = datetime.strftime(ndtg, "%Y%m%d%H")

        super().__init__(model, ndtg)

        self.field = "aod"
        self.file_out = 'aod_550_nmmb.nc'

    
    def download(self):
        #url = 'siroco.upc.edu'
        url = 'bscesftp.bsc.es'
        l = ''
        p = ''
    
        #_Setup output file
        ### file_out = dir_out + '/' + dtg + '_aod_550_nmmb.nc'
        file = self.dtg + '-BSC_MONARCH-ICAP.nc'
        utils.ftp(url, file, username=l, password=p)
        shutil.move( file, self.file_out )
    
