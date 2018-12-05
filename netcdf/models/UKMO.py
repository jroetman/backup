from ModelBase import ModelBase
from imports import *
import tarfile

class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__(model, dtg)

        self.field = "aod"
        self.file_out = 'aod_ukmo.nc'

    def download(self):
        dtg = self.dtg
        url = 'ftp.metoffice.gov.uk'
        l = ''
        p = ''

        # Setup output file
        dir = '/outgoing/ICAP'
        filer = dtg[:8] + '_0000_glm_00_NRL1_data'   #raw file
        file = dtg[:8] + '_0000_glm_00_NRL1_data.tar.gz'
        filetar =  filer + '.tar'
      
        try:
           # if os.path.exists(filer):
           #     os.rmdir( filer )

           # if os.path.exists(file):
           #     os.unlinke( file )

           # #20180807_0000_glm_00_NRL1_data.tar.gz
           # utils.ftp(url, file, l, p, dir)

           # if os.path.exists(file):
           #     tf = tarfile.open(file)
           #     tf.extractall()
           #     tf.close()
           #     os.unlink( file )

           # if os.path.exists(filer+'/'+'1.nc'):
           #     shutil.move(filer + '/' + '1.nc', self.file_out )
           #     os.rmdir (filer)

            ncdf = Dataset( self.file_out, 'r+')
            ncdf.createDimension("lat", len(ncdf.dimensions["latitude"]))
            ncdf.createDimension("lon", len(ncdf.dimensions["longitude"]))

            var = ncdf.variables["latitude"]
            t = ncdf.createVariable("lat", var.datatype, ("lat"))
            t.setncatts({k: var.getncattr(k) for k in var.ncattrs()})
            t[:] = var[:]

            var = ncdf.variables["longitude"]
            t = ncdf.createVariable("lon", var.datatype, ("lon"))
            t.setncatts({k: var.getncattr(k) for k in var.ncattrs()})
            t[:] = var[:]
          
            #cant delete old latitude and longitude. Could create a new file, but these are small variables.
            ncdf.close()

        except:
            logging.exception('failed to download %s' % file)

