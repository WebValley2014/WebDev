from models import *
import datetime
from django.core.files import File
import os
from django.contrib import messages
from utils import *

def store_before_celery(pip_id, jinput, task_id , pname):
    '''
    This Function Stores the running process and info related to the results to the database.
    Needs to be called directly after [variable]= celery.start_task()

    :param pip_id: pipeline ID from Pipeline model.
    :param jinput: Dictionary of Inputs
    :param task_id: taskid
    :param pname: Process Name
    :return: RunningProcess Database
    '''

    try:
        rundb = RunningProcess(process_name=pname,
                               pip_id=pip_id,
                               inputs=jinput,
                               submitted=datetime.datetime.now(),
                               task_id=task_id,
                           )
        rundb.save()
    except Exception, e:
        print e
    return True

def store_after_celery(rundb, task_ret, tp):
    '''
    Run after Celery Task
    :param rundb: from store_before_celery
    :param task_ret:  return of the celery task
    :param tp: filetype
    :return: True
    '''

    print str()
    rundb.started = task_ret[0]['st']
    rundb.finished = task_ret[0]['ft']
    rundb.save()

    resdb = Results(process_name=rundb.process_name,
                    task_id=rundb,
                    filepath=task_ret[0]['funct']['pathname'],
                    filetype=tp,
                    owner=rundb.pip_id.owner,
                    pip_id=rundb.pip_id
                    )
    resdb.save()
    return True

def store_after_celery_class(rundb, task_ret):
    '''

    Saving to image field was based on this
    http://andrewbrookins.com/tech/set-the-path-to-an-imagefield-in-django-manually/


    Run after Celery Task
    :param rundb: from store_before_celery
    :param task_ret:  return of the celery task
    :param tp: filetype
    :return: True
    '''

    print '+++++++++++++++++++++++++++++++++++++'
    print str(task_ret)
    print '+++++++++++++++++++++++++++++++++++++'

    #RUNDB
    rundb.started = task_ret['st']
    rundb.finished = task_ret['ft']

    #Create the new_path for the file
    pipeline = rundb.pip_id
    feat_str=task_ret['feat_str']
    #partial_path = os.path.join(pipeline.owner.username, (str(pipeline.pip_id)+feat_str))
    partial_path = os.path.join(pipeline.owner.username, str(pipeline.pip_id))
    partial_path = os.path.join(partial_path, 'classification')
    partial_path = os.path.join(partial_path, feat_str)   
    new_path = os.path.join(settings.MEDIA_ROOT, partial_path)

    #IMG
    #Create the new img directroy and file path
    img_path = os.path.join(new_path, 'img')
    #Pick the img directory
    img = task_ret['funct']['img']
    try:
        #Move the directory
        os.renames(img, img_path)
    except Exception, e:
        pass
    img_list = os.listdir(img_path)
    for img in img_list:
        img_full_path = os.path.join(new_path, img)
        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filepath = img_full_path,
            filetype='img',
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()

    #GENERIC FILE
    file_store = {
        'metrics':      os.path.join(new_path, 'metrics.txt'),
        'stability':    os.path.join(new_path, 'stability.txt'),
        'featurelist':  os.path.join(new_path, 'featurelist.txt'),
        'otu':          os.path.join(new_path, 'otu.txt'),
        'filtered_otu': os.path.join(new_path, 'filtered_otu.txt'),
        'json':         os.path.join(new_path, '3dphylo.json')
    }

    file_type = [
        ['metrics', 'nt_metrics'],
        ['stability', 'nt_stab'],
        ['featurelist', 'nt_feature'],
        ['json','json'],
        ['otu', 'nt_otu'],
        ['filtered_otu', 'nt_filt'],
    ]

    for ftype in file_type:
        try:
            #Move the file
            os.rename(task_ret['funct'][ftype[0]], file_store[ftype[0]])
        except:
            pass

        #SAVE IT IN DATABASE
        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filepath = file_store[ftype[0]],
            filetype= ftype[1],
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()
    
    save_network_input_data(new_path, task_ret['ML_input_data'], file_store)
    
    zipdir(new_path,os.path.join(new_path,feat_str+".zip"),new_path)
    return True
    

def store_after_celery_network(rundb, task_ret):
      #Create the new_path for the file
    pipeline = rundb.pip_id

    print '+++++++++++++++++++++++++++++++++++++'
    print str(task_ret)
    print '+++++++++++++++++++++++++++++++++++++'

    #IMG

    i = 0
    for img in task_ret['result']['img']:
        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filename = task_ret['result']['titles'][i] ,
            filepath = img,
            filetype='img',
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()
        i = i+1

    #Matrix File

        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filepath = task_ret['result']['matrix'],
            filetype='txt',
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()

    return True
