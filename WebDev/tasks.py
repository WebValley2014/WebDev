from celery import Celery 
import datetime
import time
import os
import optparse
import uuid
import urllib2
import multiprocessing
import sys

_cwd=os.getcwd()
_preprocess_path=os.path.join(_cwd,"preprocess")
_classification_path=os.path.join(_cwd,"classification")
#_classification_path='/home/luca/github/PipelineGIT'

_network_path=os.path.join(_cwd,"network")
#print _preprocess_path
#print _classification_path
#print _network_path
sys.path.append(_preprocess_path)
sys.path.append(_classification_path)
sys.path.append(_network_path)
#print sys.path


import sff2otu
import ml_pipeline
from Net import Net



#celery = Celery('tasks', broker = 'amqp://wvlab:wv2014@54.72.43.115/', backend = 'amqp')
celery = Celery('tasks', broker = 'amqp://guest@localhost//', backend = 'amqp')


@celery.task(bind=True , name='prepro')
def prepro(self , uniqueJobID , listofSFFfiles, listOfMappingFiles):

    print 'Prepro started'
    self.update_state(state='RUNNING')
    core = max(multiprocessing.cpu_count() - 1, 1)
    start_time = unicode(datetime.datetime.now())
    pipeline = sff2otu.SFF2OTU(uniqueJobID, listofSFFfiles, listOfMappingFiles)
    result = pipeline.run(processors = core, qtrim = 'F')
    finish_time = unicode(datetime.datetime.now())

    return {'funct': os.path.abspath(result['txt']), 'st': start_time, 'ft': finish_time}


@celery.task(bind=True , name='ml')
def mlearn(self , job_id, otu_file, class_file, *args, **kwargs):

    print 'Classification started'
    #print job_id
    print self.request.id
    self.update_state(state='RUNNING')
    start_time = unicode(datetime.datetime.now())
    
    #print job_id
    #print '++++++++++++++++++'
    #print otu_file
    #print class_file
    #print '++++++++++++++++++'
    
    #import numpy as np
    #OTUS=np.loadtxt(otu_file,delimiter='\t',dtype=str)
    #print OTUS
    #YS=np.loadtxt(class_file,delimiter='\t',dtype=str)
    #print YS
    
    #print "args:"
    #print args
    print "kwargs:"
    print kwargs
    
    
    pipeline = ml_pipeline.ML(job_id, otu_file, class_file)
    result, feat_str = pipeline.run(*args, **kwargs)
    #result = pipeline.run()
    #result = pipeline.run(args, kwargs)
    
    print result
    #print '\n\n\n'

	
    for key in result:
        result[key] = os.path.abspath(result[key])

    
    finish_time = unicode(datetime.datetime.now())


    return {'funct': result , 'st': start_time, 'ft': finish_time, 'feat_str': feat_str, 'ML_input_data': {'otu_table': otu_file, 'labels': class_file}}


@celery.task(bind=True, name="network_task")
def network_task(self, **kwargs):
    """
    Execute Davide Leonessi and Stefano Valentini network
    analysis.

    args:
    *fileData*
        (str)
        The filesystem path of the `data.txt' file.
    *fileLabel*
        (str)
        The filesystem path of the `label.txt' file.
    *fileSamples*
        (str)
        The filesystem path of the `samples.txt' file.
    *fileFeature*
        (str)
        The filesystem path of the `feature.txt' file.
    *fileRank*
        (str)
        The filesystem path of the `rank.txt' file.
    *fileMetrics*
        (str)
        The filesystem path of the `metrics.txt' file.    
    *outDir*
        (str)
        The filesystem path of the directory where store
        the output files.
    *Numerical Parameter*
        float
    
    """
    # keys mandatory in kwargs
    path_keys = ['fileData', 'fileLabel', 'fileSamples', 'fileFeature',
                 'fileRank', 'fileMetrics', 'outDir' , 'numPar']
    file_keys = path_keys[:-2]
    dir_keys = path_keys[-1]
    
    # check if i get all the args
    for key in path_keys:
        if key not in kwargs:
            e = "Missing path argument `{0}'".format(key)
            return NameError(e)
    
    # check paths
    for key in file_keys:
        path = kwargs[key]
        if not os.path.isfile(path):
            e = "File not found: {0}".format(path)
            return IOError(e)
    for d in dir_keys:
        if not os.path.isdir(d):
            try:
                os.makedirs(d)
            except Exception, e:
                msg = "Error while crating `{0}'. Details: {1}".format(d, e)
                return Exception(msg)
    

    # build args list and get instance
    args = [kwargs[arg] for arg in path_keys]
    
    # start task
    print "Starting celery network task ..."
    print self.request.id
    #try:
    self.update_state(state='RUNNING')
    start_time = unicode(datetime.datetime.now())
    netAnalysis = Net(*args)
    result = netAnalysis.run()
    finish_time = unicode(datetime.datetime.now())
    return {'result' : result, 'st': start_time, 'ft': finish_time}
    #except Exception, e:
        # msg = "Error while executing Network Analysis. "
        # msg+= "Details: {0}".format(e)
        # return Exception(e)
        #
