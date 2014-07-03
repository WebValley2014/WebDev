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
