#!/usr/bin/env python
from imports import *
import inspect
import urllib 
from ftplib import FTP
from glob import glob
import requests

dir_prod = lm.dir_prod 
debug = 1 


def backfill( dtg, download):
        ''' 
        look through past week of status files
        If any failures are found, attempt to download
        '''
        fcst_finc = 24
        ndays = 7
        dtg_loop = lt.newdtg( dtg, -ndays*24 )

        #_Build regular expression to get model name    
        regex = re.compile( 'False_\d{10}_status_([\w\d]+)' )

        #_Start one week ago, move forward
        while dtg_loop < dtg:
                prefix = dir_prod + '/status/' + dtg_loop[:6] + '/' \
                        + 'False_' + dtg_loop + '_status_'
                files = glob( prefix + '*' )

                #_If Failures  Present, build list of models to retry 
                #_Loop over status files, get model, add to list
                models = []
                for file in files:
                        #_Get model name from failure file
                        filename = file.split('/')[-1]
                        models.append( regex.search( filename ).group(1) )
                        
                        #_Delete failure files
                        os.unlink( file )

               # #_Lauch threader to retry download
               # dbg(( 'retrying', dtg_loop, str(models) ))
               # threader( dtg_loop, models=models,download=download )

                #_Increment Forward
                dtg_loop = lt.newdtg( dtg_loop, fcst_finc )

################################################################################
#_COMMON_PROTOCOLS_#############################################################
################################################################################

def http_silam(url, filePath):
    ''' downloads through http, skip the header and diagnosis because
    it returns errors when downloading SILAM data'''
    try: 
        r = requests.get(url)

        with open(filePath, 'wb') as f:  
            f.write(r.content)

        os.chmod( filePath, stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)
    except:
        logging.exception("Failed to download %s %s" % (url, sys.exc_info()))
        sys.exit(1)

def ftpurl( url, file_out):
    try: urllib.request.urlretrieve(url, file_out)
    except urllib.error.URLError as e:
        logging.exception("Failed to download from ftp %s %s" % (url, e))

def http( url ):
        ''' downloads through http '''
        dbg(( 'downloading', url ))
        file = url.split('/')[-1]
        u = requests.get(url)
        f = open(file, 'wb')
        meta = u.info()
        dbg( meta )
        f_size = int( meta.getheaders("Content-Length")[0] )
        print ("Downloading: %s Bytes: %s" % (file, f_size))

        fs_dl = 0
        blk_sz = 8192
        while True:
                buf = u.read(blk_sz)
                if not buf:
                        break

                fs_dl += len(buf)
                f.write(buf)
                status = r"%10d  [%3.2f%%]" % (fs_dl, fs_dl * 100. / f_size)
                status = status + chr(8)*( len(status)+1 )

        f.close()

def ftp( url, file, username='anonymous', password='none', dir=None ):
        ''' downloads file though ftp '''
        try: 
            #_Open handle
            ftp = FTP( url, username, password )
###         ftp_handle.login()

            #_Move to directory containing file
            if(dir != None):
                ftp.cwd( dir )
            
            #_Open local binary and stuff it in
            local_file = open( file, 'wb' )
            ftp.retrbinary( 'RETR ' + file, local_file.write, 8*1024 )

            local_file.close()
            ftp.quit()
           
        except: 
            logging.exception("Failed to download from ftp %s %s %s %s" % (url, file, dir,  sys.exc_info()))
            sys.exit(1)


def statusfile( model, dtg, status ):
        '''
        Create string for statufile
        ex:
                2011030100_MACC_False_dwnld.status

        False   : Failed to download in alloted time.
        True    : Success
        '''

        dir_log = dir_prod + '/status/' + dtg[:6]
        lt.mkdir_p( dir_log )
        log = dir_log + '/' + '_'.join(( str(status), dtg, 'status', model ))

        #_only write failures
        if not status:
                open( log, 'w' ).close()
                lt.make_readable( log )

###     #_If True, go into total log file and set it to success
###     result = 'COMPLETE' if status else 'FAILED'
###     li.cronlog( dtg, job={ model : result } )

        #_clean up old failure file if still there (which it shouldn't be)
        if status:
                fail_log = dir_log + '/' + '_'.join(( 'False', dtg, 'status',
                        model ))
                if os.path.exists( fail_log ): os.unlink( fail_log )    

################################################################################
#_MODEL_SPECIFIC_MODULES_#######################################################
################################################################################

def convert_grib2ncdf( file, match ):
        ''' 
        NGAC currently delivers files as GRIB2
        This converts them to netcdf
        '''
        expected_file_size = 10689436
      #  wgrib = '/shared/aerosol_heck2/users/sessions/bin/wgrib2'
        wgrib = '/shared/aerosol_bob1/users/xian/src/bin/grib2/wgrib2/wgrib2'

        file_tmp = file  + '.nc'

        #_Decode GRIB2 input
#       res = os.system( wgrib + ' -g2clib 0 ' + file + ' -netcdf ' + file_tmp )
        print( wgrib + ' ' + file +  match + ' ' + file_tmp)
        res = os.system( wgrib + ' ' + file +  match + ' ' + file_tmp)

        if res: 
            raise OSError('Failed to convert from grib2')

        #_Read decoded input.
        file_in = Dataset( file_tmp, 'r', format='NETCDF3_CLASSIC' )
        species = { 'AOTK_entireatmosphere' : 'dust' }

        lats = file_in.variables['latitude'][:]
        lons = file_in.variables['longitude'][:]-180
                                                #_Note this shift when read-
                                                # ing data
        nx = len(lons)
        ny = len(lats)
        nspec = len(species.keys())

        #_Get initial time from filename
        re_dtg = re.compile('(\d{10})')
        dtg_init = re_dtg.search(file).group(0)

        #_Calculate and store dts into array
        times = []
        epochs = []
        epochs[:] = file_in.variables['time'][:]
        epochs = np.array( epochs )
        [ times.append(lt.epoch2dtg(t)) for t in epochs ]
        nt = len( times )

        #_Create dimensions
        file_name = times[0] + '_aod_550_ngac.nc'
        file_out = Dataset( file_name, 'w', format='NETCDF3_CLASSIC' )
        file_out.createDimension('lon', nx)
        file_out.createDimension('lat', ny)
        file_out.createDimension('time', nt)

        #_Create global attributes
        file_out.Projection = 'LatLon'
        file_out.lat_ll = lats[0]
        file_out.lon_ll = lons[0]
        file_out.delta_lat = str(lats[1] - lats[0]) + ' degrees'
        file_out.delta_lon = str(lons[1] - lons[0]) + ' degrees'
        file_out.Nlon = str(nx) + ' grid_points'
        file_out.Nlat = str(ny) + ' grid_points'

        var = file_out.createVariable('lon','f4',('lon'))
        var[:] = lons
        var = file_out.createVariable('lat','f4',('lat'))
        var[:] = lats
        var = file_out.createVariable('time','f8',('time'))
        var[:] = epochs

        #_Define variables
        for s in species:
                specie = species[s]
                var = file_out.createVariable( specie + '_aod', 'f4', 
                        ('time' ,'lat' ,'lon') )
               # var.name = specie + '_aod'
                var.setncattr('name',specie+'_aod')
                for attr in file_in.variables[s].ncattrs():
                        value = file_in.variables[s].__getattr__( attr )
                        var.setncattr( attr, value )
                var.init_time_ut = times[0]
                nx2 =int(nx/2)
                var[:,:,:nx2] = file_in.variables[s][:,:,nx2:]
                var[:,:,nx2:] = file_in.variables[s][:,:,:nx2]
        file_out.close()
        file_in.close()
        os.unlink(file_tmp)

        #_Check to see if filesize matches expectations
        file_size = os.stat( file_name ).st_size
        if file_size != expected_file_size:
                dbg(( 'error: NGAC file not correct size, removing', file_name ))
                dbg(( 'error: 10689684 !=', file_size ))
                os.unlink( file_name )

        return file_name

def geos5( ncdf, file ):
        '''
        GEOS5 uses an OPENDAP server that is easier handled on its own

        dtg     : str*10, Expected 00.  GEOS5 is initialized at 22z
        variable: string of nrl variable name
        file    : species output file name
        '''
        #_Conversion between GSFC variables and local ones
        print(file)
        ncdf_out = Dataset( file, 'w', format='NETCDF4' )

        #Copy dimensions
        for dname, the_dim in ncdf.dimensions.items():
            ncdf_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)
        
        
        # Copy variables
        for v_name, varin in ncdf.variables.items():
            print(varin)
            outVar = ncdf_out.createVariable(v_name, varin.datatype, varin.dimensions)
            
            # Copy variable attributes
            outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
            outVar[:] = varin[:]


def geos5_join( dtg, variables, file_out ):
        ''' 
        Attempt to take individual species files and join them into
        single file in ICAP archive.  The first two hours of the forecast are 
        dropped so that the initialization time is 00z.  This is done because
        the original files also started there, as does the rest of ICAP, so
        having 22/23z data is not of particular use.

        libnrl.read_geos5fcst() calculates total_dtg and smoke_aod 
        to save on space, and legacy reasons...

        dtg     : str*10,       date-time-group
        vars    : list,         list containing all variables to merge
        '''

        #_Open new netcdf file
        ncdf = Dataset( file_out, 'w', format='NETCDF4' )
        #_wrs ncdf = Dataset( file_out, 'w', format='NETCDF3_CLASSIC' )
        var_dict = lm.aod_vars()
        dbg( file_out )

        geos_offset = 2
        dtg_icap = lt.newdtg( dtg, geos_offset )
        
        #_Get data for each variable
        for variable in variables:
                var_key = variable + '_aod'

                #_Open file with individual specie
                file_in = dtg + '_' + var_key + '_geos5.nc'
                dbg( file_in )
                ncdf_in = Dataset( file_in, 'r', format='NETCDF3_CLASSIC' )
        
                #_Create dimensions if not present, should only happen first
                # variable
                if not 'lat' in ncdf.dimensions:
                        #_Get sizes
                        ny = len( ncdf_in.dimensions['lat'] )
                        nx = len( ncdf_in.dimensions['lon'] )

                        #_Add to output file
                        ncdf.createDimension( 'lat', ny )
                        ncdf.createDimension( 'lon', nx )
                
                        #_Add dimensional variables to file
                        dim = ncdf.createVariable( 'lats', 'f4', ('lat') )
                        dim[:] = ncdf_in.variables['lats'][:]
                        dim = ncdf.createVariable( 'lons', 'f4', ('lon') )
                        dim[:] = ncdf_in.variables['lons'][:]

                        #_For time, we want to create epoch times and limit
                        # to times dtg and later
                        days = ncdf_in.variables['times'][:]
                        t_idx = lt.gsfc_day2dtg( days ).tolist().index(dtg_icap)

                        #_Create truncated dimension            
                        nt = len( days[t_idx:] )
                        #_wrs nt = len( days[t_idx:123] ) #xian,good for geos5 data after 2013121900

                        ncdf.createDimension( 'time', nt )

                        #_Add trucated times to file    
                        dim = ncdf.createVariable( 'times', 'f8', ('time') )
                        dim[:] = days[t_idx:]
                        #_wrs dim[:] = days[t_idx:123] #xian

                #_Create ncdf variable object
                v = ncdf.createVariable( variable,'f4', ('time','lat','lon') )

                #_Add attributes
                v.level = 'total column' 
                v.units = var_dict[ var_key ]['units'] 
                v.long_name = var_dict[ var_key ]['long_name'] 

                #_Add variable
                v[:] = ncdf_in.variables[ variable ][ t_idx:, :, : ]
                #_wrs v[:] = ncdf_in.variables[ variable ][ t_idx:123, :, : ]  #xian

                ncdf_in.close()

        #_Close joined netcdf file
        ncdf.close()    

        #_Return output file name 
        return file_in

def convert_grib2ncdf_ngacf( file, dtg ):
        ''' 
        NGAC full species GRIB2 file
        This converts them to netcdf for each specie, 
        as a single conversion command would not convert the whole file into one good netcdf file.  
        '''
        expected_file_size = 64122220
        wgrib = '/shared/aerosol_bob1/users/xian/src/bin/grib2/wgrib2/wgrib2'
#        wgrib = '/shared/aerosol_heck2/users/sessions/bin/wgrib2'

#       dtg='2016070100'
        #_Conversion between NGACF variables and local ones
        variables = [   'dust' , 
                        'sulfate',
                        'blackcarbon',                          
                        'organiccarbon',
                        'seasalt','total'     ]

        #Get initial time from filename
        re_dtg = re.compile('(\d{10})')
        dtg_init = re_dtg.search(file).group(0)

        #define file name for writing, containing all species aot
        file_name  = dtg_init + '_aod_550_ngac.nc'

        #define filenames of single specie aot netcdf files that converted from grib2 file
        file_dust = dtg_init + '_dust_aod_ngac.nc'
        file_sulfate= dtg_init + '_sulfate_aod_ngac.nc'
        file_bc = dtg_init + '_blackcarbon_aod_ngac.nc'
        file_oc = dtg_init + '_organiccarbon_aod_ngac.nc'
        file_seasalt = dtg_init + '_seasalt_aod_ngac.nc'
        file_total = dtg_init +'_total_aod_ngac.nc'

        #_Decode GRIB2 input
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Sulphate Dry:" -set_ext_name l -netcdf ' + file_sulfate )
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Particulate Organic Matter Dry:" -set_ext_name l -netcdf ' + file_oc )
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Black Carbon Dry:" -set_ext_name l -netcdf ' + file_bc )
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Dust Dry:" -set_ext_name l -netcdf ' + file_dust )
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Sea Salt Dry:" -set_ext_name l -netcdf ' + file_seasalt )
        res = os.system( wgrib + ' ' + file + ' -match ":aerosol=Total Aerosol:" -set_ext_name l -netcdf ' + file_total )

        if res: raise OSError('Failed to convert from grib2')



        #_Open new netcdf file for writing 
        file_out = Dataset( file_name, 'w', format='NETCDF3_CLASSIC' )
        var_dict = lm.aod_vars()
        dbg( file_name )

        #_Get data for each variable
        for variable in variables:
                var_key = variable + '_aod'

                #_Open file with individual specie, Read decoded input
                ncdf_in = dtg + '_' + var_key + '_ngac.nc'
                dbg( ncdf_in )
                file_in = Dataset( ncdf_in, 'r', format='NETCDF3_CLASSIC' )
                

                #_Create dimensions if not present, should only happen first
                # variable
                if not 'lat' in file_out.dimensions:

                        lats = file_in.variables['latitude'][:]
                        lons = file_in.variables['longitude'][:]-180
                                                #_Note this shift when read-
                                                # ing data
                        nx = len(lons)
                        ny = len(lats)
                        #nspec = len(species.keys())
                        nspec = len(variables)

                         #_Calculate and store dts into array
                        times = []
                        epochs = []
                        epochs[:] = file_in.variables['time'][:]
                        epochs = np.array( epochs )
                        [ times.append(lt.epoch2dtg(t)) for t in epochs ]
                        nt = len( times )

                        #_Create dimensions
                        file_out = Dataset( file_name, 'w', format='NETCDF3_CLASSIC' )
                        file_out.createDimension('lon', nx)
                        file_out.createDimension('lat', ny)
                        file_out.createDimension('time', nt)

                        #_Create global attributes
                        file_out.Projection = 'LatLon'
                        file_out.lat_ll = lats[0]
                        file_out.lon_ll = lons[0]
                        file_out.delta_lat = str(lats[1] - lats[0]) + ' degrees'
                        file_out.delta_lon = str(lons[1] - lons[0]) + ' degrees'
                        file_out.Nlon = str(nx) + ' grid_points'
                        file_out.Nlat = str(ny) + ' grid_points'


                        #_Create ncdf variable object
                        var = file_out.createVariable('lon','f4',('lon'))
                        var[:] = lons
                        var = file_out.createVariable('lat','f4',('lat'))
                        var[:] = lats
                        var = file_out.createVariable('time','f8',('time'))
                        var[:] = epochs

                #_Define variables
                species = { 'AOTK_entireatmosphere' : variable }
                for s in species:
                        specie = species[s]
                        var = file_out.createVariable( specie + '_aod', 'f4', 
                                ('time' ,'lat' ,'lon') )
                        #var.name = specie + '_aod'
                        var.setncattr('name',specie+'_aod')
                        for attr in file_in.variables[s].ncattrs():
                                value = file_in.variables[s].__getattr__( attr )
                                var.setncattr( attr, value )

                        var.init_time_ut = times[0]
                        nx2 =int(nx/2)
                        var[:,:,:nx2] = file_in.variables[s][:,:,nx2:]
                        var[:,:,nx2:] = file_in.variables[s][:,:,:nx2]

                file_in.close()  #close the files for reading
                os.unlink(ncdf_in)  #delete individual specie nc file

        file_out.close()  #close the file for writing

        #_Check to see if filesize matches expectations
        file_size = os.stat( file_name ).st_size
        if file_size != expected_file_size:
                dbg(( 'error: NGAC file not correct size, removing', file_name ))
                dbg(( 'error: 64122220 !=', file_size ))
                os.unlink( file_name )

        return file_name
                                
def file_size( file ): return os.stat( file ).st_size #_?!

def dbg( msg, l=1 ):
        ''' if global debug is set to true, be more verbose '''
        msg = lt.to_string( msg )
        if hasattr( msg, '__iter__'): msg = ' '.join( msg )

        if debug >= l:
                curf = inspect.currentframe()
                calf = inspect.getouterframes( curf, 2 )
                file, method = calf[1][1], calf[1][3]
                print ('[%s.%s] %s' % ( file, method, msg ))
        else:
             print(msg);
