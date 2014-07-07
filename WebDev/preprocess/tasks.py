from celery import Celery 
from django.conf import settings

celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task(bind=True)
def add(self, x, y):
    thr = 1000000
    i = 0
    while (i < thr):
        i += 1
    return x + y

__author__ = 'nebras'
import time
from django.conf import settings
#from WebDev.models import Pipeline, Results, RunningProcess
import os
import optparse
import uuid
from preproc_scripts import preprocess




@celery.task(bind=True , name='prepro')
def prepro(self , uniqueJobID , listofSFFfiles, listOfMappingFiles):

     startTime = unicode(datetime.datetime.now())
     print "Running"
     self.update_state(state='RUNNING', meta='Preprocessing...')
     t = preprocess(uniqueJobID, listofSFFfiles , listOfMappingFiles)
     finishTime = unicode(datetime.datetime.now())
     task_ret = { funct= t ,
                  st = startTime,
                  ft = finishTime
                 }


     return task_ret,


