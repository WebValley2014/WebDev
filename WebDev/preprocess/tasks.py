import celery
from django.conf import settings

# app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task(bind=True)
def add(self, x, y):
    thr = 1000000
    i = 0
    while (i < thr):
        i += 1
    return x + y

__author__ = 'nebras'
# import time
# from django.conf import settings
# from WebDev.models import Pipeline, Results, RunningProcess
# import os
#
# import optparse
# import uuid
# import multiprocessing
# from preproc_scripts import preprocess




# @celery.task(bind=True)
# def prepro(self , uniqueJobID , listofSFFfiles, listOfMappingFiles):
#     '''
#     :param UniqueJobID: Stuff that Hiromu Needs for his script.
#     :param ListofSFFfiles:
#     :param ListOfMappingFiles:
#     :return:
#     '''
#
#     tmpdir = str(Pipeline.pip_id)
#     result_path = os.path.join(settings.MEDIA_ROOT, tmpdir)
#     # result_path_full = os.path.join(result_path, tmpdir)
#     if not os.path.exists(result_path_full):
#         os.makedirs(result_path_full)
#
#     print "Running"
#     self.update_state(state='RUNNING', meta='Preprocessing...')
#     t = preprocess(uniqueJobID, listofSFFfiles , listOfMappingFiles)
#
#     try:
#          resdb = Results(
#                         process_name=pname,
#                         filepath=result_path_full,
#                         filetype=tp,
#                         filename=myn,
#                         task_id = RunningProcess.objects.get(task_id=self.request.id)
#                     )
#         resdb.filepath= t
#         resdb.process_name= preprocessing
#         resdb.filetype= 'txt'
#
#         except Exception, error:
#                     print error
#
#     try:
#                         resdb.save()
#                     except Exception, e:
#                         print e
#     return True

