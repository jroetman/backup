from . ModelBase import ModelBase
from . imports import *

class Model(ModelBase):

    def __init__(self, model, dtg):
        super().__init__(model, dtg)
        self.field = "aod"
        self.file_out = 'aod_cams.nc'

    def download(self):
        dtg = self.dtg
    	
        url = 'dissemination.ecmwf.int'
        dir = '/DATA/CAMS_NREALTIME_ICAP/'
        l   = ''
        p   = ''
     
        species = self.mod_dict['CAMS']['specn']
        fs = 4e6 #_estimated file minimum size
     
        ncdf_out = Dataset(self.file_out, 'w')

        #_Loop over and download individual species files
        for spec in species.keys():
            file = dtg + '_' + spec + '_550_cams.nc'
            dir_dtg  = dir + dtg +'/netcdf/'
            file_url = dir + '/' +dtg + '/netcdf/' + file

            if(spec == 'sulfate_aod'): file = dtg + '_sulphate__550_cams.nc'
         
            try:
                utils.ftp( url, file, dir=dir_dtg, username=l, password=p )
                ncdf_in= Dataset( file, 'r')

                for dname, the_dim in ncdf_in.dimensions.items():
                    if(dname == "latitude"):  dname = "lat"
                    if(dname == "longitude"): dname = "lon"

                    if(dname not in ncdf_out.dimensions.keys()):
                       #_Download file
                        ncdf_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)
                  
                for v_name, varin in ncdf_in.variables.items():
                    if(v_name== "latitude"): v_name = "lat"
                    if(v_name == "longitude"): v_name = "lon"

                  
                    if(v_name not in ncdf_out.variables.keys()): 
                        try:
                            if(v_name in ("lon", "lat", "time")):
                                outVar = ncdf_out.createVariable(v_name, varin.datatype, (v_name))

                            else: 
                                outVar = ncdf_out.createVariable(v_name, varin.datatype, ("time", "lat","lon"))

                            # Copy variable attributes
                            outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
                            outVar[:] = varin[:]
                        except:
                            logging.exception("Failed saving %s" % v_name)

                ncdf_in.close()
                os.unlink(file)
     
            except:
                logging.exception("Failed creating CAMS nc file")
         
        ncdf_out.close()
        os.chmod(self.file_out, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)
