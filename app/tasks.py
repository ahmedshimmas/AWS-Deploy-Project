from celery import shared_task
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER

from app import models


@shared_task
def send_daily_summary(current_user):
    user = models.Task.objects.filter(user=current_user)
    pending_tasks = user.filter(status='pending')
    pending_tasks_count = pending_tasks.count()
    completed_tasks = user.filter(status='done')
    completed_tasks_count = completed_tasks.count()

    subject = 'Daily Tasks Summary'
    message = """
    Dear {user},

    Here is your daily tasks summary:

    Completed Tasks: {completed_tasks_count}
    Pending Tasks: {pending_tasks_count}


    Thank you for using our services.
    Happy to serve you!


    Regards,
    TickTracker Team
    """

    message.format(
        user = current_user,
        completed_tasks_count = completed_tasks_count,
        pending_tasks_count = pending_tasks_count
    )

    if pending_tasks.exists():
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=current_user.email,
            fail_silently=False
        )