from celery import Celery
from celery.schedules import crontab

# app  = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

celery_app = Celery("task_tracker")

celery_app.config_from_object("src.config", namespace='CELERY')

celery_app.autodiscover_tasks([
    'src.task_tracker.tasks',
])


celery_app.conf.beat_schedule = {
    # 'add-every-10-seconds': {
    #     'task': 'src.task_tracker.tasks.test_task',
    #     'schedule': 10.0,
    #     'args': (16,),
    # },
    'add-every-30-seconds': {
        'task': 'src.task_tracker.tasks.test_task',
        'schedule': 30.0,
        'args': (16,),
    },
    'add-every-tuesday-morning': {
        'task': 'src.task_tracker.tasks.test_task',
        'schedule': crontab(hour=21, minute=35, day_of_week=2),
        'args': (16,),
    }
}