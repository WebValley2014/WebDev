from celery import Celery 
from django.conf import settings

from Net import Net
import sys
import os

__author__ = 'daniele'


celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task(bind=True)
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
    *outDir*
        (str)
        The filesystem path of the directory where store
        the output files.
    
    """
    # keys mandatory in kwargs
    path_keys = ['fileData', 'fileLabel', 'fileSamples', 'fileFeauture',
                 'fileRank', 'outDir']
    file_keys = path_keys[:-1]
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
    

    # go
    netAnalysis = Net(data_fp, label_fp, samples_fp, feature_fp, rank_fp, out)
    try:
        netAnalysis.run()
        return True
    except Exception, e:
        msg = "Error while executing Network Analysis. "
        msg+= "Details: {0}".format(e)
        return Exception(e)
    
