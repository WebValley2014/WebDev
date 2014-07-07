import csv
from django.db import models
from django.contrib.auth.models import User
import json
import os
from django.conf import settings
import djcelery
import jsonfield

__author__ = 'michele'

def get_bootsrap_badge(status):
    if status == 'SUCCESS':
        badge = 'label-success'
    elif status == 'STARTED' or status == 'RUNNING':
        badge = 'label-primary'
    elif status == 'RETRY':
        badge = 'label-default'
    elif status == 'FAILURE':
        badge = 'label-danger'
    elif status == 'PENDING':
        badge = 'label-default'
    else:
        badge = 'label-default'

    return badge

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Pipeline(models.Model):
    pip_name = models.CharField(max_length=40)
    pip_id = models.CharField(max_length=80)
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(User)

class RunningProcess(models.Model):
    #user = models.ForeignKey(User)
    process_name = models.CharField(max_length=40)
    pip_id = models.ForeignKey(Pipeline)
    task_id = models.CharField(max_length=36)
    inputs = jsonfield.JSONField()
    submitted = models.DateTimeField()
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)

    # From id returns task result
    @property
    def celery_task(self):
        try:
            return djcelery.celery.AsyncResult(self.task_id)
        except Exception:
            return None

    @property
    def badge_status(self):
        task = self.celery_task
        return '<span class="label %s">%s</span>' % (get_bootsrap_badge(task.status), task.status)

    ## Returns the result of the task
    @property
    def result(self):
        if self.celery_task.status == 'SUCCESS':
            res = self.celery_task.result
        else:
            res = None
        return res

    @property
    def result_is_sucess(self):
        if self.celery_task.status == 'SUCCESS' and isinstance(self.celery_task.result,dict):
            res = True
        else:
            res = False
        return res

    # Returns the time when the task has finished
    @property
    def execution_time(self):
        return self.started - self.finished  # tmp



class Results (models.Model):
    """
    Results table: need for storing the results instead of pass through celery
    """
    def get_tmp_dir(self, filename):
        return os.path.join(settings.RESULT_PATH, self.task_id.task_id, filename)

    FILE_TYPES = (
        ('csv', 'comma separated file'),
        ('img', 'jpg, tiff, png, pdf'),
        ('graph', 'gml, graphml'),
        ('txt', 'text description'),
        ('json', 'json file'),
        ('error', 'Error during computation'),
        ('zip', 'zip'),
        ('sff', 'sff')
    )

    process_name = models.CharField(max_length=40, null=True, blank=True)       #celery
    owner = models.ForeignKey(User)
    pip_id = models.ForeignKey(Pipeline)
    task_id = models.ForeignKey(RunningProcess, null=True, blank=True)          #Nome dell'app
    filetype = models.CharField(max_length=36, choices=FILE_TYPES)              #Tipo di file (zip)
    filename = models.CharField(max_length=40)                                  #Nome del file
    filepath = models.CharField(max_length=100)                                 #Posizione completa del file
    filestore = models.FileField(upload_to=get_tmp_dir, null=True, blank=True)  #BLANK
    filecol = models.IntegerField(blank=True, null=True)                        #BLANK
    filerow = models.IntegerField(blank=True, null=True)                        #BLANK
    filefirstrow = models.TextField(blank=True, null=True)                      #BLANK
    imagestore = models.ImageField(upload_to=get_tmp_dir, null=True, blank=True)#BLANK
    desc = models.TextField(null=True, blank=True)                              #BLANK

    def __unicode__(self):
        return u'%s: %s' % (self.task_id.task_id, self.filetype)

    @property
    def get_submitted(self):
        return self.task_id.submited

    @property
    def tables_to_json(self):
        reader = csv.reader(self.filestore, delimiter='\t')

        json_list = []
        reader.next()
        for line in iter(reader):
            json_list.append([round(float(l), 3) if is_number(l) else l for l in line])

        return {'aaData': json_list}

    @property
    def get_first_row(self):
        if self.filefirstrow:
            res = json.dumps(self.filefirstrow)
        else:
            res = None

        return json.dumps(self.filefirstrow)

    # get_submitted.short_description = 'Submit time'

