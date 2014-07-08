from celery import Celery
from django.conf import settings
import datetime
import urllib2



celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')


@celery.task(bind=True , name='mlearn')
def mlearn(self , uniqueJobID , OTUsFile):

     startTime = unicode(datetime.datetime.now())
     print "Running"
     self.update_state(state='RUNNING', meta='Classification...')



     finishTime = unicode(datetime.datetime.now())
     task_ret = { 'funct': t ,
                  'st': startTime,
                  'ft': finishTime
                 }

     x = 'http://localhost:8000/preproc/processing/%s/%s/' % (uniqueJobID, self.request.id)
     #urllib2.urlopen(x)

     return task_ret,