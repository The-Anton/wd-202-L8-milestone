from tasks.models import Task, UserProfile
from datetime import datetime, timedelta, timezone
import time

from django.contrib.auth.models import User
from django.core.mail import send_mail

from celery.decorators import periodic_task
from celery.schedules import crontab
from task_manager.celery import app


def mail_user(user: User):
    tasks = Task.objects.filter(user=user)
    pending = tasks.filter(status="PENDING").count()
    in_progress = tasks.filter(status="IN_PROGRESS").count()
    completed = tasks.filter(status="COMPLETED").count()
    cancelled = tasks.filter(status="CANCELLED").count()

    message = f"""Hey {user.username}!
    You have {pending} tasks pending, {in_progress} in progress and you have {completed} completed tasks. You also have cancelled {cancelled} tasks.

    You have recorded a total of {tasks.count()} tasks from your account. Thanks for using Task Manager!
    """
    send_mail("Task notifications", message, "admin@taskmanager.com", [user.email])


@periodic_task(run_every=timedelta(minutes=1))
def monitor_mail_times():
    print("Fetching mail addresses and configuring send times...")
    times = UserProfile.objects.filter(
        hour__gte=datetime.now(timezone.utc).hour()
    ).order_by("user_id")

    for i in times:
        try:
            if i.last_mailed.day != datetime.now(timezone.utc).day:
                mail_user(i.user)
                i.last_mailed = datetime.now(timezone.utc)
                i.save()
        except:
            print(
                f"Celery worker failed at {datetime.now(timezone.utc).strftime('%m/%d/%Y, %H:%M:%S')}"
            )
