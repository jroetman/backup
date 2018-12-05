#!/software/depot/anaconda-3-5.1.0/bin/python
import sys, os, time
from time import gmtime
import importlib

n = time.localtime()
dtg = str(n.tm_year) +  \
      str(n.tm_mon).zfill(2) +    \
      str(n.tm_mday).zfill(2) +   \
      '00'    #_Always drop to 00z str(n.tm_hour).zfill(2)\

modelName =  sys.argv[1]
print(modelName)

model = importlib.import_module(modelName)
nw = model.Model(modelName, dtg)
nw.download()
sys.exit(0)
