from ModelBase import ModelBase
from imports import *

class Model(ModelBase):

    def __init__(self, model, dtg):
        #subtract a day
        super().__init__(model, dtg)
        self.field = "aod"
        self.file_out = 'aod_550_nmmb.nc'

    def download(self):
        #url = 'siroco.upc.edu'
        url = 'bscesftp.bsc.es'
        l = ''
        p = ''

        file = self.dtg + '-NMMB_BSC_CTM-ICAP.nc'
        utils.ftp(url, file, username=l, password=p)
        shutil.move( file, self.file_out )

