from celery import Celery 
from django.conf import settings
import datetime
import time

celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task(bind=True)
def add(self, x, y):
    print 'Running add task'

    time.sleep(20)

    #x = 'http://localhost:8000/preproc/processing_finish/%s/' % (self.request.id,)
    #urllib2.urlopen(x)

    return x + y

__author__ = 'nebras'
import time
from django.conf import settings
#from WebDev.models import Pipeline, Results, RunningProcess
import os
import optparse
import uuid
from preproc_scripts import preprocess
import urllib2




@celery.task(bind=True , name='prepro')
def prepro(self , uniqueJobID , SFF1, listOfMappingFiles):

     startTime = unicode(datetime.datetime.now())
     print "Running"
     self.update_state(state='RUNNING', meta='Preprocessing...')
     t = preprocess(uniqueJobID, SFF1, listOfMappingFiles)
     finishTime = unicode(datetime.datetime.now())
     task_ret = { 'funct': t ,
                  'st': startTime,
                  'ft': finishTime
                 }

     x = 'http://localhost:8000/preproc/processing/%s/%s/' % (uniqueJobID, self.request.id)
     urllib2.urlopen(x)

     return task_ret,


