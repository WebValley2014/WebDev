from models import *
import datetime


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

    resdb = Results(process_name=rundb.process_name,
                    task_id=rundb,
                    filepath=task_ret[0]['funct']['pathname'],
                    filetype=tp,
                    owner=rundb.pip_id.owner,
                    pip_id=rundb.pip_id
                    )
    resdb.save()
    return True

def store_after_celery_network(rundb, task_ret):
    pass