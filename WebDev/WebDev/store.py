from models import *
import datetime
from django.core.files import File
import os
from django.contrib import messages

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

    #RUNDB
    rundb.started = task_ret[1]
    rundb.finished = task_ret[2]

    #Create the new_path for the file
    pipeline = rundb.pip_id
    partial_path = os.path.join(pipeline.owner.username, str(pipeline.pip_id))
    partial_path = os.path.join(partial_path, 'classification')
    new_path = os.path.join(settings.MEDIA_ROOT, partial_path)

    #IMG
    #Create the new img directroy and file path
    img_path = os.path.join(new_path, 'img')
    #Pick the img directory
    img = task_ret[0]['img']
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
        'metrics':      os.path.join(new_path, 'matrics.txt'),
        'stability':    os.path.join(new_path, 'stability.txt'),
        'featurelist':  os.path.join(new_path, 'featurelist.txt')
    }
    file_type = [['metrics', 'nt_metrics'], ['stability', 'nt_stab'], ['featurelist', 'nt_feature']]
    for type in file_type:
        try:
            #Move the file
            os.rename(task_ret[0][type[0]], file_store[type[0]])
        except:
            pass

        #SAVE IT IN DATABASE
        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filepath = file_store[type[0]],
            filetype= type[1],
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()

    return True

def store_after_celery_network(rundb, task_ret):
      #Create the new_path for the file
    pipeline = rundb.pip_id


    #IMG

    i = 0
    for img in task_ret['img']:
        resdb = Results(
            process_name=rundb.process_name,
            task_id = rundb,
            filename = task_ret['titles'][i] ,
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
            filepath = task_ret['matrix'],
            filetype='txt',
            owner = rundb.pip_id.owner,
            pip_id = rundb.pip_id
        )
        resdb.save()

    return True
