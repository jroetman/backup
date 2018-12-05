from . imports import *
import hashlib

class ModelBase():
    def __init__(self, model, dtg, mkdir=True):
        self.model = model
        self.dtg = dtg

        #self.dir_prod = lm.dir_prod 
        self.dir_prod = "/DATA/roetman/cylce/products/"
        #self.mod_dict = lm.models()
        #self.plot_dir = lm.dir_prod + '/plots/'
        #self.plt_dict = lm.fields()
        self.requestmark = "&email=peng.xian@nrlmry.navy.mil"

        self._dir_out =  self.dir_prod + '/' + self.model + '/' + self.dtg[:6]
        self._file_out = self.dir_out + '/' + self.dtg + '_'  + self.model.lower() + ".nc"

        if (mkdir is True): lt.mkdir_p(self.dir_out)

    @property
    def dir_out(self):
        return self._dir_out

    @dir_out.setter
    def dir_out(self, dir_out):
        self._dir_out = dir_out

    @property
    def file_out(self):
        return self._file_out

    @file_out.setter
    def file_out(self, suffix):
        self._file_out = self.dir_out + '/' + self.dtg + '_'  + suffix

    def getHash(self):
        mhash = self.model 
        if hasattr(self,'colorDomain'):
          mhash += "".join([str(self.colorDomain['levels'])])
          mhash += str(self.colorDomain['steps'])
          mhash += self.colorDomain['rightcolor']
          mhash += self.colorDomain['leftcolor']
          mhash += str(self.colorDomain['rightDomain'])
          mhash += str(self.colorDomain['leftDomain'])
          mhash += self.colorDomain['type']
        
        return hashlib.md5(mhash.encode()).hexdigest() 

    def custom_file_out(self, suffix):
        self._file_out = self.dir_out + '/' + suffix

    def download(self, dtg):
        print("Download not implemented for the %s model" % (self.model) )

    def plot(self):
        print("%s %s %s %s" % (self.model , self.dtg, self.field, self.file_out))
        plotUtils.netcdfPlot(self.model, self.dtg, self.field, self.file_out)

