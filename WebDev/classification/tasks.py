from celery import Celery
from django.conf import settings
import datetime
import urllib2
import ml_pipeline
import multiprocessing



celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')


@celery.task(bind=True , name='mlearn')
def mlearn(self , job_id, otu_file, class_file, *args, **kwargs):

    print 'Classification started'
    print self.request.id
    self.update_state(state='RUNNING')
    start_time = unicode(datetime.datetime.now())
    pipeline = ml_pipeline.ML(job_id, otu_file, class_file)
    result = pipeline.run(*args, **kwargs)

    for key in result:
        result[key] = os.path.abspath(result[key])

    finish_time = unicode(datetime.datetime.now())


    return {'funct': result , 'st': start_time, 'ft': finish_time}