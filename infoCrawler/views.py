from django.http import HttpResponseRedirect
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job


def index(request):
    return HttpResponseRedirect("/admin")


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(scheduler, "cron", minute='*/2', id='test', replace_existing=True)
# def test():
#     print('test')

# scheduler.start()