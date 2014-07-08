from celery import Celery 
from django.conf import settings
import datetime
import time

celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task(bind=True)
def add(self, x, y):
    print 'Running add task'
    print self.request.id
    self.update_state(state='RUNNING')
    time.sleep(200)    #x = 'http://localhost:8000/preproc/processing_finish/%s/' % (self.request.id,)
    #urllib2.urlopen(x)

    return x + y

__author__ = 'nebras'
import time
from django.conf import settings
#from WebDev.models import Pipeline, Results, RunningProcess
import os
import optparse
import uuid
import urllib2
import multiprocessing
import sff2otu




@celery.task(bind=True , name='prepro')
def prepro(self , uniqueJobID , listofSFFfiles, listOfMappingFiles):

    print 'Prepro started'
    print self.request.id
    self.update_state(state='RUNNING')
    core = max(multiprocessing.cpu_count() - 1, 1)

    start_time = unicode(datetime.datetime.now())
    pipeline = sff2otu.SFF2OTU(uniqueJobID, listofSFFfiles, listOfMappingFiles)
    result = pipeline.run(processors = core)
    finish_time = unicode(datetime.datetime.now())

    return {'funct': os.path.abspath(result['txt']), 'st': start_time, 'ft': finish_time}

