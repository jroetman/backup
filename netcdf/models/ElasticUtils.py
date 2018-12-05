#!/usr/bin/env python
import libs.libmeta as lm
import libs.libicap as li
import libs.libnva as ln
import libs.libtools as lt

dir_prd = lm.dir_prod   #_ICAP Data Dir
dir_web = lm.dir_web    #_Webpage Dir

debug = 3

def run_main( dtg ):
        import os
        from shutil import rmtree
        import shutil
        import numpy as np

        #_Var Table
        fhr     = 24 * 4        #_Number of days to forecast
        bhr     = 24 * 14       #_Number of analysis days for verif plots
        finc    = 6             #_DT between plots
        nproc   = 8             #_Number of processors to use
        dir_esc = './plot_' + str( os.getpid() )        #_Temporary Plot Dir_

#        silam=li.read_silamfcst(dtg)
#        li.plot_icap(silam,nproc=8,path=dir_esc,res='l', entity='ICAP Multi-Model Ensemble')
#
#        ngacf=li.read_ngacffcst(dtg)
#        li.plot_icap(ngacf,nproc=8,path=dir_esc,res='l',  entity='ICAP Multi-Model Ensemble')

         #ICAP ensemble#
	#_List of models to include in ICAP 
	members	= lm.current_icap()
	allsp_members = lm.allspecie_icap()
	#_List of fhrs we want plotted (not currently used)
	fhrs = np.arange( 0, fhr+finc, finc ).tolist()
	#_Earliest dtg to be read in for verification plots
	dtg_bhr = lt.newdtg( dtg, -bhr )

	#_Generate spatial plots for member models
	aod = li.read_icapfcst_raw( dtg, members=members )

	icap = ln.subset( aod, model='ICAP', fhr=fhrs )
	membersaod = ln.subset( aod, model=members, fhr=fhrs )
	ln.write_ensfcst( icap )
        
	#_Write ICAP that will be distributed to ICAP members. The only difference between the ICAP data in house
	# and this one is that this one does not contain the names of the centers, but labels each model with a
	# number from 1-7 
	ln.write_ensfcst(icap,path_out=dir_prd+'/ICAP_to7member' , numberlabel=True)

        unimodels = lt.unique( membersaod.model )
	unimodels_allsp=set(unimodels) & set(allsp_members)

	#_Reread and remerge records, for consistency 
	fcst = li.read_icapfcst( dtg )
	aod = lt.merge(( fcst, membersaod)); del fcst; del membersaod
	li.plot_icap( aod, nproc=nproc, path=dir_esc, res='l', entity='ICCAP Multi-Model Ensemble'); del aod


if __name__ == '__main__':
        import os, sys
        from time import gmtime, strftime

        #_Check how many arguments were passed,
        #_If None, get current dtg and run for this week and one week ago
        if len( sys.argv ) == 1:
                #_Get yesterday's 00z DTG
                dtg_yes = lt.newdtg( strftime("%Y%m%d00", gmtime()), -0 )

                #_and the dtg from one week ago
                dtg_1wk = lt.newdtg( dtg_yes, -24*2 )

                #_Do plots for yesterday and eight days ago
                for dtg in [ dtg_yes, dtg_1wk ]:
###                     li.cronlog( dtg, job={'PLOTTING':'STARTED'} )
                        run_main( dtg )
###                     li.cronlog( dtg, job={'PLOTTING':'COMPLETE'} )

        #_If a DTG is passed, run only for that
        elif len( sys.argv ) == 2:
                dtg = sys.argv[1]

                #_update status file with start time
                run_main( dtg )

        #_If some other config, die
        else:
                raise RuntimeError, 'USAGE: ./MOCAGE_post.py [DTG]'



