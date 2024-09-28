from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


CELERY_BEAT_SCHEDULE = {
    'generate-monthly-report': {
        'task': 'backend_jobs.generate_monthly_report',
        #'schedule': crontab(day_of_month='*'),
        'schedule': 10,
    },
    'daily-reminders': {
        'task': 'backend_jobs.daily_reminders',
        #'schedule': crontab(day_of_month='*'),
        'schedule': 10,
    },
}

celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE