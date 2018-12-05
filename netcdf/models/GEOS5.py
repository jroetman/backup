from ModelBase import ModelBase
from imports import *


class Model(ModelBase):
    def __init__(self, model, dtg):
        super().__init__(model, dtg)

        self.field = "aod"
        self.file_out = 'aod_geos5.nc'

    def download(self):
        dtg = lt.newdtg( self.dtg, -24 )
   
        #_Setup download URL
        url = 'https://opendap.nccs.nasa.gov/dods/GEOS-5/'\
        	+ 'fp/0.25_deg/fcast/inst1_2d_hwl_Nx'
        dap_file = 'inst1_2d_hwl_Nx.' + dtg[:8] + '_'+dtg[8:] 
        		# +'z', removed from url June 6th

        speciesDict = self.mod_dict['GEOS5']['specn']
        #_Get GSFC name for species and create ncdf variable

        out = Dataset( self.file_out, 'w', format='NETCDF3_CLASSIC' )
        nt, ny, nx = (0,0,0)
        ncdf = Dataset( url + '/' + dap_file )

        for idx, k in enumerate(speciesDict.keys()):
            spec = speciesDict[k]

            logging.info(url + '/' + dap_file + "?" + spec)

            if idx == 0:
                nt, ny, nx = ncdf[spec].shape
                out.createDimension( 'lon', nx )
                out.createDimension( 'lat', ny )
                out.createDimension( 'time', nt )

            v = out.createVariable( k, 'f4', ('time','lat','lon') )
            print(ncdf[spec])
            for t in range(0, len(ncdf.variables['time'][:])):
                v[t]= ncdf[spec][t]

        out.close()
        #print(ncdf)

  #      time = float(ncdf.variables['time'][0])
  #      atime = datetime.fromtimestamp(time)
  #      dtg_geos = datetime.strptime(time,"%Y%m%d%H")
  #      print(dtg_geos)
  #      file = atime + '_aod_geos5.nc' 
        
        #_If final file exist, skip

        #_Attempt to join individual variable files  
        #utils.geos5_join( self.dtg, species, self.file_out)
               	
